#!/usr/bin/python3
"""Relay iLoader anisette requests with an ADP-compatible client description.

Only the public client description is replaced. Anisette data comes from the
same upstream service; Apple authentication still happens in iLoader.
"""
import json
import os
import select
import socket
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests

HOST = "mac-ani.jkcoxson.com"
PROXY = "http://127.0.0.1:12334"
CLIENT_INFO = {
    "client_info": "<MacBookPro13,2> <macOS;13.1;22C65> <com.apple.AuthKit/1 (com.apple.akd/1.0)>",
    "user_agent": "akd/1.0 CFNetwork/808.1.4",
}


def read_headers(stream):
    data = bytearray()
    while not data.endswith(b"\r\n\r\n"):
        part = stream.recv(1)
        if not part or len(data) >= 65536:
            raise OSError("Invalid upstream response headers")
        data.extend(part)
    return bytes(data)


def connect_upstream():
    stream = socket.create_connection(("127.0.0.1", 12334), timeout=15)
    try:
        stream.sendall(f"CONNECT {HOST}:443 HTTP/1.1\r\nHost: {HOST}:443\r\n\r\n".encode())
        if read_headers(stream).split(b" ", 2)[1] != b"200":
            raise OSError("Proxy CONNECT failed")
        return ssl.create_default_context().wrap_socket(stream, server_hostname=HOST)
    except Exception:
        stream.close()
        raise


class Handler(BaseHTTPRequestHandler):
    # Keep WebSocket bytes in the socket after the HTTP upgrade.
    rbufsize = 0

    def log_message(self, *args):
        pass

    def reply(self, status, body, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/v3/client_info":
            self.reply(200, json.dumps(CLIENT_INFO).encode())
        elif self.path == "/v3/provisioning_session" and self.headers.get("Upgrade", "").lower() == "websocket":
            self.relay_websocket()
        else:
            self.reply(404, b"{}")

    def do_POST(self):
        if self.path != "/v3/get_headers":
            self.reply(404, b"{}")
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 1024 * 1024:
                self.reply(400, b"{}")
                return
            self.connection.settimeout(30)
            parts = []
            remaining = size
            while remaining:
                chunk = self.rfile.read(remaining)
                if not chunk:
                    self.reply(400, b"{}")
                    return
                parts.append(chunk)
                remaining -= len(chunk)
            body = b"".join(parts)
            with requests.Session() as session:
                session.trust_env = False
                response = session.post(
                    "https://" + HOST + self.path,
                    data=body,
                    headers={"Content-Type": "application/json"},
                    proxies={"http": PROXY, "https": PROXY},
                    timeout=(10, 30),
                    allow_redirects=False,
                )
                self.reply(response.status_code, response.content, response.headers.get("Content-Type", "application/json"))
        except (ValueError, requests.RequestException, OSError):
            self.reply(502, b'{"error":"anisette upstream request failed"}')

    def relay_websocket(self):
        upgraded = False
        self.close_connection = True
        try:
            with connect_upstream() as upstream:
                headers = [f"GET {self.path} HTTP/1.1", f"Host: {HOST}", "Upgrade: websocket", "Connection: Upgrade"]
                for key in ["Sec-WebSocket-Key", "Sec-WebSocket-Version", "Sec-WebSocket-Protocol", "Sec-WebSocket-Extensions"]:
                    value = self.headers.get(key)
                    if value:
                        headers.append(f"{key}: {value}")
                upstream.sendall(("\r\n".join(headers) + "\r\n\r\n").encode())
                response = read_headers(upstream)
                if response.split(b" ", 2)[1] != b"101":
                    raise OSError("Upstream WebSocket upgrade failed")
                self.connection.sendall(response)
                upgraded = True
                self.connection.settimeout(15)
                while True:
                    readable = [upstream] if upstream.pending() else select.select([self.connection, upstream], [], [], 60)[0]
                    if not readable:
                        break
                    for source in readable:
                        data = source.recv(65536)
                        if not data:
                            return
                        target = upstream if source is self.connection else self.connection
                        target.sendall(data)
        except (OSError, ValueError):
            if not upgraded:
                self.reply(502, b'{"error":"anisette provisioning connection failed"}')


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 12336), Handler)
    server.daemon_threads = True
    notify_socket = os.environ.get("NOTIFY_SOCKET")
    if notify_socket:
        address = "\0" + notify_socket[1:] if notify_socket.startswith("@") else notify_socket
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as channel:
            channel.connect(address)
            channel.sendall(b"READY=1")
    server.serve_forever()


if __name__ == "__main__":
    main()

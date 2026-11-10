#!/bin/sh
# Optional Linux launcher. Configure a working HTTP/mixed proxy first.
set -eu

ILOADER_PROXY_URL=${ILOADER_PROXY_URL:-http://127.0.0.1:12334}
export http_proxy="$ILOADER_PROXY_URL"
export https_proxy="$ILOADER_PROXY_URL"
export all_proxy="$ILOADER_PROXY_URL"
export HTTP_PROXY="$ILOADER_PROXY_URL"
export HTTPS_PROXY="$ILOADER_PROXY_URL"
export ALL_PROXY="$ILOADER_PROXY_URL"
export no_proxy=localhost,127.0.0.1,::1
export NO_PROXY="$no_proxy"

# Enable only after installing and configuring the optional compatibility unit.
if [ "${ILOADER_COMPAT:-0}" = 1 ]; then
    systemctl --user start iloader-anisette-compat.service
fi

if [ ! -x /usr/bin/iloader ]; then
    printf '%s\n' 'Expected iLoader at /usr/bin/iloader. Check your installation.' >&2
    exit 1
fi
exec /usr/bin/iloader "$@"

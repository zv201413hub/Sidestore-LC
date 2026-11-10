# 5. Ubuntu iLoader 的可选兼容方案

[返回首页](../README.md) · [设备内 SideStore 登录](02-login.md)

本页复现 **2026-10-25 / iLoader 2.4.0** 的两个独立问题：Linux 登录后端未使用 GNOME 系统代理；账号开启高级数据保护后，旧 Mac Anisette 客户端描述下双重验证返回 403。安装时先用当前官方版本正常登录，只有出现对应症状才采用本页设置。

以下命令供读者在自己的电脑执行，整理本仓库不会修改现有 iLoader、账号或系统服务。

## A. 登录后端没有使用代理

当时 iLoader Rust 后端未读取 GNOME 手动代理。本次通过显式传入大小写代理环境变量解决；代理地址必须是实际可用的 HTTP / mixed 监听端口。

从仓库根目录执行临时启动：

```bash
ss -lntp
ILOADER_PROXY_URL=http://127.0.0.1:12334 sh scripts/iloader-proxy.sh
```

`12334` 是本次端口，其他电脑需改成自己的端口。脚本最终调用 `/usr/bin/iloader`，该路径也需要与本机包安装结果一致。

在 iLoader 自己的脱敏日志里确认请求连接了代理；单独 curl 成功不能证明 iLoader 已经走代理。`gsa.apple.com` 使用 Apple 专用证书链，普通 curl 证书报错也不能直接证明 iLoader TLS 失败，不要关闭 TLS 校验。

如需固定入口，可复制为一个新名字，保留原启动器：

```bash
install -Dm755 scripts/iloader-proxy.sh "$HOME/.local/bin/iloader-with-proxy"
```

以后从该入口启动；端口固定时可编辑其 `ILOADER_PROXY_URL` 默认值。它默认不启用下方 Anisette 中继。

## B. 高级数据保护账号的双重验证 403

本次密码的两步 SRP 验证已经通过，但获取受信任电话号码 / 短信验证接口返回空响应 403。账号已登录真实 iPad，且高级数据保护开启；当时默认 Mac 服务报告 macOS 10.12.6。

将公开客户端描述替换为 macOS 13.1 后，真实设备验证码认证完成，iLoader 日志确认 Apple ID 登录成功。[Apple 说明](https://support.apple.com/en-us/108756)列出高级数据保护对 Mac 的最低系统要求，但不能仅凭这一条证明所有 403 都有同一原因。

### 中继做什么

[relay.py](../scripts/anisette-compat/relay.py)是本机已用实现的原样副本：

- 仅监听电脑 `127.0.0.1:12336`，`GET /v3/client_info` 返回公开的 macOS 13.1 描述。
- `POST /v3/get_headers` 和 provisioning WebSocket 转发到 `mac-ani.jkcoxson.com`。
- 上游经过 HTTP 代理 `127.0.0.1:12334`，验证 TLS；Apple 账号认证仍在 iLoader 内执行。
- 不保存请求体或密码，也不输出请求访问日志。

这不是独立生成 Anisette 的服务，仍依赖远程上游。不要把电脑的 localhost 地址填到 iPad SideStore。

### 安装与启动

1. 确认 Python 3 和 requests 可用。Ubuntu 缺少依赖时安装：

   ```bash
   sudo apt install python3-requests
   ```

2. 先检查中继源码中的地址。若代理端口不同，必须同时调整 **`PROXY`** 和 **`connect_upstream()` 的 socket 地址**，二者分别服务 HTTP 和 WebSocket。只改启动器环境变量不会改变中继内部固定端口。
3. 下方安装目标若已有文件，先备份并对比，避免覆盖自己的版本。从仓库根目录部署：

   ```bash
   install -Dm700 scripts/anisette-compat/relay.py "$HOME/.local/lib/iloader-anisette-compat/relay.py"
   install -Dm644 scripts/anisette-compat/iloader-anisette-compat.service "$HOME/.config/systemd/user/iloader-anisette-compat.service"
   systemctl --user daemon-reload
   systemctl --user start iloader-anisette-compat.service
   systemctl --user status iloader-anisette-compat.service --no-pager
   curl --noproxy '*' -fsS http://127.0.0.1:12336/v3/client_info
   ```

   unit 使用 `%h` 指向当前用户的家目录，没有固化原作者用户名。采用 `Type=notify`，端口绑定完成后才报告就绪；无需额外开机自启动。

4. 正常退出 iLoader，备份 `~/.local/share/me.nabdev.iloader/preferences.json` 到私人目录，记下原 Anisette 选择。保留 keyring 与已有 Anisette 状态。
5. 在 iLoader 自己的设置里，将远程 Anisette 服务改为 `http://127.0.0.1:12336`。当时持久化键为 `anisetteServer3-1`；优先用 UI，不把这一个键当成所有版本通用配置。
6. 从仓库根目录启动：

   ```bash
   ILOADER_COMPAT=1 ILOADER_PROXY_URL=http://127.0.0.1:12334 sh scripts/iloader-proxy.sh
   ```

   或使用上面安装的新入口：

   ```bash
   ILOADER_COMPAT=1 "$HOME/.local/bin/iloader-with-proxy"
   ```

   `ILOADER_COMPAT=1` 会在启动 iLoader 前启动并等待中继服务。每次使用这套设置都需要该变量；若要配置桌面快捷入口，保留同样的环境变量。

7. 在 iLoader 完成实际登录，验证码直接输入应用。检查最终登录结果及后续开发者会话是否成功。

### 验收范围

本次历史上已实际完成受信任设备验证码和 Apple ID 登录。`/v3/client_info` 返回 200 或服务 active，仅证明本地端点正常；不能替代完整登录、WebSocket provisioning 或应用安装验收。

当前仓库只做了静态检查和无账号的本地端点检查，没有再让原账号重新认证。

### 回退

先在 iLoader 将 Anisette 恢复为原远程服务，正常退出。以不带 `ILOADER_COMPAT=1` 的代理入口启动，或使用原启动入口；随后停止中继：

```bash
systemctl --user stop iloader-anisette-compat.service
```

需要保留代理修复时继续使用 `iloader-with-proxy`。不要仅停掉服务却让 iLoader 继续指向失效的 localhost。回退不需要删除账号、配对文件或 keyring。

升级 iLoader 后重新检查默认客户端描述和真实登录。官方已修复时应撤下旧覆盖，避免它遮蔽新行为。

# 4. 按错误排查

[返回首页](../README.md) · [VPN 设置](03-vpn-and-refresh.md) · [登录设置](02-login.md)

先记下错误的**正负号、错误域、完整文字和触发位置**。错误框出现在 Refresh 附近，不一定代表签名操作本身失败，也可能只是检查软件源更新失败。

## `-1004`：无法连接服务器

本次实际错误是 **`-1004`**，位于「LiveContainer + SideStore」软件源更新检查。用户确认开启 LocalDevVPN 后，Safari 也打不开软件源。电脑当时通过代理访问该源返回 HTTP 200，说明设备的互联网出口需要单独处理。

1. Safari 测试[官方软件源](https://github.com/LiveContainer/LiveContainer/releases/download/1.0/apps_ss_lc.json)。打不开时，先修复设备到该地址的连接。
2. 使用[小火箭 / Loon 回环方案](03-vpn-and-refresh.md)，让代理出口与设备通道同时工作；或用 LocalDevVPN 配合电脑 Wi-Fi HTTP 代理。
3. Safari 能访问后，再检查设备 Reachable 和配对 Verified，然后重试手动 Refresh。
4. 若 Safari 正常、应用仍失败，读取**这次**报错中的目标 URL 与失败阶段；可能是 IPA 下载、Anisette 或 Apple 的另一个地址，不应继续只检查源 JSON。

`NSURLErrorDomain -1004` 表示连接主机失败；它不会仅凭号码告诉你具体哪个服务器坏了。不要把它解释成账号未登录，也不要用反复输入密码代替联网检查。

## 正数 `1004` / “You are not signed in”

这是另一类错误。SideStore 的 OperationError 未登录错误与上面的 URL 连接错误不同，必须结合完整错误域和文字判断。

若内置 SideStore 手动刷新正常，但快捷指令或后台出现未登录、`CancellationError` 或无法弹出凭据界面，上游 [LiveContainer #1629](https://github.com/LiveContainer/LiveContainer/issues/1629)描述了初次电脑侧载一体包的签名兼容问题。

对应修复步骤：

1. 先确认网络、账号与手动 Refresh 正常，备份应用数据。
2. 下载当前官方 **Nightly LiveContainer + SideStore 一体 IPA**。
3. 到**内置 SideStore 的 IPA 安装入口**安装它，使用原签名账号覆盖；上游明确要求不用 **Resign** 按钮代替安装。
4. 完成后分别验证手动刷新、手动执行快捷指令，再验证自动触发。

这是上游建议，本次没有在设备上执行和验收这项修复；它也不适用于本次已经确认的 `-1004` 软件源连接错误。

## Health Check：NoVPN / Disconnected / Unreachable

| 正在使用的方案 | 优先检查 |
| --- | --- |
| LocalDevVPN | 系统设置中实际已连接；SideStore 已开启 Use Local VPN；断开重连后重新打开应用 |
| 小火箭 | 原生 `10.7.0.1/32` 包含路由开启；VPN 重连；SideStore Device IP 正确，Use Local VPN 关闭 |
| Loon | Build 1007+；插件启用；include-tun 和 reflect 均存在；无同地址 reject / drop 插件冲突 |

设备 VPN 图标不等于本地通道可用。显式端点模式应看设备的实际可达结果，不能要求它一定显示 LocalDevVPN 的名称。

## 配对未通过

先确认端点可达，再确认配对文件属于当前这台设备。缺失或确实失效时，按当前 iLoader 的配对管理向导重新生成 / 导入自己的文件；需要设备解锁并信任电脑。

Apple 认证、GitHub 网络或 DDI 的错误不是配对文件失效的充分证据。不要为任意错误删除配对文件。

## Apple `-80045` 与电脑短信 403

- 内置 SideStore `-80045`：查看[独立登录兼容流程](02-login.md)，本次由 On-Device Anisette 切到远程 Mac 服务后成功。
- 电脑 iLoader 在密码验证完成后，短信 / 双重验证返回空响应 403，且高级数据保护开启：查看[Ubuntu 兼容方案](05-ubuntu-compat.md)。

这些问题与回环配置分别验收，不能因为一个修好了就宣称整个续签链路完成。

## 一体包已经过期打不开

用电脑 iLoader 和原签名账号恢复安装 / 覆盖更新，保留原应用数据，再核对登录、配对和手动刷新。恢复前先备份；不要为了恢复启动先卸载旧应用。

如果错误明确写签名证书撤销或证书无效，再按上游证书恢复流程处理。不要把所有 `-1004` 当成证书问题，也不要未经核对撤销共享使用中的开发证书。

## 反馈时附什么

提交版本、错误发生位置、完整错误域和文字、所用 VPN 及 Build、Safari 软件源能否访问、设备和配对检查结果、手动与后台刷新是否不同。

分享截图或日志前隐藏 Apple ID、设备标识、配对内容、证书私钥、令牌和代理订阅。完整 DEBUG 日志可能包含认证数据，只摘录故障所需的脱敏片段。

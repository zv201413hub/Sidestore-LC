# 3. VPN 回环与日常续签

[返回首页](../README.md) · 上一步：[登录](02-login.md) · 排错：[错误排查](04-troubleshooting.md)

以下方案选择一个。小火箭 / Loon 提供上网代理，同时把 `10.7.0.1` 的设备流量回送本机，使 SideStore 可以在同一条 VPN 下续签。

## A. 小火箭（Shadowrocket）

适用条件：当前版本提供原生「包含路由 `10.7.0.1/32`」开关。社区有 2.2.93 成功刷新记录，但本次用户反馈没有记录小火箭具体版本，不能据此推定最低支持版本。

1. 在设备上连接 Wi-Fi，关闭 **LocalDevVPN**。
2. 小火箭进入 **设置 → 其它**，开启 **包含路由 `10.7.0.1/32`**。不同语言或版本名称可能略有差异，确认实际包含的是这个地址。
3. 使用自己已经可用的代理配置，选择能访问 GitHub 的节点，断开再连接小火箭。
4. 如果设备 Wi-Fi 以前设置了电脑的手动 HTTP 代理，到「设置 → Wi-Fi → 当前网络 ⓘ → 配置代理」将其关闭。
5. 打开内置 SideStore，完成下面的[共用端点设置](#sidestore-共用端点设置)。

这是原生设备回环方案。只有普通 DIRECT / PROXY 分流规则不会自动创建回环；旧教程中的 WireGuard 节点是另一种方案，不要混着配置。

本次用户在选择 **jkcoxson** 后反馈成功。后续是否能定时、锁屏自动续签，需要另行测试。

## B. Loon

本插件要求 **Build 1007 或更高**。请在 Loon 的版本信息中核对 **Build**，仅看主版本号不够。低于该构建时，先更新到支持版本再使用本插件。

### 导入插件

1. 打开仓库中的 [Loon-SideStore-loopback.plugin](../configs/Loon-SideStore-loopback.plugin)，保存到设备「文件」中。
2. 在 **Loon → 插件**通过当前版本提供的本地导入入口添加并启用。也可通过 URL 添加[本仓库插件的原始文件](https://raw.githubusercontent.com/zv201413hub/Sidestore-LC/main/configs/Loon-SideStore-loopback.plugin)，或新建本地插件并粘贴以下内容。
3. 确认插件已启用，关闭 LocalDevVPN，断开再连接 Loon。保留你现有的代理节点和上网规则。

```ini
#!name = SideStore Local Loopback

[General]
include-tun = 10.7.0.1/32
ipv6-vif = off

[IP Rewrite]
10.7.0.1 = reflect
```

`include-tun` 把目标流量纳入 VPN；`reflect` 回送本机，保留端口和载荷。`ipv6-vif = off` 沿用本次准备的 IPv4 配置，会关闭 VPN 接口 IPv6；其他应用是否需要 IPv6，应在自己的环境中核对。

**`[IP Rewrite]` 只允许在插件中声明**，不能把整个片段塞进主配置并期待它生效。它也不会自动添加包含路由，必须保留 `include-tun`。多个启用插件若重复配置同一地址，官方按插件顺序采用靠前的动作；出现设备不可达时检查冲突。

官方语法说明：[Plugin → IP Rewrite](https://loon0x00.github.io/docs/Plugin/#ip-rewrite)。本次已核对语法与文件，尚未收到设备实测回执。

## SideStore 共用端点设置

进入 **LiveContainer → 内置 SideStore → Settings → Connection Configuration**：

| 字段 | 小火箭 / Loon 回环方案 |
| --- | --- |
| Use Local VPN | **关闭** |
| Remote Endpoint → Device IP | `10.7.0.1` |
| RemotePair Port | **留空** |
| 保存 | 点 **Confirm**，重新打开 SideStore |

这里的 **Remote Endpoint** 是连接设置的名称；本方案仍访问本机设备，不需要另一台远程设备。不能将 Device IP 填成电脑局域网 IP、代理端口或 `127.0.0.1`。

在本次版本中，显式端点避免依赖 LocalDevVPN 的自动发现。若健康检查的 VPN 标识和 LocalDevVPN 模式不同，优先看实际设备 Reachable、配对 Verified；不要仅凭名称就认定连接失败。

Anisette 继续使用本次成功的远程 **jkcoxson**，关闭自动轮换。若端点已经连通却仍有 Apple 登录错误，按[登录教程](02-login.md)独立处理。

## 第一次手动续签：逐项验收

1. **软件源可访问**：Safari 打开 `https://github.com/LiveContainer/LiveContainer/releases/download/1.0/apps_ss_lc.json`，能显示 JSON 或下载文件。GitHub 下载可能跳转到资产域名，代理规则也需允许最终下载地址。
2. **设备可通信**：SideStore Health Check 显示 **Reachable**。
3. **配对有效**：Health Check 显示 **Verified**。
4. **续签完成**：进入 **My Apps**，先记下有效期，再点 **Refresh / Refresh All**，等待完成，检查一体包有效期延长。

首次成功后，返回 LiveContainer Settings 点 **Import Certificate from SideStore**，确认按钮变为 **Remove Certificate**，再检查 **JIT-Less Mode Diagnose**；具体步骤见[安装后证书导入](01-install.md)。然后确认容器应用能运行。免费账号通常恢复约 7 天有效期；以实际签名时间和页面显示为准。

日常保持可用 Wi-Fi 和所选 VPN，在到期前手动刷新。可每隔几天检查一次有效期，不要等到最后一天才首次测试。

## 后台与快捷指令

原作者提供了两份按代理客户端区分的快捷指令：

| 使用的客户端 | 快捷指令名称与导入链接 |
| --- | --- |
| Loon | [Refresh All Apps-loon](https://www.icloud.com/shortcuts/84320005e62e4f489e68dda6ee666aaa) |
| Shadowrocket（小火箭） | [Refresh All Apps-Shadowrocket](https://www.icloud.com/shortcuts/12a9b698cb954686814a393794e518bc) |

1. 先按本页完成对应 VPN 回环设置，确认在内置 SideStore 中手动 **Refresh** 可以延长有效期。
2. 在 iPhone / iPad 的 Safari 打开对应链接，点 **获取快捷指令 / 添加快捷指令**，按系统提示导入到「快捷指令」App。
3. 打开导入的快捷指令检查动作。若动作显示 App 缺失或名称不匹配，确认已安装对应客户端与 LiveContainer，并按当前版本选择对应动作；需要选择代理配置或节点时，使用自己的配置。
4. 先手动运行一次，按需授予动作权限。完成后返回 SideStore，核对有效期确实延长，不能只凭快捷指令显示运行结束判断续签成功。
5. 若需要定时续签，在「快捷指令 → 自动化」中新建个人自动化，例如每天固定时间，添加「运行快捷指令」动作并选择已验证的这一份。系统提供「立即运行」选项时可选择它；旧系统按其提示调整运行确认。

快捷指令链接由原作者于 2026-11-10 提供，分享页面可访问且名称已核对。本教程未在设备上逐项执行这两份指令，不预设其中动作顺序。手动执行成功后，继续分别验证定时触发、后台和锁屏场景。

本次没有自动续签验收记录，不能把导入配置等同于「永不掉签」。手动成功但后台报未登录时，查看[对应上游签名问题](04-troubleshooting.md)。

## 回退到 LocalDevVPN

1. 断开小火箭或 Loon；Loon 用户停用本回环插件。
2. SideStore `Connection Configuration` 重新启用 **Use Local VPN**，确认保存并重新打开。
3. 连接 **LocalDevVPN**，再检查设备与配对。
4. 若此网络仍无法直接访问 GitHub，使用下方电脑代理方式补充互联网出口。

### LocalDevVPN + 电脑 Wi-Fi HTTP 代理

这也是旧排查阶段提出的替代路径；本次只验证过电脑代理能访问软件源，未记录该方案的设备刷新结果。

- 电脑与设备连同一 Wi-Fi；在电脑代理客户端中，确认 HTTP / mixed 端口对局域网开放，防火墙允许该端口。
- 设备「设置 → Wi-Fi → 当前网络 ⓘ → 配置代理 → 手动」：服务器填**你电脑的局域网 IP**，端口填**你的 HTTP / mixed 端口**。只有代理本身未启用认证时才关闭认证。
- 保持 LocalDevVPN 已连接，再用 Safari 测试软件源，然后手动 Refresh。

电脑上的 `127.0.0.1:12334` 只接受本机连接时，设备访问不到；必须先确认局域网监听。离开电脑、切换网络或改回手机代理方案后，清除这项 Wi-Fi 手动代理设置。

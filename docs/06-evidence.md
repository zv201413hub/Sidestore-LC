# 版本、验证记录与参考

[返回首页](../README.md)

整理日期：**2026-11-10**。本页区分原作者设备的结果、上游文档与社区案例；参考链接可能更新，不能把别人的结果直接当成本机验收。

## 本次基线

| 对象 | 已记录的版本 / 范围 |
| --- | --- |
| 桌面 | Ubuntu，iLoader 2.4.0 |
| 原一体包 | LiveContainer 3.8.0，缺少所需客户端配置入口 |
| 覆盖更新后一体包 | LiveContainer 3.8.11 |
| 内置 SideStore | 0.7.0-20261017.511+ee3cc16a |
| 小火箭 | 本次版本未记录；社区同一体包案例为 2.2.93 |
| Loon 插件 | 按官方 Build 1007+ 的 include-tun / IP Rewrite 语法整理 |

历史一体 IPA 校验值：

```text
SHA-256: 33831bb279d74f2da1be08eb3cc6d3646992a6120da32ffb763269696052b868
LiveContainer commit: 9108ae624ea001f7d7696d48407f890b48fa2653
SideStore commit: ee3cc16a67f9fed766f79a0ed70938f0f8ad5a07
```

该值来自原安装时的核验记录。本轮原 IPA 已不在下载目录，未再次哈希；仓库不分发旧 IPA。Nightly 的同名 URL 内容会更新，以上哈希只适用于原文件。

## 已完成与待验证

| 日期 | 操作 / 观察 | 结果与边界 |
| --- | --- | --- |
| 2026-10-25 | 电脑代理后端修复 | iLoader 实际请求使用代理，默认路由正常 |
| 2026-10-25 | 桌面 macOS 13.1 客户端描述兼容 | 受信任设备验证码完成，日志确认 Apple ID 登录；高级数据保护保留 |
| 2026-10-25 | 官方一体包覆盖升级 | 版本与新菜单已核对；备份了 Documents / Library，未导出 Keychain / App Group |
| 2026-10-25 | 内置 SideStore 切到远程 Mac 服务 | 用户确认个人 Apple ID 登录成功 |
| 2026-11-09 | 刷新附近出现 `-1004` | 实际失败是 GitHub 软件源更新检查；截图另显示本地通道未连通 |
| 2026-11-09 | LocalDevVPN 连接后 Safari 测试 | 用户确认仍无法访问软件源；电脑经代理访问源为 HTTP 200 |
| 2026-11-09 | 小火箭 + jkcoxson | 用户反馈「小火箭在 anisette servers 选择 jkcoxson 成功了」；没有分项有效期截图、定时或锁屏回执 |
| 2026-11-09 | Loon 插件准备 | 生成文件并查证官方语法；没有设备实测回执 |
| 2026-11-10 | 仓库整理 | 复核历史与当前文件，核对上游安装和 Loon 文档；不再次操作设备账号 |
| 2026-11-10 | 原作者提供两份 iCloud 快捷指令 | 分享页面均可访问，名称分别为 Refresh All Apps-loon / Refresh All Apps-Shadowrocket；加入导入和自动化步骤，设备执行效果尚未逐项验收 |

因此本文可称为安装 / 登录经验及小火箭成功反馈的整理；Loon 是文档核对过的待设备验证方案。设备达到 Reachable、Verified 且有效期延长后，才可记录完整手动续签通过。

## 上游入口

- [iLoader 官网](https://iloader.app)与[源码 / 使用说明](https://github.com/nab138/iloader)：安装、USB 依赖、官方一体包与配对支持。
- [iLoader 发行页](https://github.com/nab138/iloader/releases)：选择当前系统和架构的版本。
- [LiveContainer 安装指南](https://livecontainer.github.io/zh-CN/docs/installation/lc_sidestore)：一体包安装、首次刷新、证书导入与免 JIT 诊断。本轮重新读取。
- [LiveContainer 发行页](https://github.com/LiveContainer/LiveContainer/releases)与[Nightly](https://github.com/LiveContainer/LiveContainer/releases/tag/nightly)：官方 IPA。
- [SideStore 源码说明](https://github.com/SideStore/SideStore)：设备本地通道与 7 天开发签名刷新机制。
- [Loon Plugin / IP Rewrite](https://loon0x00.github.io/docs/Plugin/#ip-rewrite)及[General](https://loon0x00.github.io/docs/General/)：Build 1007+、插件模块位置、包含路由与 reflect 行为。本轮重新读取。
- [Shadowrocket 功能公告](https://t.me/s/ShadowrocketNews/1588)：原回环功能调查时引用；本轮未重新读取公告。
- [小火箭显式端点社区案例 PR #2](https://github.com/nikiz24/shadowrocket-sidestore-rules/pull/2)：2.2.93 与同一体包的设备连接、普通 Refresh 和手动快捷指令结果。本轮重新读取；案例未验证自动定时和锁屏触发。
- [LiveContainer #1629](https://github.com/LiveContainer/LiveContainer/issues/1629)：初次电脑安装后一体包的后台签名 / 凭据问题与再次经 SideStore 安装的修法。本轮重新读取；当前官方同时要求使用最新 iLoader，不把历史问题写成所有新版必现。
- [Apple 高级数据保护](https://support.apple.com/en-us/108756)：系统兼容要求。
- [iLoader #1031](https://github.com/nab138/iloader/issues/1031)、[SideStore #1688](https://github.com/SideStore/SideStore/issues/1688)、[#1675](https://github.com/SideStore/SideStore/issues/1675)：原登录排查的参考线索，本次本机结论以实际登录反馈为准。

## 仓库内容来源

教程由本次操作记录重新编写，没有复制上游完整说明或安装包。Loon 插件和客户端 JSON 沿用当时生成的公开配置；`relay.py` 沿用原本机兼容实现；代理启动器增加可配置代理 URL 与显式的兼容服务开关，systemd 示例将个人家目录换为 `%h`。

第三方软件、服务和商标归各自项目。本仓库不代替上游项目源码、许可或支持渠道。

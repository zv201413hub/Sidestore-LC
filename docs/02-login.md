# 2. Apple ID 与 Anisette

[返回首页](../README.md) · 上一步：[安装](01-install.md) · 下一步：[VPN 与续签](03-vpn-and-refresh.md)

电脑 iLoader 和设备内 SideStore 分别登录。电脑登录成功，并不意味着 SideStore 已登录；电脑的 localhost 兼容服务也不会自动应用到设备。

Anisette 为 Apple 登录提供客户端认证数据，VPN 回环负责 SideStore 与设备通信，两者应分别核对。

## 先按正常流程登录

1. 保持 Wi-Fi 联网，按[VPN 教程](03-vpn-and-refresh.md)建立设备通道。
2. 在内置 SideStore 的 Settings 登录自己的 Apple ID，验证码直接输入应用。
3. 若当前配置已经成功，不必为和示例一致而更改所有字段。

本次小火箭操作后，选择 **jkcoxson** 得到成功反馈。要复用本次远程服务选择：

- `Settings → Anisette Servers` 选择 **jkcoxson**。
- 核对地址：`https://mac-ani.jkcoxson.com`。
- 关闭 **Enable Auto Rotation**，让测试使用同一服务。
- 若开启 **On-Device Anisette**，需要切换为远程模式后再检验服务器选择是否生效。

远程 Anisette 依赖第三方服务的可用性。以后若它不可用，按当前官方说明和实际错误重新检查，不把这个地址当成永久保证。

## 本次 `-80045` 的兼容步骤

以下是在 **2026-10-25** 的特定一体包和开启 iCloud 高级数据保护的账号中验证过的组合。`-80045` 本身不能证明所有设备都遇到了同一个原因。

当时的版本是 LiveContainer **3.8.11**，内置 SideStore **0.7.0-20261017.511+ee3cc16a**。旧版缺少菜单时，先用原签名账号[覆盖更新](01-install.md)。

1. 进入 `Settings → User Customizations → Anisette Client Configuration → Interactive`。
2. 填写这两个字段：

   **Client Info**

   ```text
   <MacBookPro13,2> <macOS;13.1;22C65> <com.apple.AuthKit/1 (com.apple.akd/1.0)>
   ```

   **User Agent**

   ```text
   akd/1.0 CFNetwork/808.1.4
   ```

   点 **Save Overrides**，退出再进入页面，确认字段已经保存。相同字段另存于 [JSON 示例](../configs/SideStore-client-macOS13.1.json)；它不是 iLoader 配置，也不是完整 SideSign 配置，不要直接覆盖其他 JSON。

3. 在 `User Customizations` 关闭 **On-Device Anisette**，弹窗选择 **Restart Now**，然后重新打开应用。
4. 进入 `Settings → Anisette Servers`，选 **jkcoxson**，关闭自动轮换。不要误选 **jkcoxson (Windows ADI)**。
5. 确认设备 Reachable、配对 Verified，再重试登录并完成验证码。

在当时的版本，切换 On-Device Anisette 会清除旧 provisioning 数据和登录会话，保留签名证书及字段覆盖；需重新登录。仅改客户端字段、仍保持 On-Device Anisette 开启时，本次仍失败；切换远程 Mac 服务后才得到成功反馈。

本次一直保留 iCloud 高级数据保护，没有通过关闭它来验收登录。

## 不要混淆这些设置

| 设置 | 用途 | 本次处理 |
| --- | --- | --- |
| Anisette Client Configuration | 认证中的 `X-MMe-Client-Info` 等字段 | 在上述兼容故障中使用 macOS 13.1 描述 |
| SideSign Config | GSA、IDMSA、Developer Services 请求参数 | 保留原设置，没有机械改成 13.1 |
| Connection Configuration | SideStore 到本机设备的连接 | 按 VPN 方案选择本地模式或显式端点 |
| 电脑 iLoader Anisette 设置 | 电脑端认证服务 | 可选 localhost 中继，仅电脑可用 |

SideSign 默认描述里出现 OS X 26.6 不等于应当修改。旧版部分输入框白字白底，看起来空白；先选中文字或查看 Raw JSON，确认真实值再操作。

## 登录完成后如何验收

登录页面显示账号只是第一步。还要检查 Health Check 的设备与配对状态，再进行一次手动 Refresh，记录有效期变化。DDI 未挂载在本次版本中是 JIT 相关提示，本次在该状态下也能登录；是否影响你要运行的 JIT 应用，另按对应指南处理。

电脑 iLoader 的短信 403 请看[Ubuntu 兼容方案](05-ubuntu-compat.md)。仍登录失败时记录错误域、完整错误文字与失败阶段，避免连续盲试或重置配对。

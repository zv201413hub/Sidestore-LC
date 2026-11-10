# 1. 安装与首次运行

[返回首页](../README.md) · 下一步：[登录](02-login.md)

## 下载正确的版本

本文使用 **LiveContainer + SideStore 一体包**。独立 `LiveContainer.ipa` 没有内置 SideStore，菜单和续签流程不同。当前官方要求使用最新 iLoader；旧签名器可能无法正确处理一体包。

1. 从 [iLoader 官方发行页](https://github.com/nab138/iloader/releases)下载适合系统与架构的安装包；Ubuntu 使用对应的 `.deb`。
2. 从 [LiveContainer 官方发行页](https://github.com/LiveContainer/LiveContainer/releases)下载 `LiveContainer+SideStore.ipa`。
3. 优先检查稳定版是否包含所需菜单。本文历史上为获得 `User Customizations` 使用了官方 Nightly；这是当时的适配措施，不要求每个人都安装 Nightly。

[稳定版一体 IPA](https://github.com/LiveContainer/LiveContainer/releases/latest/download/LiveContainer+SideStore.ipa) · [Nightly 一体 IPA](https://github.com/LiveContainer/LiveContainer/releases/download/nightly/LiveContainer+SideStore.ipa)

Nightly 地址会更新。下载后记下版本、来源和校验值；不要拿本教程旧版本的 SHA-256 去验证新包。

```bash
sha256sum /实际下载路径/LiveContainer+SideStore.ipa
```

这条命令记录本地文件哈希；若发行页提供官方校验值，还需逐字比对，单独计算哈希不等于官方校验通过。

## Ubuntu 安装与 USB 连接

需要执行下面安装命令时，先把文件路径改成自己的。已经安装的用户可跳过对应步骤。

```bash
sudo apt install usbmuxd libimobiledevice-utils
sudo apt install /实际下载路径/iloader_实际版本_实际架构.deb
```

1. 用数据线连接设备，解锁屏幕，接受「信任此电脑」并输入设备密码。
2. 打开 iLoader，确认设备被识别。
3. 若未识别，先检查线材、USB 和信任状态：

   ```bash
   lsusb
   systemctl status usbmuxd --no-pager
   ideviceinfo -k ProductVersion
   ```

   最后一条能返回系统版本，说明基本 USB 通信已经建立；它不代表安装或登录已经完成。

Windows 的驱动准备与 macOS 操作请跟随 [iLoader 官方说明](https://github.com/nab138/iloader#how-to-use)；本教程的终端命令只针对 Ubuntu。

## 用 iLoader 首次安装

1. 在 iLoader 登录自己的 Apple ID，按提示完成双重验证。电脑无法登录时先看[登录排查](02-login.md)，不要反复重装手机应用。
2. 选择安装 **LiveContainer + SideStore**；若当前版本提供 IPA 导入入口，也可选择上面下载的官方一体 IPA。
3. 按当前 iLoader 的安装向导完成证书和配对文件导入。官方 iLoader 支持自动放置 lockdown / rppairing 文件；不要把别人的配对文件复制到自己的设备。
4. 等待 iLoader 报告安装完成，在设备主屏幕确认出现 LiveContainer。
5. 按系统提示，在「设置 → 通用 → VPN 与设备管理」信任对应开发者。系统要求开发者模式时，再按官方指南启用并完成重启确认。
6. 打开 LiveContainer，在 **Apps 页左上角点 SideStore 按钮**进入内置 SideStore。菜单以一体包的实际 UI 为准；若找不到 SideStore，先核对下载的是不是独立包。

接下来先完成[设备内登录](02-login.md)与[第一次 Refresh](03-vpn-and-refresh.md)，再导入证书：

1. 退出内置 SideStore，返回 LiveContainer。
2. 在 LiveContainer Settings 点 **Import Certificate from SideStore** 并确认。
3. 按钮变为 **Remove Certificate** 表示导入成功；进入 **JIT-Less Mode Diagnose** 核对配置。
4. 若自动导入报「证书未找到」，在内置 SideStore Settings 使用 **Export Signing Certificate…**，给导出的证书设密码并保存在设备私人位置；返回 LiveContainer 使用 **Import Certificate** 选择该文件并输入密码。

这是[官方一体包安装后设置](https://livecontainer.github.io/docs/installation/lc_sidestore)的操作要求，本次历史没有单独保留证书导入回执。证书文件不要加入公开仓库。DDI 挂载与 JIT 是另一个步骤，不以它们代替登录和刷新验收。

## 已安装用户覆盖更新

1. 先备份自己的应用数据与配对文件，记录原签名 Apple ID、安装版本。备份保留在私人位置。
2. 使用原签名账号覆盖安装官方一体包；不要先删除旧应用。换账号可能改变应用标识后缀，安装出另一份应用。
3. 更新完成后，检查内置应用数据、配对状态和版本，确认 `Settings → User Customizations` 等所需入口存在。

本次从 LiveContainer 3.8.0 覆盖升级到 3.8.11 后，内置 SideStore 才具备所需客户端配置入口。升级前保存了容器 Documents / Library，但没有导出 Keychain 和 App Group，不能视为完整凭据备份。

首次通过电脑安装后，若手动刷新正常但快捷指令或组件读取不到登录状态，上游还建议在**内置 SideStore 的安装入口**再次安装官方 Nightly 一体 IPA，见[后台刷新排查](04-troubleshooting.md)。这项处理按症状使用。

## 在 LiveContainer 中使用其他应用

打开 LiveContainer，点右上角 `+`，选择自己有权使用的 IPA。导入后点应用运行，长按条目可管理应用和数据容器。

LiveContainer 的容器内应用与 SideStore 直接侧载到主屏幕的应用不同。容器内应用也有兼容性限制；不能假定所有 IPA 都可正常运行，遇到问题查询[官方 FAQ](https://livecontainer.github.io/docs/faq)。日常续签先关注宿主一体包在 SideStore 中的有效期。

完成安装后进入[登录步骤](02-login.md)，再选择[小火箭或 Loon](03-vpn-and-refresh.md)并做第一次手动 Refresh。

# 随包工具来源

应用原许可证在各项目根目录；完整上游源码注明于各 UPSTREAM.md。

- Python wheels：PyPI 官方发布，精确版本在 requirements.lock.txt，各包许可证包含于 wheel 的 dist-info。
- ChromeDriver：Chrome for Testing 官方 157.0.8103.78 Windows 64 位构建，LICENSE.chromedriver 与 THIRD_PARTY_NOTICES.chromedriver 随包保留。
- Apache Tomcat 11.0.27：https://tomcat.apache.org/ ，发行版 LICENSE、NOTICE 随包保留。
- Apache Maven 3.10.0：https://maven.apache.org/ ，发行版 LICENSE、NOTICE 随包保留。
- 构建桥接：本地 HTTP 仅监听 127.0.0.1，将 Maven Central 下载交给 Python Requests；对外使用正常校验证书的 HTTPS，没有关闭 TLS 校验。

这些工具用于本地运行。Git 忽略二进制运行包、缓存和工具目录；准备公开源码时保留本文件及项目来源说明。

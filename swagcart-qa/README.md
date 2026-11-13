# SwagCart QA · 电商页面自动化测试

它是一个模拟购物网站。你可以登录、选商品、放进购物车、填写收货信息、完成结算。你要做的工作，是让程序像人一样操作浏览器，检查这些步骤有没有出错。它没有真实付款，也没有真实电商订单后端。

技术栈：Python / Selenium / Pytest / Page Object / React / Vite。

## 启动与测试

保留上一级项目总文件夹及 tooling。双击本目录 `start.cmd` 启动，浏览器访问 http://127.0.0.1:3200/。按 Ctrl+C 停止，再双击 `test.cmd` 运行自动测试。第一次安装和排错见总目录“新手开始.md”。

## 测试范围

登录成功和错误提示；四种商品排序；购物车增删、刷新；结算必填项；中英文姓名；小计、8% 示例税额和总价；完成后购物车清空；未登录页面跳转。

## 个人改造范围

新增 qa/ 下的 Selenium Page Object 与 16 个参数化测试实例；明确页面等待条件；失败截图、HTML 和浏览器日志；替换本地页头；关闭外部错误上报；精简本地 Vite 依赖并保留原依赖清单。

主要代码：

- `qa/pages.py`
- `qa/conftest.py`
- `qa/test_storefront.py`
- `src/qaTelemetry.jsx`
- `src/components/HeaderContainer.jsx`
- `package.json`

`docs/需求与用例.md` 解释预期；`docs/问题记录.md` 记录修改前后；`docs/代码与面试讲解.md` 帮助读代码；`reports/results.xml` 是本机真实执行报告。

## 开源来源与边界

基于 [saucelabs/sample-app-web](https://github.com/saucelabs/sample-app-web)，固定提交 `d5cd655fa8a974f4ddb6fde2868586e0084211d2`（2026-11-05），许可 MIT。原业务实现、作者信息和许可证保留。详见 `UPSTREAM_README.md`、`UPSTREAM.md` 与原许可证文件。

这是个人学习和求职作品：不声称从零开发原业务系统，不代表真实生产、真实金融或 Web3 经验。当前执行范围和限制见总目录“验证汇总.md”。

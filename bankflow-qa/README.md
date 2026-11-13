# BankFlow QA · 银行交易接口与资金一致性测试

它是一家虚拟银行。账户余额、存款、取款和转账都是演示数据。你的重点是检查：转账前后双方余额是否变化正确、总金额是否守恒、是否产生配对流水，以及转账失败会不会只扣钱却没到账。

技术栈：Java 21 / Tomcat 11 / HSQLDB / Python / Requests / Pytest / Decimal。

## 启动与测试

保留上一级项目总文件夹及 tooling。双击本目录 `start.cmd` 启动，浏览器访问 http://127.0.0.1:8087/parabank/。按 Ctrl+C 停止，再双击 `test.cmd` 运行自动测试。第一次安装和排错见总目录“新手开始.md”。

## 测试范围

演示账号与账户列表；四种金额转账；借贷流水配对；0.10+0.20 精确存款；取款；零、负数、三位小数及缺失金额；同账户转账；目标账户不存在时回滚；按金额筛选流水。

## 个人改造范围

新增 15 个金融业务 HTTP 回归实例，用 Decimal 独立计算余额与金额守恒；每例重置本地演示数据；新增“正金额、最多两位小数、不同账户”的练习需求并实现 400 校验；验证失败转账的余额和流水回滚；提供 Postman 集合。

主要代码：

- `qa/conftest.py`
- `qa/test_bank_transactions.py`
- `src/main/java/com/parasoft/parabank/service/ParaBankServiceImpl.java`
- `src/main/webapp/WEB-INF/jsp/template.jsp`
- `pom.qa.xml`

`docs/需求与用例.md` 解释预期；`docs/问题记录.md` 记录修改前后；`docs/代码与面试讲解.md` 帮助读代码；`reports/results.xml` 是本机真实执行报告。

## 开源来源与边界

基于 [parasoft/parabank](https://github.com/parasoft/parabank)，固定提交 `5da29e5f7c97019b5afdd7281d2e4a0db8e941e5`（2026-11-11），许可 Apache-2.0。原业务实现、作者信息和许可证保留。详见 `UPSTREAM_README.md`、`UPSTREAM.md` 与原许可证文件。

这是个人学习和求职作品：不声称从零开发原业务系统，不代表真实生产、真实金融或 Web3 经验。当前执行范围和限制见总目录“验证汇总.md”。

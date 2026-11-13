# ClinicFlow QA · 诊所业务接口测试

它是一个宠物诊所的后台服务：登记主人、登记宠物、记录就诊。这里没有完整的挂号网页，你通过 Swagger 或 Python 发送接口请求，检查数据库里的业务结果是否正确。

技术栈：Java 21 / Spring Boot / H2 / Python / Requests / Pytest / OpenAPI。

## 启动与测试

保留上一级项目总文件夹及 tooling。双击本目录 `start.cmd` 启动，浏览器访问 http://127.0.0.1:9966/petclinic/swagger-ui.html。按 Ctrl+C 停止，再双击 `test.cmd` 运行自动测试。第一次安装和排错见总目录“新手开始.md”。

## 测试范围

主人增删改查；姓名长度 1/30/31 和中文；电话号码长度、类型和空值；主人→宠物→就诊完整流程；不存在资源；嵌套接口关系一致性；分页边界。

## 个人改造范围

新增 23 个真实 HTTP 回归实例、自动创建与清理测试数据的 fixture；修复错误主人路径仍能修改宠物或添加就诊的问题；将查询参数校验异常映射为 400；增加分页防御判断；提供 Postman 入门集合。

主要代码：

- `qa/conftest.py`
- `qa/test_clinic_api.py`
- `src/main/java/org/springframework/samples/petclinic/rest/controller/v1/OwnerRestControllerV1.java`
- `src/main/java/org/springframework/samples/petclinic/rest/controller/v2/OwnerRestControllerV2.java`
- `src/main/java/org/springframework/samples/petclinic/rest/advice/ExceptionControllerAdvice.java`

`docs/需求与用例.md` 解释预期；`docs/问题记录.md` 记录修改前后；`docs/代码与面试讲解.md` 帮助读代码；`reports/results.xml` 是本机真实执行报告。

## 开源来源与边界

基于 [spring-petclinic/spring-petclinic-rest](https://github.com/spring-petclinic/spring-petclinic-rest)，固定提交 `a4cb2c86272265c2916023074a771463f7114104`（2026-11-09），许可 Apache-2.0。原业务实现、作者信息和许可证保留。详见 `UPSTREAM_README.md`、`UPSTREAM.md` 与原许可证文件。

这是个人学习和求职作品：不声称从零开发原业务系统，不代表真实生产、真实金融或 Web3 经验。当前执行范围和限制见总目录“验证汇总.md”。

# bankflow-qa 项目摸底报告

## 基本信息

| 字段 | 值 |
| --- | --- |
| repo_path | C:\Users\ZhuanZ\Documents\Codex\2026-11-13\d\outputs\additional-qa-projects\bankflow-qa |
| generated_at | 2026-11-13T15:24:25.400435+00:00 |
| file_count_scanned | 468 |
| approx_total_bytes | 11075412 |

## 语言和文件类型

| 语言 | 文件数 |
| --- | --- |
| Java | 274 |
| Other | 172 |
| Shell | 10 |
| SQL | 7 |
| Python | 2 |
| JavaScript | 2 |
| YAML | 1 |

## 依赖和环境线索

- `Dockerfile`
- `pom.xml`

## README

- `README.md`
- `src/main/scripts/README.md`

## 核心链路线索

| 类别 | 命中文件数 | 代表路径 |
| --- | --- | --- |
| api_backend | 40 | soatest/TestAssets/PB-ParabankServices-v3.tst<br>soatest/VirtualAssets/Loan Approval Services-Proxy.pmpdd<br>soatest/VirtualAssets/REST Service-Proxy.pmpdd<br>soatest/VirtualAssets/SOAP Services-Proxy.pmpdd<br>soatest/VirtualAssets/recorded_traffic/Loan_Approval_Services_2016-09-22_15-31-50-422.txt<br>soatest/VirtualAssets/recorded_traffic/REST_Service_2016-09-22_15-31-46-297.txt<br>src/main/assembly/sources-jst_web.xml<br>src/main/java/com/parasoft/bookstore/Book.java |
| config | 6 | soatest/templatesettings.properties<br>src/main/java/com/parasoft/parabank/domain/logic/impl/ConfigurableLoanProvider.java<br>src/main/java/com/parasoft/parabank/service/ParaBankServiceConfiguration.java<br>src/main/webapp/WEB-INF/swagger.yaml<br>src/test/java/com/parasoft/parabank/service/ParaBankServiceConfigurationTest.java<br>src/test/java/com/parasoft/parabank/test/util/LoanRequestTestConfig.java |
| database_state | 40 | src/main/java/com/parasoft/bookstore/BookStoreDB.java<br>src/main/java/com/parasoft/bookstore/BookStoreMemoryDB.java<br>src/main/java/com/parasoft/bookstore/DB.java<br>src/main/java/com/parasoft/bookstore/jdbc/JdbcBookstoreDao.java<br>src/main/java/com/parasoft/bookstore2/BookStoreDB.java<br>src/main/java/com/parasoft/bookstore2/BookStoreMemoryDB.java<br>src/main/java/com/parasoft/bookstore2/DB.java<br>src/main/java/com/parasoft/parabank/dao/AccountDao.java |
| devops_deploy | 6 | Dockerfile<br>deploy-jtest-monitor.bat<br>deploy-jtest-monitor.sh<br>deploy.bat<br>soatest/docker/soatestcli<br>src/test/resources/url-ref/InsufficientFunds.xml |
| evaluation | 40 | deploy-jtest-monitor.bat<br>deploy-jtest-monitor.sh<br>jtest-ft-cov.bat<br>jtest-ft-cov.sh<br>jtest-mt-cov.bat<br>jtest-mt-cov.sh<br>jtest-sa-ut-delta.bat<br>jtest-sa-ut-delta.sh |
| frontend_mobile | 40 | soatest/Bookstore/.parasoft<br>soatest/Bookstore/.project<br>soatest/Bookstore/PB-Bookstore1.tst<br>soatest/Bookstore/PB-Bookstore2.tst<br>soatest/TestAssets/keystores/soatest.pfx<br>src/main/java/com/parasoft/bookstore/Book.java<br>src/main/java/com/parasoft/bookstore/BookStoreDB.java<br>src/main/java/com/parasoft/bookstore/BookStoreMemoryDB.java |
| inference_demo | 40 | soatest/ApplicationCoverage.properties<br>soatest/VirtualAssets/Loan Approval Services-Proxy.pmpdd<br>soatest/VirtualAssets/recorded_traffic/Loan_Approval_Services_2016-09-22_15-31-50-422.txt<br>src/main/java/com/parasoft/parabank/util/ServerBean.java<br>src/main/resources/applicationContext-base.xml<br>src/main/resources/applicationContext-hsqldb.xml<br>src/main/resources/applicationContext-jms.xml<br>src/main/resources/applicationContext.xml |
| security_auth | 1 | src/main/java/com/parasoft/parabank/web/controller/exception/AuthenticationException.java |
| testing_quality | 40 | deploy-jtest-monitor.bat<br>deploy-jtest-monitor.sh<br>jtest-ft-cov.bat<br>jtest-ft-cov.sh<br>jtest-mt-cov.bat<br>jtest-mt-cov.sh<br>jtest-sa-ut-delta.bat<br>jtest-sa-ut-delta.sh |

## Notebook / Docker / Test 线索

### Notebooks
- 无

### Docker
- `Dockerfile`
- `soatest/docker/soatestcli`

### Tests
- `deploy-jtest-monitor.bat`
- `deploy-jtest-monitor.sh`
- `jtest-ft-cov.bat`
- `jtest-ft-cov.sh`
- `jtest-mt-cov.bat`
- `jtest-mt-cov.sh`
- `jtest-sa-ut-delta.bat`
- `jtest-sa-ut-delta.sh`
- `jtest-sa-ut.bat`
- `jtest-sa-ut.sh`
- `jtest-security-sa.bat`
- `pytest.ini`
- `qa/conftest.py`
- `qa/test_bank_transactions.py`
- `soatest.bat`
- `soatest.sh`
- `soatest/TestAssets/keystores/soatest.pfx`
- `soatest/docker/soatestcli`
- `src/main/resources/com/parasoft/bookstore/resources/soatest.pfx`
- `src/main/webapp/soatest.pfx`
- `src/test/java/com/parasoft/bookstore/AbstractCartService.java`
- `src/test/java/com/parasoft/bookstore/CartServiceTest.java`
- `src/test/java/com/parasoft/bookstore2/AbstractCartService.java`
- `src/test/java/com/parasoft/bookstore2/CartServiceTest.java`
- `src/test/java/com/parasoft/bookstore2/OrderTest.java`
- `src/test/java/com/parasoft/parabank/dao/InMemoryAccountDao.java`
- `src/test/java/com/parasoft/parabank/dao/InMemoryAdminDao.java`
- `src/test/java/com/parasoft/parabank/dao/InMemoryCustomerDao.java`
- `src/test/java/com/parasoft/parabank/dao/InMemoryPositionDao.java`
- `src/test/java/com/parasoft/parabank/dao/InMemoryTransactionDao.java`

## 潜在数据/状态/模型/资源路径

- `src/main/webapp/schemas/cust.xsd`

## 目录树摘要

```text
bankflow-qa/
  docs/
  qa/
  soatest/
  src/
  .classpath
  .gitignore
  .project
  Dockerfile
  LICENSE
  README.md
  Security Rules.properties
  UPSTREAM.md
  UPSTREAM_README.md
  deploy-jtest-monitor.bat
  deploy-jtest-monitor.sh
  deploy.bat
  jtest-ft-cov.bat
  jtest-ft-cov.sh
  jtest-mt-cov.bat
  jtest-mt-cov.sh
  jtest-sa-ut-delta.bat
  jtest-sa-ut-delta.sh
  jtest-sa-ut.bat
  jtest-sa-ut.sh
  jtest-security-sa.bat
  parabank.launch
  pom.qa.xml
  pom.xml
  pytest.ini
  renovate.json
  selenic.bat
  selenic.sh
  set-vars.bat
  set-vars.sh
  soatest.bat
  soatest.sh
  start.cmd
  test.cmd
    Postman练习.md
    代码与面试讲解.md
    问题记录.md
    需求与用例.md
    conftest.py
    postman.collection.json
    test_bank_transactions.py
    Bookstore/
    TestAssets/
    VirtualAssets/
    docker/
    ApplicationCoverage.properties
    templatesettings.properties
      .parasoft
      .project
      PB-Bookstore1.tst
      PB-Bookstore2.tst
      keystores/
      system_jars/
      .parasoft
      .project
      PB-ParabankServices-v3.tst
      PB-WebUI-v3.tst
      Smoke.tst
      LoanProcessor/
      recorded_traffic/
      .project
      Loan Approval Services-Proxy.pmpdd
      REST Service-Proxy.pmpdd
      SOAP Services-Proxy.pmpdd
      VirtualAssets.xml
      admin.pmpdd
      soatestcli
    main/
    test/
      assembly/
      java/
      resources/
      scripts/
      webapp/
      java/
      resources/
```

## 下一步人工确认

- 找到最小可运行命令：API、页面、CLI、worker、测试、训练或 demo 至少一个。
- 确认依赖、环境变量、数据库/数据文件、端口和外部服务。
- 确认 baseline/demo 是否能在本地、Docker、云服务器或 GPU 环境上跑通。
- 确认自己要做的面试亮点：改造点、demo、测试、报告或实验计划。

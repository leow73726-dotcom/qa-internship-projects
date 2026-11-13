# QA Internship Projects

基于开源业务系统构建的软件测试实战项目，涵盖电商页面自动化、诊所业务接口和银行交易验证。

项目围绕需求分析、用例设计、测试数据管理、自动化执行、问题复现与回归验证展开，使用 Python、Selenium、Requests、Pytest 和 Java 实现测试与业务改造。

## 项目概览

| 项目 | 业务场景 | 核心测试内容 | 技术栈 |
| --- | --- | --- | --- |
| [SwagCart QA](./swagcart-qa/) | 模拟电商购物 | 登录、排序、购物车、结算 | Python、Selenium、Pytest、React |
| [ClinicFlow QA](./clinicflow-qa/) | 宠物诊所管理 | CRUD、参数边界、资源关联、异常响应 | Python、Requests、Pytest、Spring Boot、H2 |
| [BankFlow QA](./bankflow-qa/) | 模拟银行交易 | 金额守恒、流水配对、输入校验、事务回滚 | Python、Requests、Pytest、Java、Tomcat、HSQLDB |

## 测试与改造内容

### SwagCart QA：电商页面自动化

围绕“登录 → 浏览商品 → 加入购物车 → 填写信息 → 完成结算”设计自动化回归。

- 使用 Page Object 分离页面操作与业务断言。
- 覆盖正常登录、错误提示、锁定账号和匿名访问。
- 验证商品名称与价格的升降序排序。
- 检查购物车增删、刷新后的状态及结算后的清空行为。
- 覆盖结算必填项与中英文姓名输入。
- 使用 Decimal 独立计算小计、示例税额和总价。
- 失败时保存截图、页面 HTML、URL 和浏览器控制台日志。

### ClinicFlow QA：诊所业务接口

围绕“创建主人 → 登记宠物 → 添加就诊记录”验证接口行为与数据关联。

- 覆盖主人信息的创建、查询、修改和删除。
- 使用参数化测试验证姓名长度、中文输入、电话号码格式与空值。
- 使用 fixture 创建唯一测试数据，并在测试后清理。
- 验证主人、宠物和就诊记录之间的关联。
- 复现并修复错误主人路径仍能修改宠物或新增就诊记录的问题。
- 为查询参数校验异常增加 HTTP 400 映射。
- 提供 Postman 集合用于接口调试。

嵌套接口测试关注资源关系一致性；默认演示配置关闭身份认证。

### BankFlow QA：银行交易验证

围绕账户余额、转账和交易流水验证资金变化与失败处理。

- 使用 Decimal 进行十进制金额断言。
- 验证转账后双方余额变化及总金额守恒。
- 检查转账生成的 Debit、Credit 流水是否配对。
- 验证存款、取款与按金额查询流水。
- 验证目标账户不存在时，原账户余额与流水保持不变。
- 新增转账练习规则：金额必须为正、最多两位有效小数、来源与目标账户不同。
- 每个测试实例重置独立本地演示数据。

新增输入规则属于本仓库的业务扩展；事务回滚机制来自上游实现，本仓库增加了对应验证用例。

## 测试结果

2026-11-13 在 Windows 本地环境完成以下验证：

| 项目 | 新增测试实例 | 通过 | 失败 |
| --- | ---: | ---: | ---: |
| SwagCart QA | 16 | 16 | 0 |
| ClinicFlow QA | 23 | 23 | 0 |
| BankFlow QA | 15 | 15 | 0 |
| **合计** | **54** | **54** | **0** |

测试通过真实浏览器或真实 HTTP 请求执行。数量对应新增 `qa/` 测试实例，不代表代码覆盖率或上游完整测试套件的执行结果。

各项目的 `reports/` 包含：

- `results.xml`：JUnit 格式测试结果。
- `cases.csv`：逐例执行结果。
- `evidence.json`：验证环境、时间与报告摘要。
- `baseline.xml`：诊所、银行项目的修改前测试结果。

## 目录结构

```text
qa-internship-projects/
├── swagcart-qa/
│   ├── src/                  # 电商应用源码
│   ├── qa/                   # Selenium 页面对象与测试
│   ├── docs/                 # 需求映射与问题记录
│   └── reports/              # 测试结果
├── clinicflow-qa/
│   ├── src/                  # 诊所服务源码
│   ├── qa/                   # 接口测试与 Postman 集合
│   ├── docs/
│   └── reports/
├── bankflow-qa/
│   ├── src/                  # 银行演示系统源码
│   ├── qa/                   # 交易测试与 Postman 集合
│   ├── docs/
│   └── reports/
├── tooling/                  # 共用启动、构建脚本与依赖锁
├── setup.py                  # Python 测试环境初始化
└── 开始使用.cmd               # Windows 交互入口
```

## 环境要求

当前启动脚本以 Windows 为运行平台。

| 依赖 | 用途 |
| --- | --- |
| Python 3.12 | 测试环境与运行脚本 |
| Node.js 24.9+ | 电商应用构建 |
| Chrome | Selenium 浏览器测试 |
| JDK 21 | 诊所与银行应用 |
| Maven | Java 应用源码构建 |
| Tomcat 11.0.27 | 银行应用部署 |

Python 依赖版本固定于 `tooling/requirements.lock.txt`。浏览器驱动可通过 `CHROMEDRIVER` 指定；未提供本地驱动时，由 Selenium Manager 尝试获取匹配版本。

## 获取源码

```powershell
git clone https://github.com/leow73726-dotcom/qa-internship-projects.git
cd qa-internship-projects
python setup.py
```

GitHub 仓库提供源码、测试与文档。虚拟环境、运行包、工具二进制和依赖缓存均已通过 `.gitignore` 排除，首次运行需要安装相关工具并构建应用。

以下命令均从仓库根目录执行。

### 运行 SwagCart QA

安装依赖并构建电商应用：

```powershell
cd swagcart-qa
npm ci
npm run build
cd ..
```

准备启动脚本使用的静态文件目录：

```powershell
New-Item -ItemType Directory -Force swagcart-qa/runtime/site | Out-Null
Copy-Item swagcart-qa/build/* swagcart-qa/runtime/site/ -Recurse -Force
```

启动应用并执行测试：

```powershell
.\.venv\Scripts\python.exe tooling/launcher.py --project swagcart-qa --test
```

### 运行 ClinicFlow QA

确保 Maven 使用 JDK 21，构建并复制运行包：

```powershell
mvn -f clinicflow-qa/pom.qa.xml "-Dmaven.test.skip=true" package

New-Item -ItemType Directory -Force clinicflow-qa/runtime | Out-Null

Copy-Item clinicflow-qa/target/spring-petclinic-rest-4.0.2.jar clinicflow-qa/runtime/clinicflow.jar -Force
```

执行接口测试：

```powershell
.\.venv\Scripts\python.exe tooling/launcher.py --project clinicflow-qa --test
```

### 运行 BankFlow QA

将 Tomcat 11.0.27 二进制发行版解压至：

```text
tooling/apache-tomcat-11.0.27/
```

该目录下应包含 `bin/`、`conf/` 和 `lib/`。

构建并复制银行应用：

```powershell
mvn -f bankflow-qa/pom.qa.xml "-Dmaven.test.skip=true" package

New-Item -ItemType Directory -Force bankflow-qa/runtime | Out-Null

Copy-Item bankflow-qa/target/parabank-6.0.0-SNAPSHOT.war bankflow-qa/runtime/parabank.war -Force
```

执行交易测试：

```powershell
.\.venv\Scripts\python.exe tooling/launcher.py --project bankflow-qa --test
```

### 手动访问应用

省略启动命令中的 `--test` 即可持续运行应用；按 `Ctrl+C` 停止。

| 项目 | 本地地址 | 演示账号 |
| --- | --- | --- |
| SwagCart QA | http://127.0.0.1:3200/ | `standard_user` / `secret_sauce` |
| ClinicFlow QA | http://127.0.0.1:9966/petclinic/swagger-ui.html | 默认配置关闭认证 |
| BankFlow QA | http://127.0.0.1:8087/parabank/ | `john` / `demo` |

执行自动测试前，应停止同一项目的手动实例，避免端口占用。测试脚本会管理自己启动的应用进程。

## 测试数据与验证范围

- 诊所应用使用本地 H2 演示数据，测试通过 fixture 创建并清理记录。
- 银行测试会重置本地演示数据库，仅适用于独立测试实例。
- 自动化用例限制访问本地主机。
- Java 构建命令跳过上游测试，新增回归由 `qa/` 中的 Pytest 用例执行。
- Postman 集合用于手动调试，以上通过统计来自 Pytest。
- 当前结果覆盖指定本地配置；性能并发、跨浏览器、其他数据库和生产部署尚未验证。
- 电商与银行均为模拟业务，不涉及真实支付或真实资金。

## 开源来源与许可

本仓库在保留上游业务实现的基础上，增加测试代码、运行适配、业务规则、问题修复和文档。

| 项目 | 上游仓库 | 上游许可 |
| --- | --- | --- |
| SwagCart QA | [saucelabs/sample-app-web](https://github.com/saucelabs/sample-app-web) | MIT |
| ClinicFlow QA | [spring-petclinic/spring-petclinic-rest](https://github.com/spring-petclinic/spring-petclinic-rest) | Apache-2.0 |
| BankFlow QA | [parasoft/parabank](https://github.com/parasoft/parabank) | Apache-2.0 |

各项目的 `UPSTREAM.md` 记录基线提交与改造范围，`UPSTREAM_README.md` 保留原项目说明。许可证与版权信息以各目录中的原始文件为准。

部分代码与文档使用 AI 辅助编写。

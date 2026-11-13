# 候选项目排序

- JD 来源：`C:\Users\ZhuanZ\Documents\Codex\2026-11-13\d\work\jd.txt`
- 主项目推荐：`ClinicFlow QA · 诊所业务接口测试`，score=93.27
- 备选项目：`BankFlow QA · 银行交易接口与资金一致性测试`，score=88.46
- 分数说明：先计算 raw_score，再按 max_raw_score 归一化到 0-100。

| Rank | Name | Score | Raw | Max Raw | License | Stars | Last Commit | Runnable | Resources | Matched | Risks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ClinicFlow QA · 诊所业务接口测试 | 93.27 | 97 | 104 | Apache-2.0 | 639 | 2026-11-09 | True | 本机 CPU，无 Docker/独立数据库要求 | Python, Java, 接口测试, 回归测试, 测试数据, 缺陷复现 | 只验证本地 H2 默认配置，未验证 MySQL/PostgreSQL 或启用认证后的矩阵 |
| 2 | BankFlow QA · 银行交易接口与资金一致性测试 | 88.46 | 92 | 104 | Apache-2.0 | 63 | 2026-11-11 | True | 本机 CPU，无 Docker/独立数据库要求 | Python, Java, 接口测试, 回归测试, 测试数据, 缺陷复现 | 金融演示系统，不代表真实金融生产经验; 不使用上游可选的商业测试工具或相关许可配置 |
| 3 | SwagCart QA · 电商页面自动化测试 | 85.58 | 89 | 104 | MIT | 46 | 2026-11-05 | True | 本机 CPU，无 Docker/独立数据库要求 | Python, Selenium, Pytest, 功能测试, 回归测试, 测试环境 | 前端模拟业务，不覆盖真实支付和服务端鉴权; UI 自动化依赖 Chrome 与驱动版本匹配 |

## 使用说明

- 这个脚本只根据显式字段打分；语义判断、JD 命中度和最终选择仍需 AI 助手/人工审阅。
- 不可运行、资源要求过高、风险说明过多的项目，除非非常贴 JD，否则不建议作为主项目。
- 推荐项目应尽快进入最小路径摸底、简历 4-5 行版本和面试 Q&A，而不是卡在完美复现。

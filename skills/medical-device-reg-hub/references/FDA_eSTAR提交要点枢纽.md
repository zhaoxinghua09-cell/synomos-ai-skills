# FDA eSTAR 提交要点枢纽

> 徽章：阶段④申报 ｜ 市场：美国 ｜ 类别：510(k)/De Novo ｜ 核验：官方源核实（2026-08-28）
> 类型：实操枢纽 ｜ 状态：就绪 ｜ 格式：MD ｜ 保密：公开（FDA 公开信息）

> 美国 FDA 上市前提交已全面电子化：**510(k) 自 2023-10-01 起强制 eSTAR；De Novo 自 2025-10-01 起强制 eSTAR**。eSTAR（electronic Submission Template And Resource）是 FDA 官方提供的交互式 PDF 模板，目前核心可用的电子提交模板。

---

## 一、强制时间线与提交渠道

| 事项 | 时间/要点 |
|---|---|
| 510(k) 强制 eSTAR | **2023-10-01 起**（Traditional/Special/Abbreviated + 补充和修订，豁免除外） |
| De Novo 强制 eSTAR | **2025-10-01 起**（原始申请 + 补充和修订，豁免除外） |
| 小企业申请（SBR） | 2024-11-01 起强制走 CDRH Portal |
| 提交渠道 | **CDRH Customer Collaboration Portal**（在线上传 + 进度追踪，Okta 注册） |
| 文件限制 | 提交总量 ≤4GB；PDF 附件 ≤1GB；超大视频/图片仅必要才放 |
| 豁免情形 | 交互式审评响应、部分修订（上诉/监督审查请求、实质性摘要请求、变更通讯人、最终决定后修订）、撤回请求 |

> 来源：FDA 官网《Tracking Your Premarket Submissions: CDRH Portal》《eSTAR 510(k)/De Novo 最终指南》

## 二、eSTAR 是什么（工作方式）

- **交互式 PDF 模板**：内置问题、逻辑跳转、提示和指引，引导逐节填写；填写时自动链接 FDA 数据库（产品代码、共识标准、法规）
- **自带完整性检查**：第一页显示 Complete / Incomplete 状态——**Incomplete 的 eSTAR 不被受理审评**（取代传统 RTA 清单）
- 红色条 = 必答未答；绿色条 = 该节完成；灰色 = 可选
- 附件**嵌入 PDF 内**（不再是一堆散文件）；eSTAR 本身不受 eCopy 指南约束，但随附的其他文件须符合 eCopy 要求；FDA 建议尽量不加外部文件

## 三、提交后流程与时限（510(k)）

| 阶段 | 时限 | 要点 |
|---|---|---|
| 技术筛查（eSTAR 自动检查） | 收件后 15 天内 | 未过 → 通知补充，**180 天内补交替换 eSTAR**，逾期视为撤回 |
| 验收审查（Acceptance Review） | Day 15 | 通过 → 实质性审查；不通过 → **RTA Hold，180 天内整改**，逾期 510(k) 删除需重新提交 |
| 实质性互动（Substantive Interaction） | Day 60 内 | 两种方式：①Interactive Review（非正式、不停表）②AI 请求（正式、停表） |
| **AI（Additional Information）发补** | **收到请求后 180 天** | **无延期**；提交完整响应（有效 eSTAR/eCopy）；逾期 → 视为撤回、从系统删除，需重新提交全新 510(k) |
| MDUFA 决策 | 90 FDA 天目标 | FDA 天 = 收件至决策日，扣除 AI 搁置天数；SE/NSE 判定 |
| 超时沟通 | Day 100 | 未决出 → Missed MDUFA Communication（书面反馈 + 会议/电话） |

## 四、AI 发补响应模板（直接套用）

响应提交须包含（FDA 官方要求）：
1. **提交人名称**
2. **510(k) 编号**
3. 标识：Additional Information (AI) to 510(k)
4. **FDA 发补请求日期**
5. 按问题条目有序整理的全部所需信息（建议逐条对应 FDA AI 信函编号）

> 格式：有效 eSTAR 或 eCopy 提交至 DCC/Portal。**注意**：第 179 天才提交、若没过 eCopy 校验，会超 180 天导致撤回——预留缓冲，别卡点。

## 五、填写要点与避坑（eSTAR 实操）

1. **先备料再填模板**：建议完整技术文档先成型，再进 eSTAR 逐节填写，避免反复返工
2. **Predicate 质量决定成败**：实质等同论证（SE 讨论）是审查核心——差异对比表、技术特征、预期用途逐项对应；predicate 选错直接 NSE
3. **共识标准引用**：eSTAR 内置标准数据库，声明符合的标准要真的完整（含版本、偏差说明）
4. **RTA 三件套常漏**：IFU、标签、510(k) Summary/Statement 不齐会被拒收
5. **IVD 专用模板**：FDA 提供 IVD 专用 eSTAR 表单，别用普通 510(k) 模板填 IVD
6. **FDA 天计算**：AI 搁置不计入 90 天目标；Interactive Review 不停表——能走 Interactive 就别等 AI
7. **拿到 SE 后**：完成企业注册 + 产品列名（Establishment Registration & Device Listing）才算上市合规闭环

## 六、官方入口

| 用途 | 入口 |
|---|---|
| eSTAR 下载与说明 | fda.gov → eSTAR（Voluntary eSTAR Program 页面） |
| 510(k) 提交流程 | fda.gov/medical-devices/premarket-notification-510k/510k-submission-process |
| CDRH Portal 注册提交 | fda.gov CDRH Customer Collaboration Portal |
| 510(k) 数据库（查 SE 决定） | accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm |
| eSTAR 510(k)/De Novo 指南 | FDA Guidance：Electronic Submission Template for Medical Device 510(k) Submissions / De Novo Requests |

## 七、诚实边界与时效
- 强制时间线/时限以 FDA 官方页面与最终指南为准（数据截至 2026-08-28）
- 豁免与弃权情形按指南 Section VI.A 逐条核对；FDA 已表明原则上不批电子提交豁免
- 本文为专业参考，不构成法规意见

*FDA eSTAR 提交要点枢纽 · 核验 2026-08-28 · 版权 © 2026 注册老炮*

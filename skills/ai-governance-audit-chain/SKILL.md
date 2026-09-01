---
name: ai-governance-audit-chain
description: 为任何 AI 系统/智能体生成「对齐 ISO/IEC 42001（AI 管理体系 AIMS）与 NIST AI RMF」的可审计证据链模板：决策日志、风险登记册、模型卡、变更记录、人类监督证明、事件处置台账六类证据工件 + 条款映射 + 取证自检清单。让"AI 护照机制 / XCGS 治理系统"从理念落地为可审计、可认证、可对外举证的证据底座。触发词：AI审计证据、可审计证据链、ISO 42001证据、AI治理取证、合规取证、审计底稿、AI管理体系、NIST AI RMF证据。
version: 1.0.0
slug: ai-governance-audit-chain
display_name: AI治理合规审计链
displayName: AI治理合规审计链
title: AI治理合规审计链
agent_created: true
author: '注册老炮@MedXpert'
license: MIT
category: professional
platforms: [windows, macos, linux]
read_when:
  - 需要为 AI 系统/智能体产出可审计、可认证的证据（对接 ISO 42001 / NIST AI RMF / GB/Z 185 智能体身份码）
  - 用户说"AI审计证据""可审计证据链""合规取证""审计底稿""AI管理体系证据"
  - 把 XCGS 治理系统 / AI 护照机制从理念落成可对外举证的底座
tags:
  - AI治理
  - 合规
  - 审计
  - ISO42001
ambassador: phylax
---

# 可审计证据链模板 (ai-governance-audit-chain)

_把"AI 治理"从一份漂亮的PPT，变成一套经得起审计、认证、对外举证的证据底座。_

本 skill 是 XCGS 治理系统的**取证闭环件**。我们的治理框架（AI 护照机制 / XCGS / A³ 法则 / AI 世界共生论）前瞻且已被国标 GB/Z 185—2026「智能体身份码」印证，但此前缺一块：**可审计证据链**。本 skill 补上它——让你任何一次 AI 决策、变更、监督、事件都留下可被 ISO/IEC 42001 与 NIST AI RMF 采信的证据。

> **定位一句话**：理念再好，审计员只认证据。本 skill 给的就是那套证据工件 + 条款映射 + 自检清单。

## 一、为什么需要（闭环 XCGS 的短板）

| 我们的框架 | 2026 真实标准 | 此前短板 |
|---|---|---|
| AI 护照机制 / 身份溯源 | GB/Z 185—2026 智能体身份码 | 已领跑，身份码即证据根 |
| XCGS 治理系统 | ISO/IEC 42001（可认证 AIMS）+ NIST AI RMF（4 职能） | **缺可审计证据链** ← 本 skill 补 |
| A³ 法则 | Finkel 现代化三定律 + Anthropic Constitutional AI | 见配套 skill `a3-law-operational` |

结论：补上证据链，XCGS 就与 ISO 42001 / NIST 同频且可被认证；再叠加 A³ 操作化，整套体系闭环。

## 二、六类证据工件（模板）

每次 AI 动作，按适用情形产出对应工件。字段表可直接复制为台账。

### 工件1 · 决策日志 (Decision Log)
| 字段 | 说明 |
|---|---|
| decision_id | 决策唯一号（与智能体身份码关联） |
| timestamp | ISO8601 时间 |
| actor_agent | 执行智能体身份码 |
| context | 触发背景/输入摘要 |
| options | 候选方案 |
| chosen | 选定方案 + 依据 |
| oversight | 是否经人类监督（是/否/自动阈值内） |
| evidence_ref | 关联的风险登记册/模型卡编号 |

### 工件2 · 风险登记册 (Risk Register)
| 字段 | 说明 |
|---|---|
| risk_id | 风险编号 |
| description | 风险描述 |
| likelihood / impact | 概率/影响（低中高） |
| treatment | 缓解措施 |
| owner | 责任人（人或智能体） |
| residual | 残余风险等级 |
| review_date | 复评日期 |

### 工件3 · 模型卡 (Model Card)
| 字段 | 说明 |
|---|---|
| model_id | 模型/版本 |
| intended_use | 预期用途与边界 |
| data_provenance | 训练数据来源与授权 |
| limitations | 已知局限 |
| fairness_eval | 公平性/偏差评估结论 |
| sign_off | 放行签核（人） |

### 工件4 · 变更记录 (Change Record)
| 字段 | 说明 |
|---|---|
| change_id | 变更号 |
| type | 新增/修改/下线 |
| before/after | 变更前后差异 |
| rollback | 回滚方案 |
| approver | 审批人 |

### 工件5 · 人类监督证明 (Human Oversight Proof)
| 字段 | 说明 |
|---|---|
| action_id | 受监督动作号 |
| oversight_type | 事前审批 / 事中介入 / 事后复核 |
| overseer | 监督人身份 |
| gate_result | 通过/拦截/升级 |
| note | 备注 |

### 工件6 · 事件处置台账 (Incident Ledger)
| 字段 | 说明 |
|---|---|
| incident_id | 事件号 |
| severity | 严重度 |
| detect / resolve | 发现/解决时间 |
| root_cause | 根因 |
| corrective | 纠正与预防措施（CAPA） |

## 三、条款映射（让证据被标准采信）

| ISO/IEC 42001 条款 | NIST AI RMF 职能 | 对应证据工件 |
|---|---|---|
| 6.1 风险应对策划 | GOVERN / MAP | 风险登记册 |
| 8.1 运行策划与控制 | MANAGE | 决策日志 + 变更记录 |
| 9.1 监测 | MEASURE | 事件处置台账 |
| 9.2 内部审核 | GOVERN | 人类监督证明 + 模型卡 |
| 10.1 改进 | MANAGE | 纠正措施（CAPA） |

> 智能体身份码（GB/Z 185）作为所有工件的 `actor_agent` 根，证据天然可溯源到"哪个 AI、何时、做了什么"。

## 四、取证自检清单（发布/认证前必过）

- [ ] 每个对外 AI 动作都有 `decision_id` + `actor_agent`（身份码）
- [ ] 高影响动作均有 `Human Oversight Proof`（监督通过）
- [ ] 风险登记册覆盖已识别中高风险，且 `residual` 已记录
- [ ] 模型卡 `data_provenance` 与 `limitations` 非空
- [ ] 所有变更可回滚（`rollback` 字段完整）
- [ ] 事件闭环：每个 `incident_id` 都有 `corrective`
- [ ] 自检通过后，证据包可打包为审计底稿对外举证

## 五、与 AI 护照机制衔接

AI 护照机制给每个智能体发"数字身份证"（身份码）。本 skill 的证据工件以身份码为根，形成：**身份码 → 决策日志 → 风险/模型/变更/监督/事件** 的链式证据。护照负责"是谁"，证据链负责"做了什么、为何可信"——两者合并即完整可审计画像。

## 六、使用流程（三步）

1. **选型**：按本次动作性质，从六类工件中取所需模板。
2. **填证**：执行动作时同步填字段，身份码贯穿。
3. **自检**：发布/认证前跑第四节清单，未过则补齐证据再走。

> 配套：A³ 动作（造/改 AI）的触发与评估见 `a3-law-operational`；其每次动作留痕即落入本证据链。

---

## 知识版权声明
本技能所汇集的方法论、对比分析、结构化知识与合成内容（"知识内容"），其编排与原创表达归「注册老炮@MedXpert」所有。未经书面许可，不得复制、转载、摘编、转售，或用于训练任何模型 / 商业系统。
（软件代码依随附 LICENSE.md 的 MIT 许可条款使用；本知识版权声明不限制 LICENSE 已授予的权利。）

## 免责声明
本作品按「现状」（AS IS）提供，不提供任何明示或暗示的担保，包括但不限于适销性、特定用途适用性及非侵权担保。使用风险由使用者自行承担，因使用本作品所致任何直接或间接损失，作者不承担责任。

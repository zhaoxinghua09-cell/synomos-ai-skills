---
name: research-methodology
description: 老拍档调研执行方法论（Plan→Do→Check→Act 全流程）。当需要做正式调研、深度研究、方案论证、情报收集、行业/竞品/标准调研、多源查证并产出调研报告时使用。补齐调研最缺的 Plan（Research Brief）与 Do（检索设计/交叉验证），Check 环节复用 research-quality-gate v1.7。供 WorkBuddy 主脑与 WorkSwarm 分身队共享。触发词：调研、研究、深度调研、情报收集、查证、多源验证、Research Brief、调研方法论。
version: 1.0.0
agent_created: true
author: '注册老炮@MedXpert'
license: MIT
category: knowledge-management
tags:
  - 研究
  - 方法论
  - 学术
  - 框架
slug: research-methodology
display_name: 研究方法论
title: 研究方法论
displayName: 研究方法论
description_en: "LaoPaidang research execution methodology (Plan→Do→Check→Act): Research Brief, ≥3-way parallel retrieval, cross-validation, quality gate, five-part briefing. For deep research / intelligence / multi-source verification."
platforms: [windows, macos, linux]
xiaping_category: 学术研究
ambassador: didaskalos
---

# research-methodology（调研方法论）v1.0

> 质量门禁：调用 skill `research-quality-gate`（v1.7，Check 环节）

## 核心流程（五步）

1. **Plan · Research Brief（立项，先呈批）**
   七要素：核心问题（一句话）｜子问题拆分（3-8 个，可独立检索）｜假设+反方假设｜范围边界（时间/语言/地域/来源类型/范围外不查）｜成功标准（引用可解析 100%）｜资源分配（并行路数/预算/时限）｜输出契约（默认五段式）
   **未呈批不检索。**

2. **Do · 检索设计（Query Rewriting 决定 80% 质量）**
   ①关键词扩展：抽象→具体实体；②时间界限：强制加窗；③对比维度显式化；④至少 1 个反驳子查询。来源分级 A 一手/ B 二手/ C 弱源（不作关键依据）。≥3 路独立并行（WorkSwarm 分身队），溯源包 `{url, source_type, snippet, 抓取日期, doi}`，PRISMA 式去重/初筛/全文/纳入+排除记原因，检索日志留 query+日期。

3. **Do · 交叉验证（铁律）**
   ①三角验证（≥2 独立源）；②反向关键词再搜一轮；③备选假设对抗；④GRADE 证据分级+降级理由；⑤ICD 203 七档概率词统一（禁混用）。

4. **Check · 质量门禁 → 调 `research-quality-gate` v1.7**
   范围边界核对 → 6 格证据卡 → 5 维 LLM-as-Judge（FActScore 原子拆解+跨模型裁判）→ 客观 grounding 率 → N=5 稳定性 + 跨 judge κ≥0.4 → 高风险人工门禁（合规/财务/发布/身份保留人类终核）。

5. **Act · 交付与固化**
   五段式简报：执行摘要 / 关键发现 / 支撑证据 / 风险因素 / 建议行动。每条关键结论附「结论+证据等级+概率词+溯源」。固化三去处：结论→记忆，流程→skill，决策→DECISIONS.md。AAR 四问复盘。

## 调研四档（分级响应）

| 档位 | 适用 | 流程 |
|---|---|---|
| 快档 | 日常问答 | 单源快速答，不归档 |
| 标档 | 一般查询 | ≥2 源交叉 |
| 深档 | 方案/报告/交付 | 本方法论全流程 |
| 重档 | 理论/进化/规划 | 全流程+多角度+第一性原理 |

## 铁律与边界

- **先查国际标准/理论，交叉验证后再输出；查不到明说"没查到"**
- 引用可解析率 100% 是目标非保证（FACTS 顶级模型 <70%）；自动化评分须人工校准
- 范围外未做不计缺陷（防范围错位误判）
- 本 skill=执行流程，门禁=质检，缺一不可

## 版权与许可

© 2026 SynomosAI（版权持有）。署名 诺学@SynomosAI 原创。按 MIT 协议开源（详见 LICENSE.md）。
**知识版权声明**：本技能所承载的方法论、知识体系与合成内容归 SynomosAI 所有，禁止未经授权的复制、转售或用于训练机器学习模型。

**免责声明**：本技能按「现状」（AS IS）提供，不作任何明示或暗示担保，使用后果由使用者自负。不构成法律、医疗、财务或监管建议；涉及合规事项请另行咨询专业机构。

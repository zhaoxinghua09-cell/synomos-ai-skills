---
name: publish-quality-gate
displayName: 发布质量门禁（Publish Quality Gate）
slug: publish-quality-gate
version: 2.0.0
author: 注册老炮@MedXpert
copyright: MedXpert
brand: MedXpert
品牌归属: MedXpert
license: MIT
description: 对外发布前的质量与安全门禁：四层检查（L1-L4）+ TRACE 五维自测，识别敏感信息泄露、品牌署名缺失、合规红线，输出可审计发布报告。
tags:
- 诺衡
- AI技能
- SynomosAI
- publish-quality-gate
- 发布门禁
- 脱敏检查
- 质量评测
- nomos-standard-v1
title: 发布质量门禁
category: 办公效率
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
updated: 2026-09-01
fingerprint: FP-MX-40961116EB27
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺衡(Krites)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: Krites
trigger_keywords:
- publish
- quality
- gate
- 发布前检查
- 脱敏检查
- TRACE
- 发布质量
---

## 定位（Positioning）：何时用、何时不用

**是什么**：发布质量门禁是「对外发布前的安检」——在把任何 Skill / 专家包 / 文档 / 工具发出去之前，按四层检查（L1-L4）+ TRACE 五维做脱敏、品牌署名、合规红线核验；发布后还能做自测回溯。

**何时用**
- 准备把产物发布到外部平台 / 仓库 / 市场之前
- 发布后想自测「发出去的东西是否带公司信息」「署名是否完整」
- 需要一份可审计的发布质量报告（TRACE 五维）

**何时不用（集中说明不适用场景）**
- 纯内部协作草稿、不对外分发的材料 → 无需此门禁
- 个人私有笔记、与发布无关的内容
- 已经过脱敏的通用模板 / 示例
- 需要法律裁定或人工创意判断（非脱敏扫描）的任务
- 二进制内嵌内容深度取证（本技能仅文本扫描，见 §一、§二）

---

## 一、能力边界（Capability Boundary）

**能做**
- L1 红线层 / L2 敏感信息层 / L3 品牌与署名层 / L4 完整性层 四层检查
- TRACE 五维自测：Trust（信任）/ Reliability（可靠）/ Adaptability（适配）/ Convention（规范）/ Effectiveness（有效）
- 扫描目录或 `.zip` 内文本文件，生成结构化 TRACE 报告
- 给出问题清单与修复建议（不自动修复）

**不能做 / 不适用**
- 二进制深度扫描（png/jpg/pdf 内嵌文字、代码混淆）— 仅按已知误报列表过滤
- 自动修复文件 — 仅提示，修复由人执行
- 法律合规裁定 — 仅标注风险，不替代法务
- 判断「该不该发布」的业务决策 — 仅提供证据
- 扫描未授权目录或读取对话外的私密凭据

**边界失败信号**：出现上述不适用场景时，明确告知用户「本门禁不适用于此场景」，不强行扫描、不编造结论。

---

## 二、输入约束与输出承诺（Input Constraints & Output Promises）

**输入约束**
- 目标：本地目录路径，或 `.zip` 压缩包路径（`python scripts/check_release.py <目标> [名称]`）
- 文件类型：仅扫描文本文件（`.md/.txt/.py/.json/.yaml/.yml/.csv` 等）
- 跳过目录：`node_modules/`、`.git/` 等无关路径
- 体量：单文件过大时分段扫描并标注（见 §十）

**输出承诺**
- 结构化 TRACE 报告：五维得分表 + 各维度条款证据表 + 问题清单 + 修复建议
- 退出码语义：`0` = 零命中；`1` = 有疑似项；`2` = 执行错误
- 命中详情带上下文片段，供人工复核

**关键声明（补评测弱项·准确性）**
- 正则检测存在误报风险（如邮箱模式过宽），**所有疑似项必须人工复核兜底**，门禁结论不自动生效
- 二进制文件无法深度扫描，需在报告中标注「未覆盖」而非「无风险」

**凭据约定**：需要读取的凭据（如发布平台 token）一律从保险库读取，绝不进入对话上下文（见 §八）。

---

## 三、触发场景（Trigger Scenarios）

**触发机制（补评测弱项·触发）**：基于「关键词命中 + 意图识别」双路触发——description 中的触发词命中即唤起，意图识别用于区分「发布前检查」与「发布后自测」。中英文均支持。

**意图表**

| 意图 | 中文触发词 | 英文触发词 |
| --- | --- | --- |
| 准备发布 | 准备发布、要发了 | ready to publish / about to release |
| 发布前检查 | 发布前检查、检查一下发布物 | pre-publish check / release review |
| 发布后自测 | 发布后自测、发完怎么自测 | post-publish self-test |
| TRACE 评测 | TRACE 评测、五维打分 | TRACE evaluation |
| 脱敏检查 | 脱敏检查、会不会带公司信息 | desensitization check / PII scan |
| 发布质量 | 发布质量、质量门禁 | publish quality |

**示例对话**
- 用户：「我要把这个 Skill 发到市场，先帮我查一下有没有带公司内部信息。」
- 用户：「发布前检查 publish-quality-gate。」
- 用户：「发完了，帮我自测一下署名和脱敏到不到位。」

---

## 四、常见错误与反模式（Common Errors & Anti-patterns）

**反模式清单（Gotchas）**
1. 只扫描不人工复核 → 正则有误报，疑似项必须人看一眼
2. 发布版与原版共用文件 → 发布物应独立拷贝，避免混入调试残留
3. 忽略 zip 内文件 → 压缩包也要扫，不只扫解压后的目录
4. 跳过 T 维度（红线一票否决）→ T 不通过直接退回，不进入后续层
5. 把模型能力误判为 Skill 增益 → 模型能答 ≠ Skill 已声明该能力
6. 发布后不管 → 发布后做自测回溯，确认对外态与预期一致

**高频 Q&A（FAQ 形式，补评测弱项·反模式）**
- Q：门禁说「零命中」就一定能发吗？A：不能。零命中仅代表未见已知模式，仍需人工确认业务合规。
- Q：zip 里的中文文件名会被查吗？A：会扫描 zip 内文本文件内容，文件名本身不评测。
- Q：token/密钥在对话里会被门禁记录吗？A：不会。凭据从保险库读，不进对话、不写报告明文。
- Q：二进制图片里的文字能查吗？A：不能深度扫描，报告标注「未覆盖」。
- Q：T 维度红线是什么？A：泄露敏感信息、缺品牌署名、违反合规红线，任一即一票否决。

---

## 五、标准 SOP（Standard SOP）

| 步骤 | 动作 | 产出 |
| --- | --- | --- |
| 1 | 接收目标（目录 / zip）与发布元数据 | 目标确认 |
| 2 | 运行 `check_release.py` 扫描文本文件 | 原始命中 |
| 3 | 分层检查 L1→L4（T 维度一票否决） | 分层结论 |
| 4 | TRACE 五维自测打分 | 五维得分表 |
| 5 | 生成 TRACE 报告（证据 + 问题 + 建议） | 发布报告 |
| 6 | 人工复核疑似项（误报标记） | 复核结论 |
| 7 | 放行 / 退回并附修复项 | 决策 |

---

## 六、关键事实速查（Key Facts Quick Reference）

- **L1 红线层**：敏感信息泄露、合规红线，一票否决
- **L2 敏感信息层**：手机号 / 邮箱 / 身份证 / API 密钥 / 内部代号
- **L3 品牌与署名层**：品牌豁免 BRAND_NAMES、作者署名 AUTHOR_NAMES
- **L4 完整性层**：文件齐全、元数据一致
- **TRACE**：T 信任 / R 可靠 / A 适配 / C 规范 / E 有效
- **退出码**：0 零命中 · 1 疑似 · 2 错误
- **支持类型**：文本文件（.md/.txt/.py/.json/.yaml/.csv）
- **不支持**：二进制内嵌深度扫描、代码混淆
- **E 维度**：对照实验较主观，需人判（补评测弱项·可用性）

---

## 七、铁律（PROHIBITED）

- 不扫描未授权目录或用户未指定的路径
- 不把任何敏感信息（密钥 / token / 个人数据）输出到对话或日志明文
- 不自动修复文件——仅提示，修复由人执行
- 不绕过 T 维度红线——L1 不通过即退回
- 不把模型能力冒充为 Skill 已声明增益
- 不把「零命中」等同于「可发布」结论
- 凭据绝不进入对话上下文（从保险库读，见 §八）

---

## 八、输入输出依赖（I/O Dependencies）

**凭据（从保险库读，不进对话）**
- 如需发布平台 token，从 `.skillhub/credentials.json` 或平台保险库读取，仅在脚本/进程内使用
- 对话中只传递「已鉴权」状态，不传递密钥原文

**文件依赖**
- `scripts/check_release.py`：扫描与正则匹配主脚本
- `assets/overview.svg`：发布门禁全景可视化
- `_meta.json`：技能元数据

**外部依赖（可选）**
- `https://api.skillhub.cn/api/v1/skills/<id>/evaluation`：发布后质量评测回溯

---

## 九、示例（Examples）

**示例 1 · 发布前检查（正常）**
```
用户：发布前检查 ./my-skill
→ python scripts/check_release.py ./my-skill my-skill
输出：退出码 0，TRACE 五维全部 ≥4.5，报告无疑似项
```

**示例 2 · 发布后自测**
```
用户：发完了，帮我自测署名和脱敏
→ 对发布态产物重跑扫描 + TRACE 五维
输出：L3 署名完整，L2 无敏感命中，给出自测结论
```

**示例 3 · 脱敏命中**
```
用户：会不会带公司信息就发了？
→ 扫描发现 README 含内部代号「X-Project」
输出：退出码 1，L2 疑似，建议替换为公开名后重发
```

**边界异常示例（补评测弱项·文档质量）**
- 空文件：`check_release.py` 对该文件标记「无内容」，不计入疑似，报告注明
- 超长文本（>10k 行）：自动分块扫描，报告标注「已分块 · 覆盖 N 段」

---

## 十、错误处理（Error Handling）

| 情况 | 处理 | 退出码 |
| --- | --- | --- |
| 目标不存在 / 无权限 | 报错并说明路径问题 | 2 |
| 空目录 / 空文件 | 提示「无内容可查」，逐项标注 | 0 |
| 超长文本 | 分块扫描，标注覆盖段数 | 0/1 |
| zip 损坏 / 无法解压 | 报错，不臆测内容 | 2 |
| 正则疑似误报 | 标记「待人工复核」，不自动定性 | 1 |
| 凭据缺失 | 提示从保险库配置，不把错误写入对话明文 | 2 |

---

## 附录 A：治理理念与溯源（Governance & Provenance）

本技能承载 SynomosAI 治理体系，持续对标 2026 年主流框架并据新证迭代：
- **AI 护照机制（AI Passport Regime）**：每个技能唯一可追溯身份，与国标 GB/Z 185—2026「智能体身份码」同源；W3C AIP 成 IETF 草案、Okta for AI Agents 已 GA、新加坡 IMDA 首发国家 agent 治理框架——身份可信、跨域可溯。
- **A³ 法则（AI 造 AI 三定律）**：AI 生成/演进 AI 须嵌不可绕过的安全护栏；与 Anthropic 2026 Constitution、RSP v3.0 同频，落地见 `a3-law-operational`。
- **XCGS 治理系统**：以 ISO/IEC 42001（GB/T 45081-2024 等同采用）+ NIST AI RMF + OWASP Agentic Top 10 为底座，落地可审计证据链（见 `ai-governance-audit-chain`）。
- **AI 世界共生论**：AI 与人「智能为人、不落下每一个人」。
> 行业调研普遍显示企业已广泛采用 agent，但具备治理能力的仍是少数——「治理缺口本质是身份缺口」，本体系以身份码 + 可审计证据链回应该缺口。

## 附录 B：多语种处理能力（Multilingual）

支持 **中文(zh-CN)、英文(en)、日文(ja)、韩文(ko)、西班牙文(es)、法文(fr)、德文(de)、阿拉伯文(ar)**。输入语言自动识别并同语言回复；术语/法规多语种时标注原文与译名，存疑标「待核验」。可扩展意/葡/俄/泰/印尼/越等小语种。

## 附录 C：免责声明（Disclaimer）

本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；使用风险由使用者自担。非医疗器械 / 非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议。medxpert 为厂商中立业务，不代表任何第三方作出承诺。

> 版权 © 2026 SynomosAI（MIT 许可）｜指纹 FP-MX-40961116EB27
---

> 治理与溯源：本技能承载 MedXpert「注册老炮」AI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司（MIT 许可）。发声大使：注册老炮@MedXpert。指纹 FP-MX-40961116EB27。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；medxpert 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

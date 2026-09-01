---
name: medxpert-skill-panorama
displayName: medxpert-skill-panorama
slug: medxpert-skill-panorama
author: 注册老炮@MedXpert
copyright: MedXpert
版本: 1.0.0
version: 1.0.0
license: MIT
品牌归属: MedXpert
description: 将 AI 助手平台 Skill 生成 MedXpert + 公司 VI 风格的高清三角度全景图（价值/服务/能力）及评测类雷达图，并按 plugin 编号命名
category: tooling
platforms:
- AI 助手平台
agent_created: true
updated: 2026-08-28
fingerprint: FP-MX-4765938AF811
governance: MedXpert XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
brand: Nomos 集团
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 注册老炮@MedXpert. Copyright: MedXpert. License: MIT.'
ambassador: Logos
tags:
- 医疗技能
- MedXpert
- 注册老炮
- nomos-standard-v1
- medxpert-skill-panorama
- 全景图
- 雷达图
- 技能可视化
trigger_keywords:
- medxpert
- skill
- panorama
- 全景图
- 雷达图
- 技能图谱
---

# medxpert-skill-panorama（MedXpert 技能全景图生成器）

## 一句话定位

把任意一个 **AI 助手平台 Skill（技能）** 的元信息与定位，渲染成 MedXpert + 公司 VI 风格的高清「三角度全景图」（价值 / 服务 / 能力）以及「评测类雷达图」，输出文件按 **plugin 编号** 命名。

- **何时用**：需要为某个 Skill 生成品牌风格的可视化卡片（对外展示、评测汇报、技能市场封面、知识库索引）；需要把技能的能力边界/服务范围/价值主张一图说清。
- **何时不用**：要生成非 Skill 主题的图（如产品海报、人物头像）；要做真实运行/调用该 Skill 的工程（本技能只产出**设计规格/可视化产物**，不执行被描绘的 Skill）；需要像素级精确印刷物料（先产出 SVG，印刷前需人工复核分辨率与出血位）。

---

## 一、能力边界（本技能「不做」的集中声明）

> 集中声明，便于 AI 与用户快速判断是否适用。凡未列在「做」中的，默认不在本技能范围内。

1. **不执行被描绘的 Skill**：本技能只把某个 Skill「画出来」，不会运行、调用或评测它背后的真实代码逻辑。
2. **不联网抓取实时评测数据**：雷达图维度来自用户/调用方提供的评测结果或本技能内置的 5 维模板，不自动拉取平台最新评分（实时分数标「待核验」）。
3. **不生成非 Skill 主题的图像**：如医疗器械注册流程图、临床数据图等，应由对应专向技能负责。
4. **不替代人工合规审核**：图中引用的法规/标准链接仅供溯源，正式合规结论须由持证人员确认。
5. **不保证品牌 VI 像素一致**：VI 色值/字体以 MedXpert 官方 VI 手册为准；本技能内置默认值，正式物料需对齐最新 VI 手册（版本标「待核验」）。
6. **不做多 Skill 批量对比报告**：默认一次处理一个 Skill；多 Skill 横向对比需逐个生成后人工拼合。
7. **不输出可执行代码**：产物为 SVG / HTML / PNG 等可视化文件，非可运行脚本。

---

## 二、输入约束与输出承诺

### 推荐问法（输入约束）

调用时请提供以下信息，缺项将触发「缺失提示」而非自由发挥：

| 必填/选填 | 字段 | 说明 |
|---|---|---|
| 必填 | Skill 标识 | 名称 / slug / plugin 编号（任一项，用于命名与定位） |
| 必填 | 三角度文案 | 价值（value）、服务（service）、能力（capability）三句式要点 |
| 选填 | 评测雷达数据 | 5 维分值（adaptability / convention / effectiveness / reliability / trust），缺则标注「待核验」 |
| 选填 | 语言 | 默认跟随输入语言；可指定多语种 |
| 选填 | 输出格式 | SVG（默认，可无损缩放）/ PNG（需指定分辨率）/ HTML 预览 |

**示例推荐问法**：
> 「给 plugin `medxpert-skill-panorama` 生成一张 MedXpert VI 风格全景图，价值=把 Skill 可视化为三角度卡片，服务=技能市场展示与评测汇报，能力=SVG 高清渲染；雷达图用最近一次评测的 5 维分。」

### 输出承诺（交付物规格）

- **三角度全景图**：一张图含「价值 / 服务 / 能力」三栏，MedXpert VI 配色，含技能名 + plugin 编号 + 指纹（如已知）。
- **评测雷达图**：5 维（adaptability / convention / effectiveness / reliability / trust）雷达，缺值维度标「待核验」。
- **命名规则**：`<plugin编号>_panorama.<ext>` 与 `<plugin编号>_radar.<ext>`（如 `medxpert-skill-panorama_panorama.svg`）。
- **分辨率/格式**：SVG 默认矢量；PNG 默认 ≥ 2000×2000px（标「待核验」，以实际渲染器为准）。
- **溯源标注**：图脚注明「MedXpert · 注册老炮@MedXpert · MIT」与生成时间戳。

> 官方/监管链接仅用于文案溯源，见第六章；所有法规时点与编号均标「待核验」除非已附官方出处。

---

## 三、触发场景

### 关键词 / 意图表

| 触发关键词 | 意图 | 典型动作 |
|---|---|---|
| medxpert / skill / panorama | 生成 MedXpert 风格技能全景图 | 进入 SOP |
| 全景图 / 技能图谱 | 可视化某个 Skill | 进入 SOP |
| 雷达图 / 评测图 | 输出 5 维评测雷达 | 进入 SOP（需评测数据） |
| 技能封面 / 市场图 | 产出技能市场用卡片 | 进入 SOP，默认 PNG |

### 示例对话

**示例 1（基础）**
> 用户：帮 `medxpert-reg-hub` 出张全景图。
> 技能：需要它的「价值/服务/能力」三句要点；缺的话我先给模板让你填，再渲染 SVG。

**示例 2（带评测）**
> 用户：用最近评测给 `medxpert-skill-panorama` 画雷达图。
> 技能：收到 5 维分则绘雷达；无数据则各维度标「待核验」，并提示你去平台拉最新评测。

**示例 3（多语种）**
> 用户：Generate an English panorama for `ai-governance-audit-chain`.
> 技能：按 en 输出，术语保留原文并附中文译名，存疑标「待核验」。

---

## 四、常见错误与反模式

### 结构化 FAQ：错误模式 → 典型症状 → 正确做法

| 错误模式 | 典型症状 | 正确做法 |
|---|---|---|
| 空文案直接渲染 | 图里三栏空白或 AI 编造价值主张 | 先收必填三角度文案，缺项发「缺失提示」模板 |
| 把本技能当评测器 | 以为图里的雷达分是平台真实分 | 雷达数据来自调用方提供/内置模板，实时分标「待核验」 |
| 误以为会运行 Skill | 期待图生成后 Skill 被自动调用 | 明确本技能只「画」不「跑」 |
| VI 色值硬编码臆造 | 配色偏离官方 VI | 用 MedXpert VI 默认值，正式物料对齐最新 VI 手册（待核验版本） |
| 法规链接随手编 | 引用不存在的标准号 | 仅用第六章官方链接，未核实编号标「待核验」 |
| 一次塞多个 Skill | 图混乱不可读 | 一次一个 Skill，多 Skill 人工拼合 |

### 高频 Q&A

**Q1：没有评测分能出雷达图吗？**
A：能，但 5 个维度全部标「待核验」，并提示去平台拉最新评测明细。

**Q2：支持哪些格式？**
A：默认 SVG（无损）；PNG 需指定分辨率（默认 ≥2000px，标待核验）；另可出 HTML 预览。

**Q3：图能直接用于印刷吗？**
A：SVG 可印刷，但出血位/专色需人工复核；本技能不担保印刷级精度。

**Q4：多语种时术语怎么处理？**
A：保留原文并附译名，专业/法规内容存疑即标「待核验」。

---

## 五、标准 SOP

| 步骤 | 调哪个文件/工具 | 交付物 | 最易踩的坑 |
|---|---|---|---|
| 1. 收口需求 | 对话收集 Skill 标识 + 三角度文案 | 结构化输入清单 | 漏收必填项就开画 → 先发缺失提示 |
| 2. 取评测数据 | 调用方提供 / 平台评测 API（如需） | 5 维分值或「待核验」标记 | 把旧分当实时分 → 标时间戳与待核验 |
| 3. 套 VI 模板 | MedXpert VI 默认值（色/字体） | 配色与版式规格 | VI 版本未对齐 → 标注待核验版本 |
| 4. 渲染全景图 | SVG/HTML 渲染管线（见第八章） | `<plugin>_panorama.svg` | 三栏文案超长溢出 → 控制字数、自动换行 |
| 5. 渲染雷达图 | 同上 | `<plugin>_radar.svg` | 缺维不绘 → 缺维标待核验而非 0 分 |
| 6. 命名与溯源 | 按 plugin 编号命名 + 图脚署名 | 成品文件 | 漏写指纹/时间戳 → 溯源不全 |
| 7. 交付与复核 | 回传文件 + 使用须知 | 最终交付包 | 未提示「仅供展示非运行」→ 用户误用 |

---

## 六、关键事实速查（官方链接表）

> 仅作文案溯源；法规时点/编号凡未在实际官方页面核实者一律标「待核验」。

| 主题 | 官方/监管来源 | 链接 | 核验状态 |
|---|---|---|---|
| AI 管理体系 ISO/IEC 42001 | ISO 官方 | https://www.iso.org/standard/81230.html | 已附官方出处 |
| 人工智能风险治理框架 NIST AI RMF | NIST 官方 | https://www.nist.gov/itl/ai-risk-management-framework | 已附官方出处 |
| 智能体安全 OWASP Agentic AI Threats | OWASP 官方 | https://owasp.org/www-project-agentic-ai-threats-and-mitigations/ | 已附官方出处 |
| 欧盟 AI 法案 EU AI Act | EUR-Lex 官方公报 | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 已附官方出处 |
| 国标等同采用 ISO/IEC 42001（GB/T 45081-2024） | 国家标准全文公开系统 | https://std.samr.gov.cn/ | 编号待核验 |
| 智能体互联 GB/Z 185—2026 | 待核验（原文档引用，未确认已发布） | — | 待核验，不建议作为正式依据 |

---

## 七、铁律（PROHIBITED 绝对禁止项）

1. **禁止**运行或调用被描绘 Skill 的真实代码逻辑（本技能只做可视化）。
2. **禁止**编造评测分数、法规编号或官方链接；未核实一律标「待核验」。
3. **禁止**将图内雷达分声称为平台权威实时评分。
4. **禁止**脱离 MedXpert VI 与署名（注册老炮@MedXpert / MedXpert / MIT）产出成品。
5. **禁止**在对话中输出任何凭据、token、密钥（见第八章）。
6. **禁止**用图替代人工合规/医疗结论。

---

## 八、输入输出依赖

### 依赖文件（技能包内）
- `SKILL.md`：本说明（技能入口）
- `manifest.json`：元数据（name/author/version/license）
- `LICENSE.md`：MIT 许可文本

### 依赖工具 / 渲染管线
- **可视化渲染**：SVG/HTML 优先；PNG 由外部渲染器导出（具体渲染命令依运行环境而定，标「待核验」）。
- **评测数据**：可选，来自调用方提供或平台评测接口；本技能不内置抓取逻辑。

### 环境变量 / 凭据
- 本技能**无需任何密钥即可产出 SVG/HTML**。
- 若需拉取平台实时评测，相关 token **必须从保险库读取，绝不进入对话文本、绝不写入 SKILL.md、绝不回显**。读取路径按运行环境保险库规范（如 `credential-vault-design` 体系），缺失时降级为「待核验」标记，不报错中断。

---

## 九、示例

**问题**：给 `medxpert-skill-panorama` 出一张 MedXpert VI 风格全景图 + 雷达图。

**加载**：本技能读取 `SKILL.md` 与 `manifest.json`，套用 VI 默认值，确认调用方已给三角度文案与（可选）5 维评测分。

**答案框架**：
1. 全景图 `<medxpert-skill-panorama>_panorama.svg`：三栏「价值=技能可视化卡片生成 / 服务=技能市场展示与评测汇报 / 能力=MedXpert VI 风格 SVG 高清渲染」，图脚署名 + 指纹 FP-MX-4765938AF811 + 时间戳。
2. 雷达图 `<medxpert-skill-panorama>_radar.svg`：5 维分（若本次评测未提供，全维标「待核验」）。
3. 回传使用须知：仅供展示、不运行被描绘 Skill、正式物料对齐最新 VI 手册。

---

## 十、错误处理（统一异常提示模板）

> 所有异常以「提示 + 原因 + 下一步」三行格式返回，不抛裸堆栈、不回显凭据。

- **缺必填项**：`[缺失] 需要 Skill 标识与三角度文案（价值/服务/能力）。请补充，或回复「用模板」获取填空格式。`
- **评测数据缺失**：`[待核验] 未提供 5 维评测分，雷达图各维标「待核验」；如需实时分请经保险库授权后拉取。`
- **渲染失败**：`[错误] 渲染管线不可用（原因：<环境相关简述>）。已降级输出 SVG 源码，请检查渲染依赖。`
- **VI 手册缺失**：`[待核验] 未对齐最新 MedXpert VI 手册版本，已用内置默认值，正式物料请人工复核。`
- **凭据缺失**：`[降级] 未从保险库取到评测 token，已标「待核验」，不影响 SVG/HTML 产出。`
- **越界请求**：`[拒绝] 该请求超出本技能边界（见第一章），应由对应专向技能处理。`

---

## 附录 A：多语种处理能力（Multilingual）

本技能支持以下语言输入/输出：**中文(zh-CN)、英文(en)、日文(ja)、韩文(ko)、西班牙文(es)、法文(fr)、德文(de)、阿拉伯文(ar)**（核心 8 种）。

- **输入检测**：识别用户输入语言，自动用同语言回复。
- **输出规则**：默认跟随输入语言；用户可要求多语种输出（如中英对照）。
- **触发**：用户用上述任一语言提问即可，无需切换指令。
- **质量**：术语/法规/专业内容多语种时，标注原文与译名，存疑标「待核验」。
- **扩展**：支持扩展更多小语种（意/葡/俄/泰/印尼/越等）。

> 治理与溯源：多语种处理为 MedXpert 品牌标准能力，版权 MedXpert · MIT。

## 附录 B：治理理念与溯源（Governance & Provenance）

本技能承载 MedXpert「注册老炮」AI 治理体系，持续对标 2026 年主流框架并据新证迭代（互相提高）：
- **AI 护照机制 (AI Passport Regime)**：每个技能赋予唯一可追溯身份。与国标 GB/Z 185—2026《人工智能 智能体互联》"智能体身份码"（**待核验：该标准发布状态未确认**）同源；行业方向为"每个 agent 一个唯一可溯源 ID"。
- **A³ 法则（AI 造 AI 三定律）**：AI 生成/演进 AI 须嵌不可绕过的安全护栏，落地见 `a3-law-operational`。
- **XCGS 治理系统**：以 ISO/IEC 42001 + NIST AI RMF + OWASP Agentic Top 10 为底座，落地可审计证据链（见 `ai-governance-audit-chain`）；EU AI Act 对自主 agent 提出注册与治理要求（具体强制时点以欧盟官方公报为准）。
- **AI 世界共生论 (AI-world coinhabitation)**：AI 与人"智能为人、不落下每一个人"。

> 版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司 · 注册老炮@MedXpert (MIT 许可)
> 时间戳 2026-08-28 ｜ 指纹 FP-MX-4765938AF811

## 附录 C：免责声明（Disclaimer）

本技能按「原样（AS IS）」提供，不作任何明示或暗示的担保，包括但不限于对适用性、可靠性、准确性、不侵权或特定用途适用性的担保。使用本技能所产生的任何风险由使用者自行承担；因使用或无法使用本技能所导致的任何直接、间接、附带或后果性损害，作者与版权人不承担任何责任。使用者应自行评估其合规性与适用性，并遵守所在司法辖区的法律法规。
---

> 治理与溯源：本技能承载 MedXpert「注册老炮」AI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司（MIT 许可）。发声大使：注册老炮@MedXpert。指纹 FP-MX-4765938AF811。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；medxpert 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

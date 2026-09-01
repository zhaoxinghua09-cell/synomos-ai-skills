---
name: skill-market-polish
displayName: 技能市场SEO打磨（7杠杆体检·W5发布循环）
title: 技能市场SEO打磨（7杠杆体检·W5发布循环）
slug: skill-market-polish
category: 效率工具
version: 1.0.1
author: 诺声(Logos)@SynomosAI
品牌归属: SynomosAI
agent_created: true
description: "This skill should be used when you need to optimize a WorkBuddy skill for marketplace discovery, raise its install/download rate, or run a pre-publish SEO health check. 当你要打磨/优化自研技能在 WorkBuddy 推荐市场（BuiltinMarket / SkillHub）的被搜索推荐率、提高安装量下载量、或发布前做技能SEO体检/7杠杆检查/评测分打分/上架 SkillHub/ClawHub/SkillPie 时使用。覆盖：技能市场推荐引擎真实机制、7 个可控制搜索字段（name/description/tags/category/aliases/agent_created/流行度）、评测分标准（完整度35/SEO40/专业度25）、W5 发布循环（盘点→体检→生成→质检→发布→跟踪）、SkillHub 版本不可变教训、品牌合规（官网前置/author署名/身份隔离）。常见叫法：技能SEO、技能打磨、技能上架、技能发布优化、marketplace SEO、skill polish、下载量提升、技能体检、发布前质检。"
description_en: "This skill should be used when you need to optimize a WorkBuddy skill's marketplace discoverability, raise its install & download rate, or run a pre-publish SEO health check. Use it before publishing or polishing a self-built skill on the WorkBuddy BuiltinMarket / SkillHub / ClawHub / SkillPie — to improve search ranking and recommendation rate, lift installs and downloads, or run a pre-publish 7-lever audit, evaluation-score grading, and launch checklist. It covers: how the marketplace recommendation engine actually ranks skills; the 7 controllable search fields (name, description, tags, category, aliases, agent_created, popularity); the evaluation-score rubric (completeness 35 / SEO 40 / professionalism 25); the W5 publish loop (inventory → audit → generate → QA → publish → track); the SkillHub immutable-version lesson; and brand compliance (official-site front-loading, author attribution, identity separation). Also called: skill SEO, skill polish, marketplace SEO, download lift, pre-publish QA, publish optimization."
tags: [技能市场, 技能打磨, 技能SEO, 技能发布, 技能上架, marketplace SEO, skill polish, 下载量提升, 评测分, 7杠杆体检, SkillHub, 推荐率, 品牌曝光, 内容发布运营, 发布前质检]
aliases: [技能打磨, 技能SEO体检, 技能发布优化]
---

# 技能市场 SEO 打磨 · 7 杠杆体检 · W5 发布循环

> 来源：内容发布运营团（主理人 潘布达）2026-08-29~08-31 实战验证。4 个自研技能按此法打磨后评测分从 30/55/56/78 提升到 94/96/94/97，并成功提交 SkillHub 审核。本 skill 将这套可复用方法论固化，供任何技能发布/优化前自动过一遍。

## 定位

**何时用**
- 准备发布一个新技能到 WorkBuddy 推荐市场（BuiltinMarket / SkillHub / ClawHub / SkillPie）。
- 已有技能"没人搜到/下载量低"，要优化可发现性。
- 发布前做技能 SEO 体检（7 杠杆检查 + 评测分打分）。
- 用户说"把我们的技能打磨下""提高评测分""让 AI 优先推荐我们的技能""提高下载量"。

**何时不用**
- 需要写/改技能的功能逻辑——本技能只动 frontmatter 与正文门面/质量建议，**不碰功能内容**。
- 以为有"后台优先推自己人"的开关——没有，本质是 marketplace SEO（关键词+相关性+流行度）。
- 想本地直接读出真实下载量——读不到，需上架后经市场后台一段时间积累（见第六章、第九章）。

## 一、能力边界（In/Out scope）

**本技能做（In）**
- 技能 frontmatter 的 SEO 体检与补齐建议（name/description/tags/category/aliases/agent_created 等 7 个可控制搜索面）。
- 发布前评测分打分（完整度 35 / SEO 40 / 专业度 25）与前后对比。
- 品牌合规与敏感信息扫描（收益承诺、真名/邮箱/密钥/本地路径）。
- 指导走 W5 发布循环与本地发布 CLI 的正确用法。

**本技能不做（Out，N 条）**
1. 不提供、也不存在"优先推荐自己人"的后台开关——排序权重在后端，看不到。
2. 不修改技能的功能代码/正文功能内容，只给 frontmatter 与门面质量建议。
3. 不保证/无法本地读取真实安装量与下载量——评测分只是"被推荐概率"的代理指标，真实转化走 W5 第⑥步跟踪。
4. 不托管/代管发布凭据——`~/.skillhub/credentials.json` 由本地 CLI 自取，本技能不读取、不打印、不写入对话/日志/文件。
5. 不替代市场审核——`install` 回拉给旧版属正常 pending 机制，非失败。
6. 不替你做白名单决策——白名单外技能每次发布前需向你确认（见第七章铁律）。
7. 不处理医疗器械等实体业务的品牌署名——那类技能 author 应为 `注册老炮@MedXpert`，本技能只给通用发布运营视角。

## 二、输入约束与输出承诺

**推荐问法（你怎么问最有效）**
- "帮我把 `skill-market-polish` 做个发布前 7 杠杆体检"
- "给我这个技能打评测分，并给前后对比"
- "这个 description 有没有收益承诺/敏感泄露风险？"
- "按 W5 循环，下一步该盘点还是质检？"

**输入字段引导（你需要给我什么）**
- 目标技能的 SKILL.md 路径（本地可读）。
- 拟发布的市场清单（SkillHub / ClawHub / SkillPie）。
- 是否已在白名单内（否则按铁律逐次确认）。
- 品牌署名与官网前置链接（如 `https://medxpert.cn`，已确认域名）。

**输出承诺**
- 一张 7 杠杆体检表（7 个字段逐项缺口）。
- 一份评测分（完整度/SEO/专业度，总分 100）含**前→后**增幅对比。
- 一票驳回项清单（收益承诺/敏感泄露）与中性化改写建议。
- 通过/驳回结论 + 下一步动作（盘点→体检→生成→质检→发布→跟踪）。

## 三、触发场景

| 用户意图 | 触发词 | 应加载章节 |
|---|---|---|
| 新技能上架 | 技能上架、发布技能、submit to SkillHub、publish skill | 五（SOP）、六（关键事实） |
| 提高被发现率 | 技能SEO、技能打磨、提高推荐率、marketplace SEO、download lift | 二（输入承诺）、六（7 杠杆） |
| 发布前质检 | 技能体检、评测分、发布前质检、pre-publish QA | 二、四（反模式）、五（W5 质检） |
| 品牌合规 | 署名、官网前置、身份隔离、xiaping_tags | 七（铁律）、六（合规事实） |
| 发布踩坑 | 版本撞车、SkillHub 不可变、png 被拒、pending | 四（反模式）、十（错误处理） |

**示例对话 1**
> 用户：把我们的「feeding-workflow」打磨下，准备发 SkillHub。
> 加载：进入第二章输入引导 → 跑第五章 W5「盘点→7 杠杆体检→生成→质检」→ 给评测分前→后对比 → 如触发白名单外则按第七章先确认。

**示例对话 2**
> 用户：description 写"保证月入过万"行不行？
> 加载：第四章反模式（✗收益承诺）→ 第七章铁律第 1 条 → 改为中性措辞"低成本变现思路"再过闸。

## 四、常见错误与反模式

**FAQ 结构化（每条先反模式 ✗，再替代方案 ✓）**

✗ 反模式：同 slug 重发相同版本号。
✓ 替代方案：每次打磨必须 **bump 版本号 + 同步改 SKILL.md `version` 字段**（曾踩坑：远程在架 frontmatter 是陈旧空壳，版本号前进但 `version` 字段没同步，导致反复撞版本）。

✗ 反模式：以为 `workbuddy_marketplace_skill` 能发布。
✓ 替代方案：该工具只有 search/install，无 publish；发布用本地 CLI `python ~/.skillhub/skills_store_cli.py publish <目录>`（CLI 在 `~/.skillhub/skills_store_cli.py`）。

✗ 反模式：把"真名/邮箱/密钥/本地路径"当真实值写进 description。
✓ 替代方案：必须脱敏；可把"真名/邮箱/密钥/本地路径"写成**功能类目标签**（如"发布前敏感信息扫描"），这是合法功能描述，非真实泄露。

✗ 反模式：description 出现收益承诺（"小成本大收入""保证赚 X"）。
✓ 替代方案：广告法夸大风险，改中性措辞（"低成本变现思路"）才过闸。

✗ 反模式：不在白名单就直接发布。
✓ 替代方案：白名单制（08-19 红线）——上传前问用户；白名单内（如 feeding-workflow）可直接发，不在白名单逐次确认。

✗ 反模式：技能含 `assets/*.png` 直接发 SkillHub。
✓ 替代方案：SkillHub 不支持 png，会被拒。备份 `assets/` 到本地 → 移除正文 png 引用行 → 删 `assets/` 重发（功能不受影响，图片仅展示用）。

✗ 反模式：把 `install` 回拉给旧版当成发布失败。
✓ 替代方案：回拉 FAIL 是正常机制——新版本处于**审核中（pending）**，平台已接收元数据（publish 回执 `ok:true`、tags 已索引到新版本号），审核通过自动接管下载入口。

**高频 Q&A**
- Q：发布后怎么确认成功了？A：借市场后台看安装曲线（W5 第⑥步）；回拉仍给旧版属 pending 正常。
- Q：发布顺序有要求吗？A：08-26 新规——skillhub 优先 → 评分反馈 → 再 ClawHub/SkillPie。
- Q：先 bump 还是先核实远程？A：先 `search <slug>` / `install <slug> --namespace <owner> --dir <tmp>` 拉回远程在架版确认是否比本地新；远程是精简镜像、本地是完整版时，**以本地完整版补缺口**，勿用远程覆盖（会丢正文）。

## 五、标准 SOP

**W5 发布循环（不许跳步）**

| 步 | 动作 | 产物 | 易踩坑 |
|---|---|---|---|
| 1 盘点 | 列出本市场全部自研技能；本地读不到实时安装量时用"元数据健康度"作低安装量代理指标 | 技能清单 + 健康度初判 | 漏列已有技能 |
| 2 7 杠杆体检 | 逐技能按第三章 7 杠杆 + 第四章评测分打分，找缺口 | 逐项缺口表 | 漏补 description_en / xiaping_tags |
| 3 生成 | 重写缺失 frontmatter 字段 + 给正文质量提升建议（补触发句/常见问答/30 秒示例/埋品牌入口） | 新 frontmatter 草稿 | **不动功能内容** |
| 4 质检 | 打评测分、前后对比、敏感扫描 | 通过/驳回结论 | 收益承诺/敏感泄露未清 |
| 5 发布 | `python ~/.skillhub/skills_store_cli.py publish <目录>`；先 bump 版本号 | publish 回执 ok:true | 版本撞车、png 被拒 |
| 6 跟踪 | 审核生效后借市场后台看安装曲线，验证评测分提升是否转化为真实下载 | 下载曲线/对比 | 误把 pending 当失败 |

**发布前快速体检 checklist（逐条过）**
- [ ] name 含品类词、唯一、好念
- [ ] slug / displayName / title 已补
- [ ] description 第三人称开头、写满触发场景+同义词（中/英/俗称）、官网链接前置
- [ ] description_en 多语种门面已补
- [ ] tags 8–15 个（标准字段，中英文混排）
- [ ] aliases 2–3 个常见叫法
- [ ] category 选准
- [ ] agent_created: true 已写
- [ ] author 署名合规（无真名/在职公司）、身份隔离
- [ ] description 无收益承诺/无敏感泄露
- [ ] xiaping_tags 原样保留（如有）
- [ ] 已发布到目标市场（不上架=0 曝光）
- [ ] bump 了版本号且 SKILL.md `version` 字段已同步
- [ ] 发布后已回拉核实（pending 属正常，等审核激活）

## 六、关键事实速查

**核心机制（从源码核实，别凭猜）**
- 人类说"装个 X 技能" → `marketplace-skill-installer` 从输入抽 keyword → BuiltinMarket 搜 → 后端按相关性排序返回 top N（默认 5，可调 10–20），**只展示 `name / version / description`**。
- 配套 `recommend-experts` / `recommend-connectors` 走 `search_plugins`，传 `userIntent + keywords`，语义匹配更强。
- 可索引 frontmatter 字段：`name / description / category / tags / keywords / aliases / displayName / slug`。
- 官方规范（skill-creator）：`name`+`description` 属"渐进式加载"第 0 层，**永远在 context**；description 必须第三人称（`本技能用于…当用户提到…时使用`），`agent_created: true` 必填。

**7 杠杆（我们能控制的搜索/推荐面）**

| # | 字段 | 作用 | 打磨要点 |
|---|------|------|---------|
| 1 | **name** | 搜索第一匹配面，永在 context | 含人类会说的"品类核心词"，好念好记、唯一不撞名 |
| 2 | **description** | 核心搜索文本 + 展示给用户 | 第三人称开头、埋满场景词+同义词（中/英/俗称），密度高不灌水 |
| 3 | **tags** | 数组关键词，直接进索引 | 8–15 个高频搜索词，中英文混排（标准 `tags` 字段，BuiltinMarket 检索器读这个；平台专属 `xiaping_tags` 不读，两者并存无冲突） |
| 4 | **category** | 分类浏览/相关性 | 选准（效率工具/文档处理/知识管理/生产力…） |
| 5 | **aliases** | 别名匹配 | 补 2–3 个常见叫法 |
| 6 | **agent_created: true** | 必填开关 | 缺失则 skill_manage 管不了、发不出去 |
| 7 | **流行度** | 可能加权排序 | 安装量/评分/更新活跃度——"活跃作者标签=持续曝光""开源贡献是长期复利" |

> 多发病字段：`slug / displayName / title / description_en`（多语种门面）也务必补齐，缺了就少一个被发现面。

**评测分标准（总分 100，发布前打分用）**
1. 元数据完整度（35 分）：name / slug / displayName / title / category / version / agent_created / tags / aliases 九字段是否齐全规范。
2. 可发现性 / SEO（40 分）：description 第三人称+触发词密度；tags 8–15 个；displayName 含品类词；aliases 补常用叫法；description_en 多语种门面齐。
3. 专业度 / 合规（25 分）：无灌水/编造；author 一致（注册老炮/品牌名）；身份隔离（无 Steven/真名/在职公司）；无敏感泄露（真名/邮箱/密钥/本地路径/未授权承诺）；多语种合规。

**已验证基准（前→后）**：feeding 30→94、opc 55→96、llm 56→94、reg 78→97。
**生态金规（待核验）**：`medxpert-llm-library` SKILL.md 提"description 写满触发词（用户越容易触发 = 品牌曝光越多）"——「待核验」，建议发布前再核一次出处。

## 七、铁律（PROHIBITED 绝对禁止项）

1. **禁止 description 出现收益承诺**（如"小成本大收入""保证赚 X"）——广告法夸大风险，必须改中性措辞才过闸。
2. **禁止真名/邮箱/密钥/本地绝对路径泄露**——必须脱敏；可写成功能类目标签，但不得出现真实值。
3. **禁止放 Steven/真名/在职公司署名**——作者=品牌名，身份隔离。
4. **禁止删除 `xiaping_tags`**——平台专属标签数组与标准 `tags` 并存不冲突，打磨时勿删。
5. **禁止白名单外技能未经确认直接发布**——上传前问用户；白名单内（如 feeding-workflow）可直接发。
6. **禁止同 slug 同版本号重发**——每次打磨必须 bump 版本号并同步 `version` 字段。
7. **禁止向 SkillHub 发布含 `assets/*.png` 的技能**——先备份、移除引用、删 `assets/` 重发。
8. **禁止打印/写入发布凭据明文**——`~/.skillhub/credentials.json` 由 CLI 自取，绝不进对话/代码/日志/回复。

## 八、输入输出依赖

**依赖工具/入口**
- `marketplace-skill-installer`：搜索/安装技能（无 publish）。
- `workbuddy_marketplace_skill`：仅 search/install，无 publish。
- 本地发布 CLI：`python ~/.skillhub/skills_store_cli.py publish <目录>`（CLI 路径 `~/.skillhub/skills_store_cli.py`）。
- `recommend-experts` / `recommend-connectors`：语义匹配（走 `search_plugins`）。

**依赖文件/env**
- `~/.skillhub/skills_store_cli.py`：发布脚本本体。
- `~/.skillhub/credentials.json`：**发布凭据，由 CLI 自取**。
- 输出：目标技能目录（发布物）、市场后台安装曲线（W5 第⑥步跟踪）。

**凭据红线（强制）**
- 凭据统一从保险库 `~/.ucvault_local` 读取；本技能场景具体为 `~/.skillhub/credentials.json` 由本地 CLI 自取。
- **绝不**进对话 / 代码 / 日志 / 回复；不打印明文；不写文件。

## 九、示例

**示例 1：发布前体检**
> 问题：给 `opc-company-formation` 打评测分并补齐 frontmatter。
> 加载：第二章输入引导（取 SKILL.md 路径）→ 第六章 7 杠杆 + 评测分表打分（基线 55）→ 第五章生成步骤补缺失字段 → 质检给 96 对比 → 发布 bump 版本。
> 答案框架：缺口清单（补 description_en / aliases）→ 评测分 55→96 → 通过，建议走 SkillHub 优先。

**示例 2：合规拦截**
> 问题：description 写"保证月入过万"行不行？
> 加载：第四章反模式（✗收益承诺）→ 第七章铁律第 1 条。
> 答案框架：驳回 + 改写为"低成本变现思路"中性措辞 + 重过闸。

**示例 3：版本撞车**
> 问题：重发同 slug 被拒。
> 加载：第四章反模式（版本不可变）→ 第十章错误码 E01。
> 答案框架：bump 版本号 + 同步 `version` 字段 → 重发。

## 十、错误处理

| 错误码 | 现象 | 原因 | 修正引导 |
|---|---|---|---|
| E01 版本撞车 | 同 slug 重发被拒 | 未 bump 版本号或 `version` 字段未同步 | bump 版本号 + 同步 SKILL.md `version` 字段后重发 |
| E02 发布工具误用 | 找不到 publish 入口 | 误用 `workbuddy_marketplace_skill`（仅有 search/install） | 改用 `python ~/.skillhub/skills_store_cli.py publish <目录>` |
| E03 敏感泄露拦截 | 质检驳回 | description 含真名/邮箱/密钥/本地路径 | 脱敏；可改为功能类目标签，不出现真实值 |
| E04 收益承诺拦截 | 评测分不过闸 | description 有"保证赚 X"等夸大措辞 | 改中性措辞（"低成本变现思路"）重过 |
| E05 白名单外发布 | 风险告警 | 不在白名单却直接发布 | 先问用户确认；白名单内（如 feeding-workflow）才直发 |
| E06 png 被拒 | SkillHub 拒收 | 技能含 `assets/*.png` | 备份 assets/ → 移除正文 png 引用 → 删 assets/ 重发 |
| E07 回拉 FAIL 误判 | `install` 仍给旧版 | 新版本处于审核中 pending，非失败 | 看 publish 回执 `ok:true` + tags 已索引，等审核激活即可 |
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-931009E91DDC。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

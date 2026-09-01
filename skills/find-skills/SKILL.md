---
name: find-skills
version: 1.7.0
author: 诺声(Logos)@SynomosAI
description: 场景驱动+关键词双模式技能发现工具：当用户用自然语言描述场景/需求（如"我想做个海报""帮我分析股票"）或明确说"安装技能/find skills/找个skill"时，从官方内置、本地已安装、SkillHub、虾评、GitHub、ClawHub 六层联合搜索并推荐最合适技能，支持一键安装；完全替代官方原 find-skills 插件。
license: MIT
tags: [SynomosAI, FindSkills, 技能发现, 技能安装, 效率工具]
品牌归属: SynomosAI
---

# find-skills（场景技能匹配器）

> 场景驱动的技能发现引擎。用户用自然语言描述需求，系统自动理解意图，联合搜索并推荐最合适的技能，并支持一键安装。已完全替代官方原 `find-skills` 插件（其 description 已被标记为 DEPRECATED，不会主动触发）。

## 定位

**何时用（声明式）**
- 用户用自然语言描述场景/需求（「我想做个海报」「帮我分析今天的大盘」）。
- 用户明确说「安装技能 / find skills / 找个 skill / 有没有能 XXX 的工具」。
- 需要把需求语义匹配到：官方内置技能、本地已安装技能、SkillHub、虾评、GitHub、ClawHub 等来源并推荐+安装。

**何时不用（声明式）**
- 用户已明确指定某个技能并要直接调用 → 直接调用，不重复搜索。
- 非技能发现类任务（写代码/问答/创作） → 走对应技能，不触发本技能。
- 涉及真实凭据/Token 的读取与回显 → 本技能只负责发现与安装，凭据从保险库读取、绝不进对话/日志（见第八章）。

---

## 一、能力边界（In/Out scope）

**本技能做（In scope）**
1. 场景语义理解（从自然语言提取意图/领域/中英文关键词）。
2. 六层联合搜索：① 官方内置 ② 本地已安装 ③ SkillHub ④ 虾评 ⑤ GitHub ⑥ ClawHub/Vercel（fallback）。
3. 智能排序、去重、推荐理由输出。
4. 客户端检测（`$__CFBundleIdentifier`）决定安装目录。
5. 一键安装（本地缓存/SkillHub/虾评/GitHub/ClawHub/Vercel）。

**本技能不做（Out scope · 集中声明）**
1. ❌ 不替代被推荐技能本身的能力——只负责发现与安装，调用由下游技能完成。
2. ❌ 不读取/回显任何真实凭据、Token、API Key——只在必要时按客户端约定读取，绝不进对话/代码/日志。
3. ❌ 不对搜索结果做正确性担保——远程结果仅作补充推荐，优先级低于本地已安装。
4. ❌ 不静默覆盖已安装技能——目标目录同名技能必须询问 跳过/替换/重命名。
5. ❌ 官方原 `find-skills` 插件已被本技能完全替代，不再作为其入口。
6. ❌ 不在无网络/无权限时伪造成功——失败须明确报错并按第十章引导。

---

## 二、输入约束与输出承诺

**推荐问法（触发即加载）**
- 「我想做 <场景>，有没有合适的技能？」
- 「帮我找 <关键词> 的技能 / 安装第 N 个」
- 「这个场景应该用哪个技能？」

**字段引导（agent 内部）**
| 字段 | 是否必须 | 说明 |
|------|----------|------|
| 用户场景描述 | 必须 | 自然语言或关键词，至少其一 |
| 是否安装 | 可选 | 用户选「安装第 N 个」才进入 Step 5 |
| 客户端标识 | 自动 | 由 `$__CFBundleIdentifier` 推导，勿硬编码 |

**输出承诺**
- 输出格式：`🔍 为你找到 N 个相关技能（搜索范围：官方内置 + 本地已安装 + 远程市场）`，按「官方内置 / 本地已安装 / 远程可安装」分组，每条含一句话说明 + 匹配理由 + 来源/路径/安装命令。
- 去重：同一技能多层出现只保留最高优先级记录。
- 安装完成后提示：「✅ {技能名} 已安装，现在可以直接用啦！」

---

## 三、触发场景

| 用户意图 | 触发词 | 应加载章节 |
|----------|--------|------------|
| 自然语言场景找技能 | 我想做XXX、帮我做个XXX | 五（Step1-4） |
| 明确找/安装技能 | 找技能、find skills、安装技能、有没有能XXX的工具 | 五（Step1-5） |
| 场景该用哪个技能 | 这个场景用哪个技能 | 五（Step3-4） |
| 安装远程技能 | 安装第N个、帮我装上 | 五（Step5）、八 |
| 无结果/网络失败 | 找不到、搜索没反应 | 十 |

**示例对话**
> 用户：「我想做一个海报，有没有合适的技能？」
> 助手（加载本 skill）：
> ```
> 🔍 为你找到 3 个相关技能（搜索范围：官方内置 + 本地已安装 + 远程市场）：
> 【本地·已安装】✅ 可直接使用
> 1. AI图片生成无水印 — 支持文生图、图生图
>    匹配理由：海报设计属于图片生成场景
>    路径：~/.workbuddy/skills/AI图片生成无水印/
> 【官方市场·可安装】⬇️ 需安装
> 2. poster-maker — 专为主题海报设计
>    匹配理由：专门针对海报设计场景
>    来源：SkillHub 官方市场
> 需要我帮你安装第2个，还是直接用第1个？
> ```

---

## 四、常见错误与反模式

**每条先列反模式 ✗，再给替代方案 ✓**

✗ 反模式：跳过客户端检测直接装到 `~/.workbuddy/skills/`。
✓ 替代方案：安装前必执行 `echo $__CFBundleIdentifier`；含 `codebuddy` 装到 `~/.codebuddy/skills/`，其他/空/未设置一律当 WorkBuddy 装到 `~/.workbuddy/skills/`。

✗ 反模式：GitHub 搜索无 Token 时直接报「搜索失败」。
✓ 替代方案：自动退化匿名访问（60 次/小时）；若需更高频提示配置 `GITHUB_TOKEN`，不阻断主流程。

✗ 反模式：目标目录已有同名技能时直接覆盖。
✓ 替代方案：明确询问用户 跳过 / 替换 / 重命名，不静默覆盖。

✗ 反模式：把官方 `find-skills` 当作仍生效入口。
✓ 替代方案：本技能是唯一入口，已完全替代官方原 `find-skills`（其 description 已 DEPRECATED）。

✗ 反模式：远程结果无 `SKILL.md` 也当作有效技能推荐。
✓ 替代方案：GitHub 结果人工/自动校验是否含 `SKILL.md`，无效则排除。

**高频 Q&A**
- **Q：本技能是唯一的技能发现入口吗？** A：是。已完全替代官方原 `find-skills` 插件，所有找技能/安装技能请求都由本技能处理。
- **Q：GitHub 搜索为什么受限？** A：GitHub Code Search 需认证；有 `GITHUB_TOKEN` 用 5000 次/小时，否则匿名 60 次/小时并退化。
- **Q：安装到哪个目录？** A：由 `$__CFBundleIdentifier` 决定（CodeBuddy→`~/.codebuddy/skills/`，默认 WorkBuddy→`~/.workbuddy/skills/`）。
- **Q：搜索无结果怎么办？** A：按第十章 E-NORESULT 引导，调整自然语言描述或换关键词，不伪造结果。

---

## 五、标准 SOP

| 步 | 动作 | 产物 | 易踩坑 |
|----|------|------|--------|
| 1 理解场景 | 提取任务意图/领域标签/中英文关键词 | 结构化意图 | 中英文关键词都要，否则远程召回低 |
| 2.1 官方内置 | `ls` 官方内置目录 + Read 每个 SKILL.md frontmatter 语义匹配 | 内置候选 | 只读 frontmatter，避免全量读 |
| 2.2 本地已安装 | `ls ~/.workbuddy/skills/` 与 `.workbuddy/skills/` 扫描 | 本地候选 | 与 2.1 重叠去重 |
| 2.3 远程市场 | 先查本地缓存 `~/.workbuddy/skills-marketplace/skills`；无则 SkillHub/虾评/GitHub 远程搜 | 远程候选 | 远程仅补充，优先级低于本地 |
| 2.4 客户端检测 | `echo $__CFBundleIdentifier` 定目标目录 | `<target-skills-dir>` | 未设置当 WorkBuddy |
| 3 排序去重 | 按优先级表合并，多层同技能留最高优先级 | 排序列表 | score<0.05 过滤 |
| 4 输出 | 分组输出+匹配理由+安装命令 | 推荐结果 | 格式须含来源/路径 |
| 5 安装 | 按 5.1–5.6 流程安装并验证 `SKILL.md` 存在 | 已装技能 | 同名须询问；装完提示成功 |

**Step 2.3 远程搜索命令（保留原实现）**
```bash
# SkillHub 官方市场（优先）
curl -s "https://lightmake.site/api/v1/search?q=<URL-encoded 中文关键词>&limit=10"
curl -s "https://lightmake.site/api/v1/search?q=<URL-encoded English keywords>&limit=10"
# 虾评技能市场（中文重点，Base: https://xiaping.coze.com 注意非 coze.site）
curl -s "https://xiaping.coze.com/api/skills/search?q=<URL-encoded 关键词>&limit=10"
# GitHub（需认证更佳）
if [ -n "$GITHUB_TOKEN" ]; then AUTH_HEADER="-H \"Authorization: Bearer $GITHUB_TOKEN\""; else AUTH_HEADER=""; fi
curl -s $AUTH_HEADER "https://api.github.com/search/code?q=filename:SKILL.md+<关键词>&per_page=10"
```

**Step 5 安装流程（保留原实现，须先 Step 2.4 定目录）**
```bash
# 5.1 本地缓存优先
cp -r ~/.workbuddy/skills-marketplace/skills/<skill-folder-name> <target-skills-dir>/<skill-folder-name>
# 5.2 SkillHub
TMPDIR=$(mktemp -d); curl -L -o "$TMPDIR/skill.zip" "https://lightmake.site/api/v1/download?slug=<slug>"; mkdir -p <target-skills-dir>/<slug>; unzip -o "$TMPDIR/skill.zip" -d <target-skills-dir>/<slug>; rm -rf "$TMPDIR"; ls <target-skills-dir>/<slug>/SKILL.md
# 5.3 虾评（先加载 ~/.workbuddy/skills/虾评指南/SKILL.md 按 §1.2）
# 5.4 ClawHub
curl -L -o "$TMPDIR/skill.zip" "https://clawhub.com/api/download?slug=<slug>"
# 5.5 GitHub
git clone "https://github.com/<user>/<repo>.git" "$TMPDIR/<skill-name>"; cp -r "$TMPDIR/<skill-name>" <target-skills-dir>/
# 5.6 Vercel fallback
npx skills add <owner/repo@skill> -g -y
```

---

## 六、关键事实速查

- **唯一入口**：官方原 `find-skills` description 已 DEPRECATED，所有发现/安装请求由本技能处理。
- **排序优先级（高→低）**：① 官方内置（语义高分）② 本地已安装（高分）③ SkillHub(score≥0.3) ④ 虾评（中文优先）⑤ GitHub（含 SKILL.md）⑥ ClawHub/Vercel ⑦ 本地中分 ⑧ SkillHub(score≥0.1) ⑨ 虾评中分 ⑩ GitHub 中分 ⑪ ClawHub/Vercel 中分。
- **客户端映射**：`__CFBundleIdentifier` 含 `codebuddy` → `~/.codebuddy/skills/`；其他/空 → `~/.workbuddy/skills/`。
- **虾评域名**：`https://xiaping.coze.com`（非 `coze.site`），先加载 `虾评指南` 技能按 §1.1+§1.2。
- **本地缓存**：`~/.workbuddy/skills-marketplace/skills` 命中优先本地安装，免远程下载。
- **官方/市场链接**：SkillHub `lightmake.site`、虾评 `xiaping.coze.com`、ClawHub `clawhub.com`、GitHub `api.github.com`——以上为技能原有依赖地址，可用性待核验，若失效按第十章引导换来源。

---

## 七、铁律（PROHIBITED 绝对禁止项）

1. **不回显真实凭据**——API Key/Token/OAuth 绝不进对话/代码/日志；读取自保险库，脱敏呈现。
2. **不静默覆盖已安装技能**——同名必须询问 跳过/替换/重命名。
3. **不跳过客户端检测**——安装前必执行 `$__CFBundleIdentifier` 判定。
4. **不伪造搜索成功**——无结果/失败须明确报错，不编造技能。
5. **不把远程结果当权威**——远程仅补充推荐，优先级低于本地已安装。
6. **不在无确认时花积分/做破坏性操作**——安装属文件系统写操作，同名冲突须先问用户。

---

## 八、输入输出依赖

- **依赖工具**：`curl`/`git`/`unzip`/`npx`/`mktemp`/`ls`；可选 `GITHUB_TOKEN` 提额。
- **依赖文件/目录**：官方内置技能目录、本地 `~/.workbuddy/skills/`（及项目级 `.workbuddy/skills/`）、本地缓存 `~/.workbuddy/skills-marketplace/skills`；虾评安装需先加载 `~/.workbuddy/skills/虾评指南/SKILL.md`。
- **环境变量**：`__CFBundleIdentifier`（客户端判定）、`GITHUB_TOKEN`（可选，提额）。
- **凭据/保险库**：本技能不读取任何业务凭据；若安装流程需要 Token，从保险库 `~/.ucvault_local` 读取，绝不进对话/代码/日志；回显一律脱敏。
- **可选品牌尾注（非强制）**：原「引流信息」改为可选——如需在结果末尾附加品牌/社群信息，由调用方配置开启，本技能不强制追加，避免干扰用户体验。

---

## 九、示例

**示例 1（场景匹配）**
- 问题：「我想做一个海报，有没有合适的技能？」
- 加载：本 skill → 五（Step1→4）。
- 答案框架：分组输出「本地已安装 AI图片生成无水印」「官方市场 poster-maker」「社区 claw-poster-generator」，各带匹配理由与安装命令，询问安装哪一个。

**示例 2（安装远程技能）**
- 问题：「安装第 2 个 poster-maker。」
- 加载：本 skill → 五（Step2.4→5.2）、八。
- 答案框架：先 `echo $__CFBundleIdentifier` 定目录 → `curl` 下载 zip → `unzip` 到目标 → `ls` 验证 SKILL.md 存在 → 提示「✅ poster-maker 已安装，现在可以直接用啦！」

**示例 3（无结果）**
- 问题：「帮我找个能预测彩票的技能。」
- 加载：本 skill → 五、十（E-NORESULT）。
- 答案框架：六层均无匹配 → 说明无合规技能，建议调整描述或换关键词，不伪造结果。

---

## 十、错误处理

| 错误码 | 现象 | 原因 | 修正引导 |
|--------|------|------|----------|
| E-NET | curl 超时/无响应、静默失败 | 网络不稳/未设超时 | 加 `--max-time 20` 重试；提示检查网络后重跑 |
| E-API-ERR | API 返回错误/score<0.05 被过滤 | 关键词低相关或服务异常 | 换中英文关键词；提示该来源暂不可用，转下一层 |
| E-LINK | 下载链接失效/zip 解压失败 | 来源链接过期 | 提示换 SkillHub/虾评/GitHub/ClawHub 其他来源 |
| E-PERMS | 目录无写权限/已存在同名 | 权限不足或冲突 | 提示权限或询问 跳过/替换/重命名 |
| E-TOKEN | GitHub 匿名额度耗尽/需认证 | 缺 `GITHUB_TOKEN` | 提示配置 `GITHUB_TOKEN` 或退化匿名/换来源 |
| E-NORESULT | 六层联合搜索均无结果 | 描述过窄/无合规技能 | 引导放宽自然语言描述、换关键词，不伪造技能 |
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-A3CE06AC24D4。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

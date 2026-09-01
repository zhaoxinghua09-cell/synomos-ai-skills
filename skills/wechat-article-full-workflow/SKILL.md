---
name: wechat-article-full-workflow
version: 2.0.0
author: 诺声(Logos)@SynomosAI
description: 微信公众号文章全流程技能：选题 → 标题 → 写作 → 排版 → 配图 → QA 自检 → 推送草稿 → 知识库存档。用于回答「公众号文章从零怎么做完」「排版老出问题怎么办」「怎么把文章推到草稿箱」等问题。逐环节配自检项，把历史踩坑固化为拦截规则；事实与数据按真实参照法挂回素材来源，素材里没有的不写；各环节产出与自检结论按证据链审计留痕。
license: MIT
tags:
- 诺声
- AI技能
- SynomosAI
- wechat-article-full-workflow
- 公众号全流程
- 公众号发文
品牌归属: SynomosAI
copyright: SynomosAI
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
ambassador: Logos
languages:
- zh-CN
---

# 微信公众号文章全流程（wechat-article-full-workflow）

## 定位 + 何时用 / 不用

本技能是一套**通用方法论 + 可调用脚本**工具，覆盖一篇公众号文章从 0 到「推入草稿箱」的完整链路，并把每个环节的自检结论与素材来源留痕，形成可审计证据链。

**何时用**
- 用户要「从零写/做一篇公众号文章」「走完整发文流程」。
- 用户遇到具体环节问题：选题没思路、标题不吸睛、排版总被微信剥离样式、配图上传失败、草稿推送报错、想做发文前 QA。
- 用户想复用既有素材库（见 `assets/material_index.json`）并归档本次产出。

**何时不用**
- 用户只是要一段普通文案/朋友圈短文（用通用写作即可，不必走全流程）。
- 用户要求**群发/自动发布**到粉丝——本技能只推到**草稿箱**，群发需人工在后台操作（权限 48001 不可预览群发）。
- 用户要的不是微信公众号，而是知乎/小红书/头条等平台（排版规则不同，本技能不适用）。
- 涉及医疗器械/医疗疗效/临床声明——本技能非医疗软件，禁止此类声明（见免责声明）。

---

## 一、能力边界

**能做（IN）**
1. 按 8 环节产出公众号文章：选题、标题、写作、排版、配图、QA 自检、推送草稿、知识库存档。
2. 调用包内脚本完成：配图上传替换（`scripts/upload_to_wechat.py`）、推草稿（`scripts/push_draft.py`）。
3. 从 `assets/material_index.json` 索引既有素材，避免重复生图。
4. 对每个环节执行自检并产出带证据链的归档清单。

**不能做（OUT）**
1. 不群发、不自动发布、不生成永久二维码营销链接。
2. 不编造事实、数据、引用——素材/资料里没有的内容不写，需明确标注「待核验」。
3. 不绕过微信 API 限制（如 48001 预览权限），不破解、不爬取。
4. 不处理非微信公众号平台，不做医疗/疗效/临床声明。
5. 不读取或打印微信 `AppSecret`/凭证原文到对话（见第八章）。

---

## 二、输入约束与输出承诺

**输入约束**
- 用户至少提供：①文章主题或目标受众；②期望语气/风格（默认「实用、克制、不说教」）。
- 可选：参考素材路径、封面图路径（16:9 PNG）、二维码图路径。
- 标题硬约束：≤8 个中文字（UTF-8 字节 ≤24），超长必须截断或改短。
- 正文排版约束：仅内联 `style`，禁用 `<style>`/class/flex/grid/calc/base64 内嵌/`<!DOCTYPE>`/`<html>`/`<head>`/`<body>`，图片必须带 `width`+`height`，URL 必须 `https`。

**输出承诺**
- 必交付：①最终 HTML（`<section>` 片段，可直接粘进草稿）；②标题；③摘要(digest)；④作者名；⑤封面图 media_id；⑥QA 自检清单（含每条结论与证据）；⑦知识库存档条目。
- 推草稿后交付：`media_id`、封面 `media_id`/`url`、后台预览路径。
- 不交付：群发结果、粉丝数据、原文未提及的「权威背书」。
- 事实承诺：凡数据/引用均附来源；无来源一律标「待核验」。

---

## 三、触发场景（意图表 + 示例对话）

**意图 → 动作对照表**

| 用户意图 | 触发词示例 | 本技能动作 |
|---------|-----------|-----------|
| 从零写一篇公众号文章 | 写公众号、公众号全流程、做一篇推文 | 走完 8 环节 SOP |
| 只卡在某环节 | 排版总出问题、标题怎么起、配图上传失败 | 跳到对应环节 + 该环节自检 |
| 推到草稿箱 | 推送草稿、发到草稿箱、不群发 | 执行第七、八章脚本 |
| 复用素材/归档 | 用之前的图、归档这次产出 | 读 material_index + 写知识库 |
| 发文前 QA | 公众号自检、检查一遍再发 | 执行第六章 QA 清单 |

**示例对话 1（全流程）**
> 用户：帮我从零写一篇「AI 打工我躺平」的公众号文章，实用风格。
> 技能：进入全流程。先确认选题与受众→生成 3 个候选标题（均 ≤8 字）→写正文（事实挂素材来源）→出内联排版 HTML→按 7 图占位符配图→逐环节 QA→推草稿箱→归档。需要你提供封面图路径吗？

**示例对话 2（单环节）**
> 用户：我的排版一粘进微信样式就没了。
> 技能：这是用了 class/`<style>`/flex 导致。按第四章反模式改内联 + `<table>` 布局，我直接给你合规骨架（`references/html-template.md`）。

**示例对话 3（推草稿）**
> 用户：文章写好了，推到草稿箱，别群发。
> 技能：调用 `scripts/push_draft.py`，先清旧草稿再上传封面并推入草稿箱，返回 `media_id`，你在后台预览即可。

---

## 四、常见错误与反模式（FAQ + 高频 Q&A）

**高频 Q&A**

Q1：为什么样式一粘进微信就全没了？
A：微信编辑器会剥离 `<style>`、class、flex/grid/calc。必须全部内联 `style`，布局用 `<table>` 模拟，写死像素值。见 `references/html-template.md` 避坑表。

Q2：标题写 12 个字可以吗？
A：不行。标题硬约束 ≤8 中文字（≤24 字节），超长会在推送时被截断或告警，必须改短。

Q3：能用 base64 把图嵌进 HTML 吗？
A：不能。微信会拒绝，必须上传素材库拿到 CDN `https` URL 再替换占位符（`scripts/upload_to_wechat.py`）。

Q4：能直接群发给粉丝吗？
A：不能。本技能只推草稿箱；群发/预览受 48001 权限限制，需人工后台操作。

Q5：素材里没的数据我能编吗？
A：不能。无来源内容一律标「待核验」，禁止编造事实/数据/引用。

**反模式（PROHIBITED 预览）**
- ❌ 用 class + `<style>` 写样式 → ✅ 全内联。
- ❌ 用 flex/grid 做布局 → ✅ `<table>`。
- ❌ `<img>` 无 width/height 或 `http://` → ✅ 带尺寸 + `https`。
- ❌ 把 `AppSecret` 写进对话/日志 → ✅ 从保险库读，对话只显示掩码。
- ❌ 群发/自动发布 → ✅ 仅推草稿箱。
- ❌ 编造无来源事实 → ✅ 标「待核验」或删除。

---

## 五、标准 SOP（步骤表）

| 步 | 环节 | 关键动作 | 自检项 | 调用 |
|----|------|---------|-------|------|
| 1 | 选题 | 明确主题/受众，查 `material_index.json` 复用素材 | 主题有受众、素材已查 | — |
| 2 | 标题 | 生成 ≥3 候选，均 ≤8 中文字 | 字节 ≤24、无标题党 | — |
| 3 | 写作 | 写正文，事实挂素材来源 | 无编造、来源可溯 | — |
| 4 | 排版 | 套 `html-template.md` 内联骨架 | 无 class/style标签/flex、图有尺寸 | references/html-template.md |
| 5 | 配图 | 7 占位符 + 二维码，上传替换 | 全部 `https` CDN、二维码 200x200 | scripts/upload_to_wechat.py |
| 6 | QA 自检 | 逐环节跑第六章清单 | 全部 PASS 或标「待核验」 | — |
| 7 | 推送草稿 | 清旧草稿→传封面→推草稿箱 | 返回 media_id、未群发 | scripts/push_draft.py |
| 8 | 知识库存档 | 写产出+自检结论+来源留痕 | 证据链完整可审计 | — |

> 渐进披露：单环节问题只走对应步 + 其自检；全流程才走满 8 步。

---

## 六、关键事实速查

- **标题上限**：≤8 中文字 / ≤24 UTF-8 字节。
- **排版铁规**：内联 style；布局用 `<table>`；禁 `<style>`/class/flex/grid/calc/base64；禁 `<!DOCTYPE>`/`<html>`/`<head>`/`<body>`。
- **图片**：必须 `width`+`height`，URL 必须 `https`，走素材库拿 CDN。
- **标准配图**：`IMAGE_PLACEHOLDER_01`~`07` + `QR_CODE_PLACEHOLDER`（200x200）。
- **推送 API**：`stable_token` 取 token → `draft/batchget` 查旧稿 → `draft/delete` 清稿 → `material/add_material` 传图/封面 → `draft/add` 推草稿。
- **已知限制**：预览/群发权限 48001，只能后台手动；Bash 读不到 Windows 用户环境变量，需 PowerShell 桥接。
- **凭证**：`WECHAT_APP_ID` / `WECHAT_APP_SECRET`，从环境变量或 `wechat_config.json` 读，对话不打印原文。
- **素材索引**：`assets/material_index.json`（7 图 + 二维码）。

---

## 七、铁律（PROHIBITED）

1. 禁止群发、禁止自动发布、禁止绕过微信 API 权限限制。
2. 禁止编造事实/数据/引用；素材无来源内容必须标「待核验」。
3. 禁止在对话或日志中输出 `AppSecret`/凭证原文（仅显示掩码）。
4. 禁止用 class/`<style>`/flex/grid/calc/base64 内嵌/外链 `http` 排版。
5. 禁止输出 `<!DOCTYPE>`/`<html>`/`<head>`/`<body>` 整页，只给 `<section>` 片段。
6. 禁止把本技能用于医疗器械/疗效/临床声明。
7. 禁止跳过任一环节 QA 直接推草稿；任一项 FAIL 须先修复。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

**输入依赖**
- 运行环境：Python3 + `requests`；Windows 需用 PowerShell 桥接用户环境变量。
- 凭证来源（按顺序，绝不下沉到对话）：
  1. Bash 环境变量 `$WECHAT_APP_ID` / `$WECHAT_APP_SECRET`
  2. 配置文件 `wechat_config.json`：`{"appid":"...","secret":"..."}`
  3. Windows 用户环境变量（PowerShell 只读）：`[Environment]::GetEnvironmentVariable("WECHAT_APP_SECRET","User")`
- 内容依赖：`assets/material_index.json`、`references/html-template.md`、`references/credentials-guide.md`。

**安全/扫描（trust.scan 弱项修复）**
- 凭证只在脚本进程内使用；对话、SKILL.md、日志均**不出现 Secret 原文**。
- 脚本自身也只打印掩码：`token[:16]…`、`secret[:4]…`（见 `scripts/push_draft.py:196`）。
- AppID `wxca0592af7747824d` 属公开标识可出现在指南；Secret 永远不可出现在任何文本。
- 跨环境传递用 `powershell` 桥接赋值给当前 shell 变量，不写入文件、不 echo。

**输出依赖**
- 推草稿成功依赖有效 token + 封面图存在 + 标题合规；失败见第十章。

---

## 九、示例

**示例 A：单篇完整产出（片段）**
```
选题：AI 打工我躺平（受众：职场新人）
标题候选：①AI打工我躺平 ②把活交给AI ③躺着也能产出
正文：…（事实挂 material_index IMG_001~007 来源）
排版：套 html-template.md 骨架，7 图占位符 + 二维码
配图：upload_to_wechat.py 上传 7 图 → 替换 data-src 为 https CDN
QA：标题≤8字✓ 内联✓ 图带尺寸✓ 来源可溯✓
推送：push_draft.py 清旧稿→传封面→推草稿箱 → media_id=xxx
归档：产出+自检+来源写入知识库
```

**示例 B：只修排版**
用户提供被剥离样式的 HTML → 套 `html-template.md` 内联骨架重排 → 返回合规 `<section>` 片段。

**示例 C：推草稿命令**
```
python scripts/push_draft.py article.html "AI打工我躺平" "摘要" "作者" cover.png
# 输出仅掩码：AppID: wxca… Secret: xxxx… Token: abc123…（16位）
```

---

## 十、错误处理

| 错误 | 现象 | 处理 |
|------|------|------|
| 凭证缺失 | `WECHAT_APP_ID/SECRET not found` | 按第八章顺序补环境变量/`wechat_config.json`；不打印 Secret |
| token 失败 | `stable_token` 返回无 `access_token` | 检查 AppID/Secret 是否正确、是否过期；重试一次 |
| 封面缺失 | `Cover image not found` | 提供 16:9 PNG 封面路径，重跑 |
| 配图上传失败 | `material/add_material` 无 `media_id` | 检查图片格式/大小/网络；跳过缺失文件并告警 |
| 草稿推送失败 | `draft/add` 无 `media_id` | 查返回 errcode；48001 为权限不足，转后台手动 |
| 标题超长 | 字节 >24 | 截断或改短至 ≤8 中文字后再推 |
| HTML 被剥离 | 样式丢失 | 回第四章反模式改内联 + `<table>` |
| 预览权限 | 48001 | 仅后台手动预览，不群发 |

**兜底原则**：任一环节 FAIL 先修复再继续；不得带 FAIL 推草稿。凭证相关错误只报「缺失/失败」，绝不回显 Secret 原文。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-C71819B2CB61。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

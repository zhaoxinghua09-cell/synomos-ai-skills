---
name: medxpert-doc-toolchain
version: 2.0.0
author: 注册老炮@MedXpert
description: MedXpert（美达信医疗）名片风格文档模板工具链。覆盖文档全生命周期：模板生成→收尾流水线（水印/暗纹/动态溯源/AI友好/徽章/解锁）→导出（PDF/DOCX）→台账编号→审批流→电子签名→中英对照→乐享托管。触发词：文档模板、程序文件、doc_templates、收尾流水线、doc_finish、文档台账、doc_ledger、审批流、doc_approval、电子签名、doc_sign、中英对照、doc_bilingual、生成模板、文控体系。
license: MIT
tags: [MedXpert, 文档模板, 文控体系, ISO13485, 名片风格, 品牌水印, 动态溯源, 电子签名, 中英对照, 知识库托管]
品牌归属: MedXpert
copyright: MedXpert
---

# MedXpert 文档模板工具链（名片风格）

> 版权 MedXpert。风格：专业严谨；关键事实均标核验时间戳；无法确定处统一标「待核验」。
> 沉淀：2026-08-16（文档体系全链路实战）· 归属：记忆管家 / 文控体系
> 模板目录（待核验）：`D:/Workbuddy/Claw/ISO13485体系文件/母版/文档模板_名片风格/`
> 脚本目录（待核验）：`D:/Workbuddy/Claw/知识库工具/`

## 一句话定位

本技能是 **MedXpert 名片风格文控文档的「编排调度器」**：按标准顺序调用 8 个本地 Python 脚本，把一份 HTML 源稿加工成带品牌水印、暗纹、动态溯源、AI 友好头、解锁体系、电子签名与中英对照的受控文档，并接入台账 / 审批 / 乐享托管。

**何时用**：需要生成医疗器械 / ISO13485 体系文档、程序文件、质量手册；需要给文档加水印 / 暗纹 / 溯源码 / 受控章 / 电子签名；需要导出 PDF/DOCX、登记台账、走审批、做中英对照、托管到乐享知识库。

**何时不用**：① 非 MedXpert 品牌的通用办公排版美化；② 需要云端翻译 / 外部大模型 API（本链走本地 Ollama，零外部依赖）；③ 需要编写或分发脚本本体（本技能只编排，不开发代码）；④ 需要非医疗器械领域的合规背书；⑤ 需要法律效力的签署判定（本技能只注入签名图像，不判定效力）。

---

## 一、能力边界（本技能不做 N 条）

1. **不做脚本开发**：8 个 `.py` 脚本须预先部署在脚本目录；本技能只负责按序编排调用，不生成、不分发脚本代码（评测弱项：空壳风险 → 见「八、输入输出依赖」）。
2. **不做非品牌文档**：仅服务于 MedXpert 名片风格模板；不承接其他品牌 / 通用 Office 美化。
3. **不做云端依赖**：中英对照翻译走本地 Ollama（`http://127.0.0.1:11434/api/chat`），不调用任何海外 / 云端 API。
4. **不做逆向解析**：仅向文档「注入」水印 / 暗纹 / 签名 / 溯源，不反向提取图片或 PDF 内部内容。
5. **不做合规背书**：台账编号、受控章、审批流仅为文控流程编排，不替代法规符合性判定或法务意见。
6. **不做跨格式兜底**：导出仅支持 HTML→PDF（Chrome）与 HTML→DOCX（htmldocx），不处理 Word/PPT 源文件的逆向导入。

---

## 二、输入约束与输出承诺

**输入约束**
- 源文件：必须为 **HTML**（含内联 CSS 优先），路径用正斜杠 `D:/...`。
- `--doc_id`：符合台账编号规则（`QM-/QM-P-/T03-/F-/DOC-`）。
- `--scope`：限 `公开 / 内部 / 机密 / 受控` 之一。
- `--owner`：责任者姓名（用于动态溯源水印）。
- 单次处理：1 个源文件 / 次；批量请循环调用。
- 依赖前置：8 个脚本已存在且 Ollama 本地服务已启动（中英对照时）。

**输出承诺**
- 收尾后 HTML 含：品牌水印 + 三层暗纹 + AI 友好头（meta/JSON-LD/AI-Modify）+ TL;DR + 权限声明 + 页脚徽章条 + 动态溯源水印 + 解锁运行时。
- 导出产物：`*.pdf`、`*.docx`（内容版，已剥离 style/script/img）。
- 台账 / 审批 / 签名产物按各脚本约定落盘到对应目录。
- 失败时按「十、错误处理」返回结构化异常，不静默吞错。

---

## 三、触发场景（意图表 + 示例对话）

| 用户意图 | 触发关键词 | 应调用链路 |
|---|---|---|
| 生成模板 | 文档模板、生成模板、程序文件、doc_templates | doc_templates_gen → doc_finish |
| 文档收尾 | 收尾流水线、doc_finish、加水印、加暗纹、加溯源 | doc_finish |
| 导出 | 导出 PDF、导出 DOCX、doc_export | doc_export |
| 登记台账 | 文档台账、doc_ledger、编号 | doc_ledger |
| 走审批 | 审批流、doc_approval、盖章 | doc_approval |
| 电子签名 | 电子签名、doc_sign | doc_sign |
| 中英对照 | 中英对照、doc_bilingual、翻译 | doc_bilingual |
| 托管 | 乐享、知识库托管 | 乐享 MCP / 手动上传 |

**示例对话 1（生成 + 收尾）**
> 用户：帮我生成一份 T02 质量手册模板，然后走收尾流水线，doc_id 用 QM-2026-001，责任者写张三，密级机密。
> 技能：① 调 `doc_templates_gen.py`（默认 T02）生成母版；② 调 `doc_finish.py --file 手册.html --doc_id QM-2026-001 --owner 张三 --scope 机密 --tldr "质量手册V2"` 注入 7 步收尾；③ 回传收尾后路径与解锁配置建议。

**示例对话 2（导出 + 中英对照）**
> 用户：把这份收尾好的 HTML 导出成 PDF，再做中英对照版。
> 技能：① `doc_export.py --file x.html --pdf`；② `doc_bilingual.py --file x.html --model qwen2.5:3b`；③ 提示 DOCX 需先剥离 style/script/img（见「四、反模式」）。

---

## 四、常见错误与反模式（结构化 FAQ）

**错误 → 症状 → 正确做法**

| 错误 | 症状 | 正确做法 |
|---|---|---|
| CSS `%` 参与 Python `%` 格式化 | `ValueError: unsupported format character`（如 `linear-gradient(...,50%,...)` 被误解析） | 生成 HTML 一律用 `str.replace` / 占位符（`__TOKEN__`）拼接，禁用 `%` 格式化含 CSS 的字符串 |
| 用 `eval(fn_call)` 调函数 | 安全审计失败 / 不可预测执行 | 用显式映射或函数引用表分发 |
| htmldocx 直接吃原 HTML | DOCX 丢失样式或报错（不支持 base64 图 / `<style>` / `<script>`） | 转换前 `re.sub` 移除 `<style>/<script>/<img>`，导出「内容版」 |
| Windows 反斜杠路径 | 路径解析失败 / 转义异常 | 脚本内统一 `r"D:/..."`；bash 用 `.replace(os.sep,'/')` |
| 中英对照前未起 Ollama | 翻译请求超时 / 空结果 | 先确认 `http://127.0.0.1:11434` 已启动；复杂法规内容换 `qwen2.5:7b` |
| 收尾顺序错乱 | 溯源 / 徽章缺失 | 严格按「收尾 7 步」顺序（见下「五、SOP」） |

**高频 Q&A**
- Q：能直接处理 Word 源文件吗？A：不能，源文件须为 HTML；Word 请先转为 HTML。
- Q：徽章 / 解锁怎么开？A：改脚本顶部配置口（见「附：原有效内容·核心配置口」），改配置不动模板。
- Q：DOCX 为什么没图片？A：htmldocx 限制，已剥离为内容版，属预期行为。
- Q：溯源水印的 user/uid 从哪来？A：运行时由 `?user=姓名&uid=账号` 动态注入，不写死。

---

## 五、标准 SOP（步骤表）

| 步骤 | 调哪个文件/工具 | 交付物 | 最易踩坑 |
|---|---|---|---|
| 1 生成模板 | `doc_templates_gen.py [--blank] [--t03] [--t04]`（默认 T02） | 母版 HTML | 选错版本（T02/T03/T04） |
| 2 收尾 7 步 | `doc_finish.py --file x.html --doc_id XX --owner XX --scope 机密 --tldr "..." [--gen-codes N]` | 收尾后 HTML | 7 步顺序错、CSS `%` 冲突 |
| 3 导出 | `doc_export.py --file x.html [--pdf] [--docx]` | PDF / DOCX | DOCX 须先剥离 style/script/img |
| 4 台账 | `doc_ledger.py register/list/update/release/retire/export --csv` | 编号 + 台账 | doc_id 不符合规则 |
| 5 审批 | `doc_approval.py submit/review/approve/reject/publish/status` | 审批记录（批准自动盖章） | 未 submit 直接 approve |
| 6 签名 | `doc_sign.py --file --sign 签名.png --role 批准` | 签名后文档 | 签名图非透明 PNG |
| 7 中英对照 | `doc_bilingual.py --file x.html [--model qwen2.5:3b]` | 双语版 | Ollama 未启动 |
| 8 徽章 | `badge_gen.py [--main]` | 圆形徽章 | 配色与品牌视觉冲突 |
| 9 托管 | 乐享 MCP / 手动上传 | 知识库条目 | 目录放错（01 公司治理） |

**收尾 7 步顺序**：① 品牌水印 → ② 三层暗纹 → ③ 受控章（可选）→ ④ AI 友好头 + TL;DR + 权限 → ⑤ 页脚符号徽章条 → ⑥ 动态溯源水印（`?user=&uid=`）→ ⑦ 解锁运行时（试读 / 激活码 / 扫码 / 会员 / 试用 / 考核 / 积分 / AI 计费）。

**流程链路**：`doc_templates_gen → doc_finish → doc_export → doc_ledger → doc_approval → doc_sign → doc_bilingual → 乐享托管`

---

## 六、关键事实速查（官方链接表，标核验时间戳）

| 事实 | 值 | 核验状态 |
|---|---|---|
| MedXpert 官网 | https://medxpert.cn | 待核验（建议发布前复核） |
| 乐享知识库 MedXpert 空间 | 公司知识库「MedXpert」/ 01 公司治理 | 待核验（内部路径） |
| 本地翻译端点 | `http://127.0.0.1:11434/api/chat`（Ollama，零云端） | 本地确定，无需核验 |
| ISO13485 体系文件母版目录 | `D:/Workbuddy/Claw/ISO13485体系文件/母版/文档模板_名片风格/` | 待核验（路径随环境变） |
| 知识库工具脚本目录 | `D:/Workbuddy/Claw/知识库工具/` | 待核验（路径随环境变） |
| 品牌视觉依赖 | medxpert-brand-assets 技能 | 待核验 |
| 打包产物 | `MedXpert_文档模板体系_V2.zip` | 待核验 |
| 归纳文档 | `README_文档模板体系.md` | 待核验 |

> 时间戳说明：本地路径与内部空间名随部署环境变化，发布前请以实际环境复核，统一标「待核验」。

---

## 七、铁律（PROHIBITED）

1. **禁止**把激活码、支付渠道、会员密钥等敏感凭据写进对话或 SKILL.md 正文（须从保险库读取，见「八」）。
2. **禁止**用 `eval()` 执行任何外部传入的字符串。
3. **禁止**对含 CSS 的字符串使用 `%` 格式化。
4. **禁止**把 htmldocx 不支持的内容（base64 图 / `<style>` / `<script>`）直接喂给 DOCX 转换。
5. **禁止**跳过收尾 7 步顺序或遗漏动态溯源水印。
6. **禁止**把本技能产出用于非 MedXpert 品牌的文档美化。
7. **禁止**静默吞掉异常——任何失败必须按「十、错误处理」返回结构化信息。
8. **禁止**硬编码 user/uid 等溯源参数。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

**硬依赖（脚本本体）**
- 8 个 `.py` 脚本须已存在于脚本目录：`doc_templates_gen.py / doc_finish.py / doc_export.py / doc_ledger.py / doc_approval.py / doc_sign.py / doc_bilingual.py / badge_gen.py`。
- 本技能**只编排调用，不内嵌脚本代码**；若脚本缺失，按「十」报 `SCRIPT_MISSING`。

**凭据与配置（不进对话）**
- `ACTIVATION_CODES`、`PAYMENT_CHANNELS`、`MEMBER_TIERS`、`UNLOCK_ALL` 等敏感值：从本地保险库 / 环境变量读取，**绝不**在对话文本或本文件明文出现。
- 品牌视觉（`CN_NAME/EN_NAME/LOGO_IMG/QR_IMG/BADGES`）从 medxpert-brand-assets 技能或配置口读取。

**输入 → 输出映射**
- 输入：HTML 源稿 + 命令行参数 → 输出：收尾 HTML / PDF / DOCX / 台账 CSV / 审批记录 / 签名文档 / 双语版。

---

## 九、示例

**示例 A：完整链路（模板→收尾→导出→台账）**
```bash
# 1 生成 T02 模板
python doc_templates_gen.py
# 2 收尾（7 步注入）
python doc_finish.py --file 手册.html --doc_id QM-2026-001 --owner 张三 --scope 机密 --tldr "质量手册V2" --gen-codes 20
# 3 导出 PDF + DOCX（DOCX 自动剥离 style/script/img）
python doc_export.py --file 手册.html --pdf --docx
# 4 登记台账
python doc_ledger.py register --csv ledger.csv --doc_id QM-2026-001
```

**示例 B：解锁体系配置（改配置口，不动模板）**
```
UNLOCK_ALL / PAYMENT_CHANNELS        # 付费解锁
MEMBER_LEVEL + MEMBER_TIERS + GROWTH_ACTIONS   # 会员 + 成长体系
WECHAT_UNLOCKED + SCAN_QR_IMG        # 关注公众号 / 扫码
ACTIVATION_CODES + --gen-codes        # 激活码
TRIAL_LIMIT / TRIAL_DAYS              # 分级试读 / 限时试用
QUIZ_UNLOCK / POINTS_UNLOCK / AI_METERED   # 考核 / 积分 / AI 计费
WATERMARK_TIERED                      # 水印联动
```

**示例 C：中英对照（本地 Ollama）**
```bash
# 确保 Ollama 已启动，再执行
python doc_bilingual.py --file 手册.html --model qwen2.5:3b
```

---

## 十、错误处理（统一异常模板）

所有失败统一返回以下结构，禁止静默吞错：

```
[MEDXPERT_DOC_ERR]
code: <错误码>
stage: <步骤名, 如 doc_finish/收尾7步>
message: <人类可读中文说明>
fix: <可操作修复建议>
ts: <ISO8601 时间戳>
```

**错误码表**

| 错误码 | 触发条件 | fix |
|---|---|---|
| `SCRIPT_MISSING` | 8 个 `.py` 中任一缺失 | 确认脚本已部署到脚本目录（见「八」） |
| `CSS_FORMAT_ERR` | CSS `%` 被 Python 误解析 | 改用 `str.replace` / `__TOKEN__` 占位符 |
| `DOCX_UNSUPPORTED` | htmldocx 遇 base64/style/script | 转换前 `re.sub` 剥离再导出内容版 |
| `OLLAMA_OFFLINE` | 中英对照时本地服务未起 | 启动 `http://127.0.0.1:11434` 或换 `qwen2.5:7b` |
| `DOC_ID_INVALID` | doc_id 不符编号规则 | 使用 `QM-/QM-P-/T03-/F-/DOC-` 前缀 |
| `APPROVE_ORDER` | 未 submit 直接 approve | 先 `submit` 再 `approve` |
| `CRED_MISSING` | 解锁凭据未从保险库取到 | 从保险库 / 环境变量注入，勿明文 |
| `PATH_SEP` | Windows 反斜杠路径异常 | 统一正斜杠 `D:/...` |

---

## 附：原有效内容保留区（工具链 / 脚本 / 链接）

**工具链清单（8 脚本，均在知识库工具/）**

| 工具 | 命令 | 用途 |
|---|---|---|
| doc_templates_gen.py | `[--blank] [--t03] [--t04]`（默认 T02） | 模板生成（配置驱动，含打印规则） |
| doc_finish.py | `--file x.html --doc_id XX --owner XX --scope 机密 --tldr "..." [--gen-codes N]` | 收尾流水线（7 步注入） |
| doc_export.py | `--file x.html [--pdf] [--docx]` | PDF（Chrome）/ DOCX（htmldocx）导出 |
| doc_ledger.py | `register/list/update/release/retire/export --csv` | 台账 + 编号（QM-/QM-P-/T03-/F-/DOC-） |
| doc_approval.py | `submit/review/approve/reject/publish/status` | 审批流（批准自动盖章） |
| doc_sign.py | `--file --sign 签名.png --role 批准` | 电子签名注入 |
| doc_bilingual.py | `--file x.html [--model qwen2.5:3b]` | 中英对照版（本地 Ollama 翻译） |
| badge_gen.py | `[--main]` | 圆形徽章生成 |

**核心配置口（改脚本顶部，不用动模板）**
`CN_NAME/EN_NAME`、`CN_NAME_COLOR/EN_NAME_COLOR/FONT`、`LOGO_IMG/QR_IMG`、`BADGES/BADGE_BAR_ITEMS/BADGE_LOCK`、`DYNAMIC_WATERMARK_*`、`MEMBER_TIERS/GROWTH_ACTIONS`、`UNLOCK_ALL/PAYMENT_CHANNELS`、`VALID_DATE`

**关联**
- 模板目录：`D:/Workbuddy/Claw/ISO13485体系文件/母版/文档模板_名片风格/`
- 打包：`MedXpert_文档模板体系_V2.zip`
- 乐享：公司知识库「MedXpert」/ 01 公司治理
- 归纳文档：`README_文档模板体系.md`
- 品牌视觉：medxpert-brand-assets 技能

> 版权 MedXpert · 本技能仅编排调用，脚本本体须预先部署。
---

> 治理与溯源：本技能承载 MedXpert「注册老炮」AI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司（MIT 许可）。发声大使：注册老炮@MedXpert。指纹 FP-MX-3A289BF491D2。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；medxpert 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

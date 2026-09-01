---
name: lexiang-knowledge-base
version: 2.1.1
author: 诺源(Arche)@SynomosAI
description: 腾讯乐享知识库 MCP 全功能 Skill——搜索/读取/创建文档/Block 编辑/文件上传下载/连接器导入。当用户提到乐享、知识库、个人知识库、lexiang，或提供 lexiangla.com 链接，或涉及知识库的搜索/写入/编辑/文件/配置操作时使用。
license: MIT
tags: [SynomosAI, Arche, 知识库, MCP, 乐享]
品牌归属: SynomosAI
disable-model-invocation: true
---

# 乐享知识库 MCP Skill

当用户提到「**乐享**」「**知识库**」「**个人知识库**」「**我的知识库**」「**lexiang**」，或提供 `lexiangla.com` 链接，或给出 `space_id`、`entry_id`、`/spaces/`、`/pages/` 等乐享标识时，读取本 Skill。

> 本 Skill 通过 MCP 连接器（mcp.json）调用乐享，所有细节按意图路由到 `references/` 下对应文件，**按需加载、不要一次性全读**。

## 定位

**何时用**：用户要对乐享知识库做搜索/读取、创建文档、编辑已有页面（Block 操作）、上传/下载文件、导入腾讯会议、配置连接器或排查 401/连接问题。

**何时不用**：
1. 非乐享/知识库相关任务。
2. 用户只模糊提到"知识库"但无乐享标识且未要求操作乐享——先确认平台。
3. 平台词 + 内容词同时出现但用户未要求检索——按强制检索规则必须先检索（见七·5）。

## 一、能力边界（In/Out scope）

**本技能做（In）**
1. 搜索/查找/阅读/浏览乐享知识库内容。
2. 创建文档、写入/保存/导入内容。
3. 编辑已有页面的 Block 级增删改移。
4. 上传/下载二进制文件（PDF/Word/图片等）。
5. 导入腾讯会议录制、连接器接入。
6. 配置乐享连接器、排查 401/连接故障。

**本技能不做（Out / 明确禁止）**
1. ❌ 禁止遍历团队/知识库列表后自行选择写入目标。
2. ❌ 禁止根据名称"看起来合适"就决定写入。
3. ❌ 禁止在未确认时执行写入。
4. ❌ 禁止用 MCP endpoint 拼接用户链接（必须用 `whoami()` 返回的 `company.company_domain`）。
5. ❌ 禁止把 `company_from` 拼成子域名（只能作 `?company_from=xxx` 参数）。
6. ❌ 禁止大批量（>20 个）一次性提交（须分批 ≤20）。

## 二、输入约束与输出承诺

**推荐问法**
- 「在乐享知识库搜索关于 OKR 的文档」
- 「新建一篇乐享文档 / 保存到我的知识库」
- 「修改 /pages/xxx 这个页面，加个标题」
- 「传个 PDF 到乐享 / 下载这个文件」
- 「token 过期连不上了，帮我配置一下」

**字段引导**
| 要素 | 是否必填 | 说明 |
|---|---|---|
| 操作意图 | 必填 | 搜索/写入/编辑/文件/配置（决定加载哪个 references 文件） |
| 目标标识 | 条件 | 用户明确提供的 URL/ID/名称（写入必须基于它，禁止猜测） |
| 批量数量 | 条件 | >20 必须分批并告知策略 |

**输出承诺**
- 返回链接统一用 `whoami().company.company_domain` 生成的规范格式（见六）。
- 写入/编辑前必基于用户明确目标并确认；大批量操作先告知数量与分批策略。
- 401/连接失败立即引导续期/重配置，不盲目重试。

## 三、触发场景

| 用户意图 | 应加载 references | 典型触发词 |
|---|---|---|
| 配置乐享 / 401 错误 / Token 过期 | `references/setup.md` | 「配置乐享」「token 过期」「连不上」「401」 |
| 搜索 / 查找 / 阅读 / 浏览 | `references/search.md` | 「找一下」「搜索」「读一下这个页面」「打开链接」 |
| 创建文档 / 写入 / 保存 / 导入 | `references/writer.md` | 「写到乐享」「创建文档」「保存到知识库」「导入」 |
| 编辑已有页面 / Block 操作 | `references/blocks.md` | 「修改这个页面」「加个标题」「删掉这段」 |
| 上传/下载文件（PDF/Word/图片） | `references/files.md` | 「传个 PDF」「上传文件」「下载这个文件」 |
| 导入腾讯会议 | `references/connectors.md` | 「把会议录制导入」「导入会议录制」 |
| 数据模型 / URL 规则 / 完整安全规则 | `references/base.md` | 由上述模块内部引用 |

**易混淆场景速判**
| 场景 | 正确模块 |
|---|---|
| `/pages/xxx` + 要求"加内容/修改" | `references/blocks.md`（操作已有页面） |
| `/spaces/xxx` + 要求"写入/创建" | `references/writer.md`（知识库下新建文档） |
| `/pages/xxx` + 仅要求"读/总结" | `references/search.md`（只读） |
| 上传 PDF/Word/图片 | `references/files.md`（二进制） |
| 创建 Markdown 文本文档 | `references/writer.md`（文本） |
| 「乐享里有一篇关于 X 的文档」 | `references/search.md` → **必须先检索** |
| 「看看乐享里 XX 的写作风格」 | `references/search.md` → **必须先读取内容** |
| 「分析我知识库里关于 X 的内容」 | `references/search.md` → **必须先检索** |

**跨模块任务顺序**
- 搜索后写入：先 `search.md` → 再 `writer.md`
- 读取后编辑：先 `search.md` → 再 `blocks.md`
- 上传后记录：先 `files.md` → 再 `writer.md`
- 生成内容+保存：先生成内容，再 `writer.md`；未指定目标默认写入个人知识库

## 四、常见错误与反模式

**FAQ · 反模式（先写✗再写✓）**
- ✗ 反模式：拿到"把所有知识库内容整理一下"就遍历团队列表挑一个写入。
  ✓ 替代：写入必须基于用户明确提供的目标（URL/ID/名称），禁止遍历/猜测；未确认不写入。
- ✗ 反模式：收到"乐享里关于 X 的文档怎么样"就凭记忆/泛知识直接回答。
  ✓ 替代：强制先调用 `search_kb_search` / `search_kb_embedding_search` 获取实际内容，再分析。
- ✗ 反模式：用 MCP endpoint 域名拼接用户分享链接。
  ✓ 替代：链接一律用 `whoami().company.company_domain` 生成；`company_from` 只作 `?company_from=xxx` 参数。
- ✗ 反模式：一次提交 50 个文件导致 token 超限/超时。
  ✓ 替代：>20 个必须分批（每批 ≤20），操作前告知数量与策略。
- ✗ 反模式：401 后疯狂重试。
  ✓ 替代：立即停止重试，读取 `setup.md` 引导续期/重配置。

**高频 Q&A**
- Q：写入前一定要确认目标吗？A：是。必须基于用户明确提供的 URL/ID/名称，禁止自行遍历或按名称猜测。
- Q：链接怎么生成才对？A：用 `whoami()` 的 `company.company_domain`；含三级域名用 `{domain}/pages/{entry_id}`，顶级域名追加 `?company_from={company_from}`。
- Q：大批量文件怎么处理？A：>20 个分批 ≤20，操作前告知用户数量与策略。
- Q：401/连不上怎么办？A：停止重试，读 `setup.md` 引导重新授权（内置连接器点续期；其他平台引导续期）。
- Q：常见错误去哪查？A：见 `references/common-errors.md`（高频错误速查表：文件上传缺 size、更新文件参数混淆等）。

## 五、标准 SOP

| 步 | 动作 | 产物 | 易踩坑 |
|---|---|---|---|
| 1 | 凭证检查：调用 `whoami()` 确认 MCP 已连接 | 用户信息/401 信号 | 未连就操作 |
| 2 | 意图路由：按三的表 Read 对应 references 文件 | 模块指引 | 加载错模块 |
| 3 | 强制检索（平台词+内容词）：先 `search_kb_search`/`search_kb_embedding_search` | 实际内容 | 凭空分析（违反七·5） |
| 4 | 执行操作（搜索/写入/编辑/文件）；写入须基于用户明确目标 | 结果/链接 | 猜测写入目标 |
| 5 | 大批量（>20）分批 ≤20，操作前告知策略 | 分批回执 | 一次性提交超限 |
| 6 | 返回规范链接 + 回执；401 即转 setup 引导 | 链接/回执 | endpoint 拼链接 |

## 六、关键事实速查

**链接生成规则**
| `company.company_domain` 类型 | 链接格式 | 示例 |
|---|---|---|
| 含三级域名（如 `csig.lexiangla.com`） | `{domain}/pages/{entry_id}` | `https://csig.lexiangla.com/pages/abc` |
| 顶级域名（如 `lexiangla.com`） | `{domain}/pages/{entry_id}?company_from={company_from}` | `https://lexiangla.com/pages/abc?company_from=csig` |

- `company_from` 获取优先级：① mcp.json `url` 中的 `company_from` 参数 ② 若无则用 `whoami().company.code`。
- 写入安全红线：🚫 禁止遍历后自选目标、🚫 禁止按名称猜测、🚫 禁止未确认写入（完整规则见 `references/base.md`）。
- 重试/超时（files.md）：连接层静默重连；批量操作超时等待 3 秒、单文件重试 2 次。
- 参考文件完整索引见八；高频错误速查见 `references/common-errors.md`。

## 七、铁律（PROHIBITED 绝对禁止 / MANDATORY RULES）

1. **401/连接断开**：立即停止重试，读取 `references/setup.md`；内置连接器平台引导重新授权，其他平台引导续期。
2. **写入必须基于用户明确提供的目标**（URL/ID/名称确认），**禁止**自行遍历或猜测目标。
3. **链接生成**必须使用 `whoami()` 返回的 `company.company_domain`，**禁止**用 MCP endpoint 拼接用户链接。
4. **`company_from`** 不能拼接为子域名，只能作 `?company_from=xxx` 查询参数。
5. **强制检索**：用户消息同时含「乐享/知识库」等平台词 + 「文档/论文/文章/内容/资料/笔记/之前写的/上次的/风格」等内容词时，**必须先调用 `search_kb_search` 或 `search_kb_embedding_search` 获取实际内容**，不得凭空分析或直接生成回答。
6. **大批量保护**：文件/条目数量 > 20 个时，**必须分批执行**（每批 ≤ 20 个）；操作前告知用户数量和策略，禁止一次性提交导致 token 超限。

## 八、输入输出依赖

- **MCP 连接器**：`mcp.json` 声明 `lexiang` MCP（streamable-http），`url` 含 `company_from` 参数，`headers.Authorization: Bearer ${LEXIANG_TOKEN}`。
- **凭据管理**：Token 由连接器配置注入（`${LEXIANG_TOKEN}`），**一律从本地保险库 `~/.ucvault_local` 读取或经连接器平台托管，绝不进对话/代码/日志**。401 续期走平台 OAuth/续期流程（见 `references/setup.md`）。
- **凭证检查**：执行任何乐享操作前用 `whoami()` 确认连接；401→读 `setup.md` 引导续期；连接失败→读 `setup.md` 引导初始配置。
- **参考文件索引（按需 Read）**

| 文件 | 职责 |
|---|---|
| `references/setup.md` | Token 配置、续期、OAuth、故障排查 |
| `references/search.md` | 关键词/语义搜索、内容读取、目录浏览 |
| `references/writer.md` | 新建文档、导入内容、公众号收藏 |
| `references/blocks.md` | 已有页面 Block 级增删改移 |
| `references/files.md` | 二进制文件上传/下载（三步流程） |
| `references/connectors.md` | 腾讯会议录制导入 |
| `references/base.md` | 数据模型、完整安全规则、Block 结构、工具发现 |
| `references/index.md` | 完整索引 + 按场景推荐加载顺序 |

补充参考：`references/block-schema.md`、`mcp-examples.md`、`markdown-to-block.md`、`block-update.md`、`content-reorganize.md`、`folder-sync.md`、`markdown-import.md`、`common-errors.md`、`doc-templates.md`、`theme-config.md`、`skill-maintenance.md`。

- **scripts（辅助，可选）**：`scripts/sync-folder.ts`（文件夹同步）、`scripts/upload-files.py`、`scripts/test_upload_files.py`、`scripts/README.md`。执行脚本前同样遵守大批量保护与凭据不落日志规则。

## 九、示例

**示例一：搜索后写入（跨模块）**
> 问题：在乐享里搜一下"OKR 实践"，把找到的要点整理成一篇新文档存到我的知识库。
> 加载：三（search→writer）→ 八 setup 检查连接 → `search.md` 先检索 → `writer.md` 基于用户明确目标新建文档。
> 答案框架：返回新文档规范链接（`company_domain/pages/{entry_id}`）+ 写入回执；未指定知识库默认写入个人知识库。

**示例二：编辑已有页面（Block）**
> 问题：把 /pages/abc123 这个页面里"第一章"下面加一段说明。
> 加载：三（blocks）→ `blocks.md` 操作已有页面；先 `search.md` 读取确认内容。
> 答案框架：返回更新后页面规范链接 + 变更说明。

**示例三：大批量上传**
> 问题：把这 35 个 PDF 传到乐享。
> 加载：七·6 + `files.md` → 分两批（20+15），操作前告知数量与策略。
> 答案框架：分批回执 + 各文件规范链接；单文件失败重试 2 次、超时等待 3 秒。

**示例四：401 处理**
> 问题：连乐享提示 401。
> 加载：七·1 + `setup.md` → 停止重试，引导续期（内置连接器点续期按钮；其他平台引导续期）。
> 答案框架：给出续期/重配置步骤，不盲目重试。

## 十、错误处理

| 错误码 | 现象 | 原因 | 修正引导 |
|---|---|---|---|
| E401 | `whoami()` 返回 401 / 连接断开 | Token 过期或未配置 | 停止重试，读 `references/setup.md` 引导续期/重配置 |
| E402 | 写入目标不明确 | 未提供 URL/ID/名称 | 向用户索取明确目标，禁止遍历/猜测（七·2） |
| E403 | 链接域名异常/参数错误 | 用 endpoint 拼接或 company_from 拼子域 | 改用 `whoami().company.company_domain` + `?company_from=`（七·3/4） |
| E404 | 凭空回答无检索 | 违反强制检索 | 先 `search_kb_search`/`search_kb_embedding_search` 取实际内容（七·5） |
| E405 | token 超限/超时 | 批量 >20 一次性提交 | 分批 ≤20，操作前告知策略（七·6）；files.md 单文件重试2次/等待3秒 |
| E406 | 文件上传缺 size / 参数混淆 | 入参不规范 | 查 `references/common-errors.md` 高频错误速查表修正 |

> 高频错误与修复详见 `references/common-errors.md`；连接层静默重连机制见 `references/files.md`/`setup.md`。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺源(Arche)@SynomosAI。指纹 FP-MX-20A74CD59C03。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

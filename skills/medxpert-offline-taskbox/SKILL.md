---
name: medxpert-offline-taskbox
title: MedXpert 跨机任务箱·低配省算力
slug: medxpert-offline-taskbox
displayName: MedXpert 跨机任务箱·低配省算力
version: 2.4.1
category: 办公效率
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
agent_created: true
author: 注册老炮@MedXpert
品牌归属: MedXpert
license: MIT
description: AI 任务太烧钱？低配电脑也能跑大模型——白天派活，晚上回家让本地模型免费跑完，断网也不停。MedXpert 跨机任务箱：WorkBuddy×DSH（DeepSeek Harness）×本地 Ollama 三级协同，批量/重复/文档/敏感任务零云端消耗，复杂推理才上云端。L1-L5 分级路由已代码级实现（add 自动打标 + route 查询）、失败自动重试、同步包双机合并、防僵尸续跑，纯 Python 零依赖即下即用，旧电脑也能当执行节点。模型 API 涨价？跟它无关。省积分、断网续跑、离线任务队列、任务路由与成本控制都找它。
description_en: "AI API costs burning you? Run LLMs on low-spec machines — dispatch tasks by day, local models finish them for free at night, even offline. MedXpert Cross-Machine Taskbox: WorkBuddy x DSH (DeepSeek Harness) x local Ollama three-tier collaboration. Batch/repeat/document/sensitive tasks cost zero cloud credits; only complex reasoning goes to the cloud. L1-L5 tiered routing (code-level: add auto-tags + route query), auto-retry on failure, sync-package merge across two machines, zombie-proof resume. Pure Python, zero dependencies, run as-is — old PCs can be execution nodes. API price hikes? Not your problem. Keywords: 跨机任务箱, 断网续跑, 离线任务队列, Ollama, 省算力, 任务路由, 低配电脑跑大模型"
tags: [跨机协作, 离线, ollama, 任务队列, 自动化, 省算力, dsh, deepseek, 低配, 轻量, medxpert]
---

# MedXpert 跨机任务箱 · 断网闭环 + 省算力路由

> 本文档中的「机器 A」指白天操作端（如办公室电脑），「机器 B」指执行端（如家用电脑）。可自由替换为任意两台设备。中文编写，面向中国用户与国内网络环境（WorkBuddy 生态），无需翻墙即可使用。

## 定位

**何时用**
- 白天派活、晚上回家让本地模型免费跑完，断网也不停。
- 批量/重复/文档/敏感任务想零云端消耗，复杂推理才上云端。
- 低配/旧电脑当执行节点，跑量化小模型（Q4）参与；省积分/省算力/成本控制。
- 用户提到：任务箱 / 跨机任务 / 离线任务 / 断网跑任务 / 任务队列 / 省积分 / 本地大模型 / Ollama / 双机同步 / 断网续跑 / 失败重试 / L1-L5。

**何时不用**
- 复杂推理/高质量写作（L4/L5）——本技能只管路由与本地执行，重要决策仍走云端好模型或你本人判断。
- 把 DSH 当生产环境唯一保障——DSH 为 v0.1 开发者预览版，官方声明「会有破坏性变更」，生产慎用。
- 期望路由 100% 精准——分级是启发式关键词匹配，重要任务请用 `--level` 手动指定。

## 一、能力边界（In/Out scope）

**本技能做（In）**
- 本地 JSON 任务箱（状态机 + L1-L5 自动路由 + 同步包 export/import 双机合并）。
- 断网执行 Worker（失败自动重试 + 级别过滤 + 防僵尸续跑）。
- 三级协同编排说明（WorkBuddy 调度 × DSH 执行层 × 本地 Ollama 推理）。
- 三条通道自适应（实时直连 / 云文档信箱 / 断网兜底）。
- DSH 对接本地 Ollama 的操作指引（可选执行层）。

**本技能不做（Out，N 条）**
1. 不做复杂推理本身——L4/L5 由云端好模型或你本人完成，本技能只路由与跑本地级。
2. 不保证 L1-L5 路由 100% 精准——ROUTE_RULES 是启发式关键词匹配，误判需手动 `--level` 覆盖。
3. 不处理任何密钥/Token——同步包不含密钥，任务详情禁止写密码/token。
4. 不提供 DSH 生产级稳定性保障——v0.1 预览版，迭代快、会有破坏性变更。
5. 不替代模型本身——推理质量取决于你本地部署的 Ollama 模型权重。
6. 不做法律意见——医疗/NDA/客户任务的合规边界由你把控，本技能仅保证数据不出门（本地执行）。
7. 不在断网前自动拉模型权重——需你提前 `ollama pull` 好目标模型。

## 二、输入约束与输出承诺

**推荐问法**
- "白天派活、晚上断网让本地模型跑整理任务，怎么弄？"
- "这个任务会被路由到哪一级？怎么手动改级别？"
- "Worker 调模型失败会卡住吗？"
- "两台机器怎么合并任务不冲突？"

**输入字段引导（任务卡协议）**
- 任务卡字段：任务ID | 标题 | 详情 | 优先级 | 状态(queued/running/done/failed) | 来源 | 创建/更新时间 | 结果。
- **标题**：≤100 字，一句话说清目标（如"整理出差清单"），别用"帮我看看"模糊标题。
- **详情**：≤5000 字，背景/约束/期望输出各一句，模型才贴合需求。
- **优先级**：1–9（越大越先跑），急事 7–9，普通 5，超范围报错。
- **敏感内容**：密码/token 一律不进任务详情；批量任务逐个 `add` 即可。
- **级别覆盖**：`add ... --level L2` 可强制指定（标题关键词误判时）。

**输出承诺**
- Worker 结果强制「【结论】+分点+【下一步】」结构（≤300 字）。
- 失败任务 `result` 字段以 `[调用失败]` 开头标明原因。
- `route` 子命令给出级别分布总览与单任务级别说明。
- 同步包按任务 ID 去重、保留 updated_at 较新者，双机互不覆盖。

## 三、触发场景

| 用户意图 | 触发词 | 应加载章节 |
|---|---|---|
| 派活/离线跑 | 任务箱、跨机任务、离线任务、断网跑任务、任务队列 | 五（SOP）、七（通道 C）、九（示例） |
| 省算力 | 省积分、省算力、低配电脑跑模型、白天派活晚上跑 | 六（分级表）、一（边界） |
| 本地模型 | 本地大模型、Ollama、本地推理、数据不出门、敏感任务本地 | 二（输入）、七（铁律） |
| 路由/分级 | 任务路由、L1-L5、任务分级、失败重试 | 六（路由规则）、四（反模式）、十（错误处理） |
| 双机同步 | 双机同步、同步包、断网续跑、taskbox | 七（通道 C）、八（依赖）、十（错误处理） |

**示例对话 1**
> 用户：白天攒了一堆法规资料，晚上想让本地模型断网整理。
> 加载：第二章输入引导（逐条 `add`，标题+详情+来源）→ 第六章 L1 路由（批量/文档/敏感自动本地）→ 第五章 SOP（机器 B `offline_worker.py` 断网跑）→ 第九章示例。

**示例对话 2**
> 用户：这个"评估欧盟MDR合规差距"任务会被分到哪一级？
> 加载：第六章分级规则表（命中"评估/合规"→L4 云端）→ 第二章 `--level` 覆盖说明。

## 四、常见错误与反模式

**FAQ 结构化（每条先反模式 ✗，再替代方案 ✓）**

✗ 反模式：任务详情写密码/token。
✓ 替代方案：敏感凭证一律不进任务详情；同步包本身不含任何密钥（见第七章铁律）。

✗ 反模式：两台机器直接共享同一 taskbox.json 并发写。
✓ 替代方案：各自维护独立任务箱 → `export`/`import` 同步包交换；同一文件并发写会重复处理/冲突。

✗ 反模式：期望 L1-L5 路由 100% 精准。
✓ 替代方案：ROUTE_RULES 是启发式关键词匹配，有误判可能；重要任务用 `add --level L4` 手动指定最稳（见第六章）。

✗ 反模式：把 Ollama 直曝公网（设 `OLLAMA_HOST=0.0.0.0` 又不开 VPN）。
✓ 替代方案：Ollama 无鉴权，仅限可信内网；跨机用 Tailscale/WireGuard 组私网填 tailnet IP，切勿直曝公网（见第八章）。

✗ 反模式：断网前没 `ollama pull` 模型权重。
✓ 替代方案：断网前先 `ollama pull qwen2.5:7b`（或 deepseek-r1:8b）把模型拉好，否则本地无权重可跑。

✗ 反模式：让本地小模型硬啃 L4 复杂任务。
✓ 替代方案：本地 7B/8B 只干中低难度活，复杂活用 L4/L5 规则兜住（云端好模型或你本人）。

**高频 Q&A**
- Q：Worker 调用模型失败会卡住吗？A：不会。默认重试 2 次（指数退避 2s→4s），`--retry N` 可调；耗尽标记 failed，结果写 `[调用失败] 原因`，修正后重跑。
- Q：断电/断网任务会丢吗？A：不会。先写盘（taskbox.json）再执行；running 超 60 分钟自动重置 queued 续跑；重启后重跑 `offline_worker.py`。
- Q：导入别人同步包会搞乱自己任务吗？A：不会。按 id 去重，只合并对方更新过（updated_at 较新）的任务，本地更新者保持不动。
- Q：taskbox.json 弄坏了？A：程序提示损坏并退出（不静默清空），用最近同步包 `import` 重建。

## 五、标准 SOP

**快速上手（三步，不许跳步）**

| 步 | 动作 | 产物 | 易踩坑 |
|---|---|---|---|
| 1 装环境 | 机器 B 装 Ollama，断网前 `ollama pull qwen2.5:7b`（或 deepseek-r1:8b） | 本地模型权重就位 | 断网后无权重可跑 |
| 2 跑最小闭环 | 机器 A `add` → `export` 同步包 → 机器 B `import` → `offline_worker.py --model ...` → `export` 带回 → 机器 A `import` 收结果 | 端到端跑通 | L2/L3/L4 云端任务留本地等联网 |
| 3 上规模 | 接云文档队列（通道 B）或 DSH 执行层（第八章），配定时自动化（第九章清单） | 常态化离线队列 | 并发写同一 taskbox.json 会冲突 |

**通道 C 断网执行完整流程（核心文件本 skill 目录）**
- `local_taskbox.py`：本地 JSON 任务箱，状态机(待处理/进行中/已完成/失败) + **L1-L5 自动路由**（add 打标、route 查询）+ 同步包 export/import（按 id 去重、保留 updated_at 较新者）。纯标准库，断网可跑。
- `offline_worker.py`：读本地待办 → 逐条调本机 Ollama → 结果写回；**失败自动重试（指数退避）+ 级别过滤（默认只跑 L1）+ 防僵尸续跑**（running 超 60 分钟自动重置）。

**用法**
```bash
python local_taskbox.py add "标题" "详情" --source a            # 自动路由打 L1-L5 标签
python local_taskbox.py add "整理FDA收费" "…" --level L1        # 手动指定级别
python local_taskbox.py list                                   # 全部任务（含级别列）
python local_taskbox.py route                                  # 级别分布总览
python local_taskbox.py route 3                                # 单任务级别说明
python local_taskbox.py done <id> "结果"     # 手动标记完成
python local_taskbox.py fail <id> "原因"     # 手动标记失败
python local_taskbox.py delete <id>          # 删除任务
python local_taskbox.py export sync_out.json
python local_taskbox.py import sync_out.json
python offline_worker.py --model qwen2.5:7b                     # 默认只跑 L1 本地级
python offline_worker.py --level all --retry 3                  # 全部级别 + 最多重试 3 次
```

**典型场景：晚上让本地大模型整理知识图书馆**
1. 白天（机器 A）：待整理素材逐个 `add`（标题+详情+来源），批量/文档/敏感自动路由 L1。
2. 晚上（机器 B）：断网跑 `offline_worker.py`——本地模型逐条生成摘要、按生命周期 7 阶段归类打标。
3. 早上（机器 A）：`import` 回收结果 → 人工复核 → 归档入库。
> 示例写法：`python local_taskbox.py add "整理FDA指南更新" "5 份 2026 年新指南，每份出 200 字摘要并按 7 阶段打标" --priority 5 --source a` → 自动路由 L1。

## 六、关键事实速查

**三级协同定位**
| 层级 | 角色 | 干什么 |
|------|------|--------|
| WorkBuddy（云端/机器 A）| 总调度 | 接用户派活 → 生成任务卡 → 投递队列；取回结果 → 校验 → 交付；复杂推理兜底（L4/L5） |
| DSH（DeepSeek Harness）| 执行层 | 从队列取任务 → 编排工具/会话/调度/轨迹 → 调推理层 → 结果写回 |
| 本地大模型（Ollama）| 推理层 | 批量/重复/文档/敏感任务推理：0 成本、断网可用、数据不出门 |

**省算力路由规则（核心，代码级内置）**
| 级别 | 任务类型 | 示例 | 路由 | 云端消耗 |
|------|----------|------|------|----------|
| L1 本地 | 批量/重复/文档/敏感 | 知识库精读、摘要、格式转换、脚本、NDA/客户资料 | 机器 B 本地 Ollama | 0 |
| L2 云端 | 联网检索/资讯 | AI 日报、查资料、新闻 | 云端 | 少 |
| L3 云端 | 生图/视频 | 封面、视频 | 云端 | 多 |
| L4 云端 | 复杂推理/高质量写作 | 法规分析、方案设计、正式文档 | 云端好模型 | 该花则花 |
| L5 试跑 | 中难度推理 | 先本地小模型试，不行再云端 | 本地→云端降级 | 0→少 |

- 优先级 8-9 自动升 L4（重要决策先给好模型）、1-3 自动落 L1。
- 敏感/NDA/客户资料优先本地（数据不出门，顺带合规）。
- 手动覆盖：`add ... --level L2` 可强制指定级别。

**分级规则表（ROUTE_RULES，可按团队习惯增删）**
| 级别 | 命中关键词（示例） | 路由 |
|------|--------------------|------|
| L1 本地 | 批量/重复/文档/整理/汇总/翻译/摘要/格式转换/脚本/NDA/客户/敏感/清单 | 本地 Ollama |
| L2 云端检索 | 查/搜索/新闻/资讯/日报/检索/最新/行情 | 云端 |
| L3 云端生图 | 图片/封面/海报/视频/logo/头像/配图 | 云端 |
| L4 云端复杂 | 分析/方案/评估/报告/规划/策略/合规/风险/决策 | 云端好模型 |
| L5 试跑降级 | 总结/改写/润色/起草/初稿/大纲 | 本地→云端 |

**最低配置参考（按机器选模型，标「待核验」）**
- 纯 CPU/核显（8GB 内存）：可跑 3B 量化（慢但能用），适合简单批量。
- 8GB 显存独显 / 16–32GB 内存：7B-8B Q4 约 20-30 tok/s（甜点档，推荐）。
- 更高配置：14B+ 或直接走云端 L4/L5。
- Ollama 支持 CPU-only 运行，没独显也能跑，只是慢。

**官方链接（待核验）**：DSH 官网 `deepseek.com/harness` 或 GitHub `deepseek-ai/deepseek-harness`（`github.com/deepseek-ai/deepseek-harness` · `deepseek-harness.github.io`）；DSH 为 v0.1 预览版、迭代快，对接细节一律以官方最新文档为准。

## 七、铁律（PROHIBITED 绝对禁止项）

1. **禁止任务详情写密码/token**——敏感凭证一律不进任务箱；同步包本身不含任何密钥。
2. **禁止并发写同一 taskbox.json**——两台机器各自维护独立任务箱，靠 export/import 同步包合并，互不覆盖。
3. **禁止 Ollama 直曝公网**——`OLLAMA_HOST=0.0.0.0` 仅限可信内网；跨机用 Tailscale/WireGuard，切勿直曝。
4. **禁止重要任务不手动 `--level`**——路由是启发式，拿不准的升级 L4 求稳。
5. **禁止断网前未 `ollama pull` 模型权重**——否则本地无权重可跑。
6. **禁止把 DSH 预览版当生产唯一保障**——v0.1 开发者预览，官方声明会有破坏性变更。
7. **禁止本地小模型硬啃 L4 复杂任务**——质量打折，用 L4/L5 规则兜住（云端或你本人）。

## 八、输入输出依赖

**依赖文件（本 skill 目录）**
- `local_taskbox.py`：本地 JSON 任务箱（状态机 + L1-L5 路由 + 同步包）。
- `offline_worker.py`：断网执行 Worker（重试 + 级别过滤 + 防僵尸）。
- `taskbox.json`：任务箱数据文件，与脚本同目录，纯文本 JSON，可直接查看/备份。

**依赖工具/运行时**
- 本地推理：**Ollama**（断网前 `ollama pull` 好目标模型；OpenAI 兼容端点 `http://127.0.0.1:11434/v1`）。
- 可选执行层：**DSH（DeepSeek Harness）**——`npx @deepseek-ai/dsh web`（需 Node.js ≥22.19），浏览器开 `http://127.0.0.1:3080`；设置→模型→添加自定义提供方 `ollama-local`，API 地址 `http://127.0.0.1:11434/v1`，API 协议 `openai-completions`，API 密钥任意占位符（Ollama 不校验但 DSH 要求非空）。
- 通道 B（可选）：云文档智能表格（乐享/金山），字段 `任务ID|标题|详情|状态|结果摘要|创建时间|心跳|重试次数`。
- 跨机（局域网/外网）：Ollama 设 `OLLAMA_HOST=0.0.0.0`，DSH 填 `http://<局域网IP>:11434/v1`（仅限可信内网）；外网用 Tailscale/WireGuard 组私网。

**凭据红线（强制）**
- 云文档队列（通道 B）需平台凭证（乐享/金山）——从保险库 `~/.ucvault_local` 读取，**绝不**进对话 / 代码 / 日志 / 回复；不打印明文、不写文件。
- 同步包不含任何密钥；任务详情禁写密码/token（见第七章铁律第 1 条）。
- Ollama 仅监听 127.0.0.1（或可信内网），不直曝公网。

## 九、示例

**示例 1：断网闭环整理（完整流程）**
> 问题：白天攒了法规资料，晚上断网让本地模型整理。
> 加载：第二章输入引导（逐条 `add`）→ 第六章 L1 路由 → 第五章 SOP（机器 B `import` → `offline_worker.py --model qwen2.5:7b`）→ 机器 A `import result.json` 收结果。
> 答案框架：
> ```
> 机器 A：$ python local_taskbox.py add "整理出差清单" "护照、转换插头、名片" --priority 7
> 已添加任务 #1：整理出差清单（路由 L1）
> 机器 B：$ python offline_worker.py --model qwen2.5:7b
> == 处理 #1 [L1]：整理出差清单
> == 完成 #1，结果长度 128
> 机器 A：$ python local_taskbox.py import result.json
> [1] done  P7 L1 整理出差清单 (a)
> ```

**示例 2：路由查询**
> 问题：看看当前任务箱都被分到哪一级？
> 加载：第六章分级规则表 → 第二章 `route` 说明。
> 答案框架：`python local_taskbox.py route` 给级别分布总览；`route <id>` 给单任务级别与含义；优先级 8-9 自动 L4、1-3 自动 L1。

**示例 3：DSH 对接本地 Ollama**
> 问题：想用 DSH 编排、Ollama 推理，怎么接？
> 加载：第八章依赖（DSH 启动 + 自定义提供方）→ 第六章三级协同。
> 答案框架：`npx @deepseek-ai/dsh web` → 设置→模型→添加 `ollama-local`（API 地址 `http://127.0.0.1:11434/v1`）→ 任务箱存任务、DSH 编排、Ollama 推理，0 API 成本、断网可跑。

## 十、错误处理

| 错误码 | 现象 | 原因 | 修正引导 |
|---|---|---|---|
| E01 模型调用失败 | Worker 卡住？/标记 failed | 模型未装或名字错、Ollama 未起 | 不会卡死；默认重试 2 次（指数退避），耗尽标 failed 写 `[调用失败]` 原因；`--model` 换模型重跑 |
| E02 断电/断网任务丢失 | 担心任务没了 | 误以为未落盘 | 任务先写盘（taskbox.json）再执行；running 超 60 分钟自动重置 queued 续跑；重启重跑 `offline_worker.py` |
| E03 两 Worker 重复处理 | 同一任务被跑两次 | 并发写同一 taskbox.json | 两台机器各用独立任务箱，再 export/import 同步包合并，不共享同一文件 |
| E04 导入同步包覆盖自己任务 | 担心被冲掉 | 误以为整体覆盖 | 按 id 去重，只合并对方 updated_at 较新者，本地更新者保持不动 |
| E05 taskbox.json 损坏 | 程序报错退出 | 文件被手改坏 | 程序提示损坏并退出（不静默清空）；用最近同步包 `import` 重建，养成每次 export 留备份 |
| E06 路由误判 | 重要任务被分到本地 L1 | ROUTE_RULES 启发式漏匹配 | `add ... --level L4` 手动覆盖；拿不准升级 L4 求稳 |
| E07 Ollama 连不上 | DSH/Worker 调不通 | 权重未 pull 或 `OLLAMA_HOST` 配错 | 断网前 `ollama pull`；跨机设 `OLLAMA_HOST=0.0.0.0` + Tailscale，勿直曝公网 |
---

> 治理与溯源：本技能承载 MedXpert「注册老炮」AI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司（MIT 许可）。发声大使：注册老炮@MedXpert。指纹 FP-MX-CE29CD564BCF。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；medxpert 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

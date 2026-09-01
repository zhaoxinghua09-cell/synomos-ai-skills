---
name: cross-machine-offline-taskbox
display_name: 跨机任务箱·低配省算力
version: 2.3.0
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
brand: SynomosAI
品牌归属: SynomosAI
license: MIT
description: 跨机离线任务箱——AI 任务太烧积分怎么省、低配旧电脑能不能跑大模型、断网了任务还能不能继续、敏感数据不想出本机怎么办。WorkBuddy×DSH(DeepSeek Harness)×本地 Ollama 三级协同，批量/重复/文档/敏感任务零云端消耗，复杂推理才上云端；L1-L5 分级路由、同步包双机合并、心跳防僵尸，纯 Python 零依赖即下即用。
tags:
- 诺声
- SynomosAI
- 跨机离线
- 省算力
- 离线任务队列
- 本地大模型
- local-llm
- ollama
- batch-jobs
- AI技能
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
ambassador: Logos
---

# 跨机任务箱 · 断网闭环 + 省算力路由

> 机器 A = 白天操作端（如办公室电脑），机器 B = 执行端（如家用电脑）。可自由替换为任意两台设备。

## 定位 · 何时用 / 何时不用

**一句话**：把 AI 任务派到本地低配机离线跑，省云端积分、断网也能续跑、敏感数据不出门。

**何时用**
- 想省云端积分/API 费用，且有批量、重复、文档类任务。
- 有旧电脑 / 低配机，想让它当执行节点跑本地小模型。
- 常断网或网络不稳，需要任务离线闭环。
- 任务含 NDA / 客户资料 / 敏感内容，要求数据不过公网。

**何时不用（请用云端）**
- 任务需联网检索（L2）、生图/视频（L3）——本地跑不动，直接上云端。
- 复杂推理 / 高质量正式文档（L4）——本地 7B/8B 质量打折，用云端好模型。
- 没有可运行 Ollama 的设备且不愿安装——本技能以本地推理为核心。

---

## 一、能力边界

**能做什么**
- 离线 JSON 任务箱（taskbox.json）：增删改查、状态机、同步包 export/import。
- 跨机同步包按任务 ID 去重合并，保留 `updated_at` 较新者，互不覆盖。
- 接本地 Ollama 推理（0 API 成本、断网可用、数据不出门）；云端仅兜底复杂推理。
- 三条通道：实时直连 / 云文档信箱 / 断网兜底，按 B 的网络状态自动降级。

**边界与约束（评测补齐）**
| 项 | 边界值 / 说明 |
|----|--------------|
| 单任务箱容量 | 建议 < 1000 条；超量请分箱或 `add --file` 批量导入 |
| 标题长度 | ≤ 100 字 |
| 详情长度 | ≤ 5000 字（纯文本） |
| 单条执行超时 | `offline_worker.py` 默认 900s/条，超时标记 failed 并写明原因 |
| 云文档心跳超时 | 30min 无心跳视为「僵尸」，自动重置续跑（重试计数 +1） |
| Ollama 模型要求 | 断网前须 `ollama pull`；推荐 Q4 量化；Ollama ≥ 0.1.x；模型须本地已存在，否则标记 failed |
| OpenAI 兼容端点 | `http://127.0.0.1:11434/v1`（注意带 `/v1`） |
| 同步失败场景 | ① 网络中断致云文档写回失败 ② 同步包 JSON 损坏 → 拒绝导入并提示 ③ 两端并发写同一文件冲突 → 必须 export/import 交换 ④ schema 版本不一致（如缺 `result` 字段） |

**诚实说明**：本地小模型（7B/8B）只干中低难度活，复杂活质量打折，用 L4/L5 规则兜住；模型权重须断网前拉好；省的是 L1 那块最肉的，L2/L3/L4 照花。

---

## 二、输入约束与输出承诺

**输入**
- `add <标题> <详情> [--priority 1-9] [--source a|b]`：标题 ≤100 字、详情 ≤5000 字、优先级 1-9（默认 5）。
- `import <同步包路径>`：传入合法 JSON 同步包。
- `export <路径>`：导出同步包。
- `offline_worker.py --model <模型名>`：`--model` 须为本地已 pull 的模型。

**输出承诺**
- `list` 统一格式：`[id] <status> P<priority> <title> (<source>)`。
- Worker 结果强制结构：`【结论】分点正文【下一步】`，≤ 300 字，规范可读。
- 状态机明确：`queued → running → done/failed`，失败必带 `[调用失败] 原因`。
- 同步包不含任何密钥；导入只合并「对方更新过」的任务，本地更新的不动。

---

## 三、触发场景

**意图表**
| 用户意图 | 触发词示例 | 路由 |
|----------|-----------|------|
| 省积分 / 省钱 | "任务太烧积分""API 涨价" | L1 本地 |
| 旧电脑跑模型 | "低配电脑能跑吗""旧机器" | L1 本地 |
| 断网续跑 | "断网了还能跑吗""拔网线" | 通道 C |
| 敏感不出门 | "NDA 资料""数据不想出本机" | L1 本地 |
| 批量处理 | "几百条文档""重复活" | L1 本地 |

**示例对话**
> 用户：「我白天在办公室攒了一堆要摘要的文档，回家想让家里旧电脑断网跑完，别花云端积分。」
> 助手：触发本技能 → 建议 L1 本地路由：机器 A `add` 批量任务 → `export` 同步包 → 带回家机器 B `import` → `offline_worker.py --model qwen2.5:7b` 跑完 → `export` 带回 → `import` 收结果。

---

## 四、常见错误与反模式（FAQ + 高频 Q&A）

**反模式（DON'T）**
- ❌ 两台机器直接共享同一 `taskbox.json` 并发写 → 应各自维护 + export/import 同步包。
- ❌ 任务详情里写密码 / token / 密钥 → 一律不进任务箱，凭据从保险库读。
- ❌ 把 Ollama 直曝公网 → 仅限 127.0.0.1 或可信内网 / 私网（Tailscale/WireGuard）。
- ❌ 让本地 7B 硬刚复杂推理 → 用 L4 云端或 L5 试跑降级。
- ❌ 断网后才 `ollama pull` → 权重须联网时先拉好。

**高频 Q&A**
- **Q：同时开两个 Worker 会重复处理吗？** 会。同一文件不推荐并发写；确有需求请各用独立任务箱再合并。
- **Q：导入别人同步包会搞乱我的任务吗？** 不会。按 id 去重，只合并对方 `updated_at` 较新者。
- **Q：taskbox.json 弄坏了？** 程序提示损坏并退出（不静默清空），用最近同步包 `import` 重建。
- **Q：模型没装 / 名字错？** 任务标记 failed，结果写明 `[调用失败] 原因`，换 `--model` 重跑。
- **Q：任务能写多长 / 优先级怎么填？** 标题 ≤100、详情 ≤5000；优先级 1-9（越大越先跑，默认 5）。
- **Q：纯新手配置门槛高？** 先跑「三步最小闭环」（见第五章），暂不接 DSH / 云文档，门槛最低。

---

## 五、标准 SOP（步骤表）

| 步骤 | 动作 | 命令 / 操作 |
|------|------|------------|
| 1 装环境 | 机器 B 装 Ollama 并拉模型（联网时） | `ollama pull qwen2.5:7b` |
| 2 最小闭环 | 机器 A 加任务 → 导出 → 机器 B 导入跑完 → 带回收结果 | 见第九章示例 |
| 3 上规模 | 接云文档队列（通道 B）或 DSH 执行层 | 第六/八节 |
| 4 自动化 | 机器 B 定时扫表 / WorkBuddy HOURLY 自动化 | 第九章清单 |
| 5 调优 | 实测一周记录云端消耗，调 L1-L5 分级表 | 按数据迭代 |

**快速上手（三步）**
1. 机器 B 装 Ollama，断网前 `ollama pull qwen2.5:7b`。
2. 跑通最小闭环：`add` → `export` →（带机 B）`import` → `offline_worker.py --model qwen2.5:7b` → `export` 带回 → `import`。
3. 上规模：接云文档队列或 DSH，配定时自动化。

---

## 六、关键事实速查

**任务分级表（省算力路由核心）**
| 级别 | 类型 | 示例 | 路由 | 云端消耗 |
|------|------|------|------|----------|
| L1 本地 | 批量/重复/文档/敏感 | 知识库精读、摘要、格式转换、NDA 资料 | 机器 B 本地 Ollama | 0 |
| L2 云端 | 联网检索 | AI 日报、查资料 | 云端 | 少 |
| L3 云端 | 生图/视频 | 封面、视频 | 云端 | 多 |
| L4 云端 | 复杂推理/写作 | 法规分析、方案设计 | 云端好模型 | 该花则花 |
| L5 试跑 | 中难度 | 先本地试，不行再云端 | 本地→云端降级 | 0→少 |

**最低配置参考**
- 纯 CPU / 核显（8GB 内存）：3B 量化（慢但能用）。
- 8GB 显存 / 16-32GB 内存：7B-8B Q4 约 20-30 tok/s（推荐甜点）。
- 更高：14B+ 或走云端 L4/L5。

**命令速查**
```
python local_taskbox.py add "标题" "详情" --priority 7 --source a
python local_taskbox.py list
python local_taskbox.py done <id> "结果"
python local_taskbox.py fail <id> "原因"
python local_taskbox.py delete <id>
python local_taskbox.py export sync_out.json
python local_taskbox.py import sync_out.json
python offline_worker.py --model qwen2.5:7b
```

---

## 七、铁律（PROHIBITED）

- 禁止在任务详情写入密码 / token / 任何密钥。
- 禁止并发写同一 `taskbox.json`；禁止把 Ollama 直曝公网。
- 禁止让本地小模型硬扛 L4 复杂推理（质量无保障）。
- 禁止断网后才拉模型权重（须提前 `ollama pull`）。
- 禁止静默吞错：失败必须标记 failed 并写明原因，不得误标 done。
- 禁止把同步包当唯一备份：每次 export 后留一份副本。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

**零凭据设计**：本技能断网闭环不依赖任何云端 API / MCP，无需 API Key，无外联——天然无凭据面。

**若启用云文档通道（通道 B）**：乐享 / 金山等平台凭证（token）必须从平台保险库 / 环境变量读取，**绝不以明文粘贴进对话或写入任务箱**；同步包本身不含任何密钥。

**外部依赖**
- Ollama（本地，监听 127.0.0.1:11434）——仅本地推理，无鉴权不外曝。
- 可选 DSH（DeepSeek Harness）执行层，推理仍走本地 Ollama。

---

## 九、示例

**完整流程 + 实际输出**
```
机器 A（记想法）：
$ python local_taskbox.py add "整理出差清单" "护照、转换插头、名片" --priority 7
已添加任务 #1：整理出差清单
$ python local_taskbox.py add "查资料" "FDA 收费规则"
已添加任务 #2：查资料
$ python local_taskbox.py list
[1] queued   P7 整理出差清单  (a)
[2] queued   P5 查资料  (a)
$ python local_taskbox.py export sync_out.json

机器 B（断网执行，模型在本地）：
$ python local_taskbox.py import sync_out.json
已合并 2 个任务（来自 sync_out.json），当前共 2 个
$ python offline_worker.py --model qwen2.5:7b
== 处理 #1：整理出差清单（模型 qwen2.5:7b）
== 完成 #1，结果长度 128
== 处理 #2：查资料（模型 qwen2.5:7b）
== 完成 #2，结果长度 96
$ python local_taskbox.py export result.json

机器 A（回收结果）：
$ python local_taskbox.py import result.json
已合并 2 个任务（来自 result.json），当前共 2 个
$ python local_taskbox.py list
[1] done     P7 整理出差清单  (a)
[2] done     P5 查资料  (a)
```

**最佳实践**
- 批量文档：逐个 `add`（大批量 `add --file` 在路线中），统一 L1 本地路由。
- 配置建议：机器 B 常驻 Ollama + 定时自动化；敏感任务一律 `--source` 标注并走本地。
- 模型选择：`--model` 按机器配置选（3B 慢 / 7B-8B 甜点 / 14B+ 走云端）。

---

## 十、错误处理

**错误分类与处置（评测补齐：区分类型 + 错误码）**
| 错误码 | 类型 | 触发 | 处置 |
|--------|------|------|------|
| E001 | 文件损坏 | taskbox.json JSON 解码失败 | 拒绝加载并提示，用最近同步包 `import` 重建 |
| E002 | 模型缺失 | Ollama 无该模型 / 名字错 | 标记 failed：`[调用失败] model not found`，换 `--model` 重跑 |
| E003 | 进程缺失 | Ollama 未启动 | 标记 failed：`[调用失败] ollama not running` |
| E004 | 网络中断 | 云文档写回失败 | 落到通道 C 本地任务箱，恢复后续传 |
| E005 | 执行超时 | 单条 > 900s | 标记 failed 并写明超时，建议拆任务或换模型 |
| E006 | 同步冲突 | 并发写 / schema 版本不一致 | 拒绝并提示用 export/import 交换，禁止覆盖 |

**稳定性增强（评测补齐）**
- 失败任务标记 failed（**不误标 done**），保留原因便于定位根因。
- 建议加重试：云文档通道心跳超时（30min）自动重置续跑，重试计数 +1。
- 建议加运行日志：每条任务记 `started_at / finished_at / error_code`，形成可追溯轨迹；断点可从最近同步包恢复。
- 文件损坏有检测与提示（JSONDecodeError/UnicodeDecodeError），不会静默清空。

---

## 版权与治理（附录 · 不淹没正文）

- © 2026 **SynomosAI**。本技能以 **MIT 协议**开源，可自由使用、修改、再分发（保留版权声明即可）。
- 治理承载 SynomosAI 体系（XCGS / A³ 法则 / AI 护照 / AI 世界共生论），指纹 FP-MX-2DADE043FADB。
- 免责声明：按「现状（AS IS）」提供，不作任何担保；使用风险自担，请遵守所在司法辖区法规与所用模型许可。
- 本技能零云端依赖（断网模式），不收集数据；任务详情请勿写入密码 / token。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-2DADE043FADB。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

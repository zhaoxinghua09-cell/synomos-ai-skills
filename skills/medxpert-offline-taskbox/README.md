# MedXpert Offline Taskbox · 跨机任务箱·低配省算力

AI API costs burning you? **Run LLMs on low-spec machines** — dispatch tasks by day, local models finish them for free at night, even offline. MedXpert Cross-Machine Taskbox: WorkBuddy × DSH (DeepSeek Harness) × local Ollama three-tier collaboration. Batch/repeat/document/sensitive tasks cost **zero cloud credits**; only complex reasoning goes to the cloud.

L1-L5 tiered routing (code-level: add auto-tags + route query), auto-retry on failure, sync-package merge across two machines, zombie-proof resume. **Pure Python, zero dependencies** — old PCs can be execution nodes. API price hikes? Not your problem.

AI 任务太烧钱？低配电脑也能跑大模型——白天派活，晚上回家让本地模型免费跑完，断网也不停。省积分、断网续跑、离线任务队列、任务路由与成本控制都找它。

## Install

```bash
# ClawHub
clawhub install medxpert-offline-taskbox
# or npx-style direct install from this repo
npx skills add medxpert-cn/medxpert-offline-taskbox
```

## Files

| File | What |
|---|---|
| `SKILL.md` | Skill entry: triggers, routing rules, workflows, FAQ, boundary |
| `local_taskbox.py` | Local JSON taskbox: L1-L5 auto-routing, sync package export/import, status machine |
| `offline_worker.py` | Offline worker: pull local todos → run local Ollama → write back, auto-retry, zombie-proof |

## Quick start

```bash
python local_taskbox.py add "整理FDA指南更新" "5 份新指南，每份 200 字摘要" --priority 5
python local_taskbox.py export sync_out.json   # 带去机器 B
python offline_worker.py --model qwen2.5:7b    # 机器 B 断网跑完
```

## License

MIT © 2026 注册老炮 (MedXpert). Provided AS IS, no warranty.

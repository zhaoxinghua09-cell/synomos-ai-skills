#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地任务箱：断网可跑的任务存储、同步与 L1-L5 分级路由（纯标准库，无外部依赖）。

用于「MedXpert 跨机任务箱」的离线闭环模式：两台机器各持一份本地任务箱，
通过交换「同步包.json」合并，不依赖任何云端 API，断网也能完整工作。

v2.4.0 新增：L1-L5 省算力分级路由（add 自动打级别标签 + route 子命令查询）。

用法：
  python local_taskbox.py add "标题" "详情" [--priority 1-9] [--source a|b] [--level L1-L5]
  python local_taskbox.py list [--level L1]
  python local_taskbox.py route [<id>]         # 显示任务级别（不带 id 显示全部）
  python local_taskbox.py done <id> "结果文本"
  python local_taskbox.py fail <id> "失败原因"
  python local_taskbox.py delete <id>
  python local_taskbox.py export <path>
  python local_taskbox.py import <path>
"""
import json
import os
import sys
import argparse
import datetime

BOX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taskbox.json")
STATUSES = ("queued", "running", "done", "failed")

# ============ L1-L5 省算力分级路由 ============
LEVELS = {
    "L1": "本地执行（批量/重复/文档/敏感 → 本地 Ollama，0 云端消耗）",
    "L2": "云端检索（需联网查资料/资讯 → 云端）",
    "L3": "云端生图/视频（封面/海报/视频 → 云端）",
    "L4": "云端复杂推理（分析/方案/合规 → 云端好模型，该花则花）",
    "L5": "试跑降级（中难度先本地小模型试，不满意再升云端）",
}

# 关键词路由表：命中即归入对应级别（顺序优先，命中先者为准）。
# 可按团队习惯自行增删；add 时用 --level 可手动覆盖自动判断。
ROUTE_RULES = [
    ("L1", ["批量", "重复", "文档", "整理", "汇总", "翻译", "摘要", "格式转换",
            "脚本", "NDA", "客户", "敏感", "清单", "提取", "批处理", "拆分", "合并",
            "精读", "分类", "归档", "清洗", "转写"]),
    ("L2", ["查", "搜索", "新闻", "资讯", "日报", "检索", "最新", "查找", "查询",
            "资料", "行情", "天气"]),
    ("L3", ["图片", "封面", "海报", "视频", "logo", "Logo", "生成图", "设计图",
            "头像", "配图", "插画"]),
    ("L4", ["分析", "方案", "设计", "评估", "报告", "规划", "策略", "合规", "法规",
            "风险", "审批", "决策", "竞品", "调研", "预测", "建议书"]),
    ("L5", ["总结", "改写", "润色", "起草", "初稿", "大纲", "试写", "草稿", "头脑风暴"]),
]


def route_task(title, detail="", priority=5):
    """自动分级：优先级 8-9 直接升 L4（重要决策）；1-3 直接落 L1（批量杂活）；
    其余按关键词规则表命中归级；未命中默认 L1（本地最省）。"""
    if priority >= 8:
        return "L4"
    if priority <= 3:
        return "L1"
    text = (title or "") + " " + (detail or "")
    for level, kws in ROUTE_RULES:
        for kw in kws:
            if kw in text:
                return level
    return "L1"


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load():
    """读取任务箱。文件不存在返回空；文件损坏给出明确提示（不闪退）。"""
    if not os.path.exists(BOX_PATH):
        return []
    try:
        with open(BOX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"[错误] 任务箱文件 {BOX_PATH} 已损坏或编码异常，无法读取。")
        print("      若需恢复：请用最近的同步包执行 import 重建，或手动检查该文件。")
        sys.exit(1)


def save(tasks):
    with open(BOX_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks):
    return max([t.get("id", 0) for t in tasks], default=0) + 1


def add(title, detail="", priority=5, source="a", level=None):
    if not title or not title.strip():
        print("[错误] 标题不能为空。用法：add \"标题\" [\"详情\"]")
        sys.exit(1)
    if priority < 1 or priority > 9:
        print("[错误] 优先级需在 1-9 之间（数字越大越优先）。")
        sys.exit(1)
    if level is not None and level not in LEVELS:
        print(f"[错误] 级别须为 {list(LEVELS)} 之一（或省略由系统自动路由）。")
        sys.exit(1)
    tasks = load()
    lv = level if level else route_task(title, detail, priority)
    t = {
        "id": next_id(tasks),
        "title": title.strip(),
        "detail": detail,
        "status": "queued",
        "priority": priority,
        "source": source,
        "level": lv,
        "created_at": now(),
        "updated_at": now(),
        "result": "",
    }
    tasks.append(t)
    save(tasks)
    print(f"已添加任务 #{t['id']}：{t['title']}（路由 {lv}）")
    return t


def find_task(tasks, tid):
    for t in tasks:
        if t["id"] == tid:
            return t
    return None


def list_tasks(level=None):
    tasks = load()
    if level:
        tasks = [t for t in tasks if t.get("level") == level]
    if not tasks:
        print("（无匹配任务）" if level else "（任务箱为空）")
        return
    for t in tasks:
        lv = t.get("level", "L1")
        print(
            f"[{t['id']}] {t['status']:7} P{t.get('priority',5)} {lv} "
            f"{t['title']}  ({t.get('source','?')})"
        )


def show_route(tid=None):
    tasks = load()
    if not tasks:
        print("（任务箱为空）")
        return
    if tid is not None:
        t = find_task(tasks, tid)
        if not t:
            print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
            return
        lv = t.get("level", "L1")
        print(f"#{tid} {t['title']} → {lv}：{LEVELS.get(lv, '')}")
        return
    print("当前任务箱级别分布：")
    for lv in LEVELS:
        n = sum(1 for t in tasks if t.get("level") == lv)
        if n:
            print(f"  {lv} × {n}  {LEVELS[lv]}")
    print(f"  （合计 {len(tasks)} 个任务）")


def mark_done(tid, result):
    tasks = load()
    t = find_task(tasks, tid)
    if not t:
        print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
        return
    t["status"] = "done"
    t["result"] = result
    t["updated_at"] = now()
    save(tasks)
    print(f"任务 #{tid} 已标记完成")


def mark_fail(tid, reason):
    tasks = load()
    t = find_task(tasks, tid)
    if not t:
        print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
        return
    t["status"] = "failed"
    t["result"] = reason
    t["updated_at"] = now()
    save(tasks)
    print(f"任务 #{tid} 已标记失败")


def delete_task(tid):
    tasks = load()
    t = find_task(tasks, tid)
    if not t:
        print(f"未找到任务 #{tid}（可用 list 查看现有任务 id）")
        return
    tasks = [x for x in tasks if x["id"] != tid]
    save(tasks)
    print(f"任务 #{tid} 已删除")


def export_pack(path):
    """导出同步包（含全部任务），供对方机器 import 合并。"""
    tasks = load()
    pack = {"exported_at": now(), "tasks": tasks}
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pack, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"[错误] 导出失败：{e}（请检查路径是否可写）")
        sys.exit(1)
    print(f"已导出 {len(tasks)} 个任务到 {path}")


def import_pack(path):
    """导入对方同步包，按 id 去重，保留 updated_at 较新者。"""
    if not os.path.exists(path):
        print(f"[错误] 导入文件不存在：{path}（请检查文件名/路径是否正确）")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            pack = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
        print(f"[错误] 导入文件无法解析：{path}（{e}）")
        print("      请确认该文件是有效的同步包（export 命令产物）。")
        sys.exit(1)
    incoming = pack.get("tasks", [])
    tasks = load()
    by_id = {t["id"]: t for t in tasks}
    merged = 0
    for t in incoming:
        tid = t["id"]
        if tid not in by_id or t["updated_at"] > by_id[tid]["updated_at"]:
            by_id[tid] = t
            merged += 1
    tasks = sorted(by_id.values(), key=lambda x: x["id"])
    save(tasks)
    print(f"已合并 {merged} 个任务（来自 {path}），当前共 {len(tasks)} 个")


def main():
    p = argparse.ArgumentParser(description="本地任务箱（断网闭环 + L1-L5 路由）v2.4.0")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("list")
    a = sub.add_parser("add")
    a.add_argument("title")
    a.add_argument("detail", nargs="?", default="")
    a.add_argument("--priority", type=int, default=5)
    a.add_argument("--source", default="a")
    a.add_argument("--level", choices=list(LEVELS), default=None)
    r = sub.add_parser("route")
    r.add_argument("id", type=int, nargs="?")
    d = sub.add_parser("done")
    d.add_argument("id", type=int)
    d.add_argument("result", nargs="?", default="")
    f = sub.add_parser("fail")
    f.add_argument("id", type=int)
    f.add_argument("reason", nargs="?", default="")
    dl = sub.add_parser("delete")
    dl.add_argument("id", type=int)
    e = sub.add_parser("export")
    e.add_argument("path")
    i = sub.add_parser("import")
    i.add_argument("path")
    args = p.parse_args()

    if args.cmd == "list" or args.cmd is None:
        list_tasks()
    elif args.cmd == "add":
        add(args.title, args.detail, args.priority, args.source, args.level)
    elif args.cmd == "route":
        show_route(args.id)
    elif args.cmd == "done":
        mark_done(args.id, args.result)
    elif args.cmd == "fail":
        mark_fail(args.id, args.reason)
    elif args.cmd == "delete":
        delete_task(args.id)
    elif args.cmd == "export":
        export_pack(args.path)
    elif args.cmd == "import":
        import_pack(args.path)


if __name__ == "__main__":
    main()

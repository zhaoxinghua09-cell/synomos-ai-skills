#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc-property-badges — 文档属性徽章生成器
========================================
按「分方向 × 分级 × 分层」生成 SVG 胶囊徽章，并产出可视化预览页 gallery.html。

用法：
  python gen_badges.py                       # 生成全部徽章 + gallery
  python gen_badges.py --direction ai        # 只生成 AI 属性方向
  python gen_badges.py --layer watermark     # 生成半透明水印版（opacity≈0.18）
  python gen_badges.py --out badges_v2       # 指定输出目录
"""

import argparse
import os
import html

# 方向 → 名称 / 图标 / 级别[(级别名, 颜色)]
DIRECTIONS = {
    "copyright": {
        "name": "著作权", "icon": "©",
        "levels": [("开放许可", "#9DB8E0"), ("授权使用", "#5A8FD0"), ("全权保留", "#2C6FD6")],
    },
    "ai": {
        "name": "AI属性", "icon": "AI",
        "levels": [("人工撰写", "#9C8BE0"), ("AI辅助", "#7B5BE6"), ("AI生成", "#5B3FC0")],
    },
    "ai_rights": {
        "name": "AI权限", "icon": "权",
        "levels": [("禁止AI使用", "#9AA0A6"), ("允许AI学习", "#6FCF97"), ("允许AI合作编辑", "#27AE60")],
    },
    "payment": {
        "name": "支付属性", "icon": "¥",
        "levels": [("免费", "#F0C969"), ("付费", "#E0A200"), ("授权付费", "#B87F00")],
    },
    "tracking": {
        "name": "密文追踪", "icon": "◎",
        "levels": [("未嵌入", "#B9D8D5"), ("已嵌入", "#1FA8A0")],
    },
    "confidentiality": {
        "name": "密级", "icon": "密",
        "levels": [("公开", "#9AA0A6"), ("内部", "#6B7780"), ("受限", "#C0392B"), ("机密", "#8E1E15")],
    },
    "owner": {
        "name": "归属", "icon": "属",
        "levels": [("单位所有", "#E8743B"), ("个人所有", "#F0A868"), ("委托代管", "#C85A1F")],
    },
    "validity": {
        "name": "时效", "icon": "效",
        "levels": [("永久有效", "#A569BD"), ("限时有效", "#9B59B6"), ("已过期", "#6C3483")],
    },
    "protect_edit": {
        "name": "防编辑", "icon": "锁",
        "levels": [("可编辑", "#9AA0A6"), ("禁止编辑", "#E74C3C"), ("只读锁定", "#C0392B")],
    },
    "protect_convert": {
        "name": "防另存", "icon": "存",
        "levels": [("允许转换", "#9AA0A6"), ("禁止另存", "#D6336C"), ("禁止格式转换", "#A02850")],
    },
}

H = 30          # 徽章高度
R = 15          # 圆角半径
PAD_L = 16      # 左侧图标圆心 x
ICON_R = 11     # 图标圆半径
TEXT_X = 34     # 文字起点
FONT = 13
# 字符宽度估算（CJK 取 14，其余取 7.5）
def text_w(s):
    return sum(14 if ord(c) > 0x2E80 else 7.5 for c in s)

def esc(s):
    return html.escape(s, quote=True)

def make_svg(direction, level_name, color, opacity=1.0):
    d = DIRECTIONS[direction]
    label = f"{d['name']}·{level_name}"
    tw = text_w(label)
    W = TEXT_X + tw + 14
    # 图标文字（AI 用较小字号）
    icon_font = 11 if d["icon"] == "AI" else 13
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H}" '
               f'viewBox="0 0 {W:.0f} {H}" opacity="{opacity}">')
    svg.append(f'  <rect x="0" y="0" width="{W:.0f}" height="{H}" rx="{R}" ry="{R}" fill="{color}"/>')
    svg.append(f'  <circle cx="{PAD_L}" cy="{H/2}" r="{ICON_R}" fill="#ffffff"/>')
    svg.append(f'  <text x="{PAD_L}" y="{H/2}" font-family="Arial, Helvetica, sans-serif" '
               f'font-size="{icon_font}" font-weight="bold" fill="{color}" '
               f'text-anchor="middle" dominant-baseline="central">{esc(d["icon"])}</text>')
    svg.append(f'  <text x="{TEXT_X}" y="{H/2}" font-family="Arial, \'Microsoft YaHei\', sans-serif" '
               f'font-size="{FONT}" fill="#ffffff" '
               f'text-anchor="start" dominant-baseline="central">{esc(label)}</text>')
    svg.append('</svg>')
    return "\n".join(svg), W

def build_gallery(out_dir, layer):
    op = 0.18 if layer == "watermark" else 1.0
    items = []  # (direction, level_name, svg_str)
    for code, d in DIRECTIONS.items():
        for lvl_name, color in d["levels"]:
            svg, _ = make_svg(code, lvl_name, color, op)
            items.append((code, lvl_name, svg))
    # 生成 HTML gallery
    cards = []
    for code, lvl_name, svg in items:
        d = DIRECTIONS[code]
        cards.append(
            f'      <div class="card">\n'
            f'        <div class="badge">{svg}</div>\n'
            f'        <div class="meta">{esc(d["name"])} · {esc(lvl_name)}</div>\n'
            f'        <div class="file">{esc(code)}_{esc(lvl_name)}.svg</div>\n'
            f'      </div>'
        )
    layer_label = {"visible": "可见层 (visible)", "watermark": "水印层 (watermark, ~18%)",
                   "invisible": "不可见层 (invisible / 密文)"}[layer]
    html_doc = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>文档属性徽章 · {esc(layer_label)}</title>
<style>
 body{{font-family:'Microsoft YaHei',Arial,sans-serif;background:#f5f6f8;margin:0;padding:24px;color:#222}}
 h1{{font-size:20px;margin:0 0 4px}}
 .sub{{color:#666;font-size:13px;margin-bottom:18px}}
 .grid{{display:flex;flex-wrap:wrap;gap:14px}}
 .card{{background:#fff;border:1px solid #e6e8ec;border-radius:10px;padding:14px 16px;width:180px;
        box-shadow:0 1px 3px rgba(0,0,0,.05);display:flex;flex-direction:column;align-items:center;gap:8px}}
 .badge{{min-height:30px;display:flex;align-items:center}}
 .meta{{font-size:13px;font-weight:600}}
 .file{{font-size:11px;color:#999;font-family:monospace}}
 .note{{margin-top:20px;font-size:12px;color:#888;line-height:1.6}}
</style></head><body>
<h1>文档属性徽章体系</h1>
<div class="sub">分方向 × 分级 × 分层 ｜ 当前层：<b>{esc(layer_label)}</b></div>
<div class="grid">
{chr(10).join(cards)}
</div>
<div class="note">
 分方向：著作权 / AI属性 / AI权限 / 支付属性 / 密文追踪 / 密级 / 归属(单位·个人) / 时效 / 防编辑 / 防另存<br>
 分级：每方向内由浅→深表示程度递增（开放→全权 / 人工→AI生成 / 禁AI→可合作编辑 / 免费→授权付费 / 未嵌入→已嵌入 / 公开→机密 / 单位→个人 / 永久→已过期 / 可编辑→只读锁定 / 允许转换→禁止格式转换）<br>
 分层：visible 明示 + watermark 震慑 + invisible 密文溯源（三信息一致，仅呈现强度不同）
</div>
</body></html>"""
    gallery_path = os.path.join(out_dir, "gallery.html")
    with open(gallery_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return gallery_path

def main():
    p = argparse.ArgumentParser(description="文档属性徽章生成器")
    p.add_argument("--out", default="badges", help="输出目录")
    p.add_argument("--direction", default=None, choices=list(DIRECTIONS.keys()),
                   help="只生成指定方向")
    p.add_argument("--layer", default="visible", choices=["visible", "watermark", "invisible"])
    args = p.parse_args()

    op = 0.18 if args.layer == "watermark" else 1.0
    os.makedirs(args.out, exist_ok=True)

    codes = [args.direction] if args.direction else list(DIRECTIONS.keys())
    for code in codes:
        d = DIRECTIONS[code]
        for lvl_name, color in d["levels"]:
            svg, _ = make_svg(code, lvl_name, color, op)
            fname = f"{code}_{lvl_name}.svg"
            with open(os.path.join(args.out, fname), "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"[ok] {fname}")

    gallery = build_gallery(args.out, args.layer)
    print(f"[ok] 预览页: {gallery}")

if __name__ == "__main__":
    main()

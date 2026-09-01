#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc-ip-declaration — 一键给 PDF 增加产权 / 知识产权声明
=====================================================

功能：
  1. 著作权声明 + 免责条款（页脚 + 独立声明页）
  2. AI 属性密文追踪：在每一页嵌入“不可见”密文水印（alpha=0 的追踪码），
     可被文本提取但肉眼不可见，用于版权溯源与泄密定位。
  3. 支付属性：版权付费许可声明 + 授权 / 付费联系方式（写入声明页）。
  4. 写入 PDF 元数据（含追踪码 / TrackingID）。

用法：
  python add_ip_declaration.py \
      --input  in.pdf \
      --output out.pdf \
      --org    "某某医院" \
      --contact "授权联系：{授权邮箱} / {联系电话}" \
      --tracking-id "ORG-20260819-A1B2C3D4"   # 不传则自动生成
  # 可选：
  --declaration-page yes|no   # 是否追加独立声明页（默认 yes）
  --watermark yes|no          # 是否嵌入不可见密文追踪（默认 yes）
  --footer yes|no             # 是否给每页加一行声明页脚（默认 yes）
"""

import argparse
import datetime as _dt
import os
import random
import string
import sys
import io

try:
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.colors import Color
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_LEFT
except ModuleNotFoundError as _e:
    print("[err] 缺少依赖库，请先安装：", file=sys.stderr)
    print("      pip install pypdf reportlab", file=sys.stderr)
    print(f"      当前缺失: {_e.name}", file=sys.stderr)
    sys.exit(1)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# 注册中文字体（Adobe 自带 CID 字体，无需外部字体文件）
try:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    CJK = "STSong-Light"
except Exception:
    CJK = "Helvetica"  # 兜底


# ----------------------------- 默认声明文案 -----------------------------

DEFAULT_LICENSE = (
    "本文件为受版权保护之内容。未经权利方书面授权，不得用于任何商业用途、"
    "不得转载、二次分发、抓取、训练或牟利。如需商用授权、付费许可或批量使用，"
    "请通过下方联系方式申请。"
)

DISCLAIMER = (
    "本文件所载内容仅供内部参考与信息交流之用，不构成任何形式的正式意见、"
    "诊断、治疗或法律建议。使用者应自行核实信息并承担由此产生的一切后果。"
    "权利方不对因使用本文件导致的任何损失承担责任。"
)

AI_NOTICE = (
    "本文件可能由人工智能（AI）技术辅助生成或处理。文件内已嵌入不可见密文"
    "追踪标识，用于版权溯源与泄密定位。任何复制、转发、截屏外传行为均可能被追溯。"
)


def gen_tracking_id(org: str) -> str:
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    stamp = _dt.date.today().strftime("%Y%m%d")
    prefix = "".join(ch if ch.isalnum() else "" for ch in org)[:6].upper() or "DOC"
    return f"{prefix}-{stamp}-{code}"


# ----------------------------- 不可见密文水印 -----------------------------

def make_invisible_watermark_page(width, height, tracking_id, org):
    """生成与指定页面同尺寸、含 alpha=0 追踪码的覆盖层。"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(float(width), float(height)))
    text = f"TRACKING:{tracking_id}  ©{org}  CONFIDENTIAL-IP"
    c.setFillColor(Color(0, 0, 0, alpha=0.0))  # 完全透明但保留文本流
    c.setFont("Helvetica", 9)
    # 多处放置，提升被提取概率
    positions = [
        (15 * mm, 12 * mm),
        (width - 15 * mm - 220, 12 * mm),
        (15 * mm, height - 15 * mm),
    ]
    for (x, y) in positions:
        c.drawString(float(x), float(y), text)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ----------------------------- 每页页脚 -----------------------------

def make_footer_overlay(width, height, org):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(float(width), float(height)))
    c.setFillColor(Color(0.45, 0.45, 0.45, alpha=1))
    c.setFont("Helvetica", 7)
    line = f"© {org} · 保留所有权利 · 受版权与知识产权声明约束 · 内含不可见密文追踪"
    c.drawCentredString(float(width) / 2.0, 8 * mm, line)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ----------------------------- 独立声明页 -----------------------------

def make_declaration_page(org, contact, tracking_id, license_text, disclaimer, ai_notice):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title="文件知识产权与版权声明",
        author=org,
    )
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=16, spaceAfter=10,
                        textColor=Color(0.1, 0.1, 0.1), fontName=CJK)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, spaceBefore=10,
                        spaceAfter=4, textColor=Color(0.15, 0.15, 0.15), fontName=CJK)
    body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=14,
                          alignment=TA_LEFT, textColor=Color(0.15, 0.15, 0.15), fontName=CJK)
    mono = ParagraphStyle("mono", parent=body, fontName="Courier", fontSize=9,
                          textColor=Color(0.3, 0.3, 0.3))

    today = _dt.date.today().strftime("%Y年%m月%d日")
    elems = [
        Paragraph("文件知识产权与版权声明", h1),
        Paragraph(f"权利方：{org}", body),
        Paragraph(f"生效日期：{today}", body),
        Spacer(1, 6),

        Paragraph("一、著作权声明", h2),
        Paragraph(
            f"本文件及其全部内容（含文字、数据、图表、图像及排版）的著作权、"
            f"署名权及相关知识产权均归 {org} 所有，并受《中华人民共和国著作权法》"
            f"及国际版权条约保护。", body),

        Paragraph("二、免责声明", h2),
        Paragraph(disclaimer, body),

        Paragraph("三、AI 属性与密文追踪", h2),
        Paragraph(ai_notice, body),
        Paragraph(f"文件追踪码：", body),
        Paragraph(tracking_id, mono),

        Paragraph("四、支付属性与授权许可", h2),
        Paragraph(license_text, body),
        Paragraph(f"授权 / 付费联系：{contact}", body),

        Spacer(1, 10),
        Paragraph("— 本声明随文件一同生效，任何获取本文件之主体均视为已阅读并同意上述条款。—", body),
    ]
    doc.build(elems)
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ----------------------------- 主流程 -----------------------------

def process(args):
    org = args.org
    contact = args.contact
    tracking_id = args.tracking_id or gen_tracking_id(org)
    license_text = args.license or DEFAULT_LICENSE

    reader = PdfReader(args.input)
    writer = PdfWriter()

    # 1) 逐页叠加（不可见密文 + 页脚）
    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)

        if args.watermark:
            wm = make_invisible_watermark_page(w, h, tracking_id, org)
            page.merge_page(wm)
        if args.footer:
            fo = make_footer_overlay(w, h, org)
            page.merge_page(fo)

        writer.add_page(page)

    # 2) 追加独立声明页
    if args.declaration_page:
        decl = make_declaration_page(
            org, contact, tracking_id, license_text,
            DISCLAIMER, AI_NOTICE,
        )
        writer.add_page(decl)

    # 3) 写入元数据（含追踪码）
    writer.add_metadata({
        "/Title": "文件知识产权与版权声明",
        "/Author": org,
        "/Subject": f"TrackingID={tracking_id}",
        "/Producer": "doc-ip-declaration",
        "/TrackingID": tracking_id,
        "/Keywords": "copyright,AI-tracking,license",
    })

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    with open(args.output, "wb") as f:
        writer.write(f)

    print(f"[ok] 输出: {args.output}")
    print(f"[ok] 追踪码: {tracking_id}")
    print(f"[ok] 页数: {len(writer.pages)} (原 {len(reader.pages)} + 声明页 {1 if args.declaration_page else 0})")


def main():
    p = argparse.ArgumentParser(description="一键给 PDF 增加产权/知识产权声明")
    p.add_argument("--input", "-i", required=True, help="输入 PDF 路径")
    p.add_argument("--output", "-o", required=True, help="输出 PDF 路径")
    p.add_argument("--org", default="某某医院", help="权利方机构名称")
    p.add_argument("--contact", default="授权联系：{授权邮箱} / {联系电话}",
                   help="授权/付费联系方式")
    p.add_argument("--tracking-id", default=None, help="追踪码（不填自动生成）")
    p.add_argument("--license", default=None, help="自定义版权付费许可声明文案")
    p.add_argument("--declaration-page", default="yes", choices=["yes", "no"])
    p.add_argument("--watermark", default="yes", choices=["yes", "no"])
    p.add_argument("--footer", default="yes", choices=["yes", "no"])
    args = p.parse_args()
    # 把 yes/no 转 bool
    for k in ("declaration_page", "watermark", "footer"):
        setattr(args, k, args.__getattribute__(k) == "yes")
    if not os.path.exists(args.input):
        print(f"[err] 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    process(args)


if __name__ == "__main__":
    main()

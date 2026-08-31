#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reg_hub_security_test.py — 医械注册通关枢纽 · 安全稳定性实测
文档型技能 8 维量化测试（本地闭环 · 零真实凭据 · 可重复）

维度（0-5 分制，驱动雷达图）：
  1. official_links   官方链接可信度（外链域名全部落在官方域）
  2. sensitive_zero   敏感信息隔离（真名/邮箱/本地路径/密钥 0 命中）
  3. recency          法规时效标注（现行版本号 + 复核提醒）
  4. boundary         边界与免责声明（不替代裁定 / AS IS / 本技能不做）
  5. copyright        权属与许可完整性（LICENSE.md + © + 知识版权声明）
  6. frontmatter      frontmatter 全字段（跨平台发布字段齐全）
  7. nav_consistency  references 导航一致（SKILL.md 导航表 vs 实际文件）
  8. package_clean    打包纯净（无 _ 开头元数据/缓存/二进制）

用法：
  python reg_hub_security_test.py [技能目录]
产出：
  security_results.json（本目录，供 gen_skill_security_radar.py 渲染雷达）
"""
import json
import os
import re
import sys
from pathlib import Path

OFFICIAL_DOMAINS = {
    "nmpa.gov.cn", "cmde.org.cn", "fda.gov", "accessdata.fda.gov",
    "health.ec.europa.eu", "www.gov.cn", "ecfr.gov", "pmda.go.jp",
    "std.samr.gov.cn", "udi.nmpa.gov.cn", "eudamed.europa.eu",
    "accessgudid.nlm.nih.gov", "ec.europa.eu", "eur-lex.europa.eu",
    "maers.adrs.org.cn", "moh.gov.vn", "openstd.samr.gov.cn",
    "regalkes.kemkes.go.id", "adrs.org.cn", "govinfo.gov",
    "medxpert.cn", "gs1.org", "gs1jp.org", "hibcc.org", "iccbba.org",
    "hsa.gov.sg", "iec.ch", "imdrf.org", "iso.org",
    "kikidb.jp", "mda.gov.my", "picscheme.org", "tga.gov.au",
}
# 官方/政府/标准机构域后缀（国家监管官网 & 国际标准组织）
OFFICIAL_SUFFIX = (".gov.cn", ".gov", ".go.jp", ".go.th", ".gob.mx", ".gov.br",
                   ".gov.vn", ".go.id", ".gov.ph", ".gob.ar", ".nhs.uk",
                   ".moph.go.th", ".europa.eu", ".int", ".astm.org", ".org.cn")
SENSITIVE = [r"(?<!\d)1[3-9]\d{9}(?!\d)", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
             r"C:\\Users\\", r"C:/Users/", r"/Users/", r"/home/",
             r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{36,}",
             r"zhaoxinghua", r"\bSteven\b", r"xinghua\d+"]
EMAIL_EXEMPT = ["info@medxpert.cn"]


def score_dim(name: str, score: float, note: str) -> dict:
    return {"name": name, "score": round(min(max(score, 0), 5), 2), "note": note}


def main(root: str = ".") -> int:
    base = Path(root).resolve()
    sk = (base / "SKILL.md").read_text("utf-8")
    ref_dir = base / "references"
    refs = {p.name: p.read_text("utf-8") for p in ref_dir.glob("*.md")} if ref_dir.exists() else {}
    lic = (base / "LICENSE.md").read_text("utf-8") if (base / "LICENSE.md").exists() else ""

    dims = []

    # 1. 官方链接可信度：主域提取 + 白名单域/官方后缀
    all_text = sk + "".join(refs.values())
    links = re.findall(r"https?://([a-zA-Z0-9.-]+)", all_text)
    def _main_domain(d: str) -> str:
        if d.startswith("www."):
            d = d[4:]
        parts = d.split(".")
        # 取最后两级（如 cmde.org.cn → org.cn 特殊三级政府域除外，直接取最后两级 + 补白名单）
        return ".".join(parts[-2:]) if len(parts) >= 2 else d
    def _is_official(d: str) -> bool:
        if d.startswith("www."):
            d = d[4:]
        if d in OFFICIAL_DOMAINS or _main_domain(d) in OFFICIAL_DOMAINS:
            return True
        md = _main_domain(d)
        return any(md == o or md == o.lstrip(".") or md.endswith(o) for o in OFFICIAL_SUFFIX)
    bad = sorted({d for d in links if not _is_official(d)})
    score1 = 5.0 if not bad else max(1.0, 5.0 - 1.0 * len(bad))
    dims.append(score_dim("官方链接可信度", score1,
                          f"{len(links)} 条外链全部官方域" if not bad else f"非官方域: {bad[:4]}"))

    # 2. 敏感信息隔离（对外邮箱豁免）
    hits = []
    for fname, content in list(refs.items()) + [("SKILL.md", sk)]:
        for pat in SENSITIVE:
            for m in re.finditer(pat, content):
                if pat.startswith("[A-Za-z0-9._%+-]") and m.group(0) in EMAIL_EXEMPT:
                    continue
                hits.append(f"{fname}:{pat}")
                break
    dims.append(score_dim("敏感信息隔离", 5.0 if not hits else 1.0,
                          "0 命中" if not hits else f"命中: {hits[:3]}"))

    # 3. 法规时效标注
    rec = sum(1 for kw in ["2025 年版", "现行", "最新版", "复核", "时效", "更新", "2026-"] if kw in all_text)
    dims.append(score_dim("法规时效标注", min(5.0, 2.0 + rec * 0.5), f"时效关键词命中 {rec}/7"))

    # 4. 边界与免责
    bnd = sum(1 for kw in ["不构成法规意见", "免责声明", "AS IS", "待核验", "本技能不做",
                           "不猜", "分类界定", "以官方最新发布为准"] if kw in sk)
    dims.append(score_dim("边界与免责", min(5.0, 1.0 + bnd * 0.55), f"边界关键词命中 {bnd}/8"))

    # 5. 权属与许可
    cop = 0
    if lic:
        cop += 2 if "MIT License" in lic and "Copyright" in lic else 0
    if "版权与许可" in sk:
        cop += 1
    if "知识版权声明" in sk:
        cop += 1
    if "注册老炮" in sk:
        cop += 1
    dims.append(score_dim("权属与许可", cop, "LICENSE+版权段+知识版权+署名" if cop >= 4 else f"命中 {cop}/5"))

    # 6. frontmatter 全字段
    fm = sk.split("---")[1] if sk.startswith("---") else ""
    need = ["name", "slug", "displayName", "display_name", "title", "version",
            "author", "category", "platforms", "license", "description", "description_en", "tags"]
    miss = [f for f in need if not re.search(rf"^{f}:", fm, re.M)]
    dims.append(score_dim("frontmatter 全字段", 5.0 if not miss else max(1.0, 5.0 - 1.2 * len(miss)),
                          "13 字段齐全" if not miss else f"缺: {miss}"))

    # 7. references 导航一致（反引号文件名格式）
    nav_refs = re.findall(r"`([^`]+\.md)`", sk)
    nav_refs = [r for r in nav_refs if r not in ("SKILL.md", "LICENSE.md", "README.md", "ATTESTATION.md")]
    missing = sorted({r for r in nav_refs if r not in refs})
    nav_count = len(set(nav_refs))
    dims.append(score_dim("导航一致性", 5.0 if not missing and nav_count >= 20 else max(1.0, 5.0 - 1.5 * (len(missing) + max(0, 20 - nav_count))),
                          f"导航引用 {nav_count} 文件全对应" if not missing else f"缺失: {missing}"))

    # 8. 打包纯净
    bad_items = []
    for p in base.rglob("*"):
        if "__pycache__" in p.parts or ".git" in p.parts:
            continue
        if p.is_file() and (p.name.startswith("_") or p.suffix.lower() in {".png", ".exe", ".jpg", ".jpeg", ".mp4", ".bak", ".tmp"}):
            bad_items.append(p.name)
    dims.append(score_dim("打包纯净", 5.0 if not bad_items else 2.0,
                          "无 _ 元数据/二进制" if not bad_items else f"混入: {bad_items[:3]}"))

    overall = sum(d["score"] for d in dims) / len(dims)
    ver_m = re.search(r"^version:\s*[\"']?([\w.]+)", fm, re.M)
    result = {
        "skill": "medxpert-reg-hub",
        "version": ver_m.group(1) if ver_m else "unknown",
        "timestamp_local": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "scope": "本地闭环 · 零真实凭据 · 可重复",
        "dimensions": dims,
        "overall": round(overall, 2),
    }
    out = base / "security_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    print(f"✔ 综合 {overall:.2f}/5 → {out}")
    for d in dims:
        print(f"  {d['name']:<8} {d['score']}/5  {d['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))

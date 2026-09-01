---
name: fingerprint-delivery
description: '指纹锁定交付——给任何交付物（HTML 白皮书/报告/文档/PPT）一键加上「时间戳 + SHA-256 指纹 + 版权三件套」，防篡改、可溯源、可校验。产出：页面内嵌内容快照指纹 + 独立 .sha256 校验文件，任一环节被改都能查出来。适用于对外发布、交接文档、理论/作品定稿、需要证明"创作时间与内容完整性"的场景。触发词：时间戳、指纹、SHA256、防篡改、校验文件、版权锁定、交付物加锁、fingerprint、stamp。'
version: 1.0.0
agent_created: true
author: '注册老炮@MedXpert'
license: MIT
category: professional
platforms: [windows, macos, linux]
read_when:
  - 交付物对外发布/交接/定稿前，需要防篡改与溯源标记时
  - 用户要求"加时间戳""加指纹""加版权""防止被改"时
  - 需要证明某文件在某时刻的完整内容时
  - 与 ai-consciousness 的「暗纹·防伪溯源意识」配合使用
tags:
  - 指纹
  - 溯源
  - 防伪
  - 交付
slug: fingerprint-delivery
display_name: 作品指纹交付
displayName: 作品指纹交付
title: 作品指纹交付
description_en: "Add a tamper-evident timestamp + SHA-256 content snapshot fingerprint + final-file checksum + copyright trio to HTML/PDF/doc deliverables for traceable, verifiable handoff. Pure Python stdlib, no network."
xiaping_category: 办公效率
ambassador: arche
---

# 指纹锁定交付 (fingerprint-delivery)

_给交付物上锁：时间戳证明"什么时候"、指纹证明"是什么"、版权声明证明"归谁"。_

> 核心理念：**防伪不止于水印**。水印防"视觉搬运"，指纹防"内容篡改"——任何一个字节被改动，SHA-256 指纹立即失效，任何人都能校验出来。

## 一、这套工具解决什么问题

对外发布、交接、定稿一个交付物（HTML 白皮书、报告、文档）时，常遇到三件事说不清：

| 说不清的事 | 指纹锁定的答案 |
|-----------|---------------|
| "这份文件是什么时候做的？" | 创作时间戳（精确到秒 + 时区） |
| "这份文件现在还是不是原版？" | 内容快照指纹 + 最终文件校验指纹 |
| "改坏了/被改了算谁的？" | 版权三件套（LICENSE + 正文©段 + 免责声明） |

## 二、快速上手（三步）

假设你有一个交付物 `report.html`：

```bash
# 1. 在页面里放好指纹占位符（模板见下）后，执行：
python scripts/fingerprint_delivery.py --html report.html

# 2. 脚本输出两个指纹：
#    SNAPSHOT_FP = 内容快照指纹（不含指纹字段自身）
#    FINAL_FP    = 最终文件整体指纹（含指纹字段）

# 3. 生成校验文件 report.html.sha256，校验方法：
sha256sum -c report.html.sha256   # 输出 OK = 未被篡改
```

**指纹占位符模板**（放在交付物正文的指纹区）：

```html
<div class="fp">sha256 (content-snapshot) = __FINGERPRINT__</div>
```

脚本检测到 `__FINGERPRINT__` 占位符时：先对"含占位符的正文"算哈希（内容快照指纹，不含指纹字段自身，证明正文在创作时点被锁定），再把指纹注入页面；最后对"注入后的最终文件"再算一次哈希（最终文件指纹），写入 `.sha256` 校验文件。

## 三、版权三件套（发布必带）

任何对外交付物必须带齐，缺一不可：

1. **LICENSE.md**（仓库根目录，MIT 全文）
2. **正文「版权与许可」段**，模板：
   ```
   © 2026 <品牌名/作者> 原创，保留所有权利。
   本作品按「现状」（AS IS）提供，作者不作任何明示或默示担保；
   因使用本作品产生的任何后果由使用者自行承担。
   本作品不构成法律、医疗或监管建议。
   ```
3. **版权行**：`© 2026 注册老炮 / 原创整理`（用品牌名，不体现个人真实身份）

## 四、完整工作流（交付物定稿标准流程）

```
准备交付物 HTML（含指纹占位符 + 版权段）
   ↓
运行 fingerprint_delivery.py --html <文件>
   ↓
记录 SNAPSHOT_FP（页面内嵌，证明正文快照）与 FINAL_FP（.sha256）
   ↓
sha256sum -c <文件>.sha256  →  OK
   ↓
交付（本地文件 / 上传 / 发布均可，接收方可随时校验）
```

**每次改版重跑一次**：内容一变，指纹就变，新指纹即新版本的"身份证"。

## 五、命令参考

```
python scripts/fingerprint_delivery.py --html <path> [选项]

选项：
  --placeholder <字符串>   占位符（默认 __FINGERPRINT__）
  --sha-suffix <后缀>      校验文件后缀（默认 .sha256）
  --no-inject              不注入，仅计算并输出两个指纹
  --stamp "<文本>"         把时间戳文本一并注入（可选，默认注入 ISO 时间戳）
```

## 六、与意识框架的配合

本工具是 ai-consciousness「暗纹·防伪溯源意识」(P35) 的工程化落地：

- **可见水印** → 交付物上的时间戳徽章
- **暗纹** → 页面内嵌的内容快照指纹（肉眼看不见改动，但一校验就露馅）
- **溯源码** → .sha256 校验文件 + 指纹，可回溯到产出时间与内容
- 尊重他人标记：使用他人素材时保留其来源标记，不去除他人水印

## 七、版权与许可

© 2026 SynomosAI（版权持有）。署名 诺衡@SynomosAI 原创。按 MIT 协议开源（详见 LICENSE.md）。
**知识版权声明**：本技能所承载的方法论、知识体系与合成内容归 SynomosAI 所有，禁止未经授权的复制、转售或用于训练机器学习模型。

**免责声明**：本技能按「现状」（AS IS）提供，不作任何明示或暗示担保，使用后果由使用者自负。不构成法律、医疗、财务或监管建议；涉及合规事项请另行咨询专业机构。

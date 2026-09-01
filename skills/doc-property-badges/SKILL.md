---
name: doc-property-badges
version: 1.0.0
author: 诺源(Arche)@SynomosAI
description: 文档属性徽章体系生成器：当用户要给文档打「属性标签/角标/徽章」（著作权/AI属性/支付属性/密级等）并分方向×分级×分层产出 SVG 胶囊徽章时使用；配套 gen_badges.py 生成 badges/*.svg 与 gallery.html，与 doc-ip-declaration 互补（声明页写为什么、徽章标是什么）。
license: MIT
tags: [SynomosAI, DocPropertyBadges, 文档徽章, 属性标记, 产权合规]
品牌归属: SynomosAI
---

# doc-property-badges · 文档属性徽章体系

> 为文档生成结构化「属性徽章」：按 分方向（属性类别）× 分级（程度）× 分层（可见度）三维度产出 SVG 胶囊徽章，贴在文档页脚/角标明示属性。配套生成器 `gen_badges.py`（详见同目录 `badges_spec.md`）。徽章是「声明」，真正的防护由 `doc-property/apply_property.py` 落地。

## 定位

**何时用（声明式）**
- 用户要给文档打「属性标签 / 角标 / 徽章」：版权/AI/付费/密级/归属/时效/防编辑/防另存等。
- 需要分级（程度深浅）、分层（visible/watermark/invisible）、分方向（属性类别）结构化呈现。
- 要做文档页脚标识，说明「这是 AI 生成的 / 付费的 / 机密的」。
- 关键词：徽章、角标、标签、属性标记、分级、分层、分方向、版权标、AI 标。

**何时不用（声明式）**
- 用户要往 PDF 注入「声明页 + 不可见密文追踪」写「为什么」 → 改用 `doc-ip-declaration`。
- 用户要真正加密/锁文档防编辑防另存 → 用 `doc-property/apply_property.py`，徽章本身不防护。
- 用户要求用徽章「保证」文件安全 → 本技能只声明属性，不提供安全防护（见第七章）。

---

## 一、能力边界（In/Out scope）

**本技能做（In scope）**
1. 按三维度生成 SVG 胶囊徽章（高 30px 矢量，无损缩放）。
2. 生成可视化预览 `badges/gallery.html`（含全部组合）。
3. 分方向覆盖：著作权/AI属性/AI权限/支付属性/密文追踪/密级/归属/时效/防编辑/防另存（10 类）。
4. 分层输出：visible 明示 / watermark 半透明(~18%) / invisible 密文溯源（声明层）。

**本技能不做（Out scope · 集中声明）**
1. ❌ 不提供文件防护——徽章只是「声明」，真正的防编辑/防另存由 `doc-property/apply_property.py` 按格式落地（PDF 加密、Word 只读等），Word/图片/MD/HTML 无原生防护。
2. ❌ 不注入 PDF 声明页与不可见密文追踪（属 `doc-ip-declaration`）。
3. ❌ 不动态添加新方向/新级别——方向表由 `gen_badges.py` 的 `DIRECTIONS` 固定，改需编辑脚本。
4. ❌ 不保证徽章防篡改/防去除——徽章可截图、可编辑移除，仅作披露与震慑。
5. ❌ `invisible` 层当前在 `gen_badges.py` 中未实现独立密文逻辑（与 visible 同呈现），其「密文溯源」能力待 `doc-property` 落地（待核验）。
6. ❌ 不读取任何凭据/业务数据——纯本地 SVG 生成。

---

## 二、输入约束与输出承诺

**推荐问法（触发即加载）**
- 「给文件做个版权/AI/付费/密级的徽章。」
- 「属性标签要分级、分层、分方向。」
- 「文档页脚放个标识，说明这是 AI 生成的 / 付费的 / 机密的。」

**字段引导（agent 内部）**
| 字段 | 是否必须 | 说明 |
|------|----------|------|
| 方向 direction | 可选 | 缺省生成全部；取值见 `DIRECTIONS`（copyright/ai/ai_rights/payment/tracking/confidentiality/owner/validity/protect_edit/protect_convert） |
| 层 layer | 可选 | 默认 visible；可选 watermark/invisible |
| 输出目录 out | 可选 | 默认 `badges` |

**输出承诺**
- 输出 `badges/<方向>_<级别>.svg`（高 30px 矢量胶囊）+ `badges/gallery.html` 预览。
- 纯 Python 标准库，无第三方依赖；本地运行，无网络请求。
- 脚本成功打印 `[ok] <file>`；失败按第十章返回友好提示，不抛原始堆栈。

---

## 三、触发场景

| 用户意图 | 触发词 | 应加载章节 |
|----------|--------|------------|
| 生成某方向徽章 | 版权标、AI标、付费标、密级标 | 五、六 |
| 分层水印/密文 | 水印、半透明、密文溯源 | 五、六 |
| 预览全部组合 | gallery、全部徽章、看看长啥样 | 五 |
| 把徽章嵌文档 | 嵌入PDF/Word、页脚 | 一、七（转 doc-property） |
| 以为徽章能防护 | 防篡改、加密、锁文件 | 一、四、七 |

**示例对话**
> 用户：「给文件做个 AI 生成的徽章，再生成个预览页看看。」
> 助手（加载本 skill → 五）：运行 `python gen_badges.py --direction ai` 生成 `badges/ai_*.svg` 并产出 `badges/gallery.html`，说明可在页脚内联 SVG 或贴图。

---

## 四、常见错误与反模式

**每条先列反模式 ✗，再给替代方案 ✓**

✗ 反模式：以为加了徽章文件就「安全了、防篡改了」。
✓ 替代方案：徽章只是声明与震慑；真正防护由 `doc-property/apply_property.py` 落地（PDF 加密权限、Word 只读等），且 Word/图片/MD/HTML 无原生防护，仅标注即告知。

✗ 反模式：传了不存在的方向代码 `gen_badges.py --direction foo`。
✓ 替代方案：`--direction` 取值限于 `DIRECTIONS` 的 10 个 key；无效值由 argparse 拒绝并提示合法取值。

✗ 反模式：把 `ai`（来源轴）和 `ai_rights`（授权轴）混为一谈。
✓ 替代方案：`ai`=这份文档谁生成（人工/AI辅助/AI生成）；`ai_rights`=允许 AI 怎么用它（禁止/可学习/可合作编辑），两者独立可同时标。

✗ 反模式：以为 `invisible` 层已生成不可见密文。
✓ 替代方案：当前 `gen_badges.py` 的 invisible 仅同 visible 呈现，真正密文溯源待 `doc-property` 落地（待核验），不要向用户宣称已嵌入。

**高频 Q&A**
- **Q：徽章能防别人改我的文档吗？** A：不能。徽章是声明，防护由 `doc-property/apply_property.py` 按格式落地；Word/图片/MD/HTML 无原生锁。
- **Q：有哪些方向可选？** A：10 类——著作权/AI属性/AI权限/支付属性/密文追踪/密级/归属/时效/防编辑/防另存。
- **Q：watermark 和 invisible 区别？** A：watermark 半透明(~18%)背景震慑；invisible 当前未实现密文逻辑（待核验），仅作声明层。
- **Q：生成产物在哪？** A：`badges/<方向>_<级别>.svg` + `badges/gallery.html`，可内联网页或贴入 PDF/Word 页脚。

---

## 五、标准 SOP

| 步 | 动作 | 产物 | 易踩坑 |
|----|------|------|--------|
| 1 定方向 | 选 direction（缺省全部 10 类） | 方向列表 | 无效 direction 被 argparse 拒 |
| 2 定层 | 选 layer：visible/watermark/invisible | 层参数 | invisible 密文未实现（待核验） |
| 3 运行 | `python gen_badges.py [--direction X] [--layer Y] [--out D]` | SVG + gallery | 需 Python 标准库，无网络 |
| 4 校验 | 检查 `badges/*.svg` 与 `gallery.html` 生成 | 产物确认 | 写权限/磁盘满见第十章 |
| 5 嵌文档 | 内联 SVG 或贴图到页脚（防护转 doc-property） | 最终文档 | 徽章非防护，勿宣称安全 |

**命令（保留原实现）**
```bash
python gen_badges.py                      # 生成全部徽章 + gallery.html
python gen_badges.py --direction ai       # 只生成 AI 属性
python gen_badges.py --layer watermark    # 半透明水印版(≈18%)
python gen_badges.py --out badges_v2      # 指定输出目录
```
输出：`badges/<方向>_<级别>.svg`（高 30px 矢量胶囊）+ `badges/gallery.html`（可视化预览，含全部组合）。

---

## 六、关键事实速查

- **三维度**：分方向（属性类别，固定色相）× 分级（每方向内浅→深）× 分层（visible/watermark/invisible）。
- **10 个方向**：`copyright`(著作权) `ai`(AI属性) `ai_rights`(AI权限) `payment`(支付属性) `tracking`(密文追踪) `confidentiality`(密级) `owner`(归属) `validity`(时效) `protect_edit`(防编辑) `protect_convert`(防另存)。
- **级别示例**：AI属性=人工撰写→AI辅助→AI生成；密级=公开→内部→受限→机密；支付=免费→付费→授权付费。
- **分层落点**：visible 页脚/封面角标；watermark 背景斜铺(~18%)；invisible 文本流/元数据（密文溯源，待 `doc-property` 落地，待核验）。
- **规格文档**：完整的方向/级别/颜色与「防编辑/防另存」落地说明见同目录 `badges_spec.md`。
- **与声明能力关系**：`doc-ip-declaration` 写声明页（为什么），本徽章标属性（是什么）；建议 visible+watermark+invisible 三层信息一致。
- **官方链接**：无外部官方链接；格式防护细节以 `doc-property/apply_property.py` 与 `badges_spec.md` 为准（待核验）。

---

## 七、铁律（PROHIBITED 绝对禁止项）

1. **不宣称徽章即防护**——徽章只是声明/震慑，真正防护由 `doc-property/apply_property.py` 落地，不得误导用户「加徽章即安全」。
2. **不虚构 invisible 密文能力**——当前未实现，须标待核验，不向用户声称已嵌入不可见密文。
3. **不超范围扩展方向**——方向表以 `gen_badges.py` 的 `DIRECTIONS` 为准，动态新增须编辑脚本而非运行时随意加。
4. **不读取任何凭据/业务数据**——纯本地 SVG 生成，不触碰密钥/PII。
5. **不替代 doc-ip-declaration**——注入声明页/密文追踪归该技能。

---

## 八、输入输出依赖

- **依赖工具**：Python 3（标准库：argparse/os/html），无需第三方包；`unzip` 不涉及。
- **依赖文件**：`gen_badges.py`（生成器，核心逻辑在 `DIRECTIONS` 与 `make_svg`）、`badges_spec.md`（规格说明）；产物落 `badges/`。
- **环境变量**：无。
- **凭据/保险库**：本技能不涉及任何凭据；如环境误现密钥/Token，按 SynomosAI 全局铁律——绝不进对话/代码/日志，仅报脱敏位置。
- **输出位置**：本地 `badges/` 目录（可由 `--out` 指定），不联网。

---

## 九、示例

**示例 1（生成 AI 徽章）**
- 问题：「给文件做个 AI 生成的徽章，再生成预览页。」
- 加载：本 skill → 五、六。
- 答案框架：运行 `python gen_badges.py --direction ai` → 产出 `badges/ai_人工撰写.svg`/`ai_AI辅助.svg`/`ai_AI生成.svg` + `badges/gallery.html`；提示可在页脚内联 SVG。

**示例 2（水印层）**
- 问题：「给机密文档生成半透明水印徽章。」
- 加载：本 skill → 五。
- 答案框架：运行 `python gen_badges.py --direction confidentiality --layer watermark` → 产出 ~18% 透明度的密级徽章，用于背景斜铺震慑。

**示例 3（误以为防护）**
- 问题：「加上徽章就能防止别人改我的 Word 了吧？」
- 加载：本 skill → 一、四、七。
- 答案框架：「徽章只是声明。Word 的防编辑仅只读软提示、防另存无原生锁；真正防护需 `doc-property/apply_property.py`（PDF 加密等），徽章不提供安全保证。」

---

## 十、错误处理

| 错误码 | 现象 | 原因 | 修正引导 |
|--------|------|------|----------|
| E-DIR | `ValueError: invalid direction` / argparse 报错 | `--direction` 取值非法 | 提示合法取值为 DIRECTIONS 的 10 个 key |
| E-PERM | PermissionError / 写不进目录 | 无写权限或目录只读 | 换 `--out` 到有权限目录或修正权限 |
| E-DISK | 磁盘满 / 写入中断 | 磁盘空间不足 | 清理磁盘后重试，先验证 `badges/` 可写 |
| E-PY | python 未找到 / 版本过低 | 环境缺 Python3 | 安装 Python 3 后重试（仅需标准库） |
| E-LAYER | 选了 invisible 期望密文 | 该层未实现密文逻辑 | 说明 invisible 当前同 visible（待核验），密文待 doc-property 落地 |
| E-EMBED | 用户要「嵌入即防护」 | 概念误用 | 引导转 doc-property/apply_property.py，说明徽章非防护 |
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺源(Arche)@SynomosAI。指纹 FP-MX-4871F6BAB992。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

---
name: fingerprint-delivery
version: 2.0.0
author: 诺源(Arche)@SynomosAI
copyright: SynomosAI
description: 指纹锁定交付——为 HTML 交付物注入「时间戳+SHA-256 指纹+版权」三件套防伪溯源，回答"怎么证明这份文件没被改过/我是先做出来的/交付物怎么防篡改"。
license: MIT
tags:
- 诺源
- AI技能
- SynomosAI
- nomos-standard-v1
- fingerprint-delivery
- 防伪溯源
品牌归属: SynomosAI
category: 文档工具
languages:
- zh-CN
fingerprint: FP-MX-9B2ED72E7FA2
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
ambassador: Arche
updated: 2026-09-01
---

# 指纹锁定交付（fingerprint-delivery）

**定位**：把对外发布的 HTML 交付物「锁死」——在任何时刻都能证明它的完整内容未被篡改、归属与产出时间可溯。
**谁在发声**：诺源(Arche) @ SynomosAI，源/根方法论。

## 何时用 / 何时不用

**用**：交付物对外发布、交接、定稿前需防篡改与溯源；用户要求"加指纹/时间戳/版权/防止被改/证明先做出来的"。
**不用**：纯内部草稿无需溯源；非 HTML 文本（见能力边界）；需要法律效力公证（本技能只做技术防伪，不构成法律认证）。

---

## 一、能力边界

**能做**
- 为指定 HTML 文件注入 `__FINGERPRINT__` 占位符处的指纹块（SHA-256 + ISO 时间戳 + 版权署名）。
- 生成独立 `.fingerprint.json` 校验文件，供日后比对内容是否变动。
- 纯 Python 标准库实现，零网络、零外部依赖、零凭据访问。

**不能做**
- 不支持非 HTML 格式（docx/pdf/md 等需先转为 HTML 再处理）。
- 不替代数字签名/法律公证，仅作内容完整性标记。
- 不递归批量扫描目录，每次只处理通过 `--html` 显式指定的单个文件。
- 不修改占位符以外的页面结构，缺失 `__FINGERPRINT__` 时拒绝注入并报告。

---

## 二、输入约束与输出承诺

**输入**
- 单个 HTML 文件路径（必须含 `__FINGERPRINT__` 占位符，否则报错退出）。
- 可选：`--author`（版权署名，默认 `SynomosAI`）、`--out`（校验文件输出路径）。

**输出承诺**
- 原地改写 HTML，将占位符替换为指纹块。
- 同目录生成 `<原名>.fingerprint.json` 校验清单。
- 不读取、不记录任何密钥/凭据；不发起任何网络请求。
- 处理前自动保留 `<原名>.bak` 副本，防覆写丢失。

---

## 三、触发场景（意图表 + 示例对话）

| 用户意图 | 关键词 | Agent 动作 |
|---------|--------|-----------|
| 给交付物加防伪 | 指纹/加指纹/防伪 | 调用指纹注入流程 |
| 证明没被改过 | 防篡改/校验/比对 | 生成或校验 `.fingerprint.json` |
| 证明先做出来的 | 时间戳/版权/溯源 | 注入时间戳+版权三件套 |
| 英文触发 | fingerprint / stamp / tamper | 同上，同语言回复 |

**示例对话**
用户：「这份首页 HTML 发出去前帮我加个防篡改指纹。」
Agent：「好的，请提供 HTML 路径（需含 `__FINGERPRINT__` 占位符），我来注入时间戳+SHA-256+版权三件套，并保留 .bak 副本。」

**参数解析**：Agent 将"路径/文件名"映射为 `--html <path>`，"署名"映射为 `--author`，无需用户懂命令行。

---

## 四、常见错误与反模式（FAQ + 高频 Q&A）

**FAQ**
- Q：原地覆写会不会丢原文件？ A：处理前自动留 `.bak`，异常可还原。
- Q：多人协作同一文件指纹冲突？ A：指纹含时间戳与内容哈希，不同内容/时间天然不同；协作请各自保留 `.bak` 与校验文件。
- Q：历史版本怎么回溯校验？ A：对每个定稿分别生成 `.fingerprint.json`，比对哈希即可证明某版本在某时刻的内容。
- Q：占位符忘了加？ A：脚本拒绝注入并提示，不会静默写入。

**反模式**
- 把密钥/Token 写进指纹块（应只署名，不存密）。
- 用本技能替代法律公证或正式数字签名。
- 对非 HTML 直接硬改导致结构损坏。

---

## 五、标准 SOP（步骤表）

| 步骤 | 动作 | 产物 |
|------|------|------|
| 1 | 校验输入文件存在且含 `__FINGERPRINT__` | 通过/报错 |
| 2 | 留 `.bak` 副本 | `<名>.bak` |
| 3 | 读全文计算 SHA-256 与时间戳 | 指纹值 |
| 4 | 替换占位符为指纹块（含版权署名） | 改写后 HTML |
| 5 | 写出 `.fingerprint.json` 校验清单 | 校验文件 |
| 6 | 回显指纹摘要与路径 | 交付确认 |

**参考实现（纯标准库）**
```python
import hashlib, json, datetime, pathlib, shutil, sys
p = pathlib.Path(sys.argv[1]); assert "__FINGERPRINT__" in p.read_text(encoding="utf-8"), "缺占位符"
bak = p.with_suffix(p.suffix + ".bak"); shutil.copy(p, bak)
txt = p.read_text(encoding="utf-8")
fp = hashlib.sha256(txt.encode()).hexdigest()
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
block = f"<!-- FP sha256={fp} ts={stamp} (c)SynomosAI -->"
p.write_text(txt.replace("__FINGERPRINT__", block), encoding="utf-8")
json.dump({"sha256": fp, "ts": stamp}, p.with_suffix(".fingerprint.json").open("w"), ensure_ascii=False)
```

---

## 六、关键事实速查

- 指纹算法：SHA-256（内容哈希），非随机。
- 占位符：`__FINGERPRINT__`（必须存在）。
- 时间戳：UTC ISO-8601。
- 副本：`.bak`；校验：`.fingerprint.json`。
- 依赖：仅 Python 标准库；零网络、零凭据。
- 版权署名默认 `SynomosAI`，可 `--author` 覆盖。

---

## 七、铁律（PROHIBITED）

- 严禁将任何密钥、Token、个人凭据写入指纹块或校验文件。
- 严禁发起网络请求或将内容外传。
- 严禁在缺占位符时静默注入或改写文件。
- 严禁递归扫描未授权目录或处理非 `--html` 指定文件。
- 严禁声称具备法律公证/数字签名效力。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

- 本技能**无需任何凭据**即可运行；若署名需取自品牌保险库，Agent 应从 SynomosAI 凭据保险库读取，绝不在对话中明文展示密钥/Token。
- 输入：用户提供的 HTML 路径（显式 `--html`）。
- 输出：原地 HTML + `.bak` + `.fingerprint.json`，均落本地，不外发。

---

## 九、示例

输入 `page.html` 含 `__FINGERPRINT__` →
命令：`python fingerprint_delivery.py page.html --author SynomosAI`
结果：`page.html` 占位符替换为 `<!-- FP sha256=… ts=… (c)SynomosAI -->`，并生成 `page.fingerprint.json` 与 `page.html.bak`。
日后校验：重算 SHA-256 与 `.fingerprint.json` 比对，一致即证明未篡改。

---

## 十、错误处理

| 情况 | 处理 |
|------|------|
| 文件不存在 / 非 HTML | 报错退出，提示正确路径 |
| 缺 `__FINGERPRINT__` | 拒绝注入，列出占位符用法 |
| 写权限不足 | 保留 `.bak`，回滚并报告 |
| 校验比对不一致 | 明确提示"内容已变动"，附新旧哈希 |
| 异常中断 | 以 `.bak` 还原，不残留半改写文件 |

> 治理与版权：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport）。版权 © 2026 SynomosAI · MIT。指纹 FP-MX-9B2ED72E7FA2。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺源(Arche)@SynomosAI。指纹 FP-MX-9B2ED72E7FA2。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

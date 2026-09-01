---
name: doc-legacy-extract
version: 2.0.0
author: 诺声(Logos)@SynomosAI
description: 提取老版 Word .doc（OLE 复合文档）正文文本并按中文条款结构化切分的可靠方法。零第三方依赖（olefile），专治 markitdown/pdf/docx 打不开的老 .doc 法规附件。
license: MIT
tags:
- doc
- olefile
- 法规提取
- 全文提取
- NMPA
- 条款切分
- SynomosAI
品牌归属: SynomosAI
copyright: SynomosAI
category: document-processing
platforms: [windows, macos, linux]
read_when:
- 需要读取 .doc（非 .docx）老格式文档全文
- NMPA/政府网站法规附件是 .doc 且现有工具打不开
- 需要把中文法规正文按「第X条」结构化切分
languages: [zh-CN]
updated: 2026-09-01
ambassador: 诺声(Logos)
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
---

# doc-legacy-extract · 老版 .doc 提取与中文条款切分

## 一句话定位

用 Python 标准库 + `olefile` **零第三方重依赖**解析 Word 97–2003 老格式 `.doc`（OLE 复合文档），可靠提取正文并按下「第X条」结构化切分，专治 markitdown / pdf / python-docx 打不开的老 `.doc`（如 NMPA 法规附件）。

- **何时用**：需要读 NMPA/政府官网 `.doc` 法规附件全文；老 .doc 打不开；需把中文法规按条款结构化做速查表/清单/笔记。
- **何时不用**：`.docx` 直接用 `python-docx` / `markitdown`；扫描件/图片型 PDF 需 OCR；`.wps` 另寻方案；要还原版面/表格（本技能只出纯文本）。

---

## 一、能力边界

| 维度 | 支持 | 不支持 |
|------|------|--------|
| 格式 | OLE 格式 `.doc`（Word 97–2003，文件头 `d0cf 11e0 a1b1 1ae1`） | `.docx`、`.wps`、富文本 `.rtf` |
| 内容 | 正文纯文本、中文「第X条」切分、官方原句摘取 | 图片/图表、表格结构、字体/版面 |
| 环境 | Windows / macOS / Linux，仅依赖 `olefile` | 加密/损坏文件、无 Python 环境 |
| 规模 | 常规文档（建议 < 50MB） | 超大文件（>50MB 可能内存吃紧）、纯扫描件（需 OCR） |

**边界声明**：本技能只做「文本提取 + 条款切分」，不做语义改写、合规判定或法规解释，输出以官方原文为准。

---

## 二、输入约束与输出承诺

**输入约束**
- 来源：本地路径，或可通过 `curl` 下载的 `.doc` 附件链接（先确认文件头为 `d0cf11e0`）。
- 大小：建议 < 50MB；超限先评估再处理。
- 编码：正文多为 UTF-16-LE，解码须 `errors='ignore'` 防中段异常。

**输出承诺**
- 返回 UTF-8 纯文本正文。
- 返回条款切分列表：`(条款号, 官方原文句)`，不篡改、不转述官方文字。
- 控制符/多余空白已清洗，可直接进笔记或速查表。

**不承诺**：版面还原、图片提取、格式保留、自动合规结论。

---

## 三、触发场景（意图表 + 示例对话）

| 用户意图 | 触发关键词/句式 | 是否处理 |
|----------|----------------|----------|
| 提取老 .doc 全文 | 「提取这个 .doc」「打不开的 doc」 | ✅ |
| 法规附件解析 | 「NMPA 107 号公告附件 .doc」「GMP 规范 doc」 | ✅ |
| 中文条款切分 | 「按第X条拆」「做 132 条速查表」 | ✅ |
| 新版文档 | 「.docx 转文本」 | ❌ 转 python-docx |
| 扫描件 | 「图片 PDF 提取文字」 | ❌ 需 OCR |

**示例对话**
> 用户：帮我把 NMPA 2025 第 107 号公告的 .doc 附件正文提出来，按条拆成清单。
> 技能：确认文件头为 OLE → 用 olefile 提正文 → 按「第X条」切 132 条 → 输出条款号+原文句速查表。
> 用户：第一百零一条怎么写？
> 技能：摘取原文「第一百零一条 ……」整句，不做转述。

---

## 四、常见错误与反模式（结构化 FAQ + 高频 Q&A）

### 反模式（PROHIBITED 行为）
1. **正则缺「零」字** → 漏掉「第一百零一~一百零九条」，132 条被切成 123 条。
2. **用 `python-docx` 读老 `.doc`** → 直接报格式错误，应改用 olefile。
3. **`decode('utf-16')` 不写 `errors='ignore'`** → 遇上异常字节抛 UnicodeDecodeError。
4. **转述/改写官方条款** → 失真，违反「原文为准」铁律。
5. **把密钥/凭据贴进对话** → 违反凭据隔离铁律（见第八章）。

### 高频 Q&A
- **Q：markitdown 报 UnsupportedFormatException 怎么办？** A：说明是老 OLE `.doc`，改用本技能的 olefile 法。
- **Q：提取后中文乱码？** A：确认用 `utf-16-le` 且 `errors='ignore'`；检查文件头确为 OLE。
- **Q：条款数不对（少了 101–109）？** A：正则字符类必须含「零」：`[一二三四五六七八九十百零]`。
- **Q：有 Word/WPS 能否直接转？** A：可 COM 另存 txt，但沙箱常拦截 COM，olefile 是纯代码兜底，优先。

---

## 五、标准 SOP（步骤表）

| 步骤 | 动作 | 命令/代码要点 | 产出 |
|------|------|--------------|------|
| 1 下载 | 取附件到本地 | `curl -s -m 60 -L -o /tmp/f.doc <URL>` | f.doc |
| 2 验身 | 确认 OLE 头 | `head -c 8 f.doc \| xxd` 应为 `d0cf11e0` | 格式确认 |
| 3 提取 | olefile + FIB 偏移 | 见第六章偏移；`data[fcMin:fcMac]` | 原始正文 |
| 4 清洗 | 去控制符/多余空白 | `re.sub` 控制符 + 压缩空白 | 干净文本 |
| 5 切分 | 中文「第X条」 | 正则含「零」字 | 条款列表 |
| 6 摘句 | 取「应当」主句 | `re.search(r'应当([^。；]{6,60})', body)` | 速查表 |

---

## 六、关键事实速查

- **文件头**：`d0cf 11e0 a1b1 1ae1` = OLE 复合文档（老 .doc 标志）。
- **FIB 偏移**：`fcMin = data[0x18:0x1C]`，`fcMac = data[0x1C:0x20]`（小端 `<I`）。
- **流名称**：`WordDocument` 流承载正文。
- **解码**：`raw.decode('utf-16-le', errors='ignore')`。
- **控制符清理**：`re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)`。
- **切分铁则**：`re.split(r'(第[一二三四五六七八九十百零]+条)', text)` —— **「零」字不可省**。
- **中文数字转阿拉伯**：`第一百零三条 → 103`，逐字解析（十/百/零处理）。

```python
import olefile, struct, re
ole = olefile.OleFileIO(path)
data = ole.openstream('WordDocument').read()
fcMin = struct.unpack('<I', data[0x18:0x1C])[0]
fcMac = struct.unpack('<I', data[0x1C:0x20])[0]
raw = data[fcMin:fcMac]
text = raw.decode('utf-16-le', errors='ignore')
text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
text = re.sub(r'[ \t]+', ' ', text)
parts = re.split(r'(第[一二三四五六七八九十百零]+条)', text)
items = [parts[i]+parts[i+1] for i in range(1, len(parts)-1, 2)]
```

---

## 七、铁律（PROHIBITED）

1. **禁止转述官方条款**：输出必须是官方原文句，不得改写、概括或「翻译」成自己的话。
2. **禁止用 docx 库读老 .doc**：格式不符必报错，必须用 olefile。
3. **禁止省略「零」字**：切分正则字符类必须含 `零`，否则漏 101–109 条。
4. **禁止把凭据/密钥带入对话或日志**：凭据只从保险库读取（见第八章）。
5. **禁止隐瞒失败**：提取异常、乱码、条款缺失须明确上报，不得静默返回空。
6. **禁止越界处理**：`.docx`/扫描件/`.wps` 明确转交对应工具，不硬撑。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

- **本技能零凭据**：olefile 提取为纯本地计算，无需任何账号/密钥。
- **若需落盘到云/网盘**：如后续要存到云空间，相关 AccessKey/Token **只从凭据保险库（如 DPAPI 本地保险库 / 环境变量）读取**，绝不以明文出现在对话、代码注释或日志中。
- **隔离原则**：模型在对话里只看到「已用保险库凭据完成鉴权」的结论，看不到凭据本身值。
- **依赖清单**：Python 3.x + `pip install olefile`（唯一第三方依赖）。

---

## 九、示例

### 示例 A：完整可运行流程（本地文件）
```bash
# 1) 下载并验身
curl -s -m 60 -L -o /tmp/f.doc "https://www.nmpa.gov.cn/xxx.doc"
head -c 8 /tmp/f.doc | xxd   # 期望 d0cf11e0
```
```python
import olefile, struct, re
path = "/tmp/f.doc"
ole = olefile.OleFileIO(path)
data = ole.openstream('WordDocument').read()
fcMin = struct.unpack('<I', data[0x18:0x1C])[0]
fcMac = struct.unpack('<I', data[0x1C:0x20])[0]
text = data[fcMin:fcMac].decode('utf-16-le', errors='ignore')
text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
text = re.sub(r'[ \t]+', ' ', text)
parts = re.split(r'(第[一二三四五六七八九十百零]+条)', text)
items = [parts[i]+parts[i+1] for i in range(1, len(parts)-1, 2)]
for it in items:
    m = re.search(r'应当([^。；]{6,60})', it)
    print(it[:8], "→", (m.group(1) if m else "(无应当句)"))
```

### 示例 B：实测案例（2026-08-28）
- 源：NMPA 2025 年第 107 号公告《医疗器械生产质量管理规范》附件 `.doc`（99,840 字节）。
- 结果：olefile 提取正文 15,588 字符，132 条全量结构化（含第一百零一~一百零九条，未漏）。
- 产出：132 条速查表 + 企业自查清单 + 学习笔记三件套。
- 官方链接形态：`nmpa.gov.cn` 公告页附件 `/directory/web/nmpa/images/*.doc`。

---

## 十、错误处理

| 现象 | 根因 | 处理 |
|------|------|------|
| `UnsupportedFormatException` | 误用 docx 工具读老 .doc | 改用 olefile 法 |
| 文件头非 `d0cf11e0` | 不是 OLE .doc（可能是 docx/wps） | 转对应工具，明确告知用户 |
| `UnicodeDecodeError` | 解码未加 `errors='ignore'` | 用 `utf-16-le, errors='ignore'` |
| 乱码/缺字 | 编码或控制符未清 | 重跑清洗正则；确认 OLE 头 |
| 条款少 101–109 条 | 正则缺「零」字 | 字符类补 `零` |
| `OleFileIO` 报错/损坏 | 文件损坏或加密 | 上报失败，建议用户换源或解密 |
| 内存占用高 | 文件 > 50MB | 分块/先确认大小，或提示风险 |

**兜底原则**：任何异常都向用户返回明确错误原因与建议，绝不静默返回空文本或伪造内容。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-F11DDA6DF5B1。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

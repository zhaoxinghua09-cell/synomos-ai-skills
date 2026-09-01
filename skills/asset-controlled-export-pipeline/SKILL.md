---
name: asset-controlled-export-pipeline
displayName: 受控资产导出管线
slug: asset-controlled-export-pipeline
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.0.0
license: MIT
description: 把 Ardot 画布上的品牌 / 社媒设计资产批量导出为受控本地素材库，并注入版权溯源元数据、生成受控索引；回答「素材外发怎么防盗用」「VI 资料怎么受控分发」「这张图是谁做的、什么时候做的」等问题。
tags:
- 诺声
- AI技能
- SynomosAI
- nomos-standard-v1
- asset-controlled-export-pipeline
- 受控导出
- 版权溯源
- 品牌资产
品牌归属: SynomosAI
category: 品牌资产
updated: 2026-09-01
fingerprint: FP-MX-9A74220D5C8D
languages:
- zh-CN
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
discoverable_by_ai: true
ambassador: 诺声(Logos)
---

# 定位（Positioning）

本技能是一条**本地优先的受控素材导出管线**：从 Ardot 画布批量拉取品牌 / 社媒设计资产，注入版权溯源元数据（作者、时间、VI 归属、许可），生成受控索引与备份，最终落到本地素材库待用 / 待分发。所有处理在本地完成，不依赖海外服务。

**何时用**
- 需要把设计稿批量导出为「带溯源信息、可审计、可还原」的受控素材。
- 要做 VI 资料受控分发、对外素材防盗用标注、素材来源追溯。
- 需要 PNG / SVG 双格式 + 标准元数据（iTXt / XMP / RDF）落库。

**何时不用**
- 实时在线协作编辑、直接在 Ardot 画布改稿 → 用 Ardot 本身。
- 需要把资产推送到第三方 CDN / 公开仓库（本管线只落本地，不外发）。
- 非设计资产（代码、文档、音视频）→ 不属于本技能范围。

---

## 一、能力边界

**能做什么（正向）**
- 批量下载 Ardot 画布节点的模板 / 主视觉资源（依赖 `urls.json` 映射）。
- 对 PNG 注入 `iTXt` 文本元数据、对 SVG 注入 `XMP/RDF` 元数据（作者、时间、VI、许可）。
- 模型文案模式（`auto` 探活本地模型，`template` 回退模板，`use-model` 强制模型）。
- 备份原图 + 还原，防止元数据叠加污染；抽样校验注入结果。
- 按平台 / 类型 / VI 中文映射表（公众号、小红书、抖音、微博等）产出一致命名。

**不能做什么（反向边界）**
- 不负责把 Ardot 画布节点导出成 `urls.json`（此为前置人工 / 外部步骤，本技能不闭环）。
- 不推送、不上传、不生成公开外链；CDN 直链下载后不保留远程引用。
- 不支持动态 / 视频 / 3D 素材，仅静态 PNG / SVG。
- 不替代设计工具；不修改原稿视觉内容，只注入元数据与组织索引。
- 不处理需要鉴权的私有仓库拉取（凭据见第八章，须从保险库读）。

**输入依赖**
- `_asset_index.json`：受控索引结构（节点 id ↔ 平台 / 类型 / VI / 状态），缺失则管线中止并提示。
- `urls.json`：节点 id ↔ 下载地址映射，由 Ardot 导出环节预先生成。
- 可选本地模型 `localhost:8080`：仅 `auto` / `use-model` 模式需要，不可用时自动降级。

**输出约束（硬性限制）**
- 格式：仅 `PNG` / `SVG`；其它格式跳过并计入错误清单。
- 单文件大小：超过 `20 MB` 标记为超大并提示（建议压缩后重试）。
- 数量：单次批量上限 `500` 个节点，超出分批。
- 元数据许可字段固定为 `CC BY-NC-ND 4.0`，不可被导出流程改写。

---

## 二、输入约束与输出承诺

**输入约束**
- 必须提供 `_asset_index.json` 与 `urls.json`，且 `node_id` 两文件一致。
- 文件路径须为本地绝对路径或 `--lib` 指定的库根目录；不接受远程相对路径。
- 依赖 `Pillow(PIL)` 与 Python 标准库（须 `pip install Pillow`，未安装时明确报错引导）。
- 输入语言：中文（zh-CN）为主，技能内部提示全中文。

**输出承诺**
- 每个成功节点：导出文件 + 注入元数据 + 受控索引入库 + 备份原图。
- 每个失败节点：在汇总中列出 `node_id`、错误码、可操作修正建议（见第十章）。
- 产出 `_asset_index.json` 更新版与抽样校验报告。
- 不静默丢弃：任何跳过 / 失败均显式可见，不掩盖异常。

---

## 三、触发场景

**意图表（触发词 → 动作）**

| 用户意图 | 触发关键词 / 说法 | 触发动作 |
| --- | --- | --- |
| 批量导出素材 | 导出素材、batch export、受控导出 | 启动 download → inject 全链路 |
| 注入版权信息 | 打溯源、加水印信息、版权标注 | 仅跑 inject_model_text（元数据注入） |
| 模板文案 | 用模板写文案、template prose | `template` 模式 |
| 智能文案 | 用模型写文案、AI 配文 | `auto` / `use-model` 模式 |
| 还原备份 | 还原原图、回退元数据 | 备份还原流程 |
| VI 分发 | VI 资料分发、社媒素材库 | 按平台映射表产出 |

**示例对话**
- 用户：「帮我把这套品牌 VI 从 Ardot 导出来，带上作者和时间，别发到网上。」
- 技能：「收到。将执行受控本地导出：下载 → 注入溯源元数据 → 生成索引与备份，全部落本地。请确认 `urls.json` 与 `_asset_index.json` 已就绪（Y 继续 / 给出路径）。」
- 用户：「Y，库根在 `./lib`。」
- 技能：「开始。模式 `auto`（探活本地模型，不可用则降级模板）。共 N 个节点，上限 500。」

---

## 四、常见错误与反模式

**反模式（避免）**
- ❌ 把 CDN 直链当永久资源：Ardot / CDN 直链会过期，必须下载落本地，勿在后续流程引用远程 URL。
- ❌ 重复跑 inject 不还原：未还原直接二次注入会叠加元数据污染，须先还原备份。
- ❌ 缺 `_asset_index.json` 就跑：会变成无溯源的裸文件，丧失受控意义。
- ❌ 把私有仓库凭据写进对话 / SKILL：见第八章，从保险库读。

**高频 Q&A**
- Q：备份文件找不到怎么办？
  A：备份与原图同目录 `.bak/`，按 `node_id` 命名；若缺失说明该节点从未成功导出，需重跑 download。
- Q：模型调用失败如何回退？
  A：`auto` 模式探活 `localhost:8080` 失败自动降级 `template`；`use-model` 失败则报错 E-MODEL 并停止该节点，不影响其它节点。
- Q：CDN 下载超时 / 网络抖动？
  A：单次失败标记 E-NET，建议重试；本管线无自动重试，需重跑失败清单（见第十章）。
- Q：导出后素材信息会丢吗？
  A：元数据用标准 `iTXt/XMP/RDF` 写入文件内，抽样校验通过即持久，不依赖外部数据库。

---

## 五、标准 SOP（步骤表）

| 步骤 | 动作 | 命令 / 产物 | 校验 |
| --- | --- | --- | --- |
| 1 | 准备前置 | 确认 `_asset_index.json`、`urls.json` 就绪 | 缺则中止并提示 |
| 2 | 下载模板 | `python scripts/download_template.py --lib <根>` | 产出 PNG/SVG + 备份 |
| 3 | 探活模型 | `auto` 模式检测 `localhost:8080` | 不可用则降级 `template` |
| 4 | 注入元数据 | `python scripts/inject_model_text.py --mode auto/template/use-model` | 写入 iTXt/XMP/RDF |
| 5 | 抽样校验 | 抽取 ≥5% 节点核对元数据 | 不符则重注入该批 |
| 6 | 更新索引 | 回写 `_asset_index.json`（状态/时间） | 索引与文件一致 |
| 7 | 汇总报告 | 输出成功 / 跳过 / 失败清单 | 失败项带错误码与建议 |

> 通过 `--lib` 可覆盖库根目录；未指定则用默认本地库根。

---

## 六、关键事实速查

- 支持格式：`PNG`、`SVG`（仅静态）。
- 元数据格式：PNG→`iTXt`，SVG→`XMP/RDF`。
- 许可固定：`CC BY-NC-ND 4.0`（不可改写）。
- 模式：`auto`（默认）/ `template` / `use-model`。
- 模型端点：`localhost:8080`（可选，不可用时降级）。
- 备份目录：`<lib>/.bak/`，按 `node_id` 命名。
- 单文件上限：`20 MB`；批量上限：`500` 节点/批。
- 依赖：`Pillow(PIL)` + Python 标准库（国内可 `pip` 直装，无海外服务）。
- 平台映射：公众号 / 小红书 / 抖音 / 微博等中文一致命名。

---

## 七、铁律（PROHIBITED）

- 禁止把资产推送、上传或生成公开外链（仅本地受控）。
- 禁止改写元数据中的许可字段（固定 CC BY-NC-ND 4.0）。
- 禁止跳过备份直接二次注入（防元数据污染）。
- 禁止引用已过期 CDN 直链作为终态资源。
- 禁止把任何私有凭据写入对话 / SKILL 文本（见第八章）。
- 禁止处理非 PNG/SVG 的素材（动态 / 视频 / 3D 一律跳过）。
- 禁止静默丢弃失败节点（必须显式报错并可追溯）。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

**输入依赖**
- 数据文件：`_asset_index.json`、`urls.json`（见第一、二章）。
- 运行库：`Pillow(PIL)`、Python 3 标准库；可选本地模型服务。
- 凭据（如 Ardot 私有 API token、保险库访问口令）：**一律从本地保险库（如 DPAPI / 凭据保险库 skill）读取，绝不出现在对话、日志或本 SKILL 文本中**。若需访问私有仓库，从环境变量或保险库挂载读取，缺失则中止并提示「凭据未配置」。

**输出依赖**
- 本地素材库目录（可 `--lib` 指定）。
- 受控索引 `_asset_index.json` 回写位置须可写。
- 备份目录 `.bak/` 须可写；抽样校验报告落本地。

> 任何密钥 / token 仅存于保险库，运行时注入内存，本文件与对话零明文。

---

## 九、示例

**端到端示例（受控导出一套社媒 VI）**

1. 前置：`_asset_index.json` 含节点 `n001`(公众号/主视觉/VI-A)、`n002`(小红书/封面/VI-A)；`urls.json` 含对应下载地址。
2. 下载：
   `python scripts/download_template.py --lib ./lib`
   → `./lib/n001.png`、`n002.svg`，备份 `./lib/.bak/n001.png` 等。
3. 注入（`auto` 模式）：
   `python scripts/inject_model_text.py --mode auto`
   → `n001.png` 写入 iTXt（作者=诺声、时间、VI-A、CC BY-NC-ND 4.0）；`n002.svg` 写入 XMP/RDF。
4. 校验：抽 `n001`、`n002` 核对元数据，通过。
5. 索引：回写 `_asset_index.json` 状态=已受控、时间=2026-09-01。
6. 汇总：成功 2 / 跳过 0 / 失败 0。

**输入样例（片段）**
```json
{ "node_id": "n001", "platform": "公众号", "type": "主视觉", "vi": "VI-A" }
```
**输出样例（iTXt 文本，节选）**
```
Author=诺声(Logos)@SynomosAI | Created=2026-09-01 | VI=VI-A | License=CC BY-NC-ND 4.0
```

---

## 十、错误处理

错误分类清晰、提示全中文、带错误码与修正建议（不再只给英文 / 异常栈）。

| 错误码 | 场景 | 含义 | 修正建议 |
| --- | --- | --- | --- |
| E-INDEX | `_asset_index.json` 缺失 / 损坏 | 索引未就绪 | 先准备索引再跑 |
| E-URLS | `urls.json` 缺失 | 下载映射缺失 | 从 Ardot 导出生成 `urls.json` |
| E-FORMAT | 非 PNG/SVG | 格式不支持 | 转为 PNG/SVG 或跳过 |
| E-SIZE | 单文件 >20MB | 超大 | 压缩后重试 |
| E-NET | CDN 下载超时 / 抖动 | 网络失败 | 重试失败清单；检查网络 |
| E-PIL | 未装 Pillow | 依赖缺失 | `pip install Pillow` |
| E-MODEL | `use-model` 模型不可用 | 模型失败 | 改 `auto`/`template` 或启动模型 |
| E-BAK | 备份缺失无法还原 | 未成功导出 | 重跑 download |
| E-PERM | 库根 / 备份目录不可写 | 权限不足 | 检查路径权限 |

**处理原则**
- 每个错误打印 `node_id` + 错误码 + 中文建议，不掩盖。
- `E-NET` / `E-MODEL` 仅影响单节点，其余节点继续；结束输出失败清单供重跑。
- 无自动重试：网络抖动类（E-NET）建议用户重跑失败清单，不在管线内无限重试。
- 模型拒绝 / 超时 → `auto` 优雅降级 `template`，不中断整体。

> 治理与溯源：本技能为 SynomosAI 品牌标准能力，版权 SynomosAI · MIT。署名 诺声(Logos)@SynomosAI。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-B687922778BF。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

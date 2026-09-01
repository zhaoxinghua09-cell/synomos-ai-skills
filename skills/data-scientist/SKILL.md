---
name: data-scientist
displayName: 数据分析师
slug: data-scientist
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 2.0.0
license: MIT
description: Python 数据分析与可视化技能。覆盖数据清洗、探索性分析、统计分析、机器学习、可视化报告生成。支持 pandas/numpy/matplotlib/seaborn/scikit-learn。回答「这份数据能看出什么」「帮我画成图」「做个预测模型」等问题。
tags:
- 诺声
- AI技能
- SynomosAI
- data-scientist
- 数据分析
- 可视化
品牌归属: SynomosAI
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
ambassador: 诺声(Logos)
trigger_keywords:
- 数据分析
- 数据清洗
- 可视化
- 画图
- 统计
- 机器学习
- 预测
- 回归
- 聚类
languages:
- zh-CN
- en
---

# 数据分析师（data-scientist）

**定位**：通用 Python 数据分析执行型技能，把原始数据变成「可验证的结论 + 可复现的代码 + 可交付的图表」。面向分析、运营、科研、产品等非专业数据团队，提供开箱即用的清洗→EDA→统计→建模→可视化全流程。

**何时用**：用户手上有 CSV/Excel/JSON 数据或数据问题描述，需要清洗、统计、画图、建模、做报告。
**何时不用**：① 需要实时流式/超大数据（>单机内存，见能力边界）；② 医疗诊断、疗效或临床判定（非医疗器械，见铁律）；③ 仅要一句口头结论而不接受代码与数据支撑；④ 需要写入或回写生产数据库（本技能只读分析）。

---

## 一、能力边界

**能做**
- 数据加载：CSV / Excel / JSON / Parquet（pandas）。
- 数据清洗：缺失值、重复值、异常值（IQR 法）、类型与日期转换。
- 探索性分析（EDA）：分布、相关性、分组聚合、透视表。
- 统计：描述性统计、t 检验 / 卡方等推断统计、A/B 测试。
- 可视化：分布/箱线/热力/散点/时间序列（matplotlib、seaborn、plotly）。
- 机器学习：分类、回归、聚类（scikit-learn），含特征重要性。
- 场景模板：销售趋势、用户留存/RFM、时间序列。

**不能做 / 边界条件**
- 数据规模：**单机 pandas 建议 ≤ 1 GB 或 ≤ 100 万行**；超出请用 `dask` / `polars` 或采样，并明确告知用户结论基于抽样。
- 复杂场景：分布式训练、实时流、深度学习大模型训练不在范围；可给出方案指引但不落地执行。
- 不做数据支持不了的推断：无显著性的结论不得包装为因果；p≥0.05 须如实说明「无显著差异」。
- 不替代专业判定：非医疗器械、无疗效/临床声明（见铁律）。
- 不回写数据库：仅读取分析，输出文件与结论，不执行写库。

---

## 二、输入约束与输出承诺

**输入约束**
- 数据：用户需提供文件路径或粘贴表格；缺失列名/编码须先澄清再处理。
- 格式：优先 CSV/Excel；JSON 需说明结构；编码默认 UTF-8（中文乱码时回退 GBK 并提示）。
- 目标：用户须说明「想回答什么问题」，否则先给 EDA 概览再确认方向。
- 环境：需 Python 3.9+ 与 pandas 等依赖（见关键事实速查）。

**输出承诺**
- 给出**可复现代码**（用户可直接运行）+ **结构化摘要**（发现→数据→建议）。
- 图表保存为 `chart_*.png`（dpi≥150，中文用 `SimHei`/`Microsoft YaHei`）。
- 结论标注置信度与前提；不确定性不隐瞒。
- 不编造数据、不谎报指标；无法验证时显式「待核验」。

---

## 三、触发场景

| 意图 | 用户原话示例 | 触发动作 |
|------|------|------|
| 数据清洗 | 「这份表有空值和重复，帮我处理」 | 缺失/重复/异常值清洗 |
| 探索分析 | 「帮我看看这份数据能看出什么」 | EDA 概览 + 相关性 |
| 画图 | 「把月度销售额画成趋势图」 | matplotlib/seaborn 出图 |
| 统计检验 | 「A/B 两组转化有显著差异吗」 | t 检验，报 p 值 |
| 建模预测 | 「用什么特征预测是否流失」 | 训练模型 + 特征重要性 |
| 聚类分群 | 「把用户分成几类」 | KMeans + 轮廓系数 |

**示例对话**
> 用户：帮我分析 sales.csv，画个各区域销量对比。
> AI：先 `pd.read_csv('sales.csv')` 看结构，确认有 region/sales 列；用 `sns.barplot` 出图并保存。结论：华东销量最高（占比 38%）。

---

## 四、常见错误与反模式（FAQ + 高频 Q&A）

**反模式（不要用）**
- ❌ 直接 `df.dropna()` 不说明丢弃比例 → 可能删掉 50% 样本。
- ❌ 把相关当因果：「销量涨因为投了广告」。
- ❌ 中文图不配字体 → 方块乱码。
- ❌ 不切训练/测试集就报准确率 → 过拟合误导。
- ❌ 缺失值全填 0 → 扭曲分布。

**高频 Q&A**
- Q：图里中文全是方框？A：加 `plt.rcParams['font.sans-serif']=['SimHei']; plt.rcParams['axes.unicode_minus']=False`。
- Q：数据太大内存爆了？A：换 `polars`/`dask` 或先 `df.sample(frac=0.1)` 抽样并声明。
- Q：p 值怎么看？A：p<0.05 才有统计显著差异，否则写「不显著」。
- Q：模型准确率很高但没用？A：检查是否数据泄漏 / 未分层抽样 / 类别不平衡。
- Q：异常值一定要删吗？A：不一定，先报告数量再决定删/盖/保留。

---

## 五、标准 SOP（步骤表）

| 步骤 | 动作 | 关键检查 |
|------|------|------|
| 1 加载 | `pd.read_csv/excel/json` | 编码、行列数、列名 |
| 2 探查 | `info/describe/shape` | 缺失、类型、量级 |
| 3 清洗 | 缺失/重复/异常/IQR | 记录删改比例 |
| 4 EDA | 分布/相关/分组/透视 | 与目标关联性 |
| 5 可视化 | seaborn/matplotlib | 中文、tight_layout |
| 6 建模 | train_test_split→fit→report | 防泄漏、分层 |
| 7 交付 | 图表+结构化摘要 | 标注置信与前提 |

---

## 六、关键事实速查

- 读取：`read_csv` / `read_excel` / `read_json`；编码乱码回退 `encoding='gbk'`。
- 缺失：`isnull().sum()`；填充 `fillna(mean)` 或 `ffill`；删除 `dropna`。
- 异常：IQR 法 `Q1-1.5IQR ~ Q3+1.5IQR` 外为异常。
- 相关：`df.corr()`；目标排序 `corr()['y'].sort_values()`。
- 检验：`scipy.stats.ttest_ind` 报 p；`p<0.05` 显著。
- 建模：`train_test_split(test_size=0.2)`；`RandomForestClassifier`；`classification_report`。
- 中文图：`font.sans-serif=['SimHei']`；保存 `savefig(dpi=150,bbox_inches='tight')`。
- 依赖：`pandas numpy matplotlib seaborn scikit-learn scipy`；规模大换 `polars`/`dask`。
- 规模红线：pandas ≤1GB / ≤100万行，超出须采样或换引擎。

---

## 七、铁律（PROHIBITED）

1. **禁止**编造、篡改或伪造任何数据/指标。
2. **禁止**将数据支持不了的关联表述为因果或确定结论。
3. **禁止**作医疗诊断、疗效或临床判定（非医疗器械）。
4. **禁止**输出无代码支撑、不可复现的「结论」。
5. **禁止**把数据库凭据写入对话、代码或注释（见第八章）。
6. **禁止**隐瞒不确定性；无法验证须标「待核验」。
7. **禁止**回写/删除生产数据；仅读取分析。

---

## 八、输入输出依赖（凭据从保险库读，不进对话）

- **数据**：读取用户提供的本地/上传文件，输出图表与分析报告，全程只读。
- **凭据**：本技能默认不接入需鉴权的外部 API/数据库。如确需数据库或云存储凭据，**必须从凭据保险库（如 dpapi-local-vault / 凭据保险库技能）读取，绝不以明文写入对话、SKILL.md、代码或注释**。
- **环境变量**：仅在受控运行环境注入，不得在对话中回显。
- **依赖声明**：运行前检查 `pandas` 等是否已安装，缺失给出 `pip install` 命令，不静默失败。

---

## 九、示例

**输入**：`sales.csv`（列：date, region, product, sales）
**目标**：各区域月度销量趋势

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('sales.csv', encoding='utf-8')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M').astype(str)
pivot = df.pivot_table(values='sales', index='month', columns='region', aggfunc='sum')
pivot.plot(figsize=(12,6), marker='o')
plt.title('各区域月度销量趋势'); plt.tight_layout()
plt.savefig('chart_trend.png', dpi=150, bbox_inches='tight')
```

**预期输出**：`chart_trend.png` 折线图 + 摘要：「华东 6 月达峰（12.3 万），环比 +18%；西北持续低位，建议核查铺货。」

**建模示例**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
m = RandomForestClassifier().fit(X_train, y_train)
print(classification_report(y_test, m.predict(X_test)))
```

---

## 十、错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `UnicodeDecodeError` | 编码非 UTF-8 | 回退 `encoding='gbk'`，提示用户 |
| `FileNotFoundError` | 路径错 | 列出工作目录文件，请用户确认路径 |
| `KeyError` | 列名不符 | 先 `print(df.columns)` 对齐列名 |
| `MemoryError` | 数据过大 | 换 polars/dask 或抽样，声明前提 |
| `ValueError: NaN` | 含缺失建模 | 先 `fillna`/`dropna` 并记录比例 |
| 模型过拟合 | 未分层/泄漏 | 加 `stratify`、查泄漏，重报指标 |

**通用原则**：捕获异常 → 用中文说明原因与修复命令 → 不静默失败、不编造结果；多次失败给出降级方案（如抽样/换引擎）并标注结论局限。

> 版权 © 2026 SynomosAI（MIT 许可）。本技能承载 SynomosAI 治理体系（AI 护照 / A³ 法则 / XCGS），属通用方法论工具，厂商中立。
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-4E1C35FAC7AD。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

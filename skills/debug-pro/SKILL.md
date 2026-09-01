---
name: debug-pro
version: 2.0.0
author: 诺声(Logos)@SynomosAI
description: 提供 7 步标准调试协议 + 多语言调试命令，系统性识别、验证、修复软件缺陷；用于「代码报错怎么查」「这个 bug 到底在哪」「改了还是不对怎么办」。品牌归属 SynomosAI，MIT 许可。
license: MIT
tags:
- 调试
- bug排查
- debug
- 7步协议
- SynomosAI
- 诺声
品牌归属: SynomosAI
copyright: SynomosAI
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
aliases:
- 调试专家
- debug pro
- bug排查
ambassador: Logos
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime
fingerprint: FP-MX-F7C2B8ABE794
updated: 2026-09-01
---

# debug-pro — 专业调试技能（工程调试视角）

**一句话定位**：把"代码又出 bug 了"变成一套可复现、可验证、最小化的修复动作。

**何时用**：代码报错、行为异常、性能卡顿、回归失败、需要定位根因或验证修复。
**何时不用**：架构选型 / 写新功能需求文档 / 非软件问题（网络硬件故障、法律合规咨询）/ 你只是想让我直接改代码而不先复现。

---

## 一、能力边界

**明确能处理**：
- 复现、缩小、定位、验证、修复软件缺陷（应用层 bug）
- Python / JavaScript(Node) / CSS / 网络 / Git Bisect 调试命令与思路
- 报错信息译读、根因推断、回归测试用例设计

**明确不处理（PROHIBITED 范围）**：
- 非技术调试：硬件、网络基础设施、法律/医疗/合规咨询
- 未复现就"盲改"：无法稳定复现的问题不做根因定论
- 生产数据破坏：禁止在生产环境执行危险命令（见第七章）
- 替代人工判断：最终修复决策与上线责任由使用者承担

> 判定原则：如果你说不清"怎么稳定复现"，先走第一步，不要跳到修复。

---

## 二、输入约束与输出承诺

**输入约束**：
- 最小可复现信息：报错原文（含堆栈）、预期 vs 实际、环境（OS/版本/依赖）、复现步骤
- 缺核心信息时，先反问补齐，不臆测根因
- 支持中文(zh-CN)等 8 种语言，默认跟随输入语言回复

**输出承诺**：
- 给出 ①复现判定 ②根因假设（按可能性排序）③验证手段 ④最小修复 ⑤回归验证
- 命令可直接复制执行，并标注适用平台（macOS/Linux/Windows）
- 不保证一次性修好；若假设被证伪，明确回到协议第 3 步重提假设

---

## 三、触发场景（意图表 + 示例对话）

| 用户意图 | 示例触发词 | 是否触发 |
|----------|------------|----------|
| 报错了想查 | "debug、调试、报错、程序报错、代码出错" | ✅ |
| 想定位根因 | "找 bug、定位问题、排查、bug 在哪" | ✅ |
| 改了还不对 | "修 bug、改了还是不对、回归失败" | ✅ |
| 最小复现 | "最小复现、reproduce、git bisect" | ✅ |
| 语言无关 | "debug this、程序报错" | ✅ |

**示例对话 1（报错定位）**
> 用户：本地 `npm run dev` 报 `Cannot read property 'id' of undefined`
> debug-pro：这是读取了未定义对象的属性。①请贴出出错的完整堆栈；②在访问 `.id` 处加 `console.log(obj)` 看是否为 undefined；③优先用可选链 `obj?.id` 兜底，但先确认 `obj` 本不应为空（走协议第 3→4→5 步）。

**示例对话 2（改了还不对）**
> 用户：我加了 `try/catch` 但问题还在。
> debug-pro：try/catch 只吞异常不解决根因。请回到协议第 1 步：去掉 try/catch 让原始报错暴露，再走复现→缩小范围→假设。

---

## 四、常见错误与反模式（结构化 FAQ + 高频 Q&A）

**反模式（应避免）**：
1. 盲改代码碰运气 — 一次只改一个变量（协议第 3 步精神）
2. 跳过复现直接猜 — 不能复现就无法验证修复
3. 借机大重构 — 调试期只做最小修复，重构另开任务
4. 只看报错第一行 — 根因常在堆栈底部或调用链上游
5. 改完不写测试 — 没有回归测试，bug 会回来

**高频 Q&A**：
- **Q：断点没生效？** A：确认调试器已 attach（Node 用 `--inspect-brk`，Python 用 `python -m pdb`）；源码与运行文件是否同一份；热重载可能绕过断点。
- **Q：Git Bisect 适用于什么？** A：仅当"某个历史版本正常、现在异常"且能写判定脚本时。无法自动判定的手动 bisect 仍可用但慢。
- **Q：生产环境能直接跑调试命令吗？** A：默认禁止（见第七章）；先做影子/预发验证。
- **Q：多线程竞态怎么调？** A：先加日志复现概率，再用确定性手段（锁/队列）隔离，避免靠"多跑几次"判定修复。

---

## 五、标准 SOP（7 步调试协议步骤表）

| 步 | 动作 | 关键产出 | 失败回退 |
|----|------|----------|----------|
| 1 | 复现问题 | 稳定复现步骤、输入、环境 | 复现不了→先收集信息，不下结论 |
| 2 | 缩小范围 | 嫌疑代码区（注释/二分/git bisect） | — |
| 3 | 提出假设 | 具体、可验证的推断 | 假设被证伪→回本步重提 |
| 4 | 添加观测点 | 日志/断点/断言 | — |
| 5 | 验证假设 | 确认根因证据 | 未确认→回第 3 步 |
| 6 | 修复问题 | 最小化正确修复（不重构） | — |
| 7 | 回归测试 | 捕获该 bug 的测试用例通过 | 未通过→回第 6 步 |

**多场景调试命令**：

Python：
```bash
python -m pdb script.py
breakpoint()                       # Python 3.7+
python -X tracemalloc script.py    # 内存追踪
python -m cProfile -s cumulative script.py
```
JavaScript / Node：
```bash
node --inspect-brk app.js          # 访问 chrome://inspect
console.log(JSON.stringify(obj, null, 2))
console.trace('Call stack'); console.time('p'); console.timeEnd('p')
node --expose-gc --max-old-space-size=4096 app.js
```
CSS / 布局：
```css
* { outline: 1px solid red !important; }
.debug { background: rgba(255,0,0,0.1) !important; }
```
网络：
```bash
curl -v https://api.example.com/endpoint
dig example.com ; nslookup example.com
lsof -i :3000                # macOS/Linux
netstat -ano | findstr :3000 # Windows
```
Git Bisect：
```bash
git bisect start
git bisect bad
git bisect good abc1234
# 测试后：git bisect good | git bisect bad
git bisect reset
```

---

## 六、关键事实速查

| 报错 | 可能原因 | 修复 |
|------|----------|------|
| `Cannot read property of undefined` | 缺空值检查 | `?.` 或提前校验 |
| `ENOENT` | 文件/目录不存在 | 检查路径、手动创建 |
| `CORS error` | 后端未配跨域 | 加 CORS 中间件 |
| `Module not found` | 依赖/路径错误 | `pip install`/`npm install` |
| `Connection refused` | 服务未启动 | 检查端口与进程 |
| `Permission denied` | 权限不足 | `chmod`/管理员 |
| `Segmentation fault` | 内存越界/空指针 | 查数组边界/指针 |
| `KeyError` (py) | 键不存在 | `.get()`/`in` 检查 |
| `AttributeError` (py) | 无此属性 | `hasattr()`/类型确认 |
| `TypeError` (py) | 类型不匹配 | `isinstance()` 检查 |

快速诊断：`lsof -i :PORT` / `ps aux | grep P` / `df -h` / `top -l 1 | head -10`。

调试黄金法则：先复现再修复 · 一次只改一变量 · 最小化修复 · 写测试防回归 · 橡皮鸭法（讲给同事听常能自悟）。

---

## 七、铁律（PROHIBITED）

1. 禁止在未复现前提下断言"根因就是 X"
2. 禁止生产环境执行破坏性命令（`rm -rf`、`DROP`、`git reset --hard`、批量删数据）
3. 禁止借调试之名做大重构
4. 禁止忽略用户输入的原始报错而凭空编造堆栈
5. 禁止在缺证据时声称"已修复"
6. 禁止处理非软件调试诉求（硬件/医疗/法律）并冒充专业意见
7. 禁止跳过回归测试直接交付

---

## 八、输入输出依赖

**输入依赖**：用户提供的报错文本 / 复现步骤 / 环境信息；可选仓库路径（用于 git bisect）。
**输出依赖**：可执行的调试命令（依赖目标语言运行时已安装）；回归测试依赖对应测试框架（pytest / jest 等）。
**无外部服务依赖**：纯方法论 + 本地命令，可完全离线使用；不调用任何在线 API。
**治理溯源**：本技能承载 SynomosAI XCGS / A³ 法则 / AI Passport 机制，版权 SynomosAI · MIT。

---

## 九、示例

**场景：Python 偶发 `KeyError: 'user'`**
1. 复现：记录触发请求与参数，确认稳定复现路径
2. 缩小：定位到 `data['user']`，打印 `data.keys()`
3. 假设：上游接口偶发不返回 `user` 字段
4. 观测：`assert 'user' in data, data` 或日志打印 `data`
5. 验证：复现请求确证 `user` 缺失
6. 修复：`user = data.get('user')` 或上游补字段（最小改动）
7. 回归：写 pytest 模拟缺 `user` 的响应，断言兜底生效

**场景：前端布局错位**
- 加 `* { outline: 1px solid red }` 高亮，逐层定位溢出/浮动元素；优先用开发者工具盒模型，而非反复改数值猜。

---

## 十、错误处理

- **用户缺信息**：先列出必填项（报错/环境/复现步骤），用反问补齐，不臆测
- **假设被证伪**：明确"上一假设不成立"，回到协议第 3 步重提，记录排除项
- **命令执行失败**：区分"命令不存在"（运行时未装）与"逻辑错误"，给安装提示或替代命令
- **无法复现**：标注"未复现，暂不修复"，提供临时观测手段而非盲改
- **超出边界**：礼貌说明不在本技能范围，建议对应专业渠道
- **免责**：本技能按 AS IS 提供，风险由使用者承担；非医疗器械/非医疗软件，提及标准仅为语境不构建议。

> 版权 © SynomosAI · 许可 MIT · 署名 诺声(Logos)@SynomosAI
---

> 治理与溯源：本技能承载 SynomosAI 治理体系（XCGS / A³ Laws / AI Passport / AI-world coinhabitation），持续对标 ISO/IEC 42001、NIST AI RMF、OWASP Agentic Top 10。版权 © 2026 SynomosAI（MIT 许可）。发声大使：诺声(Logos)@SynomosAI。指纹 FP-MX-F947B84FC72F。
>
> **免责声明**：本技能按「原样（AS IS）」提供，不作任何明示或暗示担保；非医疗器械/非医疗软件，无疗效或临床声明；提及 FDA·CE·MDR 仅为语境，不构成法规建议；SynomosAI 为厂商中立业务，不代表任何第三方承诺。使用风险由使用者自行承担。

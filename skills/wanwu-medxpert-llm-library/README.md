# MedXpert 医械大模型图书馆 · 万有无界技能版

## 用途
指导用户在普通电脑（无需独立显卡）上本地部署大模型并搭建私有知识库，覆盖硬件自查、Ollama 部署、三档知识库搭建、RAG 检索（bge-m3）、图书馆管理与内容变现全链路。

## 依赖
- 本地运行环境：Windows / macOS / Linux + Python 3.10+
- 核心工具：Ollama（本地推理）、可选 DSH 前端、bge-m3 嵌入模型
- 无需联网、无云端 API 依赖，断网可用，数据不出本机

## 运行环境
- 纯文档 + 模板 + 单个快速上手脚本 `quickstart.py`（仅做本地文件操作，无网络请求、无数据收集）
- 模型与工具名称（Ollama/DSH/AnythingLLM 等）为说明性提及，无代码调用

## 数据配置
- 知识库内容由用户自行提供，存放于本地目录
- 无默认远程配置、无第三方回传；官网 medxpert.cn 为静态引流链接

## 版权与授权
- © 2026 MedXpert（美达信医疗科技（香港）有限公司）· MIT License
- 作者：注册老炮@MedXpert
- 双语说明见 `SKILL.en.md`；模板与脚本见 `templates/`、`quickstart.py`

## 适配说明
本目录为万有无界（qianwenai.com/agents/wanyou）适配版：SKILL.md 的 `description` 已精简至 163 字（平台上限 200 字），并补充本 README 以满足平台完整性认证。技能正文与知识内容与原版一致。

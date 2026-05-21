---
name: user-research
description: 用户研究 AI Agents 系统 - 访谈分析、PRD生成、报告撰写
---

# 用户研究 AI Agents 系统

欢迎使用用户研究 AI Agents 系统。本系统通过 Claude Code Skills 提供用户研究全流程自动化支持。

## 可用命令

| 命令 | 功能 |
|------|------|
| `/ur-start` | 初始化项目工作区 |
| `/ur-interview` | 分析用户访谈记录 |
| `/ur-requirements` | 生成产品需求文档 |
| `/ur-usability` | 辅助可用性测试设计 |
| `/ur-competitive` | 竞品信息采集分析 |
| `/ur-report` | 生成研究报告 |
| `/ur-insights` | 跨项目知识检索 |

## 项目结构

本系统使用 Obsidian 作为知识库，所有研究资料存储在 Obsidian Vault 中：

- `00-项目/` - 项目文档和配置
- `01-用户访谈/` - 原始访谈记录
- `02-洞察笔记/` - 分析洞察
- `03-需求池/` - PRD 草案
- `04-报告/` - 最终报告

## 开始使用

1. 首先运行 `/ur-start` 初始化项目
2. 在 `01-用户访谈/` 目录创建访谈记录
3. 使用 `/ur-interview` 分析访谈内容
4. 使用 `/ur-requirements` 将洞察转化为需求
5. 使用 `/ur-report` 生成最终报告

## Agent 职责

- **全球洞察 Agent**: 动态画像、趋势预判、竞品对标
- **全周期用研 Agent**: 概念验证、可用性测试、NPS分析
- **数据融合 Agent**: 定性定量交叉验证、标签化
- **流程协同 Agent**: 需求流转、Backlog同步
- **合规安全 Agent**: 隐私脱敏、数据分级
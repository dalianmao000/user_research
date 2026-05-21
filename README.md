# 用户研究 AI Agents 项目

基于 Claude Code Skills + Obsidian + Docker 的用户研究自动化系统。

## 项目概述

本项目旨在通过 AI Agents 技术实现用户研究全流程的自动化，包括：
- 用户访谈记录分析
- 洞察提取与标签化
- 产品需求文档（PRD）生成
- 用户研究报告撰写

## 技术架构

```
┌─────────────────────────────────────────┐
│         Claude Code (Skills)            │
│   /ur-start, /ur-interview, /ur-report │
├─────────────────────────────────────────┤
│              Obsidian                   │
│   知识库 / 笔记管理 / 向量检索           │
├─────────────────────────────────────────┤
│           Docker Services               │
│   n8n (工作流) │ Weaviate │ PostgreSQL │
└─────────────────────────────────────────┘
```

## 快速开始

### 1. 环境要求
- macOS (M1/M2/M3 chip)
- Docker Desktop
- Claude Code CLI
- 16GB+ 内存

### 2. 安装步骤

```bash
# 克隆项目
git clone https://github.com/your-username/user-research-agents.git
cd user-research-agents

# 启动 Docker 服务
./scripts/setup.sh

# 初始化 Obsidian Vault
python3 scripts/obsidian-sync.py init

# 安装 Skills
cp -r skills/* ~/.claude/skills/
```

### 3. 使用方法

#### 初始化项目
```bash
/ur-start
```

#### 分析访谈记录
```bash
/ur-interview
```

#### 生成 PRD
```bash
/ur-requirements
```

#### 生成报告
```bash
/ur-report
```

## 目录结构

```
user-research-agents/
├── .github/
│   ├── ISSUE_TEMPLATE/           # GitHub Issue 模板
│   │   ├── bug_report.yml       # Bug 报告模板
│   │   ├── feature_request.yml  # 功能请求模板
│   │   └── config.yml           # Issue 配置
│   └── workflows/               # CI/CD 工作流
│       ├── ci.yml              # 持续集成配置
│       └── release.yml          # 发布工作流
│
├── .vscode/                     # VS Code 配置
│   └── settings.json
│
├── docker/                      # Docker 容器配置
│   └── docker-compose.yml       # n8n + Weaviate + PostgreSQL
│
├── docs/                        # 项目文档
│   └── plans/                   # 实现计划
│       └── 2026-05-21-user-research-agents-implementation-plan.md
│
├── obsidian-vault/              # Obsidian 知识库模板
│   ├── .obsidian/              # Obsidian 配置
│   │   └── settings.json       # Text Generator 插件配置
│   ├── 00-项目/                # 项目文档
│   │   └── 项目概览.md         # 项目信息模板
│   ├── 01-用户访谈/            # 原始访谈记录
│   │   └── 访谈记录模板.md     # 访谈记录模板
│   ├── 02-洞察笔记/            # 分析洞察
│   │   └── 洞察笔记模板.md     # 洞察笔记模板
│   ├── 03-需求池/              # PRD 草案
│   │   └── 需求文档模板.md     # 需求文档模板
│   └── 04-报告/                # 最终报告
│       └── 报告模板.md         # 报告模板
│
├── scripts/                     # 工具脚本
│   ├── setup.sh                # Docker 服务启动脚本
│   └── obsidian-sync.py        # Obsidian 同步工具
│
├── skills/                      # Claude Code Skills
│   ├── skill.json             # 技能元数据
│   └── user-research/          # 用户研究技能
│       ├── skill.md           # 主技能入口
│       ├── agents/            # AI Agents 定义
│       │   ├── compliance.md              # 合规安全 Agent
│       │   ├── data-fusion.md            # 数据融合 Agent
│       │   ├── full-cycle-ur.md          # 全周期用研 Agent
│       │   ├── global-insight.md         # 全球洞察 Agent
│       │   └── process-orchestrate.md    # 流程协同 Agent
│       └── prompts/           # Prompt 模板
│           ├── interview-analysis.md  # 访谈分析模板
│           ├── prd-generation.md     # PRD 生成模板
│           └── report-writing.md     # 报告撰写模板
│
├── tests/                       # 测试文件
│   ├── __init__.py
│   └── test_obsidian_sync.py   # obsidian-sync 测试
│
├── CHANGELOG.md                # 变更日志
├── CODE_OF_CONDUCT.md         # 行为准则
├── CONTRIBUTING.md            # 贡献指南
├── LICENSE                    # MIT 许可证
├── README.md                  # 项目说明文档
├── SECURITY.md                # 安全政策
└── requirements.txt           # Python 依赖
```

## 目录说明

| 目录 | 说明 |
|------|------|
| `.github/` | GitHub 配置（Issue 模板、CI/CD） |
| `docker/` | Docker Compose 配置文件 |
| `docs/plans/` | 项目实现计划文档 |
| `obsidian-vault/` | Obsidian 知识库模板 |
| `scripts/` | 工具脚本（启动、同步） |
| `skills/` | Claude Code Skills 和 Agents |
| `tests/` | 单元测试和集成测试 |

## Agent 说明

| Agent | 职责 |
|-------|------|
| data-fusion | 访谈分析、洞察提取 |
| full-cycle-ur | PRD 生成、需求管理 |
| global-insight | 报告生成、趋势分析 |
| process-orchestrate | 流程协调、进度追踪 |
| compliance | 隐私脱敏、合规检查 |

## 开发指南

### 添加新的 Agent
1. 在 `skills/user-research/agents/` 创建新的 `.md` 文件
2. 定义角色、职责、输入输出
3. 更新 `skill.md` 中的 Agent 列表

### 修改 Prompt 模板
1. 编辑 `skills/user-research/prompts/` 下的模板文件
2. 测试修改效果
3. 更新文档

## License

MIT
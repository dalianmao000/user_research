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
├── docker/              # Docker Compose 配置
├── obsidian-vault/      # Obsidian 知识库
├── skills/              # Claude Code Skills
├── scripts/            # 工具脚本
└── docs/               # 文档
```

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
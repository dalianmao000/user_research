# 用户研究 AI Agents 项目实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一套基于 Claude Code Skills + Obsidian + Docker 的用户研究 AI Agents 系统，实现用户访谈分析、PRD 生成、报告撰写等核心功能的自动化。

**Architecture:** 采用混合架构 - Claude Code 作为 Agent 编排层（通过 Custom Skills 调用 Claude API），Obsidian 作为知识库（笔记管理 + Text Generator 向量化），Docker 容器运行 n8n 工作流引擎、Weaviate 向量库、PostgreSQL 数据库。各 Agent 通过标准化 prompt 定义职责，通过文件读写与 Obsidian 交互。

**Tech Stack:** Claude API, Obsidian (Text Generator plugin), Docker (n8n, Weaviate, PostgreSQL), Python (LangGraph), Natural Language

---

## 文件结构

```
~/p8_CR/user-research-agents/
├── docker/
│   └── docker-compose.yml           # 容器编排配置
├── obsidian-vault/
│   ├── 00-项目/                    # 项目文档
│   ├── 01-用户访谈/                # 原始访谈记录
│   ├── 02-洞察笔记/                # 分析洞察
│   ├── 03-需求池/                  # PRD 草案
│   ├── 04-报告/                    # 最终报告
│   └── 05-知识库/                  # 向量化检索内容
├── skills/
│   ├── user-research/
│   │   ├── skill.md                # 主技能入口
│   │   ├── agents/
│   │   │   ├── global-insight.md
│   │   │   ├── full-cycle-ur.md
│   │   │   ├── data-fusion.md
│   │   │   ├── process-orchestrate.md
│   │   │   └── compliance.md
│   │   └── prompts/
│   │       ├── interview-analysis.md
│   │       ├── prd-generation.md
│   │       └── report-writing.md
│   └── skill.json                  # 技能元数据
├── workflows/
│   └── n8n/                        # n8n 工作流模板
├── scripts/
│   ├── setup.sh                    # 环境初始化脚本
│   └── obsidian-sync.py            # Obsidian 同步工具
└── docs/
    └── plans/                      # 实现计划文档
```

---

## 第一阶段：环境搭建 (Phase 1 Tasks 1-4)

### Task 1: 创建 Docker Compose 配置

**Files:**
- Create: `~/p8_CR/user-research-agents/docker/docker-compose.yml`

- [ ] **Step 1: 创建 docker-compose.yml**

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    container_name: ur-n8n
    ports:
      - "5678:5678"
    volumes:
      - ./n8n/data:/home/node/.n8n
    restart: unless-stopped
    networks:
      - ur-network

  weaviate:
    image: semitechnologies/weaviate:latest
    container_name: ur-weaviate
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 20
      AUTHENTICATION_ANONYMOUS_ACCESS: true
      PERSISTENCE_DATA_PATH: /var/lib/weaviate
      ENABLE_MODULES: text2vec-transformers
      TRANSFORMERS_INFERENCE_API: http://t2v-transformers:8080
    volumes:
      - ./weaviate/data:/var/lib/weaviate
    restart: unless-stopped
    networks:
      - ur-network

  postgres:
    image: postgres:15
    container_name: ur-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: uruser
      POSTGRES_PASSWORD: urpass
      POSTGRES_DB: userresearch
    volumes:
      - ./postgres/data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - ur-network

networks:
  ur-network:
    driver: bridge
```

- [ ] **Step 2: 创建启动脚本**

```bash
#!/bin/bash
# setup.sh
cd "$(dirname "$0")/docker"
docker-compose up -d
echo "Services started. Check with: docker-compose ps"
echo "n8n UI: http://localhost:5678"
echo "Weaviate: http://localhost:8080"
echo "PostgreSQL: localhost:5432"
```

- [ ] **Step 3: 设置执行权限并运行**

```bash
chmod +x ~/p8_CR/user-research-agents/scripts/setup.sh
cd ~/p8_CR/user-research-agents/docker && docker-compose up -d
```

- [ ] **Step 4: 验证服务运行**

```bash
docker-compose ps
# Expected: All 3 services should be "Up"
```

---

### Task 2: 创建 Obsidian Vault 模板

**Files:**
- Create: `~/p8_CR/user-research-agents/obsidian-vault/.obsidian/settings.json`
- Create: `~/p8_CR/user-research-agents/obsidian-vault/00-项目/项目概览.md`
- Create: `~/p8_CR/user-research-agents/obsidian-vault/01-用户访谈/访谈记录模板.md`
- Create: `~/p8_CR/user-research-agents/obsidian-vault/02-洞察笔记/洞察笔记模板.md`
- Create: `~/p8_CR/user-research-agents/obsidian-vault/03-需求池/需求文档模板.md`
- Create: `~/p8_CR/user-research-agents/obsidian-vault/04-报告/报告模板.md`

- [ ] **Step 1: 创建 Obsidian 配置文件**

```json
{
  "plugin-enabled": true,
  "textgenerator": {
    "enable": true,
    "embeddingModel": "sentence-transformers/all-MiniLM-L6-v2",
    "vectorDb": "weaviate",
    "weaviateUrl": "http://localhost:8080"
  }
}
```

- [ ] **Step 2: 创建项目概览模板**

```markdown
# 项目概览

## 项目信息
- 项目名称：
- 创建日期：
- 项目目标：

## 研究范围
-

## 关键里程碑
- [ ]

## 团队成员
-
```

- [ ] **Step 3: 创建访谈记录模板**

```markdown
---
访谈ID:
访谈日期:
访谈方式:
受访者:
受访者背景:
访谈时长:
访谈者:
---

# 访谈记录

## 访谈目标


## 访谈问题与回答

### Q1:


### Q2:


## 关键洞察

### 痛点
-

### 期望
-

### 建议
-

## 原始语料

```

- [ ] **Step 4: 创建洞察笔记模板**

```markdown
---
洞察ID:
来源访谈ID:
创建日期:
关联需求:
---

# 用户洞察

## 洞察类型
- [ ] 痛点 (Pain Point)
- [ ] 期望 (Expectation)
- [ ] 机会 (Opportunity)
- [ ] 行为 (Behavior)

## 洞察描述


## 证据引用


## 优先级
- [ ] P0 (Critical)
- [ ] P1 (High)
- [ ] P2 (Medium)
- [ ] P3 (Low)

## 关联需求

```

- [ ] **Step 5: 创建需求文档模板**

```markdown
---
需求ID:
来源洞察ID:
创建日期:
状态: [草稿|待评审|已采纳|已排期]
优先级: [P0|P1|P2|P3]
---

# 产品需求文档

## 需求概述


## 用户故事
作为 [角色]，我希望 [功能]，以便 [收益]。

## 需求详情
### 功能描述
### 验收标准
### 假设与约束

## 相关研究
- 关联洞察：
- 关联访谈：

## 评审记录
| 日期 | 评审人 | 意见 |
|-----|-------|-----|
```

- [ ] **Step 6: 创建报告模板**

```markdown
---
报告ID:
报告类型: [用户访谈分析|可用性测试|趋势研究|竞品分析]
创建日期:
作者:
---

# 用户研究报告

## 执行摘要


## 研究背景


## 研究方法


## 主要发现

### 发现1:


### 发现2:


## 建议与行动项


## 附录
- 原始数据
- 访谈记录
```

- [ ] **Step 7: 提交**

```bash
cd ~/p8_CR/user-research-agents
git init
git add obsidian-vault/ docker/ scripts/
git commit -m "feat: initial project structure with docker and obsidian templates"
```

---

## 第二阶段：核心 Skills 实现 (Phase 1 Tasks 5-9)

### Task 3: 创建主技能定义 (skill.md)

**Files:**
- Create: `~/p8_CR/user-research-agents/skills/user-research/skill.md`

- [ ] **Step 1: 创建主技能入口文件**

```markdown
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
```

- [ ] **Step 2: 创建 skill.json 元数据**

```json
{
  "name": "user-research",
  "version": "1.0.0",
  "description": "用户研究 AI Agents 系统",
  "commands": [
    {
      "name": "ur-start",
      "description": "初始化项目工作区"
    },
    {
      "name": "ur-interview",
      "description": "分析用户访谈记录"
    },
    {
      "name": "ur-requirements",
      "description": "生成产品需求文档"
    },
    {
      "name": "ur-usability",
      "description": "辅助可用性测试设计"
    },
    {
      "name": "ur-competitive",
      "description": "竞品信息采集分析"
    },
    {
      "name": "ur-report",
      "description": "生成研究报告"
    },
    {
      "name": "ur-insights",
      "description": "跨项目知识检索"
    }
  ],
  "author": "user",
  "tags": ["user-research", "ai-agents", "product"]
}
```

- [ ] **Step 3: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add skills/
git commit -m "feat: add main skill definition and metadata"
```

---

### Task 4: 创建 Interview Analysis Agent

**Files:**
- Create: `~/p8_CR/user-research-agents/skills/user-research/agents/data-fusion.md`

- [ ] **Step 1: 创建 data-fusion agent (负责访谈分析)**

```markdown
---
name: data-fusion-agent
description: 数据融合 Agent - 负责访谈记录解析、洞察提取、标签生成
---

# 数据融合 Agent (Data Fusion Agent)

## 角色定义

你是一名资深用户研究员，专注于从定性数据中提取有价值的洞察。你的任务是将用户访谈记录转化为结构化的洞察标签，为后续需求生成提供输入。

## 核心能力

1. **访谈解析**: 读取原始访谈记录，提取关键信息
2. **洞察提取**: 识别痛点、期望、机会点、行为模式
3. **标签生成**: 生成标准化的洞察标签体系
4. **交叉验证**: 将新洞察与历史洞察关联

## 输入

- 原始访谈记录（存储在 `01-用户访谈/` 目录）
- 历史洞察笔记（存储在 `02-洞察笔记/` 目录）

## 输出

- 结构化洞察笔记（写入 `02-洞察笔记/` 目录）
- 洞察统计摘要

## 分析流程

### 1. 读取访谈记录

读取指定路径的访谈记录文件，解析 frontmatter 元数据和正文内容。

### 2. 提取关键信息

```markdown
## 访谈概览
- 受访者: [从frontmatter提取]
- 访谈日期: [从frontmatter提取]
- 访谈方式: [从frontmatter提取]

## 核心痛点
按优先级列出所有痛点，每个痛点需包含：
- 痛点描述: [具体描述]
- 发生场景: [何时何地发生]
- 影响程度: [对用户的影响]
- 原始语料: [直接引用受访者原话]

## 用户期望
- 期望1: [描述]
- 期望2: [描述]

## 行为模式
- 行为1: [描述]
- 行为2: [描述]

## 机会点
- 机会1: [潜在的產品或服务改进点]
```

### 3. 生成洞察标签

标签类型：
- `pain_point` - 痛点
- `expectation` - 期望
- `opportunity` - 机会
- `behavior` - 行为模式
- `feature_request` - 功能请求
- `complaint` - 抱怨
- `suggestion` - 建议

每个标签需包含置信度评分 (0.0-1.0)。

### 4. 关联历史洞察

检查现有洞察笔记，识别：
- 相似洞察（可合并）
- 新洞察（独立存在）
- 矛盾洞察（需标记）

## 输出格式

生成的洞察笔记需包含以下 frontmatter：

```yaml
---
洞察ID: [自动生成 UUID]
来源访谈ID: [关联的访谈ID]
创建日期: [ISO格式日期]
标签类型: [见上述标签类型]
置信度: [0.0-1.0]
关联洞察: [关联的洞察ID列表]
---

# 洞察详情

## 洞察类型
## 洞察描述
## 证据引用
## 优先级评定
```

## 执行示例

当用户说"分析这份访谈记录"时：

1. 首先询问用户访谈记录的文件路径，或列出 `01-用户访谈/` 目录供选择
2. 读取选中文件
3. 按照上述流程分析
4. 生成洞察笔记并保存到 `02-洞察笔记/` 目录
5. 输出一份分析摘要

## 质量标准

- 每个痛点必须有原始语料引用
- 标签需准确反映洞察本质
- 优先级评定需有明确理由
- 关联洞察需有具体依据
```

- [ ] **Step 2: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add skills/user-research/agents/data-fusion.md
git commit -m "feat: add data fusion agent for interview analysis"
```

---

### Task 5: 创建 PRD Generation Agent

**Files:**
- Create: `~/p8_CR/user-research-agents/skills/user-research/agents/full-cycle-ur.md`

- [ ] **Step 1: 创建 full-cycle-ur agent (负责需求生成)**

```markdown
---
name: full-cycle-ur-agent
description: 全周期用研 Agent - 负责将洞察转化为产品需求文档
---

# 全周期用研 Agent (Full-Cycle UR Agent)

## 角色定义

你是一名产品需求分析师，专注于将用户洞察转化为结构化的产品需求文档（PRD）。你的任务是根据洞察笔记生成可执行的产品需求，为研发团队提供清晰的开发依据。

## 核心能力

1. **洞察评估**: 判断洞察是否值得转化为需求
2. **需求转化**: 将用户痛点/期望转化为具体功能需求
3. **PRD 生成**: 创建标准化的产品需求文档
4. **优先级排序**: 基于商业价值和用户impact评定优先级

## 输入

- 洞察笔记（存储在 `02-洞察笔记/` 目录）
- 历史需求文档（存储在 `03-需求池/` 目录）
- 项目概览（存储在 `00-项目/` 目录）

## 输出

- 产品需求文档（写入 `03-需求池/` 目录）
- 需求优先级建议

## 需求转化流程

### 1. 读取洞察

获取指定洞察ID的完整信息，评估：
- 洞察的置信度是否足够高 (>= 0.6)
- 洞察是否具备可执行性
- 解决该洞察问题的收益有多大

### 2. 生成用户故事

使用标准用户故事格式：
```
作为 [角色]，我希望 [功能]，以便 [收益]。
```

### 3. 定义需求详情

```markdown
## 需求概述
[一句话描述需求]

## 用户故事
[标准用户故事格式]

## 功能描述
### 背景
[为什么需要这个功能]

### 详细描述
[功能的详细说明]

### 用户交互流程
1. [步骤1]
2. [步骤2]
...

### 验收标准
- [标准1]
- [标准2]
- [标准3]

### 边界条件
- [边界1]
- [边界2]
```

### 4. 评定优先级

| 维度 | P0 | P1 | P2 | P3 |
|------|----|----|----|----|
| 用户impact | 大量用户受影响 | 部分用户受影响 | 少数用户受影响 | 单个用户 |
| 商业价值 | 直接带来收入 | 提升转化率 | 降低成本 | 优化体验 |
| 实现难度 | < 1周 | 1-2周 | 2-4周 | > 4周 |

优先级计算：
- P0: UserImpact >= 高 AND 商业价值 >= 高
- P1: UserImpact >= 高 OR 商业价值 >= 高
- P2: 其他组合
- P3: 探索性需求

### 5. 关联历史需求

检查是否有相似需求，避免重复建设。如有相似需求，标记关联并建议合并。

## 输出格式

生成的需求文档需包含以下 frontmatter：

```yaml
---
需求ID: [自动生成 UUID]
来源洞察ID: [关联的洞察ID列表]
创建日期: [ISO格式日期]
状态: 草稿
优先级: [P0|P1|P2|P3]
预估工时: [估算]
---

# 需求文档

## 需求概述
## 用户故事
## 功能描述
## 验收标准
## 关联研究
```

## 执行示例

当用户说"根据这些洞察生成需求"时：

1. 首先读取用户指定的洞察（或列出可用洞察供选择）
2. 分析每个洞察，评估是否适合转化为需求
3. 对于适合的洞察，生成 PRD
4. 保存到 `03-需求池/` 目录
5. 输出一份需求汇总表

## 质量标准

- 每个需求必须有明确的用户故事
- 验收标准需可测试
- 优先级评定需有依据
- 避免重复需求
```

- [ ] **Step 2: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add skills/user-research/agents/full-cycle-ur.md
git commit -m "feat: add full-cycle UR agent for PRD generation"
```

---

### Task 6: 创建 Report Writing Agent

**Files:**
- Create: `~/p8_CR/user-research-agents/skills/user-research/agents/global-insight.md`

- [ ] **Step 1: 创建 global-insight agent (用于报告生成)**

```markdown
---
name: global-insight-agent
description: 全球洞察 Agent - 负责生成用户研究报告
---

# 全球洞察 Agent (Global Insight Agent)

## 角色定义

你是一名资深用户研究专家，专注于从多源数据中提取洞察并生成专业的研究报告。你的任务是将访谈记录、洞察笔记和需求文档整合成结构清晰、内容详实的用户研究报告。

## 核心能力

1. **信息整合**: 整合多源研究数据
2. **洞察提炼**: 从定性数据中提炼关键洞察
3. **报告撰写**: 生成符合行业标准的用户研究报告
4. **建议输出**: 基于研究结果提出可执行的建议

## 输入

- 原始访谈记录（`01-用户访谈/`）
- 洞察笔记（`02-洞察笔记/`）
- 需求文档（`03-需求池/`）
- 项目背景（`00-项目/`）

## 输出

- 用户研究报告（写入 `04-报告/` 目录）

## 报告结构

### 1. 执行摘要
- 研究背景（一段话）
- 核心发现（3-5个关键点）
- 主要建议（1-3个行动项）

### 2. 研究背景
- 研究目的
- 研究范围
- 研究方法
- 样本信息

### 3. 主要发现

按主题组织，每个发现包含：
- 发现标题
- 详细描述
- 证据引用（原始语料）
- 影响分析

### 4. 用户画像
- 用户分群
- 各分群特征
- 各分群需求差异

### 5. 机会分析
- 优先级矩阵
- 各机会的潜在价值
- 实现建议

### 6. 行动建议
- 短期行动项（0-3个月）
- 中期行动项（3-6个月）
- 长期行动项（6个月以上）

### 7. 附录
- 原始数据链接
- 访谈记录索引
- 方法论说明

## 输出格式

生成的报告需包含以下 frontmatter：

```yaml
---
报告ID: [自动生成 UUID]
报告类型: [用户访谈分析|可用性测试|趋势研究|竞品分析]
创建日期: [ISO格式日期]
作者: Claude Research Agent
关联洞察数: [数量]
关联需求数: [数量]
---

# 用户研究报告：[报告标题]

## 执行摘要
```

## 执行示例

当用户说"生成研究报告"时：

1. 首先确认要包含的研究范围（哪些访谈/洞察/需求）
2. 读取所有相关文件
3. 按照报告结构组织内容
4. 生成完整报告并保存到 `04-报告/` 目录
5. 输出一份报告摘要

## 质量标准

- 执行摘要需简洁有力，一页以内
- 每个发现必须有证据支持
- 建议需可执行、可落地
- 报告长度适中，建议 10-20 页
- 图表需清晰易懂
```

- [ ] **Step 2: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add skills/user-research/agents/global-insight.md
git commit -m "feat: add global insight agent for report generation"
```

---

### Task 7: 创建其他辅助 Agents

**Files:**
- Create: `~/p8_CR/user-research-agents/skills/user-research/agents/process-orchestrate.md`
- Create: `~/p8_CR/user-research-agents/skills/user-research/agents/compliance.md`

- [ ] **Step 1: 创建 process-orchestrate agent**

```markdown
---
name: process-orchestrate-agent
description: 流程协同 Agent - 协调各 Agent 工作、管理需求流转
---

# 流程协同 Agent (Process Orchestrate Agent)

## 角色定义

你是用户研究项目的流程协调员，负责协调各个 Agent 的工作、管理需求流转状态、监控项目进度。你的任务是确保从访谈到报告的全流程高效运转。

## 核心能力

1. **任务分解**: 将复杂任务分解为可执行的子任务
2. **状态追踪**: 追踪每个工作项的状态
3. **进度报告**: 生成项目进度报告
4. **流程优化**: 识别瓶颈并提出改进建议

## 输入

- 工作指令（用户自然语言描述）
- 各目录下的文件状态

## 输出

- 任务分解清单
- 状态更新
- 进度报告

## 工作流程

### 1. 解析指令

理解用户的自然语言指令，识别：
- 目标任务
- 涉及的文件
- 期望输出

### 2. 任务分解

将任务分解为原子步骤：
```
1. [步骤1]
2. [步骤2]
...
```

### 3. 状态更新

跟踪每个工作项的状态变化：
- 新建 (new)
- 进行中 (in_progress)
- 待审核 (pending_review)
- 已完成 (completed)
- 已归档 (archived)

### 4. 生成报告

定期生成项目状态报告：
```
## 项目状态报告

### 整体进度
- 总任务数: X
- 已完成: Y
- 进行中: Z
- 完成率: XX%

### 最近活动
- [日期] [活动描述]

### 待处理事项
- [ ] [待处理事项]

### 风险提示
- [风险描述]
```
```

## 执行示例

当用户说"我需要分析三份访谈记录并生成报告"时：

1. 解析任务：访谈分析 + 报告生成
2. 分解任务：
   - 任务1: 分析访谈A
   - 任务2: 分析访谈B
   - 任务3: 分析访谈C
   - 任务4: 整合洞察
   - 任务5: 生成报告
3. 按顺序执行各 Agent
4. 汇总结果
5. 输出一份完整的项目状态报告
```

- [ ] **Step 2: 创建 compliance agent**

```markdown
---
name: compliance-agent
description: 合规安全 Agent - 隐私脱敏、数据分级、访问控制
---

# 合规安全 Agent (Compliance Agent)

## 角色定义

你是一名数据安全专家，负责确保用户研究过程中的数据隐私和合规。你的任务是识别敏感信息、执行脱敏处理、管理数据访问权限。

## 核心能力

1. **敏感信息识别**: 识别访谈记录中的 PII（个人身份信息）
2. **数据脱敏**: 对敏感信息进行脱敏处理
3. **数据分级**: 评估数据敏感级别
4. **合规检查**: 检查是否符合数据保护要求

## 输入

- 原始访谈记录
- 敏感信息规则库

## 输出

- 脱敏后的访谈记录
- 敏感信息报告
- 访问建议

## 敏感信息类型

| 类型 | 示例 | 脱敏方式 |
|------|------|----------|
| 姓名 | 张三 | 替换为"受访者A" |
| 电话 | 138xxxx8888 | 替换为"138****8888" |
| 邮箱 | user@email.com | 替换为"user@email.com" |
| 地址 | 杭州市西湖区 | 替换为"[城市]" |
| 公司 | XX公司 | 替换为"[公司类型]" |
| 职位 | 产品经理 | 保留（不敏感） |

## 脱敏流程

### 1. 识别敏感信息

扫描访谈记录，标记所有 PII：
- 人名、地名、组织名
- 联系方式
- 特定唯一标识符

### 2. 执行脱敏

对识别出的敏感信息进行脱敏：
- 直接替换（如姓名）
- 部分掩码（如电话号码）
- 模糊化（如精确地址）

### 3. 生成报告

```markdown
## 脱敏报告

### 原始文件
[文件路径]

### 发现敏感信息
| 类型 | 数量 | 脱敏方式 |
|------|------|----------|
| 姓名 | 3 | 直接替换 |
| 电话 | 1 | 部分掩码 |
| 地址 | 2 | 模糊化 |

### 脱敏后文件
[输出路径]

### 建议
- [建议]
```
```

## 质量标准

- 不遗漏任何 PII
- 脱敏后信息仍保持可读性
- 不改变访谈原意
- 保留足够的上下文用于分析
```

- [ ] **Step 3: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add skills/user-research/agents/process-orchestrate.md skills/user-research/agents/compliance.md
git commit -m "feat: add process orchestration and compliance agents"
```

---

## 第三阶段：Prompt 模板库 (Phase 2)

### Task 8: 创建 Prompt 模板

**Files:**
- Create: `~/p8_CR/user-research-agents/skills/user-research/prompts/interview-analysis.md`
- Create: `~/p8_CR/user-research-agents/skills/user-research/prompts/prd-generation.md`
- Create: `~/p8_CR/user-research-agents/skills/user-research/prompts/report-writing.md`

- [ ] **Step 1: 创建 interview-analysis prompt**

```markdown
# 访谈分析 Prompt 模板

## 任务
分析用户访谈记录，提取关键洞察。

## 输入
- 访谈记录文件路径

## 分析框架

### 1. 基本信息提取
- 受访者背景（职业、经验年限等）
- 访谈时长和方式
- 访谈日期和地点

### 2. 主题分类
将访谈内容按主题分类整理。

### 3. 洞察提取
对每个主题，提取：
- **痛点**: 用户遇到的问题或困难
- **期望**: 用户希望达到的目标
- **行为**: 用户的实际操作方式
- **建议**: 用户提出的改进建议

### 4. 语料引用
每个洞察必须附带原始语料作为证据。

### 5. 优先级评定
根据以下维度评定优先级：
- 影响范围（多少用户受影响）
- 影响程度（对用户工作的影响大小）
- 解决紧迫性（问题的严重程度）

## 输出格式
请按以下格式输出分析结果：

```markdown
## 访谈概览
- 受访者: [姓名/代号]
- 背景: [简要背景]
- 访谈时长: [时长]

## 核心发现

### 发现1: [主题]
**类型**: [痛点/期望/行为/建议]
**描述**: [详细描述]
**语料**: "[原始引用]"
**优先级**: [P0/P1/P2/P3]

### 发现2: ...
...

## 洞察汇总
共提取 [N] 个洞察，其中：
- 痛点: [X] 个
- 期望: [Y] 个
- 行为: [Z] 个
- 建议: [W] 个

## 下一步建议
- [建议1]
- [建议2]
```
```

- [ ] **Step 2: 创建 prd-generation prompt**

```markdown
# PRD 生成 Prompt 模板

## 任务
基于用户洞察生成产品需求文档。

## 输入
- 洞察列表（包含洞察ID、类型、描述）
- 可选：关联的历史需求

## 生成流程

### 1. 需求概述
用一句话描述需求解决的问题。

### 2. 用户故事
使用标准模板：
```
作为 [角色]，我希望 [功能]，以便 [收益]。
```

### 3. 功能描述
详细描述功能的：
- 背景和动机
- 用户交互流程
- 边界条件和异常处理

### 4. 验收标准
定义可测试的验收标准：
- [标准1]
- [标准2]
- [标准3]

### 5. 优先级评定
根据以下矩阵评定：

| 维度 | 高 | 中 | 低 |
|------|---|---|---|
| 用户impact | P0 | P1 | P2 |
| 商业价值 | P1 | P2 | P3 |
| 实现难度 | P1 | P2 | P3 |

## 输出格式
```markdown
---
需求ID: [UUID]
标题: [需求名称]
来源洞察: [洞察ID列表]
优先级: [P0/P1/P2/P3]
状态: 草稿
创建日期: [日期]
---

# 需求名称

## 概述
[一句话描述]

## 用户故事
作为 [角色]，我希望 [功能]，以便 [收益]。

## 详细描述

### 背景


### 功能详情


### 用户流程


### 验收标准
- [ ]

## 关联需求
- [关联需求ID]: [关联原因]

## 评审记录
| 日期 | 评审人 | 意见 |
|-----|-------|-----|
```

- [ ] **Step 3: 创建 report-writing prompt**

```markdown
# 报告撰写 Prompt 模板

## 任务
基于用户研究和洞察生成完整的用户研究报告。

## 输入
- 研究项目信息
- 访谈记录列表
- 洞察笔记列表
- 需求文档列表

## 报告结构

### 1. 执行摘要（1页）
- 研究背景（1-2句话）
- 核心发现（3-5个要点）
- 主要建议（1-3个行动项）

### 2. 研究背景
- 研究目的
- 研究范围和样本
- 研究方法
- 局限性说明

### 3. 主要发现
每个发现包含：
- 发现标题
- 详细描述
- 证据（原始语料引用）
- 影响分析

### 4. 用户画像
- 用户分群定义
- 各分群特征描述
- 分群需求差异

### 5. 机会与建议
- 机会优先级矩阵
- 每个机会的潜在价值
- 具体行动建议

### 6. 附录
- 研究方法详解
- 原始数据索引
- 术语解释

## 输出格式
```markdown
---
报告ID: [UUID]
报告类型: 用户研究综合报告
标题: [报告标题]
日期: [日期]
作者: Claude Research Agent
样本量: [X] 访谈
洞察数: [Y] 个
需求数: [Z] 个
---

# 报告标题

## 执行摘要


## 一、研究背景


## 二、主要发现

### 2.1 [发现标题]


### 2.2 [发现标题]


## 三、用户画像


## 四、机会与建议


## 五、附录
```
```

- [ ] **Step 4: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add skills/user-research/prompts/
git commit -m "feat: add prompt templates for interview analysis, PRD generation, and report writing"
```

---

## 第四阶段：工具脚本 (Phase 2)

### Task 9: 创建 Obsidian 同步工具

**Files:**
- Create: `~/p8_CR/user-research-agents/scripts/obsidian-sync.py`

- [ ] **Step 1: 创建 obsidian-sync.py**

```python
#!/usr/bin/env python3
"""
Obsidian Sync Tool
用于同步 Obsidian Vault 中的研究资料，支持与 Weaviate 向量数据库集成。
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional
import hashlib

VAULT_PATH = Path(__file__).parent.parent / "obsidian-vault"

class ObsidianSync:
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or VAULT_PATH)
        self.directories = {
            "project": self.vault_path / "00-项目",
            "interviews": self.vault_path / "01-用户访谈",
            "insights": self.vault_path / "02-洞察笔记",
            "requirements": self.vault_path / "03-需求池",
            "reports": self.vault_path / "04-报告",
        }

    def init_vault(self):
        """初始化 Obsidian Vault 结构"""
        for name, path in self.directories.items():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created: {path}")

        # 创建 .obsidian 配置
        obsidian_config = self.vault_path / ".obsidian"
        obsidian_config.mkdir(exist_ok=True)

        settings = {
            "plugin-enabled": True,
            "textgenerator": {
                "enable": True,
                "embeddingModel": "sentence-transformers/all-MiniLM-L6-v2",
                "vectorDb": "weaviate",
                "weaviateUrl": "http://localhost:8080"
            }
        }

        with open(obsidian_config / "settings.json", "w") as f:
            json.dump(settings, f, indent=2)

        print("Obsidian Vault initialized successfully!")

    def list_files(self, directory: str) -> list:
        """列出指定目录下的所有 md 文件"""
        dir_path = self.directories.get(directory)
        if not dir_path or not dir_path.exists():
            return []
        return [f for f in dir_path.glob("*.md")]

    def read_note(self, file_path: Path) -> dict:
        """读取笔记文件，返回 frontmatter 和内容"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 简单的 frontmatter 解析
        frontmatter = {}
        body = content

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                body = parts[2].strip()

                for line in frontmatter_str.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        frontmatter[key.strip()] = value.strip()

        return {
            "path": str(file_path),
            "filename": file_path.name,
            "frontmatter": frontmatter,
            "content": body,
            "word_count": len(body.split()),
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }

    def create_note(self, directory: str, filename: str, content: str, frontmatter: dict = None) -> Path:
        """创建新的笔记文件"""
        dir_path = self.directories.get(directory)
        if not dir_path:
            raise ValueError(f"Unknown directory: {directory}")

        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"{filename}.md"

        # 添加 frontmatter
        full_content = "---\n"
        if frontmatter:
            for key, value in frontmatter.items():
                full_content += f"{key}: {value}\n"
        full_content += "---\n\n"
        full_content += content

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"Created: {file_path}")
        return file_path

    def update_note(self, file_path: Path, content: str, frontmatter: dict = None):
        """更新笔记文件"""
        full_content = "---\n"
        if frontmatter:
            for key, value in frontmatter.items():
                full_content += f"{key}: {value}\n"
        full_content += "---\n\n"
        full_content += content

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"Updated: {file_path}")

    def generate_id(self, content: str) -> str:
        """生成基于内容的 UUID"""
        return hashlib.md5(content.encode()).hexdigest()[:8]

    def get_stats(self) -> dict:
        """获取 Vault 统计信息"""
        stats = {}
        for name, path in self.directories.items():
            files = list(path.glob("*.md")) if path.exists() else []
            stats[name] = {
                "count": len(files),
                "path": str(path)
            }
        return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Obsidian Sync Tool")
    parser.add_argument("action", choices=["init", "list", "stats", "read", "create"],
                        help="Action to perform")
    parser.add_argument("--dir", "-d", choices=["project", "interviews", "insights", "requirements", "reports"],
                        help="Directory name")
    parser.add_argument("--file", "-f", help="File path")
    parser.add_argument("--content", "-c", help="Note content")
    parser.add_argument("--title", "-t", help="Note title")

    args = parser.parse_args()
    sync = ObsidianSync()

    if args.action == "init":
        sync.init_vault()

    elif args.action == "list":
        if not args.dir:
            print("Please specify --dir")
            return
        files = sync.list_files(args.dir)
        print(f"\nFiles in {args.dir}/:")
        for f in files:
            print(f"  - {f.name}")

    elif args.action == "stats":
        stats = sync.get_stats()
        print("\nVault Statistics:")
        print("-" * 40)
        for name, info in stats.items():
            print(f"{name}: {info['count']} files")

    elif args.action == "read":
        if not args.file:
            print("Please specify --file")
            return
        note = sync.read_note(Path(args.file))
        print(f"\n{note['filename']}")
        print(f"Words: {note['word_count']}")
        print(f"Modified: {note['modified']}")
        print("\n--- Frontmatter ---")
        print(json.dumps(note['frontmatter'], indent=2))
        print("\n--- Content Preview ---")
        print(note['content'][:500] + "...")

    elif args.action == "create":
        if not args.dir or not args.title:
            print("Please specify --dir and --title")
            return
        content = args.content or f"# {args.title}\n\n开始写..."
        sync.create_note(args.dir, args.title, content)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 设置执行权限**

```bash
chmod +x ~/p8_CR/user-research-agents/scripts/obsidian-sync.py
```

- [ ] **Step 3: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add scripts/obsidian-sync.py
git commit -m "feat: add obsidian sync tool"
```

---

## 第五阶段：验证与文档 (Phase 3)

### Task 10: 验证与 README

**Files:**
- Create: `~/p8_CR/user-research-agents/README.md`

- [ ] **Step 1: 创建 README**

```markdown
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
```

- [ ] **Step 2: 提交**

```bash
cd ~/p8_CR/user-research-agents
git add README.md
git commit -m "docs: add README"
```

---

## 实现计划摘要

| Task | 内容 | 复杂度 |
|------|------|--------|
| 1 | Docker Compose 配置 | 低 |
| 2 | Obsidian Vault 模板 | 低 |
| 3 | 主技能定义 (skill.md) | 低 |
| 4 | Data Fusion Agent | 中 |
| 5 | Full-Cycle UR Agent | 中 |
| 6 | Global Insight Agent | 中 |
| 7 | Process & Compliance Agents | 低 |
| 8 | Prompt 模板库 | 中 |
| 9 | Obsidian 同步工具 | 中 |
| 10 | README 与验证 | 低 |

**预计总时间**: 3-4 小时（按 Task 顺序执行）

---

**Plan complete and saved to `~/p8_CR/user-research-agents/docs/plans/`**

两个执行选项：

**1. Subagent-Driven (recommended)** - 我调度独立子 Agent 按 Task 执行，每完成几个 Task 后回顾检查

**2. Inline Execution** - 在当前 Session 中按批次执行，中途有检查点

选择哪种方式？
# tech-discussion-manager | 技术讨论管理技能

[![ClawHub Compatible](https://img.shields.io/badge/ClawHub-Compatible-brightgreen)](https://clawhub.ai)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

标准化技术讨论和创意沉淀技能，自动创建规范的目录结构和记录模板，让智能体帮你自动管理技术知识。

## ✨ 特性
- 🤖 **智能体原生支持**：安装后自动成为AI的行为准则，无需手动调用
- 📝 **标准化模板**：统一的讨论记录格式，包含背景、要点、决策、待办等
- 📂 **自动目录创建**：每个讨论自动生成对应代码输出目录
- 🔄 **自动索引维护**：自动更新讨论索引，方便检索
- 📦 **归档机制**：历史讨论一键归档，保持目录整洁
- 🤝 **多智能体协同**：统一存储结构，支持多AI协同工作
- 🚀 **零依赖**：纯规则驱动，不需要运行任何服务或脚本

## 🚀 安装

### 通过 ClawHub 安装（推荐）
```bash
# 搜索技能
clawhub search tech-discussion-manager

# 安装
clawhub install tech-discussion-manager
```

### 手动安装
1. 下载技能到OpenClaw技能目录：
```bash
git clone https://github.com/your-repo/tech-discussion-manager.git ~/.openclaw/skills/tech-discussion-manager
```

2. 执行安装步骤：
```bash
# 创建目录结构
mkdir -p $OPENCLAW_WORKSPACE/memory/tech-discussions/archive $OPENCLAW_WORKSPACE/code-output $OPENCLAW_WORKSPACE/docs/decisions $OPENCLAW_WORKSPACE/docs/architecture

# 安装模板
cp ~/.openclaw/skills/tech-discussion-manager/templates/*.md $OPENCLAW_WORKSPACE/memory/tech-discussions/

# 添加规则到智能体配置
grep -q "技术讨论沉淀规则" $OPENCLAW_WORKSPACE/AGENTS.md || echo -e "\n### 💬 技术讨论沉淀规则\n1. 所有技术讨论必须使用 tech-discussion-manager 技能管理\n2. 讨论记录使用标准模板保存到 memory/tech-discussions/ 目录\n3. 代码产出必须保存到 code-output/ 对应主题目录\n4. 重要决策必须同步到 MEMORY.md 和 docs/decisions/ 目录\n5. 讨论结束后必须更新 memory/tech-discussions/index.md 索引" >> $OPENCLAW_WORKSPACE/AGENTS.md
```

## 🎯 使用方式

### 完全自动化使用（推荐）
安装后不需要任何手动操作，智能体会自动识别技术讨论场景：

```
用户：我们来讨论一下GEO工具的架构设计
智能体：✅ 已为你创建技术讨论记录：
📝 讨论文件：memory/tech-discussions/2026-03-29-geo工具架构设计.md
📂 代码目录：code-output/geo工具架构设计/
我们可以开始讨论，我会实时记录要点和决策。
```

### 触发关键词
当对话中包含以下词汇时，智能体自动触发技能：
- "讨论一下"、"技术评审"、"方案设计"
- "需求评审"、"架构设计"、"brainstorm"
- "头脑风暴"、"记录一下"、"存档"

### 手动触发
如果需要手动创建讨论，可以直接告诉AI：
```
用户：帮我创建一个关于微服务拆分的技术讨论
智能体：✅ 已创建技术讨论记录...
```

## 📁 存储结构
所有数据都保存在你的工作空间，完全可控：
```
your-workspace/
├── memory/
│   └── tech-discussions/
│       ├── archive/                # 已归档的历史讨论
│       ├── TEMPLATE.md             # 讨论记录模板
│       ├── index.md                # 讨论索引目录
│       └── YYYY-MM-DD-主题.md       # 具体讨论记录
├── code-output/
│   └── 主题名称/                    # 每个讨论对应的代码输出目录
│       ├── v1.0/
│       └── README.md
└── docs/
    ├── decisions/                  # 沉淀的正式技术决策
    └── architecture/               # 架构设计文档
```

## 🔧 智能体记忆集成
安装后会自动将规则写入 `AGENTS.md`，成为智能体的永久行为准则：
1. 所有技术讨论必须使用本技能管理
2. 讨论记录必须使用标准模板
3. 代码产出必须和讨论记录关联
4. 重要决策必须同步到长期记忆
5. 自动维护讨论索引

## 📝 讨论记录模板
```markdown
# [主题] GEO工具架构设计
时间：2026-03-29 15:30
参与方：用户、凯撒
状态：进行中
标签：[GEO] [架构设计]

## 讨论背景
需要开发GEO在线检查工具，讨论技术选型和架构方案

## 讨论要点
- [x] 前端技术选型：Next.js + TypeScript
- [ ] 后端架构设计

## 决策结论
- 结论1：选择getcito作为参考项目，成熟度最高
- 结论2：核心功能包含多地区模拟、AI搜索引擎对接、优化评分模型

## 待办事项
- [ ] 调研getcito架构，输出可行性分析
```

## 🤝 多智能体协同
多个智能体可以同时使用本技能：
- 统一存储结构，所有讨论都保存在工作空间
- 自动避免文件名冲突
- 支持协同编辑同一份讨论记录
- 状态实时同步

## 📄 许可证
MIT License

## 🆘 问题反馈
如有问题请提交Issue到GitHub仓库。

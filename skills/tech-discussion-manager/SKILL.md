---
name: tech-discussion-manager
version: "0.1.1"
description: 技术讨论管理技能，自动创建结构化的讨论记录、代码输出目录，沉淀技术决策和创意，支持多智能体协同使用。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": [],
            "env": ["OPENCLAW_WORKSPACE"],
          },
        "install":
          [
            {
              "id": "setup-directories",
              "kind": "shell",
              "script": "mkdir -p \"$OPENCLAW_WORKSPACE/memory/tech-discussions/archive\" \"$OPENCLAW_WORKSPACE/code-output\" \"$OPENCLAW_WORKSPACE/docs/decisions\" \"$OPENCLAW_WORKSPACE/docs/architecture\"",
              "label": "创建标准目录结构",
            },
            {
              "id": "install-templates",
              "kind": "shell",
              "script": "cp -n ./templates/*.md \"$OPENCLAW_WORKSPACE/memory/tech-discussions/\" 2>/dev/null || true",
              "label": "安装模板文件",
            },
          ],
      },
  }
---

# tech-discussion-manager 技术讨论管理技能

## 功能概述
标准化管理技术讨论和创意沉淀的技能，帮助自动创建规范的目录结构、讨论记录模板，确保技术知识完整留存。

## 核心功能
- 📝 标准化技术讨论记录模板
- 📂 自动创建关联代码输出目录
- 🔄 自动维护讨论索引
- 📦 讨论归档机制
- 🤝 多智能体协同支持
- 🔍 便于后续检索和回顾

## 智能体使用规范
当用户发起技术讨论时，智能体**推荐**按照以下流程执行：

### 1. 讨论启动流程
当用户提到以下关键词时，**可以**触发技能：
- "我们讨论一下..."
- "技术方案评审"
- "需求评审"
- "架构设计讨论"
- "创意 brainstorm"
- "记录一下这个讨论"

**注意：** 也可以直接在当前对话中记录讨论，不强制使用技能。

自动执行以下操作：
```markdown
我已经帮你创建了技术讨论记录：
📝 讨论文件：`memory/tech-discussions/YYYY-MM-DD-主题.md`
📂 代码目录：`code-output/[主题]/`

我们可以开始讨论了，我会实时记录要点和决策。
```

### 2. 讨论记录格式
建议按照以下结构记录：
```markdown
# [主题] 技术方案讨论
时间：YYYY-MM-DD HH:MM
参与方：{{PARTICIPANTS}}
状态：进行中 / 已完成
标签：{{TAGS}}

## 讨论背景
[自动填充讨论背景]

## 讨论要点
- [ ] 要点1：xxx
- [ ] 要点2：xxx

## 决策结论
- 结论1：xxx，原因：xxx
- 结论2：xxx，原因：xxx

## 待办事项
- [ ] 任务1：xxx，负责人：xxx，截止时间：xxx
- [ ] 任务2：xxx，负责人：xxx，截止时间：xxx

## 相关产出
- 代码输出：`code-output/[主题]/`
- 文档：`docs/`
- 参考链接：
```

### 3. 讨论结束流程
当用户表示讨论结束时，可以执行：
1. 整理讨论内容，提炼核心结论
2. 更新讨论状态为"已完成"
3. 如有需要，将重要结论同步到 `MEMORY.md`
4. 如需归档，移动到 `archive/` 目录
5. 更新 `index.md` 索引

### 4. 目录结构规范
```
$OPENCLAW_WORKSPACE/
├── memory/
│   └── tech-discussions/
│       ├── archive/                # 归档历史讨论
│       ├── TEMPLATE.md             # 讨论模板
│       ├── index.md                # 讨论索引
│       └── YYYY-MM-DD-主题.md       # 具体讨论记录
├── code-output/                    # 代码输出目录
│   └── [讨论主题]/                  # 每个讨论对应独立代码目录
└── docs/
    ├── decisions/                  # 正式决策文档
    └── architecture/               # 架构设计文档
```

### 5. 讨论索引维护
在 `memory/tech-discussions/index.md` 中维护所有讨论的索引：

```markdown
# 技术讨论索引

## 进行中
| 日期 | 主题 | 状态 | 标签 |
|------|------|------|------|
| YYYY-MM-DD | 主题名称 | 进行中 | xxx |

## 已完成
| 日期 | 主题 | 决策摘要 | 标签 |
|------|------|----------|------|
| YYYY-MM-DD | 主题名称 | 决策简述 | xxx |
```

## 记忆系统集成
本技能作为**可选工具**提供：
- 推荐使用本技能管理技术讨论（但不强制）
- 讨论记录默认保存到 `memory/tech-discussions/`（可自定义位置）
- 也可以直接在当前对话中记录，不强制使用技能
- 重要结论建议同步到 `MEMORY.md` 长期保存
- 所有讨论结构化留存，便于后续检索

## 与其他技能的关系
- 本技能专注于**讨论记录和知识沉淀**
- 代码产出可以配合其他技能（如 code generator）使用
- 决策文档可以配合文档类技能使用

## 用户使用示例
```
用户：我们讨论一下GEO工具的架构设计
智能体：✅ 已创建技术讨论记录：
📝 讨论文件：memory/tech-discussions/2026-04-02-geo工具架构设计.md
📂 代码目录：code-output/geo工具架构设计/
请开始讨论，我会实时记录要点。

---

用户：讨论结束
智能体：好的，已整理讨论结论：
📝 讨论文件：memory/tech-discussions/2026-04-02-geo工具架构设计.md
📝 索引已更新：memory/tech-discussions/index.md
💡 核心决策已同步到 MEMORY.md
```

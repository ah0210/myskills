---
name: 技术讨论管理和沉淀
slug: tech-discussion-manager
version: "0.5.0"
description: 技术讨论管理和沉淀技能，自动创建结构化的讨论记录、代码输出目录，沉淀技术决策和创意，支持 Git 版本管理（可选），支持多智能体协同使用。
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
              "script": "mkdir -p \"$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/discussions\" \"$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/decisions\" \"$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/architecture\" \"$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/dev-plans\" \"$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/code-output\"",
              "label": "创建标准目录结构",
            },
            {
              "id": "install-templates",
              "kind": "shell",
              "script": "cp -n ./templates/*.md \"./$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/\" 2>/dev/null || true",
              "label": "安装模板文件",
            },
          ],
      },
  }
---

# 技术讨论管理和沉淀

## 功能概述
标准化管理技术讨论和创意沉淀的技能，帮助自动创建规范的目录结构、讨论记录模板，确保技术知识完整留存。支持 Git 版本管理作为可选增强功能。

## 核心功能
- 📝 标准化技术讨论记录模板
- 📂 自动创建关联代码输出目录
- 🔄 自动维护讨论索引
- 📦 讨论归档机制
- 🤝 多智能体协同支持
- 🔍 便于后续检索和回顾
- 🌿 Git 版本管理（可选增强）
- 📋 决策文档和架构文档生成
- 📅 开发规划生成（含甘特图）
- 🏷️ 版本记录和标签管理（需 Git）

## Git 增强功能（可选）
- 💡 **说明**：Git 是可选增强功能，不影响基础功能使用
- ✅ **有 Git 时**：自动启用版本管理、自动提交、标签管理
- ❌ **无 Git 时**：所有基础功能正常使用，仅跳过 Git 相关操作

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
📝 讨论文件：`projects/tech-discussion-manager/docs/discussions/YYYY-MM-DD-主题.md`
📂 代码目录：`projects/tech-discussion-manager/code-output/[主题]/`

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
- 代码输出：`projects/tech-discussion-manager/code-output/[主题]/`
- 文档：`projects/tech-discussion-manager/docs/`
- 参考链接：
```

### 3. 列出讨论列表
当用户提到以下关键词时，列出所有讨论：
- "列出讨论"
- "讨论列表"
- "查看讨论"

输出格式：
```markdown
📋 技术讨论列表

## 已完成
- [2026-04-04] GEO工具架构设计 ✅
- [2026-04-03] 数据库选型讨论 ✅

## 进行中
- [2026-04-04] API接口设计 🔄
```

### 4. 生成决策文档
当用户提到以下关键词时，生成决策文档：
- "生成决策"
- "决策文档"

### 5. 生成架构文档
当用户提到以下关键词时，生成架构文档：
- "生成架构"
- "架构文档"

### 6. 开始开发流程
当用户提到以下关键词时，开始开发流程：
- "开始开发"
- "启动开发"

流程：
1. 列出已完成的讨论
2. 用户选择一个讨论
3. 确认决策文档
4. 确认架构文档
5. 生成开发规划文档
6. 创建代码目录
7. （可选）初始化 Git 仓库
8. （可选）Git 提交所有变更

### 7. 开发规划文档
开发规划包含：
- 项目信息
- 技术栈
- 开发阶段划分
- 甘特图（Mermaid）
- 里程碑
- 任务清单

### 8. 记录版本（需 Git）
当用户提到以下关键词时，记录版本：
- "记录版本"
- "版本更新"

**注意**：此功能需要 Git 支持。

流程：
1. 检查 Git 是否可用
2. 询问版本号（v1.0.0, v1.0.1 等）
3. 询问版本说明
4. Git add 所有变更
5. Git commit
6. Git tag 打版本标签

### 9. 确认开发完成
当用户提到以下关键词时，确认开发完成：
- "开发完成"
- "确认完成"

### 10. 讨论结束流程
当用户表示讨论结束时，可以执行：
1. 整理讨论内容，提炼核心结论
2. 更新讨论状态为"已完成"
3. 如有需要，将重要结论同步到 `MEMORY.md`
4. 如需归档，移动到 `archive/` 目录
5. 更新 `index.md` 索引
6. （可选）Git 提交变更

### 11. 目录结构规范
```
$OPENCLAW_WORKSPACE/
└── projects/
    └── tech-discussion-manager/
        ├── .git/                    # Git 仓库（可选）
        ├── .gitignore                # Git 忽略文件
        ├── docs/                     # 所有文档
        │   ├── discussions/          # 讨论记录
        │   │   └── YYYY-MM-DD-主题.md
        │   ├── decisions/            # 决策文档
        │   │   └── [项目名]-decision.md
        │   ├── architecture/         # 架构文档
        │   │   └── [项目名]-architecture.md
        │   ├── dev-plans/            # 开发规划
        │   │   └── [项目名]-plan.md
        │   └── index.md              # 讨论索引
        └── code-output/              # 代码输出
            └── [项目名]/
                ├── .git/             # 独立 Git 仓库（可选）
                ├── .gitignore
                ├── README.md
                └── [代码文件]
```

### 12. 讨论索引维护
在 `projects/tech-discussion-manager/docs/index.md` 中维护所有讨论的索引：

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
- 讨论记录默认保存到 `projects/tech-discussion-manager/docs/`（可自定义位置）
- 也可以直接在当前对话中记录，不强制使用技能
- 重要结论建议同步到 `MEMORY.md` 长期保存
- 所有讨论结构化留存，便于后续检索
- Git 版本管理为可选增强功能

## Git 使用说明（可选）

### Git 可用性检查
使用前先检查 Git 是否可用：
- 可用：自动启用 Git 相关功能
- 不可用：跳过 Git 操作，基础功能正常使用

### 初始化 Git 仓库（可选）
首次使用且 Git 可用时，可自动执行：
```bash
git init
git add .
git commit -m "初始化 tech-discussion-manager 项目"
```

### 自动提交（可选）
Git 可用时，每次生成或修改文档时自动提交：
- 新建讨论：`新增讨论: [主题]`
- 更新决策：`更新决策文档: [项目名] v1.0 -> v1.1`
- 生成规划：`新增开发规划: [项目名]`

### 版本标签（可选，需 Git）
使用 Git tag 标记版本：
```bash
git tag -a v1.0.0 -m "版本 v1.0.0"
```

### 远程仓库（可选）
用户可以配置远程仓库：
```bash
git remote add origin <仓库URL>
git push -u origin main
```

## 与其他技能的关系
- 本技能专注于**讨论记录和知识沉淀**
- 代码产出可以配合其他技能（如 code generator）使用
- 决策文档可以配合文档类技能使用
- Git 版本管理为可选增强，与其他 Git 工具兼容

## 用户使用示例

### 基础模式（无 Git）
```
用户：我们讨论一下GEO工具的架构设计
智能体：✅ 已创建技术讨论记录：
📝 讨论文件：projects/tech-discussion-manager/docs/discussions/2026-04-02-geo工具架构设计.md
📂 代码目录：projects/tech-discussion-manager/code-output/geo工具架构设计/
请开始讨论，我会实时记录要点。

---

用户：讨论结束
智能体：好的，已整理讨论结论：
📝 讨论文件：projects/tech-discussion-manager/docs/discussions/2026-04-02-geo工具架构设计.md
📝 索引已更新：projects/tech-discussion-manager/docs/index.md
💡 核心决策已同步到 MEMORY.md
```

### 增强模式（有 Git）
```
用户：我们讨论一下GEO工具的架构设计
智能体：✅ 已创建技术讨论记录：
📝 讨论文件：projects/tech-discussion-manager/docs/discussions/2026-04-02-geo工具架构设计.md
📂 代码目录：projects/tech-discussion-manager/code-output/geo工具架构设计/
🌿 Git 已提交：新增讨论: geo工具架构设计
请开始讨论，我会实时记录要点。

---

用户：讨论结束
智能体：好的，已整理讨论结论：
📝 讨论文件：projects/tech-discussion-manager/docs/discussions/2026-04-02-geo工具架构设计.md
📝 索引已更新：projects/tech-discussion-manager/docs/index.md
💡 核心决策已同步到 MEMORY.md
🌿 Git 已提交

---

用户：开始开发
智能体：📋 已完成的讨论列表：
1. [2026-04-02] GEO工具架构设计
2. [2026-04-01] 数据库选型

请选择要开发的讨论（输入序号）：

用户：1
智能体：✅ 已选择讨论：GEO工具架构设计
📝 生成决策文档...
📝 生成架构文档...
📝 生成开发规划...
📂 创建代码目录...
🌿 初始化 Git 仓库...
✅ 所有变更已提交到 Git

开发规划已生成：projects/tech-discussion-manager/docs/dev-plans/geo工具-plan.md
代码目录：projects/tech-discussion-manager/code-output/geo工具/

---

用户：记录版本
智能体：请输入版本号（例如 v1.0.0）：

用户：v1.0.0
智能体：请输入版本说明：

用户：初始版本发布
智能体：✅ 版本 v1.0.0 已记录
🌿 Git commit: v1.0.0 - 初始版本发布
🏷️ Git tag: v1.0.0
```

## 跨环境使用指南

### 支持的环境
- ✅ OpenClaw（原生支持）
- ✅ 其他 AI 智能体平台
- ✅ 本地 IDE（VS Code、PyCharm 等）
- ✅ 命令行直接使用

### 环境要求
| 依赖 | 必需 | 说明 |
|------|------|------|
| OPENCLAW_WORKSPACE 环境变量 | ✅ 是 | 指定工作空间根目录 |
| Bash（Linux/macOS）或 PowerShell（Windows） | ✅ 是 | 运行安装脚本 |
| Git | ❌ 否 | 可选增强功能 |

### 快速开始

#### 方式 1：在 OpenClaw 中使用（推荐）
无需额外配置，直接使用技能即可。

#### 方式 2：使用安装脚本（推荐）
1. **设置环境变量**
   ```bash
   # Linux/macOS
   export OPENCLAW_WORKSPACE=/path/to/your/workspace
   
   # Windows PowerShell
   $env:OPENCLAW_WORKSPACE = "C:\path\to\your\workspace"
   ```

2. **运行安装脚本**
   ```bash
   # Linux/macOS
   bash install.sh
   
   # Windows PowerShell
   .\install.ps1
   ```

3. **按照使用规范开始使用**

#### 方式 3：手动安装
如果无法运行脚本，请参考下文的"手动安装步骤"。

---

## 环境变量配置详解

### OPENCLAW_WORKSPACE
这是唯一必需的环境变量，指定你的工作空间根目录。

#### Linux/macOS 配置
```bash
# 临时设置（当前终端有效）
export OPENCLAW_WORKSPACE=/home/你的用户名/workspace

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export OPENCLAW_WORKSPACE=/home/你的用户名/workspace' >> ~/.bashrc
source ~/.bashrc
```

#### Windows PowerShell 配置
```powershell
# 临时设置（当前终端有效）
$env:OPENCLAW_WORKSPACE = "C:\Users\你的用户名\workspace"

# 永久设置（当前用户）
[Environment]::SetEnvironmentVariable('OPENCLAW_WORKSPACE', 'C:\Users\你的用户名\workspace', 'User')
```

#### Windows CMD 配置
```cmd
# 临时设置（当前终端有效）
set OPENCLAW_WORKSPACE=C:\Users\你的用户名\workspace

# 永久设置（需要管理员权限）
setx OPENCLAW_WORKSPACE "C:\Users\你的用户名\workspace"
```

#### 在 IDE 中配置

##### VS Code
创建或编辑 `.vscode/settings.json`：
```json
{
  "terminal.integrated.env.linux": {
    "OPENCLAW_WORKSPACE": "/home/你的用户名/workspace"
  },
  "terminal.integrated.env.osx": {
    "OPENCLAW_WORKSPACE": "/Users/你的用户名/workspace"
  },
  "terminal.integrated.env.windows": {
    "OPENCLAW_WORKSPACE": "C:\\Users\\你的用户名\\workspace"
  }
}
```

##### PyCharm
1. 打开 `Run` → `Edit Configurations`
2. 选择你的配置
3. 在 `Environment variables` 中添加：
   - Name: `OPENCLAW_WORKSPACE`
   - Value: 你的工作空间路径

---

## 手动安装步骤

如果无法运行安装脚本，可以按照以下步骤手动操作：

### 1. 创建目录结构

#### Linux/macOS
```bash
mkdir -p "$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/discussions"
mkdir -p "$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/decisions"
mkdir -p "$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/architecture"
mkdir -p "$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/dev-plans"
mkdir -p "$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/code-output"
```

#### Windows PowerShell
```powershell
$workspace = $env:OPENCLAW_WORKSPACE
New-Item -ItemType Directory -Path "$workspace\projects\tech-discussion-manager\docs\discussions" -Force
New-Item -ItemType Directory -Path "$workspace\projects\tech-discussion-manager\docs\decisions" -Force
New-Item -ItemType Directory -Path "$workspace\projects\tech-discussion-manager\docs\architecture" -Force
New-Item -ItemType Directory -Path "$workspace\projects\tech-discussion-manager\docs\dev-plans" -Force
New-Item -ItemType Directory -Path "$workspace\projects\tech-discussion-manager\code-output" -Force
```

### 2. 复制模板文件

将技能包 `templates/` 目录下的所有文件复制到：
```
$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/docs/
```

### 3. （可选）初始化 Git 仓库

```bash
cd "$OPENCLAW_WORKSPACE/projects/tech-discussion-manager"
git init
git add .
git commit -m "初始化 tech-discussion-manager 项目"
```

---

## 安装脚本使用说明

### install.sh（Linux/macOS）

#### 功能特性
- ✅ 自动检查环境变量
- ✅ 彩色输出，清晰易读
- ✅ 错误处理和友好提示
- ✅ 不覆盖已存在的文件
- ✅ 可选 Git 初始化

#### 使用方法
```bash
# 基本使用
bash install.sh
```

### install.ps1（Windows PowerShell）

#### 功能特性
- ✅ 自动检查环境变量
- ✅ 彩色输出，清晰易读
- ✅ 错误处理和友好提示
- ✅ 不覆盖已存在的文件
- ✅ 可选 Git 初始化
- ✅ 支持 Windows 路径格式

#### 使用方法
```powershell
# 基本使用
.\install.ps1
```

#### 执行策略问题
如果遇到执行策略限制：
```powershell
# 临时允许（当前终端有效）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 然后运行脚本
.\install.ps1
```

---

## 常见问题

### Q: 提示 "OPENCLAW_WORKSPACE 环境变量未设置"
A: 请参考上方的"环境变量配置详解"章节进行设置。

### Q: 权限被拒绝
A: 确保你对工作空间目录有读写权限。

### Q: Git 初始化失败
A: Git 是可选功能，即使初始化失败，基础功能仍然可以使用。

### Q: 可以在多个工作空间使用吗？
A: 可以！每次切换工作空间时，只需更新 `OPENCLAW_WORKSPACE` 环境变量即可。

### Q: 如何卸载？
A: 直接删除 `$OPENCLAW_WORKSPACE/projects/tech-discussion-manager/` 目录即可。

# 安装指南

## 标准安装方式（通过 SkillHub）

### 1. 安装 SkillHub CLI（如果未安装）
```bash
skillhub install tech-discussion-manager
```

SkillHub CLI 会自动检测环境并安装全部依赖。

### 2. 安装技能
```bash
skillhub install_skill tech-discussion-manager
```

安装过程会自动完成：
- ✅ 创建标准目录结构
- ✅ 安装模板文件

## 手动安装方式

### 1. 下载技能
将技能文件复制到 OpenClaw 技能目录：
```
~/.openclaw/skills/tech-discussion-manager/
```

### 2. 创建目录结构
```powershell
# PowerShell 示例
$workspace = $env:OPENCLAW_WORKSPACE
New-Item -ItemType Directory -Path "$workspace/memory/tech-discussions/archive" -Force
New-Item -ItemType Directory -Path "$workspace/code-output" -Force
New-Item -ItemType Directory -Path "$workspace/docs/decisions" -Force
New-Item -ItemType Directory -Path "$workspace/docs/architecture" -Force
```

### 3. 安装模板文件
```powershell
Copy-Item -Path "./templates/*.md" -Destination "$env:OPENCLAW_WORKSPACE/memory/tech-discussions/" -ErrorAction SilentlyContinue
```

## 验证安装

安装完成后，可以通过以下方式验证：

1. 检查目录结构是否创建成功：
```powershell
Get-ChildItem $env:OPENCLAW_WORKSPACE/memory/tech-discussions/
# 应该包含 archive/ 目录、模板文件
```

2. 测试智能体触发：
```
用户：我们讨论一下GEO工具的开发
智能体应该回复：✅ 已为你创建技术讨论记录...
```

## 卸载方式

### 通过 SkillHub 卸载
```bash
skillhub uninstall tech-discussion-manager
```

### 手动卸载
1. 删除技能目录：
```powershell
Remove-Item -Recurse -Path "~/.openclaw/skills/tech-discussion-manager"
```

2. （可选）删除讨论数据：
```powershell
# 注意：这会删除所有历史讨论记录，请谨慎操作
Remove-Item -Recurse -Path "$env:OPENCLAW_WORKSPACE/memory/tech-discussions/"
```

## 升级方式

### 通过 SkillHub 升级
```bash
skillhub update tech-discussion-manager
```

### 手动升级
下载最新版本的技能文件，覆盖到技能目录即可。

## 多工作空间支持

技能安装在集中位置，但数据保存在各工作空间：
- 技能本身：集中管理，一处安装多处使用
- 讨论数据：保存在各 `$OPENCLAW_WORKSPACE` 目录下
- 工作空间之间完全隔离，互不影响

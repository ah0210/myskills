# ==========================================
# 技术讨论管理和沉淀 - Windows PowerShell 安装脚本
# 要求：PowerShell 7.0+
# ==========================================

#Requires -Version 7.0

# 脚本目录
$ScriptDir = $PSScriptRoot

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  技术讨论管理和沉淀 - 安装脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查环境变量
Write-Host "[1/5] 检查环境变量..." -ForegroundColor Cyan

$Workspace = $env:OPENCLAW_WORKSPACE
if (-not $Workspace) {
    Write-Host "错误: " -ForegroundColor Red -NoNewline
    Write-Host "OPENCLAW_WORKSPACE 环境变量未设置"
    Write-Host ""
    Write-Host "请先设置环境变量，例如："
    Write-Host "  `$env:OPENCLAW_WORKSPACE = 'C:\Users\你的用户名\workspace'"
    Write-Host ""
    Write-Host "然后重新运行此脚本"
    exit 1
}

Write-Host "✓" -ForegroundColor Green -NoNewline
Write-Host " OPENCLAW_WORKSPACE=$Workspace"

# 2. 创建目录结构
Write-Host ""
Write-Host "[2/5] 创建目录结构..." -ForegroundColor Cyan

$BaseDir = Join-Path $Workspace "projects\tech-discussion-manager"
$Dirs = @(
    Join-Path $BaseDir "docs\discussions"
    Join-Path $BaseDir "docs\decisions"
    Join-Path $BaseDir "docs\architecture"
    Join-Path $BaseDir "docs\dev-plans"
    Join-Path $BaseDir "code-output"
)

foreach ($Dir in $Dirs) {
    if (-not (Test-Path $Dir)) {
        New-Item -ItemType Directory -Path $Dir -Force | Out-Null
        Write-Host "✓" -ForegroundColor Green -NoNewline
        Write-Host " 创建目录: $Dir"
    } else {
        Write-Host "⚠" -ForegroundColor Yellow -NoNewline
        Write-Host "  目录已存在: $Dir"
    }
}

# 3. 复制模板文件
Write-Host ""
Write-Host "[3/5] 复制模板文件..." -ForegroundColor Cyan

$TemplateDir = Join-Path $ScriptDir "templates"
$DestDir = Join-Path $BaseDir "docs"

if (-not (Test-Path $TemplateDir)) {
    Write-Host "⚠" -ForegroundColor Yellow -NoNewline
    Write-Host "  模板目录不存在: $TemplateDir"
} else {
    $Templates = Get-ChildItem -Path $TemplateDir -File
    foreach ($Template in $Templates) {
        $DestFile = Join-Path $DestDir $Template.Name
        if (-not (Test-Path $DestFile)) {
            Copy-Item -Path $Template.FullName -Destination $DestFile
            Write-Host "✓" -ForegroundColor Green -NoNewline
            Write-Host " 复制模板: $($Template.Name)"
        } else {
            Write-Host "⚠" -ForegroundColor Yellow -NoNewline
            Write-Host "  模板已存在，跳过: $($Template.Name)"
        }
    }
}

# 4. 检查 Git
Write-Host ""
Write-Host "[4/5] 检查 Git..." -ForegroundColor Cyan

$GitAvailable = $false
try {
    $null = Get-Command git -ErrorAction Stop
    $GitAvailable = $true
    Write-Host "✓" -ForegroundColor Green -NoNewline
    Write-Host " Git 已安装"
} catch {
    Write-Host "⚠" -ForegroundColor Yellow -NoNewline
    Write-Host "  Git 未安装，跳过 Git 相关功能"
    Write-Host "⚠" -ForegroundColor Yellow -NoNewline
    Write-Host "  基础功能仍然可以正常使用"
}

if ($GitAvailable) {
    $GitDir = Join-Path $BaseDir ".git"
    if (-not (Test-Path $GitDir)) {
        Write-Host ""
        Write-Host "初始化 Git 仓库..." -ForegroundColor Cyan
        try {
            Push-Location $BaseDir
            git init | Out-Null
            git add . | Out-Null
            git commit -m "初始化 tech-discussion-manager 项目" | Out-Null
            Pop-Location
            Write-Host "✓" -ForegroundColor Green -NoNewline
            Write-Host " Git 仓库初始化完成"
        } catch {
            Write-Host "⚠" -ForegroundColor Yellow -NoNewline
            Write-Host "  Git 初始化失败，继续执行"
        }
    } else {
        Write-Host "⚠" -ForegroundColor Yellow -NoNewline
        Write-Host "  Git 仓库已存在，跳过初始化"
    }
}

# 5. 完成
Write-Host ""
Write-Host "[5/5] 安装完成！" -ForegroundColor Cyan
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  安装成功！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "项目目录: $BaseDir"
Write-Host ""
Write-Host "下一步："
Write-Host "  1. 阅读 SKILL.md 了解使用方法"
Write-Host "  2. 开始你的技术讨论！"
Write-Host ""

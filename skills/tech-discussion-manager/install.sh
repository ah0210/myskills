#!/bin/bash
set -e

# ==========================================
# 技术讨论管理和沉淀 - Linux/macOS 安装脚本
# ==========================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}"
echo "=========================================="
echo "  技术讨论管理和沉淀 - 安装脚本"
echo "=========================================="
echo -e "${NC}"

# 1. 检查环境变量
echo -e "${BLUE}[1/5]${NC} 检查环境变量..."
if [ -z "$OPENCLAW_WORKSPACE" ]; then
    echo -e "${RED}错误:${NC} OPENCLAW_WORKSPACE 环境变量未设置"
    echo ""
    echo "请先设置环境变量，例如："
    echo "  export OPENCLAW_WORKSPACE=/home/你的用户名/workspace"
    echo ""
    echo "然后重新运行此脚本"
    exit 1
fi

echo -e "${GREEN}✓${NC} OPENCLAW_WORKSPACE=$OPENCLAW_WORKSPACE"

# 2. 创建目录结构
echo ""
echo -e "${BLUE}[2/5]${NC} 创建目录结构..."

BASE_DIR="$OPENCLAW_WORKSPACE/projects/tech-discussion-manager"
DIRS=(
    "$BASE_DIR/docs/discussions"
    "$BASE_DIR/docs/decisions"
    "$BASE_DIR/docs/architecture"
    "$BASE_DIR/docs/dev-plans"
    "$BASE_DIR/code-output"
)

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✓${NC} 创建目录: $dir"
    else
        echo -e "${YELLOW}⚠${NC}  目录已存在: $dir"
    fi
done

# 3. 复制模板文件
echo ""
echo -e "${BLUE}[3/5]${NC} 复制模板文件..."

TEMPLATE_DIR="$SCRIPT_DIR/templates"
DEST_DIR="$BASE_DIR/docs"

if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${YELLOW}⚠${NC}  模板目录不存在: $TEMPLATE_DIR"
else
    for template in "$TEMPLATE_DIR"/*; do
        if [ -f "$template" ]; then
            filename=$(basename "$template")
            dest="$DEST_DIR/$filename"
            if [ ! -f "$dest" ]; then
                cp "$template" "$dest"
                echo -e "${GREEN}✓${NC} 复制模板: $filename"
            else
                echo -e "${YELLOW}⚠${NC}  模板已存在，跳过: $filename"
            fi
        fi
    done
fi

# 4. 检查 Git
echo ""
echo -e "${BLUE}[4/5]${NC} 检查 Git..."

if command -v git &> /dev/null; then
    echo -e "${GREEN}✓${NC} Git 已安装"
    
    # 检查是否已初始化
    if [ ! -d "$BASE_DIR/.git" ]; then
        echo ""
        echo -e "${BLUE}初始化 Git 仓库...${NC}"
        cd "$BASE_DIR"
        git init > /dev/null 2>&1
        git add . > /dev/null 2>&1
        git commit -m "初始化 tech-discussion-manager 项目" > /dev/null 2>&1
        echo -e "${GREEN}✓${NC} Git 仓库初始化完成"
    else
        echo -e "${YELLOW}⚠${NC}  Git 仓库已存在，跳过初始化"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Git 未安装，跳过 Git 相关功能"
    echo -e "${YELLOW}⚠${NC}  基础功能仍然可以正常使用"
fi

# 5. 完成
echo ""
echo -e "${BLUE}[5/5]${NC} 安装完成！"
echo ""
echo -e "${GREEN}=========================================="
echo "  安装成功！"
echo "==========================================${NC}"
echo ""
echo "项目目录: $BASE_DIR"
echo ""
echo "下一步："
echo "  1. 阅读 SKILL.md 了解使用方法"
echo "  2. 开始你的技术讨论！"
echo ""

#!/bin/bash

# Linux/Mac 虚拟环境设置脚本

echo "========================================"
echo "WebParser 虚拟环境设置脚本"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "[1/4] 检查 Python 版本..."
python3 --version
echo ""

# 创建虚拟环境
echo "[2/4] 创建虚拟环境..."
if [ -d ".venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "错误: 创建虚拟环境失败"
        exit 1
    fi
    echo "虚拟环境创建成功"
fi
echo ""

# 激活虚拟环境
echo "[3/4] 激活虚拟环境..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "错误: 激活虚拟环境失败"
    exit 1
fi
echo "虚拟环境激活成功"
echo ""

# 升级 pip
echo "升级 pip..."
python -m pip install --upgrade pip
echo ""

# 安装依赖
echo "[4/4] 安装依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 安装依赖失败"
    exit 1
fi
echo ""

echo "========================================"
echo "设置完成！"
echo "========================================"
echo ""
echo "使用说明:"
echo "1. 激活虚拟环境: source .venv/bin/activate"
echo "2. 运行示例: python examples/basic_usage.py"
echo "3. 退出虚拟环境: deactivate"
echo ""

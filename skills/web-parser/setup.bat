@echo off
REM Windows PowerShell 虚拟环境设置脚本

echo ========================================
echo WebParser 虚拟环境设置脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

echo [1/4] 检查 Python 版本...
python --version
echo.

REM 创建虚拟环境
echo [2/4] 创建虚拟环境...
if exist .venv (
    echo 虚拟环境已存在，跳过创建
) else (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo 错误: 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)
echo.

REM 激活虚拟环境
echo [3/4] 激活虚拟环境...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 错误: 激活虚拟环境失败
    pause
    exit /b 1
)
echo 虚拟环境激活成功
echo.

REM 升级 pip
echo 升级 pip...
python -m pip install --upgrade pip
echo.

REM 安装依赖
echo [4/4] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo 设置完成！
echo ========================================
echo.
echo 使用说明:
echo 1. 激活虚拟环境: .venv\Scripts\activate.bat
echo 2. 运行示例: python examples\basic_usage.py
echo 3. 退出虚拟环境: deactivate
echo.
pause

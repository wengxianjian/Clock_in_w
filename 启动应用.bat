@echo off
chcp 65001 >nul
title 每日打卡应用
echo ========================================
echo       每日打卡应用 - 启动程序
echo ========================================
echo.
echo 正在启动应用...
echo.

cd /d "%~dp0"
python main.py

if %errorlevel% neq 0 (
    echo.
    echo 启动失败！请检查Python是否已安装。
    echo.
    pause
)
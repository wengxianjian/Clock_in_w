@echo off
chcp 65001
echo ========================================
echo 每日计划打卡应用 - 打包脚本
echo ========================================
echo.

echo [1/4] 检查PyInstaller是否已安装...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo 安装失败，请手动运行: pip install pyinstaller
        pause
        exit /b 1
    )
) else (
    echo PyInstaller已安装
)
echo.

echo [2/4] 清理旧的打包文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo 清理完成
echo.

echo [3/4] 开始打包...
pyinstaller --onefile --windowed --icon=clock_in_icon.png --name="每日计划打卡" main.py
if %errorlevel% neq 0 (
    echo 打包失败！
    pause
    exit /b 1
)
echo.

echo [4/4] 打包完成！
echo.
echo ========================================
echo 打包结果：
echo 可执行文件位置: dist\每日计划打卡.exe
echo.
echo 按任意键打开dist文件夹...
pause >nul
explorer dist

# ========================================
# Polygon Stock Fetcher 一鍵啟動腳本 (PowerShell)
# ========================================
# 說明：
# 此腳本會自動啟動 Polygon Stock Fetcher 應用程式
# 使用 Conda 環境 Polygon_stock_fetcher
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Polygon Stock Fetcher 啟動中..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 設置工作目錄
Set-Location -Path $PSScriptRoot
Write-Host "當前工作目錄: $PWD"
Write-Host ""

# 檢查 Python 環境
Write-Host "[1/3] 檢查 Python 環境..." -ForegroundColor Yellow
$pythonPath = "C:\Users\admin\anaconda3\envs\Polygon_stock_fetcher\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "[錯誤] 找不到 Python 環境！" -ForegroundColor Red
    Write-Host "請確認 Conda 環境 'Polygon_stock_fetcher' 已經安裝。" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}
Write-Host "[✓] Python 環境檢查完成" -ForegroundColor Green
Write-Host ""

# 檢查主程式
Write-Host "[2/3] 檢查主程式文件..." -ForegroundColor Yellow
if (-not (Test-Path "run_with_polygon.py")) {
    Write-Host "[錯誤] 找不到 run_with_polygon.py！" -ForegroundColor Red
    Write-Host "請確認您在正確的目錄中運行此腳本。" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}
Write-Host "[✓] 主程式文件檢查完成" -ForegroundColor Green
Write-Host ""

# 檢查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "[警告] 找不到 .env 文件！" -ForegroundColor Yellow
    Write-Host "請確認已經配置好 API Keys。" -ForegroundColor Yellow
    Write-Host ""
}

# 啟動應用程式
Write-Host "[3/3] 啟動應用程式..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  程式運行中..." -ForegroundColor Cyan
Write-Host "  按 Ctrl+C 可以停止程式" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 使用完整路徑執行 Python
try {
    & $pythonPath run_with_polygon.py
} catch {
    Write-Host ""
    Write-Host "[錯誤] 程式執行時發生錯誤：" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
}

# 程式結束
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  程式已結束" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
pause

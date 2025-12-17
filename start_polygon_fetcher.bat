@echo off
chcp 65001 >nul
REM ========================================
REM Polygon Stock Fetcher - Quick Start Script
REM ========================================
REM This script automatically starts the Polygon Stock Fetcher application
REM Using Conda environment: Polygon_stock_fetcher
REM ========================================

echo.
echo ========================================
echo   Polygon Stock Fetcher Starting...
echo ========================================
echo.

REM Set working directory
cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Check Python environment
echo [1/3] Checking Python environment...
if not exist "C:\Users\admin\anaconda3\envs\Polygon_stock_fetcher\python.exe" (
    echo [ERROR] Python environment not found!
    echo Please ensure Conda environment 'Polygon_stock_fetcher' is installed.
    echo.
    pause
    exit /b 1
)
echo [OK] Python environment check complete
echo.

REM Check main program
echo [2/3] Checking main program file...
if not exist "run_with_polygon.py" (
    echo [ERROR] run_with_polygon.py not found!
    echo Please ensure you are running this script in the correct directory.
    echo.
    pause
    exit /b 1
)
echo [OK] Main program file check complete
echo.

REM Start application
echo [3/3] Starting application...
echo.
echo ========================================
echo   Program is running...
echo   Press Ctrl+C to stop the program
echo ========================================
echo.

REM Execute Python with full path
C:\Users\admin\anaconda3\envs\Polygon_stock_fetcher\python.exe run_with_polygon.py

REM Program finished
echo.
echo ========================================
echo   Program terminated
echo ========================================
echo.
pause

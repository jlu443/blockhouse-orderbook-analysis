@echo off
echo Compiling Order Book Analysis (C++)...

REM Add MinGW to PATH
set PATH=%PATH%;C:\msys64\mingw64\bin

REM Check if g++ is available
where g++ >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: g++ not found. Please install MinGW-w64 or MSYS2.
    echo You can download it from: https://www.msys2.org/
    pause
    exit /b 1
)

REM Compile the program
g++ -std=c++17 -O3 -Wall -Wextra -o order_book_analysis.exe order_book_analysis.cpp

if %ERRORLEVEL% EQU 0 (
    echo Compilation successful!
    echo Running analysis...
    echo.
    order_book_analysis.exe
) else (
    echo Compilation failed!
    pause
)

pause

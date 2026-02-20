@echo off
REM Build script for Scumgenics Save Manager
REM Creates a standalone executable in the dist/ folder

echo ========================================
echo Building Scumgenics Save Manager
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Build the executable
echo Building executable...
pyinstaller Scumgenics.spec
echo.

REM Check if build was successful
if exist "dist\Scumgenics.exe" (
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo Executable location: dist\Scumgenics.exe
    echo.
    echo The exe is ready to distribute. Users can run it without Python installed.
    echo.
    echo IMPORTANT: When distributing, remind users that:
    echo   - The app creates logs/ and backups/ folders in the same directory as the exe
    echo   - They should place the exe in a permanent location (not Downloads or Temp^)
    echo   - Mewgenics must be installed and run at least once before using this tool
    echo.
    goto :success
)

echo ========================================
echo Build failed!
echo ========================================
echo Check the output above for errors.
echo.

:success

pause

# Windows Build Testing Guide

This guide helps test the Windows build process without actually being on Windows.

## 🧪 Testing Windows Batch Files

### Syntax Validation

The batch files use standard Windows batch syntax:
- `@echo off` - Suppress command echoing
- `%errorlevel%` - Exit code checking
- `call` - Execute other batch files
- `if exist` - File/directory existence checks
- `pause` - Wait for user input

### Key Windows-Specific Elements

**setup.bat:**
- Uses `venv\Scripts\activate` (Windows path separators)
- Creates `.env` with Windows line endings
- Uses `rmdir /s /q` for recursive directory removal

**build.bat:**
- Uses `venv\Scripts\activate` for virtual environment
- Checks for `TVTools.exe` output file
- Uses Windows path separators throughout

### Cross-Platform Compatibility in Python Scripts

**build_executable.py already handles:**
```python
# Detects Windows and uses .exe extension
exe_name = "TVTools.exe" if sys.platform == "win32" else "TVTools"

# Uses os.path for cross-platform paths
exe_path = f"dist/{exe_name}"
```

## 🔍 Manual Testing Steps (When on Windows)

1. **Test setup.bat:**
   ```cmd
   setup.bat
   # Should create venv, install dependencies, create .env
   ```

2. **Test build.bat:**
   ```cmd
   build.bat
   # Should build TVTools.exe in TVTools_Distribution/
   ```

3. **Test executable:**
   ```cmd
   TVTools_Distribution\TVTools.exe
   # Should run and generate watchlist files
   ```

## 🐛 Common Windows Issues & Solutions

### Python PATH Issues
**Problem:** `python` command not found
**Solution:** Reinstall Python with "Add to PATH" checked

### Virtual Environment Issues
**Problem:** `venv\Scripts\activate` fails
**Solution:** 
```cmd
# Try PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use full path
C:\path\to\project\venv\Scripts\activate.bat
```

### PyInstaller Issues
**Problem:** Build fails with import errors
**Solution:**
```cmd
# Install Visual C++ Redistributable
# Or try:
pip install --upgrade pyinstaller
pip install --upgrade setuptools
```

### Antivirus False Positives
**Problem:** Executable flagged as malware
**Solution:**
- Add exception for TVTools_Distribution folder
- Use `--debug` flag in PyInstaller for more verbose executable

## 📋 Windows Build Checklist

- [ ] Python 3.8+ installed with PATH
- [ ] Git for Windows installed
- [ ] setup.bat runs without errors
- [ ] Virtual environment created in `venv/`
- [ ] Dependencies installed successfully
- [ ] build.bat runs without errors
- [ ] TVTools.exe created in TVTools_Distribution/
- [ ] Executable runs and generates files
- [ ] Files can be imported to TradingView

## 🔄 Automated Testing (Future)

Consider GitHub Actions for automated Windows testing:

```yaml
name: Windows Build Test
on: [push, pull_request]
jobs:
  windows-build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - run: setup.bat
    - run: build.bat
    - run: TVTools_Distribution\TVTools.exe --help
```

This would ensure Windows compatibility on every commit.
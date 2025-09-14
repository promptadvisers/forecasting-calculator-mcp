# 🪟 Windows Setup Guide for Forecasting Calculator MCP

## Complete Windows Installation Instructions

This guide provides step-by-step instructions for setting up the Forecasting Calculator MCP server on Windows machines.

## Prerequisites

- Windows 10/11
- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- Claude Desktop for Windows ([Download Claude](https://claude.ai/download))
- Git for Windows (optional, for cloning)

## Step 1: Install Python (if needed)

1. Download Python from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation:
```cmd
python --version
```

## Step 2: Download the Server

### Option A: Using Git
```powershell
git clone https://github.com/marwankashef/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp
```

### Option B: Download ZIP
1. Download repository as ZIP from GitHub
2. Extract to desired location (e.g., `C:\Users\YourName\Documents\`)

## Step 3: Set Up Virtual Environment

### Using Command Prompt:
```cmd
cd C:\path\to\forecasting-calculator-mcp
python -m venv mcp_venv
mcp_venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Using PowerShell:
```powershell
cd C:\path\to\forecasting-calculator-mcp
python -m venv mcp_venv
.\mcp_venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Note**: If you get an execution policy error in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 4: Create Windows Wrapper Script

Create a file named `run_forecasting_calculator.bat`:

```batch
@echo off
cd /d "C:\path\to\forecasting-calculator-mcp"
call mcp_venv\Scripts\activate.bat
python forecasting_calculator_server.py
```

**Replace** `C:\path\to\forecasting-calculator-mcp` with your actual path.

## Step 5: Test the Server

```cmd
cd C:\path\to\forecasting-calculator-mcp
mcp_venv\Scripts\activate.bat
echo {"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1} | python forecasting_calculator_server.py
```

You should see a JSON response with server information.

## Step 6: Configure Claude Desktop

1. **Find config location**:
   - Windows 10: `%APPDATA%\Claude\claude_desktop_config.json`
   - Windows 11: `%APPDATA%\Claude\claude_desktop_config.json`
   
   Full path typically: `C:\Users\YourName\AppData\Roaming\Claude\claude_desktop_config.json`

2. **Edit the config file** (create if doesn't exist):

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "C:\\path\\to\\forecasting-calculator-mcp\\run_forecasting_calculator.bat",
      "args": [],
      "env": {}
    }
  }
}
```

**Important**: Use double backslashes `\\` in the path!

3. **Save the file**

## Step 7: Restart Claude Desktop

1. Close Claude Desktop completely (check system tray)
2. Start Claude Desktop again
3. The forecasting calculator should now be available

## Windows-Specific Troubleshooting

### Issue: "python is not recognized"

**Solution 1**: Use full path to Python
```batch
"C:\Users\YourName\AppData\Local\Programs\Python\Python39\python.exe" -m venv mcp_venv
```

**Solution 2**: Add Python to PATH
1. Search "Environment Variables" in Windows
2. Edit System Environment Variables
3. Add Python installation directory to PATH

### Issue: "cannot be loaded because running scripts is disabled"

**Solution**: Enable script execution in PowerShell
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned
```

### Issue: "Access is denied"

**Solutions**:
- Run Command Prompt as Administrator
- Check folder permissions
- Ensure antivirus isn't blocking

### Issue: Server not showing in Claude

**Checklist**:
1. Verify config file path is correct
2. Use double backslashes in JSON paths
3. Ensure .bat file has correct paths
4. Check Windows Event Viewer for errors
5. Try running .bat file directly to see errors

### Issue: Path with spaces

**Solution**: Use quotes in batch file
```batch
cd /d "C:\Program Files\My Folder\forecasting-calculator-mcp"
```

## Alternative: Using WSL (Windows Subsystem for Linux)

If you prefer a Linux-like environment:

1. **Install WSL**:
```powershell
wsl --install
```

2. **Follow macOS/Linux instructions** within WSL

3. **Configure Claude** to use WSL path:
```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "wsl",
      "args": ["/home/username/forecasting-calculator-mcp/run_forecasting_calculator.sh"],
      "env": {}
    }
  }
}
```

## Quick Setup Script for Windows

Save as `quick_setup.bat`:

```batch
@echo off
echo Setting up Forecasting Calculator MCP Server...

REM Create virtual environment
python -m venv mcp_venv
call mcp_venv\Scripts\activate.bat

REM Install dependencies
pip install mcp numpy scipy

REM Create wrapper script
echo @echo off > run_forecasting_calculator.bat
echo cd /d "%CD%" >> run_forecasting_calculator.bat
echo call mcp_venv\Scripts\activate.bat >> run_forecasting_calculator.bat
echo python forecasting_calculator_server.py >> run_forecasting_calculator.bat

REM Test the server
echo Testing server...
echo {"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1} | python forecasting_calculator_server.py

echo.
echo Setup complete! 
echo Add this to your Claude Desktop config:
echo {
echo   "mcpServers": {
echo     "forecasting-calculator": {
echo       "command": "%CD%\run_forecasting_calculator.bat",
echo       "args": [],
echo       "env": {}
echo     }
echo   }
echo }
pause
```

## Verifying Installation

After setup, you can verify the installation:

1. **Check if server runs**:
```cmd
run_forecasting_calculator.bat
```
(Press Ctrl+C to stop)

2. **Check Claude Desktop logs**:
```
%APPDATA%\Claude\logs\
```

3. **Test in Claude**:
Type: "Use the forecasting calculator to forecast [100, 200, 300] for 3 periods using linear method"

## Performance Tips for Windows

1. **Use SSD**: Place the server on an SSD for faster startup
2. **Exclude from antivirus**: Add folder to Windows Defender exclusions
3. **Use Python 3.11+**: Better performance on Windows
4. **Close unnecessary apps**: Free up resources for calculations

## Security Considerations

1. **Don't run as Administrator** unless necessary
2. **Keep Python updated** for security patches
3. **Use virtual environment** to isolate dependencies
4. **Review code** before running from unknown sources

## Need Help?

- Check the [main documentation](README.md)
- Review [implementation guide](COMPLETE_IMPLEMENTATION_GUIDE.md)
- Open an issue on GitHub
- Check Claude Desktop logs for errors

---

**Tested on**: Windows 10 (22H2), Windows 11 (23H2)
**Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
**Claude Desktop**: Latest version as of 2024
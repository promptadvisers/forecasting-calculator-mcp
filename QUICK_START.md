# ⚡ Quick Start Guide

Get the Forecasting Calculator MCP running in 5 minutes!

## 🚀 macOS/Linux Quick Install

```bash
# Clone the repository
git clone https://github.com/promptadvisers/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp

# Set up virtual environment
python3 -m venv mcp_venv
source mcp_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x forecasting_calculator_server.py run_forecasting_calculator.sh

# Test the server
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}' | python forecasting_calculator_server.py
```

## 🪟 Windows Quick Install

```powershell
# Clone the repository
git clone https://github.com/promptadvisers/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp

# Set up virtual environment
python -m venv mcp_venv
.\mcp_venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create batch wrapper (copy and save as run_forecasting_calculator.bat)
@echo off
cd /d "C:\path\to\forecasting-calculator-mcp"
call mcp_venv\Scripts\activate.bat
python forecasting_calculator_server.py
```

## 🔧 Configure Claude Desktop

### macOS
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "/absolute/path/to/run_forecasting_calculator.sh",
      "args": [],
      "env": {}
    }
  }
}
```

### Windows
Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "C:\\path\\to\\run_forecasting_calculator.bat",
      "args": [],
      "env": {}
    }
  }
}
```

## 🔄 Restart Claude Desktop

**macOS:**
```bash
osascript -e 'quit app "Claude"' && sleep 2 && open -a "Claude"
```

**Windows:**
Close Claude from system tray and restart

## ✅ Test It!

In Claude, type:
```
Use the forecasting calculator to forecast [100, 200, 300] for 3 periods using linear method
```

## 🎯 Available Commands

- **Forecast data**: `forecast [300, 400, 500] for 3 periods using linear`
- **Explain methods**: `explain the forecasting methods`

## 📊 Forecasting Methods

- `linear` - Straight line trend
- `moving_average` - Smoothed average
- `exponential_smoothing` - Recent-weighted
- `polynomial` - Curved trends
- `simple_arima` - Time-dependent

## 🆘 Need Help?

1. Check server is running: `ps aux | grep forecasting`
2. View logs: `~/Library/Logs/Claude/mcp.log`
3. Test directly: Run wrapper script manually
4. [Open an issue](https://github.com/promptadvisers/forecasting-calculator-mcp/issues)

---

**Built in under 10 minutes** using MCP best practices!
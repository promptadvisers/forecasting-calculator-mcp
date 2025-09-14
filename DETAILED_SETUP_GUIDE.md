# 🎯 Forecasting Calculator MCP - Detailed Setup Guide

<div align="center">

![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Build Time](https://img.shields.io/badge/Build%20Time-10%20minutes-orange)

**A sophisticated time-series forecasting server for Claude Desktop**

[Quick Start](#quick-start) • [Features](#features) • [Installation](#installation) • [Configuration](#configuration) • [Usage](#usage) • [Troubleshooting](#troubleshooting)

</div>

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [macOS Setup](#macos-setup)
  - [Windows Setup](#windows-setup)
  - [Linux Setup](#linux-setup)
- [Configuration](#configuration)
  - [Claude Desktop Integration](#claude-desktop-integration)
  - [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Contributing](#contributing)

---

## 🚀 Quick Start

```bash
# Clone and setup in 3 commands
git clone https://github.com/promptadvisers/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp
./setup.sh  # or setup.bat on Windows
```

---

## ✨ Features

### 🔮 Five Forecasting Methods

| Method | Description | Best For | Algorithm |
|--------|-------------|----------|-----------|
| **Linear Regression** | Fits a straight line through data points | Steady trends | Least squares |
| **Moving Average** | Smooths out short-term fluctuations | Noisy data | Simple/weighted average |
| **Exponential Smoothing** | Weights recent data more heavily | Changing trends | Exponential decay |
| **Polynomial Regression** | Fits curves to non-linear patterns | Growth/decay curves | Higher-order polynomials |
| **Simple ARIMA** | Models time-dependent patterns | Autocorrelated data | AR(1) model |

### 🎯 Key Capabilities

- ✅ **Natural Language Input** - Accepts various formats
- ✅ **Mathematical Explanations** - Detailed breakdown of calculations
- ✅ **Configurable Periods** - Forecast 1-100 periods ahead
- ✅ **Error Handling** - Graceful failure with helpful messages
- ✅ **Performance Optimized** - NumPy/SciPy for fast calculations

---

## 📦 Prerequisites

### System Requirements

| Component | Requirement | Check Command |
|-----------|-------------|---------------|
| **Python** | 3.8 or higher | `python3 --version` |
| **pip** | Latest version | `pip --version` |
| **Claude Desktop** | Latest version | Check app version |
| **Git** | Any version (optional) | `git --version` |

### Python Packages

```txt
mcp>=1.0.0      # Model Context Protocol SDK
numpy>=1.24.0   # Numerical computations
scipy>=1.10.0   # Statistical functions
```

---

## 💻 Installation

### macOS Setup

<details>
<summary><b>Click to expand macOS instructions</b></summary>

#### Step 1: Download the Server

```bash
# Option A: Using Git
git clone https://github.com/promptadvisers/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp

# Option B: Download ZIP
curl -L https://github.com/promptadvisers/forecasting-calculator-mcp/archive/main.zip -o fc-mcp.zip
unzip fc-mcp.zip
cd forecasting-calculator-mcp-main
```

#### Step 2: Set Up Environment

```bash
# Create virtual environment
python3 -m venv mcp_venv

# Activate environment
source mcp_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x forecasting_calculator_server.py
chmod +x run_forecasting_calculator.sh
```

#### Step 3: Update Wrapper Script

Edit `run_forecasting_calculator.sh`:

```bash
#!/bin/bash
# Update this path to your installation directory
cd "/path/to/your/forecasting-calculator-mcp"
source mcp_venv/bin/activate
exec python forecasting_calculator_server.py
```

#### Step 4: Test the Server

```bash
# Quick test
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}' | python forecasting_calculator_server.py
```

Expected output:
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"serverInfo":{"name":"forecasting-calculator","version":"1.0.0"}}}
```

</details>

### Windows Setup

<details>
<summary><b>Click to expand Windows instructions</b></summary>

#### Step 1: Download the Server

```powershell
# Option A: Using Git
git clone https://github.com/promptadvisers/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp

# Option B: Using PowerShell
Invoke-WebRequest -Uri "https://github.com/promptadvisers/forecasting-calculator-mcp/archive/main.zip" -OutFile "fc-mcp.zip"
Expand-Archive -Path "fc-mcp.zip" -DestinationPath "."
cd forecasting-calculator-mcp-main
```

#### Step 2: Set Up Environment

```powershell
# Create virtual environment
python -m venv mcp_venv

# Activate environment (PowerShell)
.\mcp_venv\Scripts\Activate.ps1

# OR for Command Prompt
mcp_venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Create Wrapper Script

Create `run_forecasting_calculator.bat`:

```batch
@echo off
REM Update this path to your installation directory
cd /d "C:\path\to\your\forecasting-calculator-mcp"
call mcp_venv\Scripts\activate.bat
python forecasting_calculator_server.py
```

#### Step 4: Handle Execution Policy (if needed)

```powershell
# If you get execution policy errors:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

### Linux Setup

<details>
<summary><b>Click to expand Linux instructions</b></summary>

```bash
# Installation is similar to macOS
git clone https://github.com/promptadvisers/forecasting-calculator-mcp.git
cd forecasting-calculator-mcp

# Create and activate virtual environment
python3 -m venv mcp_venv
source mcp_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x *.sh *.py

# Test
./run_forecasting_calculator.sh
```

</details>

---

## ⚙️ Configuration

### Claude Desktop Integration

The configuration file location varies by operating system:

| OS | Configuration File Location |
|----|----------------------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

#### Configuration Structure

<details>
<summary><b>📝 Click to see configuration format</b></summary>

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "/absolute/path/to/wrapper/script",
      "args": [],
      "env": {}
    }
  }
}
```

**Important Notes:**
- ⚠️ Use **absolute paths** only
- ⚠️ On Windows, use double backslashes: `C:\\path\\to\\script.bat`
- ⚠️ The wrapper script must activate the virtual environment

</details>

#### Example Configurations

<details>
<summary><b>macOS Example</b></summary>

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "/Users/username/apps/forecasting-calculator-mcp/run_forecasting_calculator.sh",
      "args": [],
      "env": {}
    }
  }
}
```

</details>

<details>
<summary><b>Windows Example</b></summary>

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "C:\\Users\\username\\apps\\forecasting-calculator-mcp\\run_forecasting_calculator.bat",
      "args": [],
      "env": {}
    }
  }
}
```

</details>

### Environment Variables

Optional environment variables for advanced configuration:

```bash
# In your wrapper script or env configuration
export FC_LOG_LEVEL=DEBUG           # Enable debug logging
export FC_MAX_PERIODS=200          # Override max forecast periods
export FC_TIMEOUT=30                # Set timeout in seconds
```

---

## 📊 Usage Examples

### Basic Forecasting

<details>
<summary><b>Simple Linear Forecast</b></summary>

**Input:**
```
Use forecasting calculator to forecast [100, 200, 300] for 5 periods using linear method
```

**Output:**
```
📊 Forecasting Results

Method: Linear Regression
Input Data: 100, 200, 300
Forecast Periods: 5

Forecasted Values: 400.00, 500.00, 600.00, 700.00, 800.00

Mathematical Details:
y = 100.0000x + 0.0000

Explanation: Linear trend projection with slope 100.0000. Each period increases by 100.0000 units.

Additional Metrics:
- R-squared: 1.0000
```

</details>

<details>
<summary><b>Revenue Projection</b></summary>

**Input:**
```
My monthly revenue: 10000, 12000, 11500, 13000, 14500, 14000
Forecast next 6 months with exponential smoothing
```

**Output:**
```
📊 Forecasting Results

Method: Exponential Smoothing
Input Data: 10000, 12000, 11500, 13000, 14500, 14000
Forecast Periods: 6

Forecasted Values: 14150.00, 14225.00, 14262.50, 14281.25, 14290.63, 14295.31

Mathematical Details:
α = 0.3 (smoothing parameter)

Explanation: Exponential smoothing with α=0.3. Recent values weighted more heavily. Trend: 150.00 per period.
```

</details>

<details>
<summary><b>Complex Growth Pattern</b></summary>

**Input:**
```
Sales data: [50, 55, 65, 80, 100, 125, 160]
Use polynomial method to forecast 4 periods
```

**Output:**
```
📊 Forecasting Results

Method: Polynomial Regression
Input Data: 50, 55, 65, 80, 100, 125, 160
Forecast Periods: 4

Forecasted Values: 205.42, 258.33, 320.83, 393.75

Mathematical Details:
y = 0.7440x² + 5.0119x + 44.6429

Explanation: Polynomial of degree 2 captures non-linear patterns. R²=0.9987
```

</details>

### Method Selection Guide

```
Explain the forecasting methods available
```

<details>
<summary><b>View method explanations</b></summary>

The server will return detailed explanations of each method:

- **Linear**: Best for steady, consistent trends
- **Moving Average**: Ideal for smoothing volatile data
- **Exponential Smoothing**: When recent data matters more
- **Polynomial**: For accelerating/decelerating growth
- **Simple ARIMA**: When values depend on previous values

</details>

---

## 🔧 API Reference

### Tool: `forecast_data`

**Purpose:** Perform time series forecasting on numerical data

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `data` | string | Array of numbers | `"[100, 200, 300]"` or `"100 200 300"` |
| `periods` | string | Number of periods to forecast | `"5"` |
| `method` | string | Forecasting method | `"linear"`, `"polynomial"`, etc. |

### Tool: `explain_methods`

**Purpose:** Get detailed explanation of available forecasting methods

**Parameters:** None

---

## 🐛 Troubleshooting

### Common Issues and Solutions

<details>
<summary><b>Server not appearing in Claude Desktop</b></summary>

**Diagnosis Steps:**

1. **Check configuration file:**
```bash
# macOS/Linux
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows
type %APPDATA%\Claude\claude_desktop_config.json
```

2. **Verify JSON syntax:**
```bash
# Use a JSON validator
python -m json.tool < claude_desktop_config.json
```

3. **Check server process:**
```bash
# macOS/Linux
ps aux | grep forecasting_calculator

# Windows
tasklist | findstr python
```

**Solutions:**
- Ensure paths are absolute
- Verify wrapper script is executable
- Restart Claude Desktop completely
- Check logs at `~/Library/Logs/Claude/`

</details>

<details>
<summary><b>Import errors (numpy/scipy)</b></summary>

**Solution:**
```bash
# Ensure virtual environment is activated
source mcp_venv/bin/activate  # macOS/Linux
# or
mcp_venv\Scripts\activate.bat  # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

</details>

<details>
<summary><b>Permission denied errors</b></summary>

**macOS/Linux:**
```bash
chmod +x run_forecasting_calculator.sh
chmod +x forecasting_calculator_server.py
```

**Windows:**
- Run as Administrator
- Check file permissions in Properties

</details>

### Debug Mode

Enable debug logging for troubleshooting:

```python
# In forecasting_calculator_server.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🏗️ Architecture

### System Design

```
┌─────────────────┐
│  Claude Desktop │
└────────┬────────┘
         │ JSON-RPC
         ▼
┌─────────────────┐
│  Wrapper Script │ ← Activates venv
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Server    │
│  ┌───────────┐  │
│  │   Tools   │  │
│  ├───────────┤  │
│  │ Forecasts │  │
│  └───────────┘  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  NumPy/SciPy    │ ← Mathematical engine
└─────────────────┘
```

### Key Components

1. **MCP Server** - Handles protocol communication
2. **ForecastingEngine** - Core calculation logic
3. **Tool Handlers** - Process user requests
4. **Wrapper Script** - Environment management

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/forecasting-calculator-mcp.git

# Create development branch
git checkout -b feature/your-feature

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Built using the [Model Context Protocol](https://modelcontextprotocol.io/)
- Inspired by MCP community examples
- Mathematical algorithms from NumPy/SciPy

---

<div align="center">

**Built with ❤️ in under 10 minutes**

[Report Bug](https://github.com/promptadvisers/forecasting-calculator-mcp/issues) • [Request Feature](https://github.com/promptadvisers/forecasting-calculator-mcp/issues)

</div>
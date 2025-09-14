# Forecasting Calculator MCP Server

A sophisticated Model Context Protocol (MCP) server that provides multiple statistical forecasting methods for time series data.

## Features

- **Multiple Forecasting Methods**:
  - Linear Regression - For steady trends
  - Moving Average - For smoothing fluctuations
  - Exponential Smoothing - For recent-weighted predictions
  - Polynomial Regression - For non-linear patterns
  - Simple ARIMA - For autocorrelated data

- **Interactive Usage**: Ask for forecasts with natural language
- **Mathematical Explanations**: Get detailed breakdowns of calculations
- **Flexible Input**: Accepts arrays or space/comma-separated numbers
- **Configurable Periods**: Forecast 1-100 periods into the future

## Installation

1. Create and activate virtual environment:
```bash
cd forecasting-calculator-mcp
python3 -m venv mcp_venv
source mcp_venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make scripts executable:
```bash
chmod +x forecasting_calculator_server.py
chmod +x run_forecasting_calculator.sh
```

## Testing

Test the server directly:
```bash
# Test initialization
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}' | python forecasting_calculator_server.py

# Test tool listing
echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2}' | python forecasting_calculator_server.py
```

## Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "forecasting-calculator": {
      "command": "/Users/marwankashef/Desktop/Early AI-dopters/Claude Code Demo 16/forecasting-calculator-mcp/run_forecasting_calculator.sh",
      "args": [],
      "env": {}
    }
  }
}
```

## Usage Examples

### In Claude Desktop:

1. **Simple Linear Forecast**:
   - "Forecast [300, 400, 500] for 3 periods using linear regression"

2. **Revenue Projection**:
   - "My revenue was 1000, 1200, 1400, 1650. Forecast next 6 months with exponential smoothing"

3. **Understand Methods**:
   - "Explain the forecasting methods available"

## Methods Overview

| Method | Best For | Use Case |
|--------|----------|----------|
| Linear | Steady trends | Consistent growth/decline |
| Moving Average | Noisy data | Smoothing volatility |
| Exponential Smoothing | Recent trends | Fast-changing conditions |
| Polynomial | Curves | Acceleration/deceleration |
| Simple ARIMA | Time dependencies | Autocorrelated series |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named 'mcp'` | Activate virtual environment |
| `spawn python ENOENT` | Use python3 in wrapper script |
| Server not showing in Claude | Restart Claude Desktop |
| Import errors | Install all requirements with pip |

## Technical Details

- Uses standard MCP SDK (not FastMCP)
- Includes ServerCapabilities in initialization
- Safe mathematical operations with NumPy
- Comprehensive error handling
- Virtual environment isolation

## License

MIT
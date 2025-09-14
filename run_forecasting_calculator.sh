#!/bin/bash

# Activate the virtual environment and run the server
# UPDATE THIS PATH to your installation directory
cd "/path/to/your/forecasting-calculator-mcp"
source mcp_venv/bin/activate
exec python forecasting_calculator_server.py
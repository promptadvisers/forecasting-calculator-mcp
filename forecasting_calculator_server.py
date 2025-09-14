#!/usr/bin/env python3
"""
Forecasting Calculator MCP Server
A sophisticated forecasting server that provides multiple methods for time series prediction
"""

import asyncio
import sys
import json
import numpy as np
from typing import List, Dict, Any, Tuple
from enum import Enum

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ServerCapabilities
import mcp.server.stdio

# Initialize the MCP server
server = Server("forecasting-calculator")

class ForecastMethod(Enum):
    LINEAR = "linear"
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    POLYNOMIAL = "polynomial"
    SIMPLE_ARIMA = "simple_arima"

class ForecastingEngine:
    """Core forecasting logic"""
    
    @staticmethod
    def validate_data(data: List[float]) -> Tuple[bool, str]:
        """Validate input data"""
        if not data or len(data) < 3:
            return False, "Need at least 3 data points for forecasting"
        if len(data) > 10000:
            return False, "Data series too large (max 10000 points)"
        if not all(isinstance(x, (int, float)) for x in data):
            return False, "All data points must be numeric"
        return True, "Valid"
    
    @staticmethod
    def linear_regression(data: List[float], periods: int) -> Dict[str, Any]:
        """Simple linear regression forecasting"""
        n = len(data)
        x = np.arange(n)
        y = np.array(data)
        
        # Calculate linear regression coefficients
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        
        # Generate forecasts
        future_x = np.arange(n, n + periods)
        forecasts = slope * future_x + intercept
        
        # Calculate R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            "method": "Linear Regression",
            "forecasts": forecasts.tolist(),
            "equation": f"y = {slope:.4f}x + {intercept:.4f}",
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "explanation": f"Linear trend projection with slope {slope:.4f}. Each period increases by {slope:.4f} units."
        }
    
    @staticmethod
    def moving_average(data: List[float], periods: int, window: int = None) -> Dict[str, Any]:
        """Moving average forecasting"""
        if window is None:
            window = min(len(data) // 3, 12)  # Default window size
        window = min(window, len(data))
        
        # Calculate the moving average
        recent_avg = np.mean(data[-window:])
        
        # For simplicity, use the recent average as forecast
        # In practice, could use trend from moving averages
        forecasts = [recent_avg] * periods
        
        # Calculate historical moving averages for context
        if len(data) >= window:
            historical_ma = []
            for i in range(len(data) - window + 1):
                historical_ma.append(np.mean(data[i:i+window]))
        else:
            historical_ma = [np.mean(data)]
        
        return {
            "method": "Moving Average",
            "forecasts": forecasts,
            "window_size": window,
            "recent_average": recent_avg,
            "historical_moving_averages": historical_ma[-5:],  # Last 5 MAs
            "explanation": f"Using {window}-period moving average. Forecast is based on average of last {window} values: {recent_avg:.2f}"
        }
    
    @staticmethod
    def exponential_smoothing(data: List[float], periods: int, alpha: float = 0.3) -> Dict[str, Any]:
        """Simple exponential smoothing"""
        n = len(data)
        
        # Initialize
        smoothed = [data[0]]
        
        # Apply exponential smoothing
        for i in range(1, n):
            smoothed_val = alpha * data[i] + (1 - alpha) * smoothed[-1]
            smoothed.append(smoothed_val)
        
        # Forecast using last smoothed value
        last_smoothed = smoothed[-1]
        
        # Calculate trend from smoothed values
        if len(smoothed) >= 2:
            recent_trend = smoothed[-1] - smoothed[-2]
        else:
            recent_trend = 0
        
        # Generate forecasts with slight trend
        forecasts = []
        current = last_smoothed
        for i in range(periods):
            current = current + recent_trend * 0.5  # Damped trend
            forecasts.append(current)
        
        return {
            "method": "Exponential Smoothing",
            "forecasts": forecasts,
            "alpha": alpha,
            "last_smoothed_value": last_smoothed,
            "trend": recent_trend,
            "explanation": f"Exponential smoothing with α={alpha}. Recent values weighted more heavily. Trend: {recent_trend:.4f} per period."
        }
    
    @staticmethod
    def polynomial_regression(data: List[float], periods: int, degree: int = 2) -> Dict[str, Any]:
        """Polynomial regression forecasting"""
        n = len(data)
        x = np.arange(n)
        y = np.array(data)
        
        # Limit degree based on data points
        degree = min(degree, n - 1, 4)  # Cap at 4 for stability
        
        # Fit polynomial
        coefficients = np.polyfit(x, y, degree)
        poly = np.poly1d(coefficients)
        
        # Generate forecasts
        future_x = np.arange(n, n + periods)
        forecasts = poly(future_x).tolist()
        
        # Calculate R-squared
        y_pred = poly(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Create equation string
        equation_parts = []
        for i, coef in enumerate(coefficients):
            power = degree - i
            if power == 0:
                equation_parts.append(f"{coef:.4f}")
            elif power == 1:
                equation_parts.append(f"{coef:.4f}x")
            else:
                equation_parts.append(f"{coef:.4f}x^{power}")
        equation = " + ".join(equation_parts)
        
        return {
            "method": "Polynomial Regression",
            "forecasts": forecasts,
            "degree": degree,
            "coefficients": coefficients.tolist(),
            "equation": equation,
            "r_squared": r_squared,
            "explanation": f"Polynomial of degree {degree} captures non-linear patterns. R²={r_squared:.4f}"
        }
    
    @staticmethod
    def simple_arima(data: List[float], periods: int) -> Dict[str, Any]:
        """Simplified ARIMA-like forecasting (AR(1) model)"""
        n = len(data)
        y = np.array(data)
        
        # Calculate differences (for stationarity insight)
        if n > 1:
            differences = np.diff(y)
            mean_diff = np.mean(differences)
            std_diff = np.std(differences)
        else:
            mean_diff = 0
            std_diff = 0
        
        # Simple AR(1) model: y_t = c + φ*y_{t-1} + ε
        # Estimate parameters
        if n > 2:
            y_lag = y[:-1]
            y_current = y[1:]
            
            # Calculate AR coefficient
            cov = np.cov(y_lag, y_current)[0, 1]
            var = np.var(y_lag)
            phi = cov / var if var != 0 else 0.5
            
            # Calculate constant
            c = np.mean(y_current) * (1 - phi)
        else:
            phi = 0.5
            c = y[-1] * 0.5
        
        # Generate forecasts
        forecasts = []
        last_value = y[-1]
        
        for i in range(periods):
            next_value = c + phi * last_value
            # Add some mean reversion if phi is large
            if abs(phi) > 0.9:
                next_value = 0.9 * next_value + 0.1 * np.mean(y)
            forecasts.append(next_value)
            last_value = next_value
        
        return {
            "method": "Simple ARIMA (AR(1))",
            "forecasts": forecasts,
            "ar_coefficient": phi,
            "constant": c,
            "mean_difference": mean_diff,
            "std_difference": std_diff,
            "equation": f"y_t = {c:.4f} + {phi:.4f} * y_{{t-1}}",
            "explanation": f"Autoregressive model with coefficient φ={phi:.4f}. {'Mean-reverting' if phi < 1 else 'Trending'} behavior."
        }

def parse_forecast_request(data_str: str, periods_str: str, method_str: str) -> Tuple[List[float], int, ForecastMethod]:
    """Parse and validate forecast request parameters"""
    
    # Parse data
    try:
        # Handle various input formats
        data_str = data_str.strip()
        if data_str.startswith('[') and data_str.endswith(']'):
            data = json.loads(data_str)
        else:
            # Try comma or space separated
            data_str = data_str.replace(',', ' ')
            data = [float(x) for x in data_str.split() if x]
    except Exception as e:
        raise ValueError(f"Could not parse data: {str(e)}")
    
    # Parse periods
    try:
        periods = int(periods_str)
        if periods < 1:
            raise ValueError("Periods must be at least 1")
        if periods > 100:
            raise ValueError("Maximum 100 periods for forecasting")
    except ValueError as e:
        raise ValueError(f"Invalid periods: {str(e)}")
    
    # Parse method
    method_map = {
        "linear": ForecastMethod.LINEAR,
        "moving average": ForecastMethod.MOVING_AVERAGE,
        "moving_average": ForecastMethod.MOVING_AVERAGE,
        "exponential": ForecastMethod.EXPONENTIAL_SMOOTHING,
        "exponential smoothing": ForecastMethod.EXPONENTIAL_SMOOTHING,
        "exponential_smoothing": ForecastMethod.EXPONENTIAL_SMOOTHING,
        "polynomial": ForecastMethod.POLYNOMIAL,
        "poly": ForecastMethod.POLYNOMIAL,
        "arima": ForecastMethod.SIMPLE_ARIMA,
        "simple arima": ForecastMethod.SIMPLE_ARIMA,
        "simple_arima": ForecastMethod.SIMPLE_ARIMA,
        "ar": ForecastMethod.SIMPLE_ARIMA
    }
    
    method_lower = method_str.lower().strip()
    if method_lower not in method_map:
        available = ", ".join(method_map.keys())
        raise ValueError(f"Unknown method '{method_str}'. Available: {available}")
    
    return data, periods, method_map[method_lower]

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="forecast_data",
            description="""Perform time series forecasting on numerical data.
            
This tool analyzes a sequence of numbers and projects future values using various statistical methods.
Perfect for revenue projections, trend analysis, and time series prediction.

Required inputs:
- data: Array of at least 3 numbers (e.g., "[300, 400, 500]" or "300 400 500")
- periods: Number of future periods to forecast (1-100)
- method: Forecasting method to use

Available methods:
- "linear": Linear regression trend line
- "moving_average": Moving average smoothing
- "exponential_smoothing": Exponentially weighted average
- "polynomial": Polynomial regression for non-linear trends
- "simple_arima": Autoregressive model

Examples:
- Revenue: "[1000, 1200, 1400]", 3 periods, "linear"
- Sales: "50 55 60 58 65", 6 periods, "exponential_smoothing"
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Array of numbers as string (e.g., '[100, 200, 300]' or '100 200 300')"
                    },
                    "periods": {
                        "type": "string",
                        "description": "Number of periods to forecast (e.g., '5')"
                    },
                    "method": {
                        "type": "string",
                        "description": "Forecasting method: linear, moving_average, exponential_smoothing, polynomial, simple_arima"
                    }
                },
                "required": ["data", "periods", "method"]
            }
        ),
        Tool(
            name="explain_methods",
            description="Explains the available forecasting methods and when to use each one",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "forecast_data":
        try:
            # Extract arguments
            data_str = arguments.get("data", "")
            periods_str = arguments.get("periods", "")
            method_str = arguments.get("method", "")
            
            # Parse and validate
            data, periods, method = parse_forecast_request(data_str, periods_str, method_str)
            
            # Validate data
            engine = ForecastingEngine()
            valid, message = engine.validate_data(data)
            if not valid:
                return [TextContent(
                    type="text",
                    text=f"Data validation error: {message}"
                )]
            
            # Perform forecasting based on method
            if method == ForecastMethod.LINEAR:
                result = engine.linear_regression(data, periods)
            elif method == ForecastMethod.MOVING_AVERAGE:
                result = engine.moving_average(data, periods)
            elif method == ForecastMethod.EXPONENTIAL_SMOOTHING:
                result = engine.exponential_smoothing(data, periods)
            elif method == ForecastMethod.POLYNOMIAL:
                result = engine.polynomial_regression(data, periods)
            elif method == ForecastMethod.SIMPLE_ARIMA:
                result = engine.simple_arima(data, periods)
            else:
                return [TextContent(
                    type="text",
                    text=f"Method {method} not yet implemented"
                )]
            
            # Format response
            forecasts = result["forecasts"]
            forecast_str = ", ".join([f"{v:.2f}" for v in forecasts])
            
            response = f"""📊 **Forecasting Results**

**Method:** {result['method']}
**Input Data:** {', '.join([str(x) for x in data])}
**Forecast Periods:** {periods}

**Forecasted Values:** {forecast_str}

**Mathematical Details:**
{result.get('equation', '')}

**Explanation:** {result['explanation']}

**Additional Metrics:**"""
            
            # Add method-specific metrics
            if 'r_squared' in result:
                response += f"\n- R-squared: {result['r_squared']:.4f}"
            if 'window_size' in result:
                response += f"\n- Window Size: {result['window_size']}"
            if 'alpha' in result:
                response += f"\n- Smoothing Parameter (α): {result['alpha']}"
            if 'ar_coefficient' in result:
                response += f"\n- AR Coefficient: {result['ar_coefficient']:.4f}"
            
            return [TextContent(type="text", text=response)]
            
        except ValueError as e:
            return [TextContent(
                type="text",
                text=f"Input error: {str(e)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Forecasting error: {str(e)}"
            )]
    
    elif name == "explain_methods":
        explanation = """📈 **Forecasting Methods Guide**

**1. Linear Regression** (`linear`)
- Best for: Steady, consistent trends
- How it works: Fits a straight line through your data
- Use when: Data shows clear upward or downward trend
- Example: Steady revenue growth

**2. Moving Average** (`moving_average`)
- Best for: Smoothing out fluctuations
- How it works: Averages recent values to predict future
- Use when: Data is noisy but stable around a mean
- Example: Seasonal sales with random variations

**3. Exponential Smoothing** (`exponential_smoothing`)
- Best for: Recent trends matter more
- How it works: Weights recent data more heavily
- Use when: Recent changes are more predictive
- Example: Rapidly changing market conditions

**4. Polynomial Regression** (`polynomial`)
- Best for: Non-linear patterns
- How it works: Fits a curve through your data
- Use when: Growth is accelerating or decelerating
- Example: Product adoption curves, market saturation

**5. Simple ARIMA** (`simple_arima`)
- Best for: Data with autocorrelation
- How it works: Uses past values to predict future
- Use when: Values depend on previous values
- Example: Stock prices, economic indicators

**Tips for Choosing:**
- Start with `linear` for simple trends
- Use `exponential_smoothing` for recent-weighted forecasts
- Try `polynomial` if you see curves in your data
- Use `moving_average` to smooth volatility
- Choose `simple_arima` for time-dependent patterns"""
        
        return [TextContent(type="text", text=explanation)]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Run the server"""
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="forecasting-calculator",
                server_version="1.0.0",
                capabilities=ServerCapabilities(
                    tools={}
                )
            )
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
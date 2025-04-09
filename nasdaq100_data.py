import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Calculate date range
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Fetch NASDAQ 100 data
ndx = yf.Ticker("^NDX")
hist = ndx.history(start=start_date, end=end_date)

# Calculate RSI
def calculate_rsi(data, periods=14):
    # Calculate price changes
    delta = data.diff()
    
    # Separate gains and losses
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    
    # Calculate RS and RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate Fibonacci retracement levels
def calculate_fibonacci_levels(data):
    high = data['High'].max()
    low = data['Low'].min()
    diff = high - low
    
    levels = {
        '0%': low,
        '23.6%': low + 0.236 * diff,
        '38.2%': low + 0.382 * diff,
        '50%': low + 0.5 * diff,
        '61.8%': low + 0.618 * diff,
        '78.6%': low + 0.786 * diff,
        '100%': high
    }
    return levels

# Calculate RSI
rsi = calculate_rsi(hist['Close'])

# Calculate Fibonacci levels
fib_levels = calculate_fibonacci_levels(hist)

# Display closing prices and RSI
print("\nNASDAQ 100 Data for the Past 30 Days:")
print("=====================================")
print("Date         | Closing Price | RSI")
print("-------------------------------------")
for date, row in hist.iterrows():
    rsi_value = rsi[date] if not pd.isna(rsi[date]) else "N/A"
    print(f"{date.strftime('%Y-%m-%d')} | {row['Close']:11.2f} | {rsi_value if isinstance(rsi_value, str) else f'{rsi_value:.2f}'}")

# Display Fibonacci retracement levels
print("\nFibonacci Retracement Levels:")
print("============================")
for level, value in fib_levels.items():
    print(f"{level:6} | {value:11.2f}")

# Find the swing high and low dates
swing_high_date = hist['High'].idxmax()
swing_low_date = hist['Low'].idxmin()

print(f"\nSwing High: {swing_high_date.strftime('%Y-%m-%d')} at {hist['High'].max():.2f}")
print(f"Swing Low:  {swing_low_date.strftime('%Y-%m-%d')} at {hist['Low'].min():.2f}") 
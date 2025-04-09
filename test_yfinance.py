import yfinance as yf
from datetime import datetime, timedelta

# Calculate date range
end_date = datetime.now()
start_date = end_date - timedelta(days=30)  # Last 30 days

# Fetch data for S&P 500
print("Fetching S&P 500 data...")
spx_data = yf.download("^GSPC", start=start_date, end=end_date)
print(f"S&P 500 data shape: {spx_data.shape}")
print(f"S&P 500 date range: {spx_data.index[0]} to {spx_data.index[-1]}")
print(f"S&P 500 columns: {spx_data.columns.tolist()}")

# Fetch data for NASDAQ 100
print("\nFetching NASDAQ 100 data...")
ndx_data = yf.download("^NDX", start=start_date, end=end_date)
print(f"NASDAQ 100 data shape: {ndx_data.shape}")
print(f"NASDAQ 100 date range: {ndx_data.index[0]} to {ndx_data.index[-1]}")
print(f"NASDAQ 100 columns: {ndx_data.columns.tolist()}") 
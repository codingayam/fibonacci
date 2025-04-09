import yfinance as yf
from datetime import datetime, timedelta

# Try different time periods
periods = [
    "max",  # Maximum available
    "10y",  # 10 years
    "5y",   # 5 years
    "1y",   # 1 year
    "6mo",  # 6 months
    "3mo",  # 3 months
    "1mo"   # 1 month
]

print("Testing maximum historical data availability for NASDAQ 100 (^NDX):")
print("================================================================")

ndx = yf.Ticker("^NDX")

for period in periods:
    try:
        data = ndx.history(period=period)
        start_date = data.index[0].strftime('%Y-%m-%d')
        end_date = data.index[-1].strftime('%Y-%m-%d')
        days = (data.index[-1] - data.index[0]).days
        print(f"\nPeriod '{period}':")
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")
        print(f"Total days: {days}")
        print(f"Data points: {len(data)}")
    except Exception as e:
        print(f"\nError with period '{period}': {str(e)}") 
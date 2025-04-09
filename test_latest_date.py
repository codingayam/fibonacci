import yfinance as yf
from datetime import datetime, timedelta

def test_latest_date():
    print("Testing latest available date for S&P 500 and NASDAQ 100")
    print("=" * 50)
    
    # Set date range to just the last few days to get the most recent data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)  # Last 5 days
    
    # Test S&P 500
    print("\nTesting S&P 500 (^GSPC):")
    try:
        spx = yf.download("^GSPC", start=start_date, end=end_date)
        print(f"Data shape: {spx.shape}")
        print(f"All available dates:")
        for date in spx.index:
            print(f"  {date}")
        print(f"\nLatest date: {spx.index[-1]}")
    except Exception as e:
        print(f"Error fetching S&P 500 data: {str(e)}")
    
    # Test NASDAQ 100
    print("\nTesting NASDAQ 100 (^NDX):")
    try:
        ndx = yf.download("^NDX", start=start_date, end=end_date)
        print(f"Data shape: {ndx.shape}")
        print(f"All available dates:")
        for date in ndx.index:
            print(f"  {date}")
        print(f"\nLatest date: {ndx.index[-1]}")
    except Exception as e:
        print(f"Error fetching NASDAQ 100 data: {str(e)}")

if __name__ == "__main__":
    test_latest_date() 
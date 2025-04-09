import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def test_data_fetch():
    print("Testing data fetching for S&P 500 and NASDAQ 100")
    print("=" * 50)
    
    # Set date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days for testing
    
    # Test S&P 500
    print("\nTesting S&P 500 (^GSPC):")
    try:
        spx = yf.download("^GSPC", start=start_date, end=end_date)
        print(f"Data shape: {spx.shape}")
        print(f"Columns: {spx.columns.tolist()}")
        print(f"Date range: {spx.index[0]} to {spx.index[-1]}")
        print("\nFirst few rows:")
        print(spx.head())
        
        # Test column access
        print("\nTesting column access:")
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if isinstance(spx.columns, pd.MultiIndex):
                # Try both direct access and tuple access
                try:
                    value = spx[(col, '^GSPC')].iloc[-1]
                    print(f"{col}: {value} (accessed via tuple)")
                except:
                    try:
                        value = spx[col].iloc[-1]
                        print(f"{col}: {value} (accessed directly)")
                    except:
                        print(f"Could not access {col}")
            else:
                try:
                    value = spx[col].iloc[-1]
                    print(f"{col}: {value}")
                except:
                    print(f"Could not access {col}")
    except Exception as e:
        print(f"Error fetching S&P 500 data: {str(e)}")
    
    # Test NASDAQ 100
    print("\nTesting NASDAQ 100 (^NDX):")
    try:
        ndx = yf.download("^NDX", start=start_date, end=end_date)
        print(f"Data shape: {ndx.shape}")
        print(f"Columns: {ndx.columns.tolist()}")
        print(f"Date range: {ndx.index[0]} to {ndx.index[-1]}")
        print("\nFirst few rows:")
        print(ndx.head())
        
        # Test column access
        print("\nTesting column access:")
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if isinstance(ndx.columns, pd.MultiIndex):
                # Try both direct access and tuple access
                try:
                    value = ndx[(col, '^NDX')].iloc[-1]
                    print(f"{col}: {value} (accessed via tuple)")
                except:
                    try:
                        value = ndx[col].iloc[-1]
                        print(f"{col}: {value} (accessed directly)")
                    except:
                        print(f"Could not access {col}")
            else:
                try:
                    value = ndx[col].iloc[-1]
                    print(f"{col}: {value}")
                except:
                    print(f"Could not access {col}")
    except Exception as e:
        print(f"Error fetching NASDAQ 100 data: {str(e)}")

if __name__ == "__main__":
    test_data_fetch() 
import yfinance as yf
import time
from datetime import datetime, timedelta

def test_rate_limits():
    print("Testing yfinance API limits and best practices:")
    print("=============================================")
    
    # Test 1: Multiple rapid requests
    print("\nTest 1: Multiple rapid requests")
    ticker = yf.Ticker("^NDX")
    
    start_time = time.time()
    for i in range(5):
        try:
            data = ticker.history(period="1d")
            print(f"Request {i+1}: Success")
            time.sleep(1)  # Best practice: Add delay between requests
        except Exception as e:
            print(f"Request {i+1}: Failed - {str(e)}")
    
    # Test 2: Large historical data request
    print("\nTest 2: Large historical data request")
    try:
        start_time = time.time()
        data = ticker.history(period="max")
        end_time = time.time()
        print(f"Successfully fetched {len(data)} data points")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Failed to fetch large dataset: {str(e)}")
    
    # Test 3: Caching demonstration
    print("\nTest 3: Caching demonstration")
    try:
        # First request
        start_time = time.time()
        data1 = ticker.history(period="1mo")
        end_time = time.time()
        print(f"First request time: {end_time - start_time:.2f} seconds")
        
        # Second request (should be faster due to caching)
        start_time = time.time()
        data2 = ticker.history(period="1mo")
        end_time = time.time()
        print(f"Second request time: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Cache test failed: {str(e)}")

if __name__ == "__main__":
    test_rate_limits() 
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from openai import OpenAI
import os

# Set page config
st.set_page_config(
    page_title="S&P 500 & NASDAQ 100 Technical Analysis",
    page_icon="📈",
    layout="wide"
)

# Initialize OpenAI client
client = None

# Title and description
st.title("S&P 500 & NASDAQ 100 Technical Analysis Dashboard")
st.markdown("This dashboard shows technical analysis for both S&P 500 and NASDAQ 100 indices including price data and Fibonacci retracement levels.")

# Add OpenAI API key input in sidebar
with st.sidebar:
    st.header("OpenAI Settings")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if api_key:
        try:
            # Initialize the client with the API key
            client = OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {str(e)}")

# Sidebar for date range selection
st.sidebar.header("Settings")
start_year = st.sidebar.slider("Start Year", 2008, 2024, 2008)

# Calculate date range
end_date = datetime.now()
start_date = datetime(start_year, 1, 1)

# Fetch data function with bi-monthly sampling
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def fetch_data(ticker, start_date, end_date):
    # Fetch data from yfinance with retries
    max_retries = 3
    for attempt in range(max_retries):
        try:
            data = yf.download(ticker, start=start_date, end=end_date, timeout=30)
            break
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                st.error(f"Failed to fetch data for {ticker} after {max_retries} attempts: {str(e)}")
                return pd.DataFrame()
            time.sleep(2)  # Wait before retrying
    
    # Check if the data is empty
    if data.empty:
        st.error(f"No data available for {ticker}")
        return pd.DataFrame()
    
    # Debug: Print column names to see what's available
    st.write(f"Columns for {ticker}: {data.columns.tolist()}")
    
    # Print the last date in the data for debugging
    st.write(f"Last date in raw data for {ticker}: {data.index[-1]}")
    
    # Handle multi-level column names and resample
    try:
        # Create a copy of the data with simplified column names
        processed_data = pd.DataFrame()
        
        # Map the multi-level columns to single level
        if isinstance(data.columns, pd.MultiIndex):
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                processed_data[col] = data[(col, ticker)]
        else:
            processed_data = data.copy()
        
        # Resample to bi-monthly data
        resampled_data = processed_data.resample('2ME').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })
        
        # Print the last date after resampling for debugging
        st.write(f"Last date after resampling for {ticker}: {resampled_data.index[-1]}")
        
        return resampled_data
        
    except Exception as e:
        st.error(f"Error processing data for {ticker}: {str(e)}")
        st.write("Available columns:", data.columns.tolist())
        return pd.DataFrame()

# Calculate Fibonacci retracement levels
def calculate_fibonacci_levels(data, direction='down'):
    if data.empty:
        return {}
    
    if direction == 'down':
        high = data['High'].max()
        low = data['Low'].min()
        diff = high - low
        
        # Calculate retracement levels from the high point
        levels = {
            '0%': high,  # Start from the high point
            '23.6%': high - 0.236 * diff,
            '38.2%': high - 0.382 * diff,
            '50%': high - 0.5 * diff,
            '61.8%': high - 0.618 * diff,
            '78.6%': high - 0.786 * diff,
            '100%': low  # End at the low point
        }
    else:  # upward retracement
        latest_low = data['Low'].iloc[-1]  # Latest trading day's low
        high = data['High'].max()
        diff = high - latest_low
        
        # Calculate retracement levels from the latest low
        levels = {
            '0%': latest_low,  # Start from the latest low
            '23.6%': latest_low + 0.236 * diff,
            '38.2%': latest_low + 0.382 * diff,
            '50%': latest_low + 0.5 * diff,
            '61.8%': latest_low + 0.618 * diff,
            '78.6%': latest_low + 0.786 * diff,
            '100%': high  # End at the high point
        }
    return levels

# Fetch data for both indices
spx_data = fetch_data("^GSPC", start_date, end_date)
ndx_data = fetch_data("^NDX", start_date, end_date)

# Check if we have data
if spx_data.empty or ndx_data.empty:
    st.error("Could not fetch data for one or both indices. Please check the ticker symbols and try again.")
    st.stop()

# Calculate Fibonacci levels for both directions
spx_fib_levels_down = calculate_fibonacci_levels(spx_data, 'down')
spx_fib_levels_up = calculate_fibonacci_levels(spx_data, 'up')
ndx_fib_levels_down = calculate_fibonacci_levels(ndx_data, 'down')
ndx_fib_levels_up = calculate_fibonacci_levels(ndx_data, 'up')

# Create two columns for the layout
col1, col2 = st.columns(2)

# Function to create price chart with Fibonacci levels
def create_price_chart(data, fib_levels_down, fib_levels_up, title):
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=title
    ))
    
    # Add downward Fibonacci levels as horizontal lines (red)
    colors_down = ['rgba(255,0,0,0.5)', 'rgba(255,165,0,0.5)', 'rgba(255,255,0,0.5)', 
              'rgba(0,255,0,0.5)', 'rgba(0,0,255,0.5)', 'rgba(75,0,130,0.5)']
    
    for (level, value), color in zip(fib_levels_down.items(), colors_down):
        fig.add_hline(y=value, line_dash="dash", line_color=color,
                     annotation_text=f"Down {level}", annotation_position="right")
    
    # Add upward Fibonacci levels as horizontal lines (green)
    colors_up = ['rgba(0,255,0,0.5)', 'rgba(0,200,0,0.5)', 'rgba(0,150,0,0.5)',
                'rgba(0,100,0,0.5)', 'rgba(0,50,0,0.5)', 'rgba(0,25,0,0.5)']
    
    for (level, value), color in zip(fib_levels_up.items(), colors_up):
        fig.add_hline(y=value, line_dash="dot", line_color=color,
                     annotation_text=f"Up {level}", annotation_position="left")
    
    fig.update_layout(
        title=title,
        yaxis_title='Price',
        xaxis_title='Date',
        height=600
    )
    
    return fig

# Display S&P 500 chart
with col1:
    st.subheader("S&P 500 (^GSPC)")
    fig_spx = create_price_chart(spx_data, spx_fib_levels_down, spx_fib_levels_up, 'S&P 500 with Fibonacci Retracement Levels')
    st.plotly_chart(fig_spx, use_container_width=True)
    
    # Display S&P 500 Fibonacci levels
    st.subheader("S&P 500 Fibonacci Levels")
    col1a, col1b = st.columns(2)
    with col1a:
        st.write("Downward Retracement")
        spx_fib_df_down = pd.DataFrame(list(spx_fib_levels_down.items()), columns=['Level', 'Price'])
        st.table(spx_fib_df_down)
    with col1b:
        st.write("Upward Retracement")
        spx_fib_df_up = pd.DataFrame(list(spx_fib_levels_up.items()), columns=['Level', 'Price'])
        st.table(spx_fib_df_up)

# Display NASDAQ 100 chart
with col2:
    st.subheader("NASDAQ 100 (^NDX)")
    fig_ndx = create_price_chart(ndx_data, ndx_fib_levels_down, ndx_fib_levels_up, 'NASDAQ 100 with Fibonacci Retracement Levels')
    st.plotly_chart(fig_ndx, use_container_width=True)
    
    # Display NASDAQ 100 Fibonacci levels
    st.subheader("NASDAQ 100 Fibonacci Levels")
    col2a, col2b = st.columns(2)
    with col2a:
        st.write("Downward Retracement")
        ndx_fib_df_down = pd.DataFrame(list(ndx_fib_levels_down.items()), columns=['Level', 'Price'])
        st.table(ndx_fib_df_down)
    with col2b:
        st.write("Upward Retracement")
        ndx_fib_df_up = pd.DataFrame(list(ndx_fib_levels_up.items()), columns=['Level', 'Price'])
        st.table(ndx_fib_df_up)

# Display current statistics
st.subheader("Current Statistics")
col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric("S&P 500 Current Price", f"${spx_data['Close'].iloc[-1]:,.2f}")
    st.write(f"Last Updated: {spx_data.index[-1].strftime('%Y-%m-%d %H:%M:%S')}")
with col4:
    spx_change = ((spx_data['Close'].iloc[-1] - spx_data['Close'].iloc[0]) / spx_data['Close'].iloc[0]) * 100
    st.metric("S&P 500 Period Change", f"{spx_change:.2f}%")
with col5:
    st.metric("NASDAQ 100 Current Price", f"${ndx_data['Close'].iloc[-1]:,.2f}")
    st.write(f"Last Updated: {ndx_data.index[-1].strftime('%Y-%m-%d %H:%M:%S')}")
with col6:
    ndx_change = ((ndx_data['Close'].iloc[-1] - ndx_data['Close'].iloc[0]) / ndx_data['Close'].iloc[0]) * 100
    st.metric("NASDAQ 100 Period Change", f"{ndx_change:.2f}%")

# Add AI Analysis Section
st.markdown("---")
st.subheader("🤖 AI Technical Analysis Assistant")
st.markdown("Ask questions about the technical analysis, Fibonacci levels, or market trends.")

# Create a text input for user queries
user_query = st.text_input("Enter your question about the technical analysis:", 
                         placeholder="e.g., What do the current Fibonacci levels suggest about market direction?")

if user_query and client is not None:
    # Prepare context for OpenAI
    context = f"""
    Current Market Data:
    - S&P 500 Current Price: ${spx_data['Close'].iloc[-1]:,.2f}
    - S&P 500 Period Change: {spx_change:.2f}%
    - NASDAQ 100 Current Price: ${ndx_data['Close'].iloc[-1]:,.2f}
    - NASDAQ 100 Period Change: {ndx_change:.2f}%
    
    S&P 500 Fibonacci Levels (Downward):
    {spx_fib_levels_down}
    
    S&P 500 Fibonacci Levels (Upward):
    {spx_fib_levels_up}
    
    NASDAQ 100 Fibonacci Levels (Downward):
    {ndx_fib_levels_down}
    
    NASDAQ 100 Fibonacci Levels (Upward):
    {ndx_fib_levels_up}
    """
    
    try:
        # Call OpenAI API using the new API format
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional technical analyst specializing in Fibonacci analysis and market trends. Provide clear, concise, and insightful analysis based on the provided data."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_query}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Display the response
        st.markdown("### Analysis")
        st.write(response.choices[0].message.content)
        
    except Exception as e:
        st.error(f"Error getting AI analysis: {str(e)}")
elif user_query and client is None:
    st.warning("Please enter your OpenAI API key in the sidebar to get AI analysis.") 
# S&P 500 & NASDAQ 100 Technical Analysis Dashboard

A Streamlit application that provides technical analysis for S&P 500 and NASDAQ 100 indices, including price data and Fibonacci retracement levels. The app also features an AI-powered analysis assistant using OpenAI's GPT-4o.

## Features

- Real-time data from Yahoo Finance for S&P 500 (^GSPC) and NASDAQ 100 (^NDX)
- Interactive candlestick charts with Fibonacci retracement levels
- Customizable date range selection
- AI-powered technical analysis using OpenAI's GPT-4o
- Responsive layout with detailed statistics

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/yfinance.git
cd yfinance
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
python -m streamlit run app_simple.py
```

## Usage

1. Enter your OpenAI API key in the sidebar
2. Select your desired start year using the slider
3. View the interactive charts and Fibonacci levels
4. Ask questions about the technical analysis in the AI Assistant section

## Cloud Deployment

This app can be deployed to Streamlit Cloud:

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app

### Troubleshooting Cloud Deployment

If you encounter issues with data fetching in the cloud environment:

1. The app will automatically try alternative ticker symbols (SPY for S&P 500, QQQ for NASDAQ 100)
2. Check the logs in Streamlit Cloud for detailed error messages
3. You may need to adjust the date range if historical data is not available

## Requirements

- Python 3.9+
- streamlit
- yfinance
- pandas
- numpy
- plotly
- requests

## License

MIT

## Acknowledgments

- Data provided by Yahoo Finance
- AI analysis powered by OpenAI 
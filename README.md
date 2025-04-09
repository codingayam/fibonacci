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
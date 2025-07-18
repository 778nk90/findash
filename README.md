# Simple Financial Dashboard

A real-time financial dashboard built with Dash, yfinance, and Plotly.

## Features

- **Dark-themed UI** with modern styling
- **Stock Ticker Selection** - Choose from 6 major stocks (AAPL, TSLA, SPY, GOOGL, AMZN, MSFT)
- **Real-time Key Metrics** - Latest price, percentage change, and volume
- **Interactive Line Chart** - 5-day price history with hourly intervals
- **Auto-refresh** - Updates every 30 seconds
- **Error Handling** - Graceful handling of data fetching issues

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd findash
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:
```bash
python app.py
```

The dashboard will be available at `http://127.0.0.1:8050/`

## Dependencies

- `dash>=2.0.0` - Web application framework
- `yfinance>=0.2.0` - Yahoo Finance data fetching
- `plotly>=5.0.0` - Interactive charts
- `pandas>=1.3.0` - Data manipulation

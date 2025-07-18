import yfinance as yf
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# -------------------------
# CONFIGURATION
# -------------------------
TICKERS = ["AAPL", "TSLA", "SPY", "GOOGL", "AMZN", "MSFT"]

# -------------------------
# DASH APP SETUP
# -------------------------
app = Dash(__name__)
app.title = "Simple Financial Dashboard"

# App layout
app.layout = html.Div(
    style={
        "backgroundColor": "#121212",
        "color": "white",
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
    },
    children=[
        html.H1(
            "Simple Financial Dashboard",
            style={
                "textAlign": "center",
                "padding": "10px",
                "color": "#00d4ff",
                "fontSize": "2.5em",
            },
        ),
        html.Div(
            style={"marginBottom": "20px", "textAlign": "center"},
            children=[
                dcc.Dropdown(
                    id="ticker-dropdown",
                    options=[{"label": ticker, "value": ticker} for ticker in TICKERS],
                    value=TICKERS[0],
                    placeholder="Select a stock ticker...",
                    style={
                        "width": "50%",
                        "margin": "auto",
                        "backgroundColor": "#1e1e1e",
                        "color": "white",
                        "border": "1px solid #00d4ff",
                        "borderRadius": "5px",
                    },
                ),
            ],
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-around",
                "marginBottom": "20px",
            },
            children=[
                html.Div(
                    id="key-metrics",
                    style={
                        "width": "30%",
                        "padding": "10px",
                        "backgroundColor": "#1e1e1e",
                        "borderRadius": "10px",
                        "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",
                        "textAlign": "center",
                    },
                ),
                dcc.Graph(
                    id="stock-line-chart",
                    style={
                        "width": "65%",
                        "backgroundColor": "#1e1e1e",
                        "borderRadius": "10px",
                        "padding": "10px",
                    },
                ),
            ],
        ),
        dcc.Interval(id="interval-component", interval=30 * 1000, n_intervals=0),
    ],
)

# -------------------------
# CALLBACKS
# -------------------------
@app.callback(
    [Output("key-metrics", "children"), Output("stock-line-chart", "figure")],
    [Input("ticker-dropdown", "value"), Input("interval-component", "n_intervals")],
)
def update_dashboard(selected_ticker, n_intervals):
    print(f"Fetching data for {selected_ticker}...")

    try:
        # Fetch stock data
        data = yf.download(tickers=selected_ticker, period="5d", interval="1h")
        if data.empty:
            raise ValueError(f"No data for {selected_ticker}")
        latest_price = data["Close"].iloc[-1]
        previous_close = data["Close"].iloc[-2]
        percentage_change = ((latest_price - previous_close) / previous_close) * 100
        volume = data["Volume"].iloc[-1]

        # Key metrics
        key_metrics = html.Div(
            children=[
                html.H4(f"Ticker: {selected_ticker}", style={"color": "#00d4ff"}),
                html.P(f"Latest Price: ${latest_price:.2f}"),
                html.P(
                    f"Change: {percentage_change:.2f}%",
                    style={"color": "green" if percentage_change > 0 else "red"},
                ),
                html.P(f"Volume: {volume:,}"),
            ]
        )

        # Line chart
        line_chart = go.Figure(
            data=[
                go.Scatter(
                    x=data.index,
                    y=data["Close"],
                    mode="lines",
                    line=dict(color="#00d4ff"),
                )
            ]
        )
        line_chart.update_layout(
            title=f"{selected_ticker} Price History",
            xaxis_title="Time",
            yaxis_title="Price",
            template="plotly_dark",
        )

        return key_metrics, line_chart

    except Exception as e:
        print(f"Error fetching data for {selected_ticker}: {e}")
        return (
            html.Div(
                children=[
                    html.H4("Error", style={"color": "red"}),
                    html.P(f"Unable to fetch data for {selected_ticker}."),
                ]
            ),
            go.Figure(),
        )


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    print("Starting Dash server...")
    app.run(debug=True)
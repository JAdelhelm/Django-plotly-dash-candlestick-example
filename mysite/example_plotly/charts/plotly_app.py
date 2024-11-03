
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from django_plotly_dash import DjangoDash

from .create_figures import create_candlestick_figure, create_app_layout_candlesticks

import re
from datetime import datetime,date

import pandas as pd
from django.conf import settings

import yfinance as yf

def sanitize_app_name(stock_symbol):
    raw_name = f"{stock_symbol}"
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', raw_name)  
    return sanitized_name


def create_dash_app(stock_symbol):
    app_name = sanitize_app_name(stock_symbol)

    if app_name in settings.APP_REGISTRY:
        return app_name
    
    app = DjangoDash(app_name, add_bootstrap_links=True)
    settings.APP_REGISTRY[app_name] = app

    app = create_app_layout_candlesticks(app, app_name)

    @app.callback(
        Output(f"interval_counter_{app_name}", "children"),
        Input("interval", "n_intervals")
    )
    def interval_c(n_intervals):
        return f"Counting intervals: {str(n_intervals)}"
    

    @app.callback(
        Output(f"candles_{app_name}", "figure"),
        [Input("interval", "n_intervals"),
         Input(f"candles_{app_name}", "relayoutData")
        ],
    )
    def update_figure_candlesticks(n_intervals, relOut,  session_state=None, **kwargs):  
        stock_symbol = session_state.get(f"{app_name}_stock_symbol")

        ticker_symbol = "AAPL"
        ticker =  yf.Ticker(ticker_symbol)
        data = ticker.history(period="1y")
        data = data.sort_index(ascending=False).reset_index(drop=False)

        data.columns = map(str.lower, data.columns)
        data['date'] = data['date'].dt.tz_convert('UTC')  # Convert to UTC
        data['date'] = data['date'].dt.date               # Extract only the date part
        
        data['date'] = pd.to_datetime(data['date'])

        fig = create_candlestick_figure(data=data, stock_symbol=stock_symbol)

        if relOut is None or "xaxis.range[0]" not in relOut or "xaxis.range[1]" not in relOut:
            y_min_global = data['low'].min()
            y_max_global = data['high'].max()
            
            fig.update_yaxes(range=[y_min_global, y_max_global])
            return fig

        x_min = pd.to_datetime(relOut["xaxis.range[0]"])
        x_max = pd.to_datetime(relOut["xaxis.range[1]"])

        zoomed_data = data[(data['date'] >= x_min) & (data['date'] <= x_max)]


        if not zoomed_data.empty:
            y_min = zoomed_data['low'].min()
            y_max = zoomed_data['high'].max()


            y_range = y_max - y_min
            zoom_factor = len(data) / len(zoomed_data) 
            dynamic_padding = y_range * 0.05 * min(zoom_factor, 1.5)  

            y_min -= dynamic_padding
            y_max += dynamic_padding


            fig.update_yaxes(range=[y_min, y_max])

        return fig
                

    return app_name 

















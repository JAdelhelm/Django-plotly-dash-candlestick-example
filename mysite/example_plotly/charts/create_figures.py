import plotly.graph_objects as go
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import json
import base64
import datetime
import requests
import pathlib
import math
import pandas as pd
import dash

from plotly.tools import FigureFactory as FF
from datetime import datetime, date, time, timedelta, timezone
import pytz
from plotly import tools




def apply_log_function(df) -> pd.DataFrame:
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    for c in [c for c in df.columns if df[c].dtype in numerics]:
        df[c] = np.log10(df[c])

    return df


def create_candlestick_figure(data, stock_symbol) -> go.Figure:
        # data = apply_log_function(df=data)
        # data, minTimeStampChart, maxTimeStampChart, newRangeLow, newRangeHigh = get_correct_date(df=data)

        fig = go.Figure(
            data = [
                    go.Candlestick(
                                x=data['date'],
                                open=data['open'],
                                high=data['high'],
                                low=data['low'],
                                close=data['close'],
                                showlegend=False,
                                name="candlestick"
                                )])

        fig.update_xaxes(
            fixedrange=False,
            # rangeslider_visible=True,
            rangebreaks=[
                # NOTE: Below values are bound (not single values), ie. hide x to y
                dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                # dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
                dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
            ],

                
        )


        fig.update_layout(
            
            uirevision='fixed',  # Keeps the UI state on data updates
            autosize=False,
            title={
                "text": f"{stock_symbol}",
                "font": {
                    "color": "#ffffff",
                    "size": 18
                }
            },
            # title_subtitle=dict({
            #     "text":f"(adjusted chart) - historical split/dividend events"}),
            # title_subtitle_font=dict({
            #     "color":"#ffffff",
            #     "size" : 16
            # }),

            dragmode="pan",  # Set pan as the default drag mode
            margin={"t": 150, "l": 50, "r": 50, "b": 50},

            height=700,

            
            xaxis={
                "rangeslider": {
                    "visible": False
                },
                "color": "#ffffff",
                "showgrid":True,
                "gridcolor": "#3E3F40",
                "showticklabels": True,  # Move showticklabels to xaxis
                # "autorange" : False,
                # "range":[minTimeStampChart, maxTimeStampChart]
            },
            yaxis={
                "showgrid": True,
                "gridcolor": "#3E3F40",
                # "gridwidth": 1,
                "color": "#ffffff",
                # "fixedrange": False,
                "showticklabels": True,  # Move showticklabels to yaxis
                # "tick0":0.500,
                # "dtick":.0001,
                # "autorange": False,
                # "range" : [newRangeLow, newRangeHigh]
            },
            # annotations = getChartBarNumbers(df=data),
            paper_bgcolor="#21252C",
            plot_bgcolor="#21252C",
        )
        return fig

def create_app_layout_candlesticks(app, app_name):
    # Layout App
    app.layout = dbc.Container([
        dcc.Graph(
                id=f"candles_{app_name}",
                config={
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": ['toImage', "zoomIn2d", "zoomOut2d","lasso2d", "select2d"],
            "scrollZoom": True,
            "displayModeBar": True,
            "modeBarButtonsToAdd": ["drawline","drawopenpath","v1hovermode","eraseshape"],
            }),
        
        html.Div(
            children=[
                html.H1(id=f"interval_counter_{app_name}")
            ]
        ),

        dcc.Interval(id="interval", interval = 5_000)

    ],id="container-das-id",    
    className = "four columns vstack gap-2 h-75",
        style = {'padding':'2rem'})
    
    return app






import sys

import pandas as pd
import colorlover as cl
from reactpy import html, component, event, use_state, utils
from reactpy_select import Select, ActionMeta

from utils.options import Options
from dash import dcc

# ReactPy clone of the classic Plotly/Dash Stock Tickers Demo App
#
# See https://github.com/plotly/dash-stock-tickers-demo-app
#
# Integration of plotly.graph_objects with ReactPy:
#
# See https://energybeam.blogspot.com/2023/08/how-to-add-plotly-charts-in-reactpy.html


try:
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')
except Exception:
    print("Unable to read 'dash-stock-ticker-demo.csv' from github, no internet connection?")
    sys.exit(0)

colourStyles = {

  'multiValueLabel': '''(styles, { data }) => ({
    ...styles,
    color: '#5ca3ff',
  })''',

  'multiValue': '''(styles, { data }) => {
    return {
      ...styles,
      backgroundColor: '#ebf5ff',
      border: '1px solid #c2e0ff'
    }
  }''',

  'multiValueRemove': '''(styles, { data }) => ({
    ...styles,
    color: '#5ca3ff',
    ':hover': {
      backgroundColor: '#d9ebfd',
    },
  })''',
}

colorscale = cl.scales['9']['qual']['Paired']

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

def update_graph(tickers=None):
    tickers = tickers or []
    graphs = []

    if not tickers:
        graphs.append(html.h2({'style': {'marginTop': 20, 'marginBottom': 20}}, "Select a stock ticker."))
    else:
        for i, ticker in enumerate(tickers):

            dff = df[df['Stock'] == ticker]

            candlestick = {
                'x': dff['Date'],
                'open': dff['Open'],
                'high': dff['High'],
                'low': dff['Low'],
                'close': dff['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(dff.Close)
            bollinger_traces = [{
                'x': dff['Date'], 'y': y,
                'type': 'scatter',
                'mode': 'lines',
                'line': {'width': 2, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': (i == 0),
                'name': f'{ticker} - Bollinger Bands'
            } for i, y in enumerate(bb_bands)]

            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))

    return html.div(graphs)


@component
def Layout():

    values, set_values =  use_state([])

    tickers=[{'label': s[0], 'value': str(s[1])}
                for s in zip(df.Stock.unique(), df.Stock.unique())]

    @event
    def on_change(selectedTickers: Options, actionMeta: ActionMeta):
        set_values(selectedTickers)

    return html.div(
        html.h2('Finance Explorer'),
        html.br(),
        Select(
            default_value=values,
            onchange=on_change,
            options=tickers,
            multi=True,
            styles=colourStyles
            ),
        html.div({'id': 'graphs'}, update_graph([val['value'] for val in values]))
    )

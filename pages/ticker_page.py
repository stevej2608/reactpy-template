import sys
from typing import Any, Dict, List, Tuple

import colorlover as cl
import pandas as pd
from reactpy import component, event, html, use_state
from reactpy.core.types import VdomDict
from reactpy_router import Navigate
from reactpy_router.core import use_query
from reactpy_select import ActionMeta, Options, Select


from dash import dcc
from utils.logger import log


# ReactPy clone of the classic Plotly/Dash Stock Tickers Demo App
#
# See https://github.com/plotly/dash-stock-tickers-demo-app
#
# Integration of plotly.graph_objects with ReactPy:
#
# See https://energybeam.blogspot.com/2023/08/how-to-add-plotly-charts-in-reactpy.html

try:
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv') # type: ignore
except Exception:
    print("Unable to read 'dash-stock-ticker-demo.csv' from github, no internet connection?")
    sys.exit(0)


TICKERS: Options = [{'label': s[0], 'value': str(s[1])}
            for s in zip(df.Stock.unique(), df.Stock.unique())] # type: ignore

NULL_OPTIONS: Options = [] 

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

def bbands(price: Any, window_size:int=10, num_of_std:int=5) -> Tuple[float, float, float]: # type: ignore

    rolling_mean: float = price.rolling(window=window_size).mean()
    rolling_std: float = price.rolling(window=window_size).std()
    upper_band: float = rolling_mean + (rolling_std*num_of_std)
    lower_band: float = rolling_mean - (rolling_std*num_of_std)

    return rolling_mean, upper_band, lower_band

def update_graphs(tickers: List[str] | None =None) -> VdomDict:
    tickers = tickers or []
    graphs: List[VdomDict] = []

    log.info('update_graph(tickers=%s)', tickers)

    if not tickers:
        graphs.append(html.h2({'style': {'marginTop': 20, 'marginBottom': 20}}, "Select a stock ticker."))
    else:
        for _i, ticker in enumerate(tickers):

            dff = df[df['Stock'] == ticker]

            candlestick: Dict[str, Any] = {
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

            bb_bands = bbands(dff.Close) # type: ignore

            bollinger_traces: List[Dict[str, Any]] = [{
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
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                },
                config={'displayModeBar': False}
            ))

    return html.div(graphs)


@component
def TickerSelect(tickers: Options):

    to, set_to = use_state('')

    def get_url_search(tickers:Options) -> str:
        t: List[str] = [ ticker['value'] for ticker in tickers]
        if t:
            return f"?tickers={'+'.join(t)}"
        else:
            return ''

    @event
    def on_change(selectedTickers: Options, actionMeta: ActionMeta):
        loc = get_url_search(selectedTickers) 
        set_to(loc)

    log.info('TickerSelect tickers=%s', tickers)

    return html._(
        Select(
            default_value=tickers,
            onchange=on_change,
            options=TICKERS,
            multi=True,
            styles=colourStyles
            ),
        Navigate(to=to)
    )


@component
def Layout() -> VdomDict:

    def qs_tickers():
        """Extract tickers from query string"""

        # http://127.0.0.1:8000/tickers?tickers=TSLA+GOOGL

        try:
            tickers = use_query()['tickers'][0].split(' ')
        except Exception:
            tickers = []

        return [{'label': ticker, 'value': ticker} for ticker in tickers]


    tickers = qs_tickers()

    log.info('TickerSelect tickers=%s', tickers)

    return html.div(
        html.h2('Finance Explorer'),
        html.br(),
        TickerSelect(tickers),
        html.div({'id': 'graphs'}, update_graphs([ticker['value'] for ticker in tickers])),
    )

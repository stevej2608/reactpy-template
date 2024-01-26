
from io import StringIO
import plotly.graph_objects as go
from reactpy import utils

# A plotly.graph_objects wrapper that mimics the Dash 
# core components Graph interface. This is a very simplistic
# effort. It's only supports the minimal graph types and
# attributes required to render the Dash examples that have
# been ported over to this project.
#
# Dash Graph: https://dash.plotly.com/dash-core-components/graph
# Plotly Graph Objects: https://plotly.com/python/graph-objects/
# Plotly Overview : https://plotly.com/python/plotly-fundamentals/
# Plotly API : https://plotly.com/python/reference/candlestick/

def Graph(figure:dict, config:dict):
    traces = []

    for chart in figure['data']:
        if 'type' in chart:
            if chart['type'] == 'candlestick':
                ct = go.Candlestick(chart)
                traces.append(ct)
                continue
            if chart['type'] == 'scatter':
                ct = go.Scatter(chart)
                traces.append(ct)
                continue
            raise(f"Unsupported chart type: {chart['type']}")
        else:
            if 'x' in chart and 'y' in chart:
                args = {**chart}
                ct = go.Scatter(args)
                traces.append(ct)


    fig = go.Figure(data=traces)

    fig.update_layout(
        legend=dict(
            bgcolor='White',
            yanchor="top",
            y=1.00,
            xanchor="left",
            x=0.00
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin={'b': 0, 'r': 10, 'l': 60, 't': 20},
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Create an html object in memory from fig.

    buffer = StringIO()
    fig.write_html(buffer, include_plotlyjs='cdn', config=config)
    fig_html = buffer.getvalue()
    return utils.html_to_vdom(fig_html)

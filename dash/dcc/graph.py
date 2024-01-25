
from io import StringIO
import plotly.graph_objects as go
from reactpy import utils

def Graph(id:str, figure:dict):
    charts = []

    for chart in figure['data']:
        if chart['type'] == 'candlestick':
            ct = go.Candlestick(chart)
            charts.append(ct)
            continue
        if chart['type'] == 'scatter':
            ct = go.Scatter(chart)
            charts.append(ct)

    fig = go.Figure(data=charts)

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
    fig.write_html(buffer, include_plotlyjs='cdn', config={'displayModeBar': False})
    fig_html = buffer.getvalue()
    return utils.html_to_vdom(fig_html)

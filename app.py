# SWEAR WORDS IN MOVIES MOVIES
# Michal Kollar, April 2020

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import os
from random import randint
import flask

words = ['slut_movavg', 'shit_movavg', 'nigger_movavg', 'fuck_movavg', 'faggot_movavg', 'dick_movavg', 'cunt_movavg', 'bitch_movavg', 'bastard_movavg', 'asshole_movavg']
colors = ['#ffe119', '#ee0000', '#f58231', '#336699', '#000075', '#9a6324', '#911eb4', '#008080', '#808080', '#808000', '#ffffff','#800000', '#aaffc3', '#000000', '#ffd8b1', '#fabebe', '#bcf60c', '#f032e6','#46f0f0', '#3cb44b', '#e6beff', '#fffac8', ]

df = pd.read_csv('data_aggs.csv')
df = df[['year', 'asshole_movavg', 'bastard_movavg', 'bitch_movavg', 'cunt_movavg', 'dick_movavg', 'faggot_movavg', 'fuck_movavg', 'nigger_movavg', 'shit_movavg', 'slut_movavg']]
df = df.melt(id_vars=["year"], var_name="word", value_name="count")

x = pd.DatetimeIndex(df['year']).year

fig = go.Figure()

for j, k in zip(words, colors):
    fig.add_trace(go.Scatter(
        x=x,
        y=df.loc[df['word'] == j]['count'],
        name=j.replace("_movavg",""),
        marker=go.scatter.Marker(
            color=k,
        ),
        # opacity=1,
        fillcolor=k,
        mode='lines',
        line=dict(width=0.5, color=k, shape='spline'),
        stackgroup='one',
        # groupnorm='percent'# sets the normalization for the sum of the stackgroup
    ))

fig.update_layout(
    showlegend=True,
    xaxis = {'type': 'date',
             'title': '',
             'titlefont': dict(family='sans-serif', size=12, color='#222'),
             'tickangle': -90,
             'ticksuffix': "  ",
             'nticks': 10,
             'showline': True,
             'linewidth': 0.1,
             'linecolor': '#ccc'
             },
    yaxis = {'title': 'Count per movie (avg.)',
             'titlefont': dict(family='sans-serif', size=12, color='#222'),
             'ticksuffix': "  ",
             'nticks': 5,
             'tick0': '50',
             'showspikes': True,
             'spikethickness': 0.5,
             'spikedash': 'solid',
             'showgrid': True,
             'gridcolor': '#fff',
             'gridwidth': 0.01,
             },
    margin = {'l': 50, 'b': 60, 't': 50, 'r': 10},
    legend = {'x': 0, 'y': 1, 'font': dict(family='sans-serif', size=10, color='#222')},#, 'title': dict(text=' WORD ', font=dict(size=15))},
    plot_bgcolor = "#fff",
    paper_bgcolor = "#fff",
    hovermode = 'closest',
    font = dict(
        family="Helvetica, sans-serif",
        size=10,
        color="#7f7f7f"
        )
    )
fig.show()

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
external_stylesheets = ['https://codepen.io/majkl65/pen/LYpVxEP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div([
    html.H1(children='● THE MOVIE VOCABULARY',
            className='header'),

    html.P(
        "Average count of bad words heard in movies.",
        className='subheader',
    ),
    dcc.Graph(
        id='fig_1',
        config={
            #'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ["zoom2d", "pan2d", "select2d", "lasso2d", "autoScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d", "orbitRotation", "tableRotation","resetGeo", "hoverClosestGeo", "sendDataToCloud", "hoverClosestGl2d", "hoverClosestPie", "toggleHover", "toggleSpikelines"]
            #'modeBarButtonsToRemove': ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d", "orbitRotation", "tableRotation", "zoomInGeo", "zoomOutGeo", "resetGeo", "hoverClosestGeo", "toImage", "sendDataToCloud", "hoverClosestGl2d", "hoverClosestPie", "toggleHover", "resetViews", "toggleSpikelines", "resetViewMapbox"]
        },
        figure=fig
    ),

    html.P(
        "data: yifysubtitles.com",
        className='dataheader',
    ),
    html.P(
        "trendspotting.site",
        className='brandheader',
    )
])

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
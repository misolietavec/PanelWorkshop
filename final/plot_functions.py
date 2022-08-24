# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import panel as pn
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %%
wkeys = ['clouds', 'rain', 'wind_speed', 'humidity', 'pressure', 'temp']
w_colors = dict(zip(wkeys,['green', 'darkblue', 'blue', 'magenta', 'darkgray', 'red']))
fig_height, fig_width = 250, 800


# %%
def plot_48h(wdata, val):
    df = wdata['hourly']
    fig = go.Figure()
    plot_function = go.Bar if val == 'rain' else go.Scatter
    fig.add_trace(plot_function(x=df.index, y=df[val], marker_color=w_colors[val], name=val))
    fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b")
    fig.update_layout(height=fig_height, width=fig_width, margin=dict(t=20, b=0, r=10, l=10), showlegend=False)
    return fig


# %%
def plot_8d(wdata, val):
    df = wdata["daily"]
    fig = go.Figure()
    plot_function = go.Bar if val == 'rain' else go.Scatter
    if val != "temp":
        fig.add_trace(plot_function(x=df.index, y=df[val], marker_color=w_colors[val], name=val))
    else:
        add_temp_traces(fig, df)
    fig.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b",
                     ticklabelmode="period")
    fig.update_layout(height=fig_height, width=fig_width, margin=dict(t=20, b=0, r=10, l=10), showlegend=False)
    return fig


# %%
def add_temp_traces(fig, wdata):
    xval = wdata.index
    fig.add_trace(go.Bar(x=xval, y=wdata['day'],
                  marker_color='green', name='day'))
    fig.add_trace(go.Bar(x=xval, y=wdata['night'],
                  marker_color='darkblue', name='night'))
    fig.add_trace(go.Bar(x=xval, y=wdata['max'],
                  marker_color='red', name='max'))
    fig.add_trace(go.Bar(x=xval, y=wdata['min'],
                  marker_color='blue', name='min'))
    # return fig


# %%
def plot_forecasts(wdata, period='hourly', values=["temp","rain"]):
    pass

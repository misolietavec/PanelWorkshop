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
import folium
from folium import plugins
import json
import os
import final.weather_functions as wf

# %%
wkeys = ['clouds', 'rain', 'wind_speed', 'humidity', 'pressure', 'temp']
w_colors = dict(zip(wkeys,['green', 'darkblue', 'blue', 'magenta', 'darkgray', 'red']))
fig_height, fig_width = 250, 800
dir_path = os.path.dirname(os.path.realpath(__file__))


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
def add_temp_traces(fig, wdata, **kwargs):
    xval = wdata.index
    fig.add_trace(go.Bar(x=xval, y=wdata['day'],
                  marker_color='green', name='day'),**kwargs)
    fig.add_trace(go.Bar(x=xval, y=wdata['night'],
                  marker_color='darkblue', name='night'),**kwargs)
    fig.add_trace(go.Bar(x=xval, y=wdata['max'],
                  marker_color='red', name='max'),**kwargs)
    fig.add_trace(go.Bar(x=xval, y=wdata['min'],
                  marker_color='blue', name='min'),**kwargs)


# %%
def plot_forecasts(wdata, period='hourly', values=["temp","rain"]):
    df = wdata[period]
    nplots = len(values) 
    fig = make_subplots(rows=nplots, cols=1, subplot_titles=values, vertical_spacing=0.09)

    xval = df.index
    for ind, val in enumerate(values):
        nrow = ind + 1
        if period == 'daily' and val == 'temp':
            add_temp_traces(fig, df, row=nrow, col=1)
        else:
            plot_function = go.Bar if val == 'rain' else go.Scatter
            fig.add_trace(plot_function(x=xval, y=df[val], marker_color=w_colors[val],
                                        name=val), row=nrow, col=1)
        if period == 'hourly':
            fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b", row=nrow, col=1)
        else:   # daily
            fig.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b",
                             ticklabelmode="period", row=nrow, col=1)
    fig.update_layout(height=nplots * fig_height, width=fig_width, margin=dict(t=20, b=0, r=10, l=10), showlegend=False)
    return fig    


# %%
Stanice = wf.Stations_SK

def slovakia_map():
    map_slovakia = folium.Map(location=[48.7, 19.6], zoom_start=8)
    
    with open(f"{dir_path}/data/slovakia.json", "r") as file:
        geo_data = json.load(file)

    style_fcn =  lambda x : {'fillColor': '#228B2255', 'color': '#228B22'}    
    folium.GeoJson(geo_data, name="slovakia", style_function=style_fcn).add_to(map_slovakia)

    polohy, popy = [], []
    for station in Stanice:
        lat, lon = Stanice[station]
        poptext = f"{station}"
        polohy.append([lat, lon])
        popy.append(poptext)
    
    plugins.MarkerCluster(polohy, popups=popy).add_to(map_slovakia)
    return map_slovakia


# %%
def choosen_onmap(station):
    map = slovakia_map()
    folium.CircleMarker(location=Stanice[station], radius=15, color='red',
                        fill_color='red', fill=True).add_to(map)
    return map

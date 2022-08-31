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

# import for map functions
import folium
from folium import plugins

import final.weather_functions as wf

# %%
w_colors = {'clouds': 'green', 'rain': 'darkblue', 'wind_speed': 'blue', 
            'humidity': 'magenta', 'pressure': 'darkgray', 'temp': 'red'}
fig_height, fig_width = 250, 800
Stations = wf.Stations_SK


# %%
def plot_48h(wdata, val):
    df = wdata['hourly']
    fig = go.Figure()
    plot_function = go.Bar if val == 'rain' else go.Scatter  # this is different from 01_Plotting Weather
    fig.add_trace(plot_function(x=df.index, y=df[val], marker_color=w_colors[val], name=val))
    fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e.%b")
    fig.update_layout(height=fig_height, width=fig_width)   # plot width and height
    return fig


# %%
temp = {"day": "green", "night": "darkblue", "max": "red", "min": "blue"}

# as in 01_Plotting Weather, but only adds traces to existing Figure fig, which we make with plot_8d
def add_temp_traces(fig, daily, **kwargs):   # **kwargs - variable number of named arguments
    xval = daily.index
    for val in temp:
        fig.add_trace(go.Bar(x=xval, y=daily[val], marker_color=temp[val], name=val), **kwargs)


# %%
def plot_8d(wdata, val):
    df = wdata["daily"]
    fig = go.Figure()
    plot_function = go.Bar if val == 'rain' else go.Scatter
    if val != "temp":
        fig.add_trace(plot_function(x=df.index, y=df[val], marker_color=w_colors[val], name=val))
    else:
        add_temp_traces(fig, df)  # add traces for temperatures throughout the day
    fig.update_xaxes(dtick=60*60*1000*24, tickformat="%e.%b",
                     ticklabelmode="period")
    fig.update_layout(height=fig_height, width=fig_width, showlegend=False)
    return fig


# %%
# general function, mentioned in 01_Plotting_Weather

def plot_forecasts(wdata, period='hourly', values=["temp","rain"]):
    df = wdata[period]
    num_plots = len(values) 
    fig = make_subplots(rows=num_plots, cols=1, subplot_titles=values)

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
            fig.update_xaxes(tickformat="%e.%b", ticklabelmode="period", row=nrow, col=1)
    fig.update_layout(height=num_plots * fig_height, width=fig_width, showlegend=False)
    return fig    


# %%
# Mapping functions added

def slovakia_map():
    map_SK = folium.Map(location=[48.7, 19.6], zoom_start=8)
    loc, pops = [], []
    for name in Stations:
        location = Stations[name]
        poptext = f"{name}"
        loc.append(location)
        pops.append(poptext)

    plugins.MarkerCluster(locations=loc, popups=pops).add_to(map_SK)    
    return map_SK


# %%
def choosen_onmap(station):
    map = slovakia_map()
    folium.CircleMarker(location=Stations[station], radius=15, color='red',
                         fill_color='red', fill=True).add_to(map)
    return map

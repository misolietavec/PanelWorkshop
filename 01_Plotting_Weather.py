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
import plotly.graph_objects as go          # figure and plots
from plotly.subplots import make_subplots  # we will use several plots "in column"

# our weatherdata
from final.weather_functions import StaNames, Stations_SK, one_call, get_weather

# %%
station = "Oravská Lesná"
wdict = one_call(station)   # actual one call API call, use sparsely :-)

# %%
wdata = get_weather(wdict)  # dictionary with current, hourly, daily weatherdata 

# %%
# wdata["daily"][:10]

# %%
# budu funkcie plot_48h(wdata), plot_temp_8d(dtemp), plot_8d(wdata), plot_forecasts(wdata, values); dtemp je wdata['daily']['temp']
# values je zoznam meteovelicin, import len plot_48h, plot_8d, plot_forecasts 

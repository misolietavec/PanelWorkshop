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
# all graphics will be tested on the data for one meteostation 
station = "Oravská Lesná"
wdict = one_call(station)   # actual one call API call, use sparsely :-)

# %%
wdata = get_weather(wdict)  # dictionary with current, hourly, daily weatherdata 

# %%
# wdata["hourly"][:10]
# wdata["daily"]

# %%
# vo final/plot_functions budu implementovane plot_48h(wdata, val), plot_temp_8d(wdaily), plot_8d(wdata, val), plot_forecasts(wdata, values)
# wdaily je wdata['daily'], values je zoznam meteovelicin, value je jedna velicina, import len plot_48h, plot_8d, plot_forecasts 

# %%
from final.plot_functions import plot_48h, plot_8d, plot_forecasts

# %%
figtemp = plot_forecasts(wdata, period="daily",values=["rain","temp","wind_speed"])
figtemp

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
import folium
from folium import plugins

from final.weather_functions import Stations_SK


# %%
def slovakia_map():
    map_SK = folium.Map(location=[48.7, 19.6], zoom_start=8)
    loc, pops = [], []
    for name in Stations_SK:
        location = Stations_SK[name]
        poptext = f"{name}"
        loc.append(location)
        pops.append(poptext)

    plugins.MarkerCluster(locations=loc, popups=pops).add_to(map_SK)    
    return map_SK


# %%
def choosen_onmap(station):
    map = slovakia_map()
    folium.CircleMarker(location=Stations_SK[station], radius=15, color='red',
                         fill_color='red', fill=True).add_to(map)
    return map

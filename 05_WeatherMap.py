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

# %% [markdown]
# #### V tomto notebooku pridáme zobrazenie meteostaníc na mape, s vyznačenou vybranou stanicou.
# #### Na to použijeme modul `folium` (iná možnosť - `ipyleaflet`), oba sú založené na [JS knižnici Leaflet](https://leafletjs.com/).

# %%
# meteostations with geographic coordinates
from final.weather_functions import Stations_SK

# imports for folium
import folium
from folium import plugins

# %%
# making map with folium: location is (lat, lon), zoom_start - initial map zoom
# map_SK = folium.Map(location=[48.7, 19.6], zoom_start=8)
# map_SK

# %%
# making "clear" map and adding markers at locations of stations
# Stations_SK
map_SK = folium.Map(location=[48.7, 19.6], zoom_start=8)
for name in Stations_SK:
    # map_SK.add_child(folium.Marker(location=Stations_SK[name])) # simplest, but ?
    map_SK.add_child(folium.CircleMarker(location=Stations_SK[name],))
                                         # radius=6, tooltip=name, color="green", fill_color="blue"))
# map_SK

# %% [markdown]
# #### Stanice tvoria v niektorých miestach zhluky (clusters). Bolo by pekné, keby pri menšom zväčšení nebolo vidno jednotlivé stanice a po kliknutí na "cluster" by sa to pekne rozbalilo. 
# #### Nato máme vo `folium.plugins` funkciu `MarkerCluster`.

# %%
# clear map, without markers
map_SK = folium.Map(location=[48.7, 19.6], zoom_start=8)

# make list of locations and corresponding popups
loc, pops = [], []
for name in Stations_SK:
    location = Stations_SK[name]
    poptext = f"{name}"
    loc.append(location)
    pops.append(poptext)
    
plugins.MarkerCluster(locations=loc, popups=pops).add_to(map_SK);
# map_SK

# %% [markdown]
# #### Máme dosť znalostí, aby sme pochopili dve jednoduché mapové funkcie [v notebooku working/map_functions](working/map_functions.ipynb).
# #### Tie funkcie, `slovakia_map` a `choosen_onmap` sú pridané do `final/plot_functions` a odtiaľ ich budeme používať v [konečnej verzii aplikácie](working/weatherapp_map.ipynb).

# %%

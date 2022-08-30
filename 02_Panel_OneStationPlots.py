# %%
import panel as pn
from final.weather_functions import get_weather, StaNames
from final.plot_functions import plot_forecasts, plot_8d

# Displaying Panel objects in the notebook requires the panel extension to be loaded
pn.extension()

# %%
select_station = pn.widgets.Select(name="Choose a station", 
                                  options=StaNames,
                                  value="Bratislava", 
                                  width=500, 
                                  height=50)

# %%
select_station

# %%
select_station.value

# %%
select_station.value = "Košice"

# %%
station_name = pn.widgets.TextInput(name="Chosen station", disabled=True)
station_name

# %% [markdown]
# Na zoskupenie viacerých widgetov do 1 spoločného widgetu je možné použiť **Row** alebo **Column**.
# - Row poukladá widgety za sebou do riadku
# - Column ich poukladá pod seba do stĺpca.

# %%
pn.Row(select_station, station_name)

# %%
pn.Column(select_station, station_name)


# %% [markdown]
# Na "oživenie" widgetu použijeme dekorátor **pn.depends**  
# Parameter bude názov widgetu, ktorý chceme sledovať.  
# Funkcia musí mať rovnaký počet parametrov ako dekorátor! (názov parametru funkcie nemusí byť rovnaký ako názov widgetu)  
# Ako argument sa do funkcie pošle hodnota - **value** sledovaného widgetu

# %%
@pn.depends(select_station)
def update_station_name(select_station):
    station_name.value = select_station


# %%
col = pn.Column(select_station, station_name, update_station_name)
col

# %% [markdown]
# Na zobrazenie zoskupených widgetov môžeme použiť atribút **objects**

# %%
print(col.objects)
print("Druhý objekt", col.objects[1])

# %% [markdown]
# ### Zobrazovanie grafov

# %%
# ukazat najprv bez extension, aby sa vypisala chyba a nefungovali grafy
pn.extension('plotly')


# %%
@pn.depends(select_station)
def view_hourly_temp(select_station):
    data = get_weather(select_station)
    fig = plot_forecasts(data, 'hourly', values=['temp'])
    return fig


# %%
pn.Column(select_station, view_hourly_temp)


# %%
@pn.depends(select_station)
def view_hourly_trh(select_station):
    data = get_weather(select_station)
    fig = plot_forecasts(data, 'hourly', values=['temp', 'rain', 'humidity'])
    return fig


# %%
pn.Column(select_station, view_hourly_trh)

# %%

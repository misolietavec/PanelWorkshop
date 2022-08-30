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
# our weatherdata
from final.weather_functions import StaNames, get_weather

# %%
# all graphics will be tested on the data for one meteostation, choose from StaNames
station = "Oravská Lesná"
wdata = get_weather(station)   # dictionary with current, hourly, daily weatherdata

# %%
# to neatly display all data in cell, not only last row - Jupyter is the true child of IPython notebook :-)
from IPython.display import display
if False:
    display(wdata["current"])
    display(wdata["hourly"][:6])
    display(wdata["daily"])

# %% [markdown]
# ### Dáta sú tu, nakoniec :) Na ich znázorňovanie použijeme modul `plotly` (v `panel` aplikáciach možno použiť veľa iných grafických modulov, napr. `bokeh, holoviews, matplotlib, vega-lite,`...). V `plotly` sa ľahko sa pracuje s časovou osou, čo budeme potrebovať.

# %%
# only needed imports from using plotly
import plotly.graph_objects as go          # figure and plots
from plotly.subplots import make_subplots  # we will use several plots "in column"

# %%
# minimal example - display temperature or another meteodata forecast for next 48 hours
df = wdata["hourly"]    # pd.DataFrame with hourly meteodata; no need to import pandas in this NB
# always we have the values of independent variable x (type datetime.datetime) and the dependent variable, y
val = "temp" # can change
# print(df[val].index[:10], df[val].values[:10], sep="\n\n")
xval = df[val].index
yval = df[val]
if False:  # set to True for graphics
    fig = go.Figure()    # empty graphics "window" with default parameters
    temp_graph = go.Scatter(x=xval, y=yval)
    fig.add_trace(temp_graph)
    # beautifying the plot - ticks every 3 hours, format: hour, \n short name of month, day of month
    fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e. %b")  # time in milliseconds; for formatting, remember strftime? 
    # we get tooltips and tools "for free", try it
    display(fig)   

# %%
# # go.layout.XAxis?
# overwhelming number of options - RTFM https://plotly.com/python/reference/layout/xaxis/ :)
# we want ticks every 3 hours, this is the dtick property, tickformat is how to display them - see strftime

# %% [markdown]
# ### Stačí dať dohromady, čo sme si vyskúšali a máme funkciu `plot_48h` pre vykreslenie teploty, ale aj iných veličín v hodinovej predpovedi.

# %%
# what walues we have for plotting in hourly forecast?
print(list(df.columns))


# %%
def plot_48h(wdata, val):
    "display forecast from next 48 hours"
    df = wdata["hourly"]
    if not val in df.columns:
        raise ValueError("No such observation.")
    xval, yval = df[val].index, df[val]
    fig = go.Figure()
    graph = go.Scatter(x=xval, y=yval)
    fig.add_trace(graph)
    fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e. %b")
    return fig


# %%
# plot_48h(wdata, "zrazky")
# plot_48h(wdata, "clouds")   # try "rain", ...

# %% [markdown]
# ### Denná predpoveď (`daily`) sa líši časovým rozsahom a tým, že nie je len jedna teplota (`temp`), ale niekoľko (`max, min, day, night`, ...).

# %%
# let us try to plot same "daily" value, e. g. clouds; similarly to hourly example above
df = wdata["daily"]    # pd.DataFrame with daily meteodata; no need to import pandas in this NB
val = "clouds"   # change for day, rain, ...
xval = df[val].index
yval = df[val]
if False:      # set to True for graphics
    fig = go.Figure()    # empty graphics "window" with default parameters
    plot_function = go.Bar # change for go.Bar
    val_graph = plot_function(x=xval, y=yval,)  # marker_color = "MidnightBlue")
    fig.add_trace(val_graph)
    # ticklabels are not at the center of days, midday
    fig.update_xaxes(tickformat="%e. %b", ticklabelmode="period") 
    display(fig)


# %% [markdown]
# ### Teraz môžeme funkciu `plot_8d` vytvoriť metódou `Copy - Paste` z funkcie `plot_48h`, zmeníme len formátovanie časovej osi.

# %%
def plot_8d(wdata, val):
    "display forecast from next 8 days"
    df = wdata["daily"]
    if not val in df.columns:
        raise ValueError("No such observation.")
    xval, yval = df[val].index, df[val]   
    fig = go.Figure()
    graph = go.Scatter(x=xval, y=yval)
    fig.add_trace(graph)
    fig.update_xaxes(tickformat="%e. %b")  # dtick are OK, but the format we changed
    return fig


# %%
# plot_8d(wdata, "facina")
# plot_8d(wdata, "max")

# %% [markdown]
# ### Chceli by sme mať všetky údaje o teplote (`day, night, max, min`) v jednom grafe. 
# ### Nie je to ťažké, použijeme pre každú hodnotu funkciu `fig.add_trace(...)`.

# %%
# dictionary of temperature keys and corresponding colors we choose for them
temp = {"day": "green", "night": "darkblue", "max": "red", "min": "blue"}

def plot_dailytemps(wdata):
    # Copy-Paste from plot_8d, small changes
    df = wdata["daily"] 
    fig = go.Figure()
    for val in temp:
        xval, yval = df[val].index, df[val]
        val_graph = go.Bar(x=xval, y=yval, marker_color=temp[val], name=val)  # try go.Bar
        fig.add_trace(val_graph)
    fig.update_xaxes(tickformat="%e. %b")
    return fig


# %%
# plot_dailytemps(wdata)

# %% [markdown]
# ### Nakoniec, chceli by sme zobraziť niekoľko grafov pre rôzne veličiny pod sebou (podobne, ako je to na SHMU). 
# ### To sa dá, ak namiesto `Figure` použijeme `make_subplots` (vráti viac podgrafov v jednom "okne", usporiadaných v "gride", počet riadkov je `rows`, počet stĺpcov `cols`).

# %%
## let us plot hourly values for temperature and humidity
df = wdata["hourly"]
values = ["temp", "humidity"] # can change
num_plots = len(values)
fig = make_subplots(rows=num_plots, cols=1, subplot_titles=values) # our grid has num_plots rows and one column
act_row = 1   # actual row
for val in values:
    xval = df[val].index
    yval = df[val]
    val_graph = go.Scatter(x=xval, y=yval)
    fig.add_trace(val_graph, row=act_row, col=1)
    fig.update_xaxes(dtick=60*60*1000*3, tickformat="%H\n%e. %b")
    act_row += 1 
fig.update_layout(height=num_plots * 250, width=1000, showlegend=False) 
display(fig)

# %% [markdown]
# ### Iste sme si všimli, že podstatná časť kódu sa v horeuvedených funkciách opakuje. To nie je dobre.
# ### Môžeme vytvoriť jedinú funkciu `plot_forecasts(wdata, period, values)`, ktorá zahrnie všetko, čo sme doteraz urobili. 
# ### Pozrieme si to v notebooku v adresári `working` [nazvanom `plot_functions`](working/plot_functions.ipynb) 

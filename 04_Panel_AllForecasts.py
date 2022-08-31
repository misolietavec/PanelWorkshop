# %%
import panel as pn
from final.weather_functions import get_weather, wkeys, StaNames
from final.plot_functions import plot_forecasts

pn.extension('plotly')

# %% [markdown]
# #### Požičané z notebooku 03_Panel_ChooseMeteodata

# %%
observ_choice = pn.widgets.CheckBoxGroup(options=wkeys, value=['temp', 'clouds'], width=200)

def set_observ(*events):  
    for event in events:
        if event.type == "changed" and len(event.new) > 3:
            observ_choice.value = event.old
            
observ_watcher = observ_choice.param.watch(set_observ, ['value'], onlychanged=True)

# %%
station_choice = pn.widgets.Select(name="Select a station", options=StaNames, width=200)

@pn.depends(station_choice, observ_choice)
def view_hourly(station_choice, observ_choice):
    data = get_weather(station_choice)
    fig = plot_forecasts(data, 'hourly', values=observ_choice)
    return fig


options = pn.Column(station_choice, observ_choice)
pn.Row(options, view_hourly)


# %% [markdown]
# #### Teraz by sme chceli zobraziť merania na nasledujúci týždeň
# #### Vďaka plot_forecasts to ľahko hravo vyriešiť

# %%
@pn.depends(station_choice, observ_choice)
def view_daily(station_choice, observ_choice):
    data = get_weather(station_choice)
    fig = plot_forecasts(data, 'daily', values=observ_choice)
    return fig


# %%
# we will use the same widgets for choosing station & observations
pn.Row(options, view_daily)

# %% [markdown]
# #### Keďže zdieľame widgety pre hodinové aj denné zobrazenia, tak ak zmeníme napr. denné merania, zmenia sa aj hodinové, a naopak

# %% [markdown]
# #### Ale ako ich teraz spojiť dokopy?
# #### Na to nám pomôže`Tabs`

# %%
# we define each tab with a tuple (tab name, widget to display)
# we can also define a with only a widget - panel gives it a name (but it is ugly)

tabs = pn.Tabs(
    ("Hourly", view_hourly),
    ("Daily", view_daily),
    # pn.Row(pn.pane.Markdown("# Simple example of an 'ugly' tab name")),
    dynamic=True,  # can prevent bugs (and headaches)
    tabs_location='above'  # options: 'left', 'right', 'above'
)

tabs


# %% [markdown]
# #### A ešte aby sme nezabudli na aktuálne počasie

# %%
@pn.depends(station_choice)
def view_current(station_choice):
    df = get_weather(station_choice)['current']  # we want only the current weather
    float_format_function = lambda s: '%.1f' %s  # or f"{x:.1}"
    return pn.pane.DataFrame(df, justify='center', width=240, float_format=float_format_function)


# %%
widgets = pn.Column(options, view_current)
widgets

# %% [markdown]
# #### A nakoniec to spojiť dokopy

# %%
app = pn.Row(widgets, tabs)
app

# %%

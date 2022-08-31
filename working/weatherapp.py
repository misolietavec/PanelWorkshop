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
import panel.widgets as pnw

from final.weather_functions import get_weather, StaNames
from final.plot_functions import plot_forecasts

pn.extension('plotly')

# %%
observations = {"Teplota": "temp", "Tlak": "pressure", "Oblaky": "clouds", 
                "Vietor": "wind", "Zrážky": "rain", "Vlhkosť": "humidity"}

MAX_SELECTED_VALUES = 3

# %%
station_choice = pnw.Select(options=list(StaNames), value="Bratislava")
observ_choice = pnw.CheckBoxGroup(options=observations, value=["temp","rain"])


# %%
def set_observ(*events):
    for event in events:
        if event.type == "changed" and len(event.new) > MAX_SELECTED_VALUES:
            observ_choice.value = event.old
            
observ_watcher = observ_choice.param.watch(set_observ, ['value'], onlychanged=True) 


# %%
@pn.depends(station_choice)
def view_current(station_choice):
    float_fmt = lambda s: '%.1f' %s
    df = get_weather(station_choice)['current']
    return pn.pane.DataFrame(df, justify='center', width=240, float_format=float_fmt)


# %%
@pn.depends(station_choice, observ_choice)
def view_hourly(station_choice, observ_choice):
    fig = plot_forecasts(get_weather(station_choice), 'hourly', values=observ_choice)
    return fig


# %%
@pn.depends(station_choice, observ_choice)
def view_daily(station_choice, observ_choice):
    fig = plot_forecasts(get_weather(station_choice), 'daily', values=observ_choice)
    return fig


# %%
@pn.depends(station_choice)
def view_map(station_choice):
    return pn.pane.plot.Folium(choosen_onmap(station_choice), width=1000, height=600)


# %%
observe_row = pn.Row(observ_choice, width=250, align='center')
restriction = pn.pane.Markdown("<b>Najviac tri veličiny</b>")
widgets = pn.Column(pn.Row(station_choice, width=250), pn.Row(restriction), observe_row, pn.Row(view_current), align='center')
apptitle = pn.pane.Markdown("## Počasie na Slovensku<br/>", align='center')

# %%
tabs = pn.Tabs(("Predpoveď 48 hod.", pn.Column(view_hourly)), 
               ("Predpoveď 8 dní", pn.Column(view_daily)),
               dynamic=True, tabs_location="above")

# %%
weather_info = pn.Column(apptitle,tabs)
app = pn.Column(pn.Row(widgets, 
                pn.Spacer(width=20),
                weather_info)).servable(title="Počasie na Slovensku")
app

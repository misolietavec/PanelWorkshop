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
import pickle
import pandas as pd
import requests
from os import environ
import os
from datetime import datetime

# %%
dir_path = os.path.dirname(os.path.realpath(__file__))
picklefile = open(f"{dir_path}/data/stanice.pickle",'rb')
Stations_SK = pickle.load(picklefile)
# for convenience, alphabetically sorted names of meteostations
StaNames = sorted(list(Stations_SK.keys()))

owkey =  environ["OWM_APIKEY"]


# %%
def one_call(city):
    if not city in StaNames:
        raise ValueError("No such meteostation.")
    lat, lon = Stations_SK[city]
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,allerts&appid={owkey}&units=metric"
    one_call_result = requests.get(URL)
    return one_call_result.json()


# %%
wkeys = ['clouds', 'rain', 'wind_speed', 'humidity', 'pressure', 'temp']


# %%
def wkeys_dict(wdict):
    time = datetime.fromtimestamp(wdict['dt'])
    return time, {key: wdict.get(key, 0) for key in wkeys}


# %%
def get_current(wdict):
    time, wd = wkeys_dict(wdict["current"])
    wd['time'] = time
    return pd.DataFrame.from_dict(wd, orient='index',columns=['Aktuálne počasie'])


# %%
def get_hourly(wdict):
    wh = {}
    for rec in wdict['hourly']:
        time, wd = wkeys_dict(rec)
        if type(wd['rain']) is dict:
            wd['rain'] = wd['rain']['1h']
        wh[time] = wd
    return pd.DataFrame.from_dict(wh, orient='index', columns=wkeys)


# %%
tempkeys = ['day', 'night', 'min', 'max', 'eve', 'morn']

def get_daily(wdict):
    wday = {}
    for rec in wdict['daily']:
        time, wd = wkeys_dict(rec)
        for tk in tempkeys:
            wd[tk] = wd['temp'][tk]    
        wday[time] = wd
    return pd.DataFrame.from_dict(wday, orient='index', columns=wkeys[:-1] + tempkeys)    


# %%
def get_weather(wdict):
    return {"current": get_current(wdict), "hourly": get_hourly(wdict), "daily": get_daily(wdict)}

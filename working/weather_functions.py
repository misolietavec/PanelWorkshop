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
from datetime import datetime

# %%
picklefile = open("data/stanice.pickle",'rb')
Stations_SK = pickle.load(picklefile)
# for convenience, alphabetically sorted names of meteostations
# StaNames = sorted(list(Stations_SK.keys()))

owkey =  environ["OWM_APIKEY"]


# %%
# using our knowledge from Data NB
def one_call(city):
    "returns dict of current weather, hourly, daily forecast"
    lat, lon = Stations_SK[city]
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,allerts&appid={owkey}&units=metric"
    one_call_result = requests.get(URL)
    wdict = one_call_result.json()
    return wdict


# %%
wdict = one_call("Prievidza")
# print(f"daily item: {wdict['daily'][0]}", f"hourly item: {wdict['hourly'][0]}", f"current: {wdict['current']}", sep='\n\n')

# %%
# we will be interested only in values for certain keys:
wkeys = ['clouds', 'rain', 'wind_speed', 'humidity', 'pressure', 'temp']


# %%
def wkeys_dict(wrec):
    "helper function, returns datetime from weather record and also the dictionary only for keys in wkeys"
    wd = {}
    for key in wkeys:
        wd[key] = wrec[key] # if wrec.get(key) else 0  # beware "rain" key, can be missing
    time = datetime.fromtimestamp(wrec['dt'])    
    return time, wd    


# %%
# wkeys_dict(wdict['current'])
# wkeys_dict(wdict['hourly'][0])   # first item for hourly forecast
# wkeys_dict(wdict['daily'][0])    # first item for daily forecast

# %%
def get_current(wdict):
    "returns pandas DataFrame with current weather - use pd.DataFrame.from_dict :-)"
    time, currdict = wkeys_dict(wdict['current'])
    # currdict['time'] = time # add time to currdict
    curr_DF = pd.DataFrame.from_dict(currdict, orient='index', columns=['Actual weather'])
    return curr_DF


# %%
# get_current(wdict)

# %%
def get_hourly(wdict):
    "returns pd.DataFrame with hourly forecast - 48 rows with wkeys as column names; iterate through items in wdict['hourly']"
    wh = {}
    for rec in wdict['hourly']:
        time, wd = wkeys_dict(rec)
        # if type(wd['rain']) is dict:
        #     wd['rain'] = wd['rain']['1h']
        wh[time] = wd

    return pd.DataFrame.from_dict(wh, orient='index', columns=wkeys) # times as keys


# %%
# get_hourly(wdict)

# %%
tempkeys = ['day', 'night', 'min', 'max', 'eve', 'morn']  # temperatures at day duration

def get_daily(wdict):
    "returns pd.DataFrame with daily forecast - 8 rows with wkeys + tempkeys; iterate through items in wdict['daily']"
    wday = {}
    for rec in wdict['daily']:
        time, wd = wkeys_dict(rec)
        # add keys from tempkeys    
        # for key in tempkeys:
        #     wd[key] = wd['temp'][key]
        wday[time] = wd
    return pd.DataFrame.from_dict(wday, orient='index', columns=wkeys) # [:-1] + tempkeys)


# %%
# get_daily(wdict)

# %%
def get_weather(wdict):
    return {"current": get_current(wdict), "hourly": get_hourly(wdict), "daily": get_daily(wdict)}

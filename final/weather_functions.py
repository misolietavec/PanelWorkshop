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
from sqlitedict import SqliteDict
from time import time

# %%
dir_path = os.path.dirname(os.path.realpath(__file__))
picklefile = open(f"{dir_path}/data/stanice.pickle",'rb')
Stations_SK = pickle.load(picklefile)
StaNames = sorted(list(Stations_SK.keys()))

owkey =  environ["OWM_APIKEY"]
db = SqliteDict(f"{dir_path}/one_call.sqlite", autocommit=True, tablename='weather')


# %%
def one_call(city, autoupdate=60*60*4):
    if not city in StaNames:
        raise ValueError("No such meteostation.")
    no_update = False
    if city in db.keys():
        ref_time, one_call_result = db[city]
        no_update =  (int(time()) - ref_time < autoupdate)  
    if not no_update:
        lat, lon = Stations_SK[city]
        URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,allerts&appid={owkey}&units=metric"
        one_call_result = requests.get(URL).json()
        ref_time = one_call_result["current"]["dt"]
        db[city] = (ref_time, one_call_result)
    return one_call_result


# %%
wkeys = ['clouds', 'rain', 'wind_speed', 'humidity', 'pressure', 'temp']
sk_wkeys = {"Teplota": "temp", "Tlak": "pressure", "Oblaky": "clouds", 
            "Vietor": "wind", "Zrážky": "rain", "Vlhkosť": "humidity"}


# %%
def wkeys_dict(wdict):
    time = datetime.fromtimestamp(wdict['dt'])
    return time, {key: wdict.get(key, 0) for key in wkeys}


# %%
def get_current(wdict):
    time, wd = wkeys_dict(wdict["current"])
    wd['time'] = time.strftime("%-d.%b %H:%M")
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
def get_weather(city):
    wdict = one_call(city)
    return {"current": get_current(wdict), "hourly": get_hourly(wdict), "daily": get_daily(wdict)}

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
import requests
from os import environ

from sqlitedict import SqliteDict
from time import time

# %%
picklefile = open("data/stanice.pickle",'rb')
Stations_SK = pickle.load(picklefile)
StaNames = sorted(list(Stations_SK.keys()))

owkey =  environ["OWM_APIKEY"]

# we will use sqlite database for caching
# but working with it as with ordinary Python dictionary
db = SqliteDict("one_call.sqlite", autocommit=True, tablename='weather')


# %%
# see for which stations data are cached and no actual call of One Call API is made
# list(db.keys())

# %%
# function for getting meteodata

def one_call(city, timeout=60*60*4, debug=False):      # timeout is in seconds, i.e. 4 hours
    if not city in StaNames:
        raise ValueError("No such meteostation.")
    no_update = False                        # let us assume the worst, we need actual API call
    if city in db.keys():
        ref_time, one_call_result = db[city] # if cached, get result - time and meteodata  
        no_update =  (int(time()) - ref_time < timeout)
        # no_udate is True -> we have valid results, in the 4 hour interval before current time
    if not no_update:     # no_update is False, results are older than 4 hours or not in db 
        lat, lon = Stations_SK[city]
        URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,allerts&appid={owkey}&units=metric"
        one_call_result = requests.get(URL).json()
        ref_time = one_call_result["current"]["dt"]
        db[city] = (ref_time, one_call_result)   # write the atual time and meteodata to db for the future...
        if debug:
            print("One Call API call made")
    return one_call_result


# %%
list(db.keys())  

# %%
# experiment with meteostations from StaNames
result = one_call('Košice', debug=True)

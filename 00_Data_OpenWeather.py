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
#
# ## Prvotné sú dáta. Ak ich máme, môžeme rozmýšľať, ako ich čo najnázornejšie interpretovať.
# Dáta môžu byť v rôznych formátoch, my budeme používať ```pickle, json, csv```. Importujeme moduly na ich načítanie.
#


# %%
# this is code cell, execute with Ctrl-Enter
import pickle
import json
import pandas as pd  # for reading csv files as pandas DataFrame

# %%
# we begin with reading file with meteostations in Slovakia
picklefile = open('final/data/stanice.pickle','rb')   # relative path; why binary?
Stations_SK = pickle.load(picklefile)
# for convenience, alphabetically sorted names of meteostations
StaNames = sorted(list(Stations_SK.keys()))

# %%
# look at data, guess what is what
# Stations_SK

# %% [markdown]
# ### Neskôr budeme často využívať dátovy typ  ```pandas DataFrame```. Dnes poobede sa môžete zúčastniť workshopu **Pandas watching movies**, takže sa nebudeme venovať objasneniu tohto typu. Stačí vedieť, že:
# ### **pd.DataFrame je tabuľka s pomenovanými stĺpcami a  indexovým stĺpcom, (obsahujúcim pomenovania riadkov - pozorovaní).**

# %%
# making pd.Dataframe from Stations_SK dictionary, lat is zem. šírka, lon is zem. dĺžka, show this beautiful table
Stations_DF = pd.DataFrame.from_dict(Stations_SK, orient='index', columns=['lat','lon'])
# Stations_DF

# %% [markdown]
# <b>Bolo by pekné, keby sme pre tie slovenské stanice mali nejaké dáta o počasí (aktuálne, predpovede, historické dáta).</b>
# ### Meteodáta získame zo stránky [OpenWeatherMap](https://openweathermap.org/api) s využitím ```One Call API 3.0```.

# %% [markdown]
# ### Pripomeňme si názvy staníc zo ```StaNames```
# ```python
# ['Banská Bystrica', 'Banská Štiavnica', 'Bardejov', 'Bašovce', 'Bojnice', 'Boľkovce', 'Bratislava', 'Brezno', 'Brezno - Zadné Halny', 'Brezová pod Bradlom', 'Bytča', 'Bánovce nad Bebravou', 'Chlmec', 'Detva', 'Dobšiná', 'Dolný Kubín', 'Dubnica nad Váhom', 'Dunajská Streda', 'Dúbravka', 'Fiľakovo', 'Galanta', 'Gbely', 'Gelnica', 'Gemerská Hôrka', 'Giraltovce', 'Handlová', 'Hlohovec', 'Hnúšťa', 'Hody', 'Holíč', 'Hontianska Vrbica', 'Hriňová', 'Humenné', 'Hurbanovo', 'Hybe', 'Ilava', 'Istebník', 'Kamenica nad Cirochou', 'Kežmarok', 'Kolárovo', 'Komárno', 'Kotešová', 'Košice', 'Kremnica', 'Krompachy', 'Krupina', 'Kysucké Nové Mesto', 'Leopoldov', 'Levice', 'Levoča', 'Likavka', 'Lipany', 'Liptovský Hrádok', 'Liptovský Mikuláš', 'Lovce', 'Lučenec', 'Malacky', 'Martin', 'Medzev', 'Medzilaborce', 'Michalovce', 'Modra nad Cirochou', 'Moldava nad Bodvou', 'Most pri Bratislave', 'Myjava', 'Nemšová', 'Nitra', 'Nižné Nemecké', 'Nová Baňa', 'Nová Dubnica', 'Nová Lesná', 'Nováky', 'Nové Mesto nad Váhom', 'Nové Zámky', 'Námestovo', 'Oravská Lesná', 'Palúdzka', 'Partizánske', 'Pezinok', 'Piešťany', 'Podolínec', 'Poltár', 'Poprad', 'Považská Bystrica', 'Poľný Kesov', 'Prešov', 'Pribylina', 'Prievidza', 'Púchov', 'Rajec', 'Revúca', 'Rimavská Sobota', 'Rožňava', 'Rožňové Mitice', 'Ružindol', 'Ružomberok', 'Sabinov', 'Senec', 'Senica', 'Sečovce', 'Skalica', 'Sládkovičovo', 'Smolenice', 'Snina', 'Sobrance', 'Sološnica', 'Spišská Belá', 'Spišská Nová Ves', 'Spišské Podhradie', 'Stará Turá', 'Stará Ľubovňa', 'Stropkov', 'Stráňany', 'Strážske', 'Stupava', 'Svidník', 'Svit', 'Svodín', 'Svätý Jur', 'Tisovec', 'Tlmače', 'Topoľčany', 'Trebišov', 'Trenčianske Teplice', 'Trenčín', 'Trnava', 'Trstená', 'Turzovka', 'Turčianske Teplice', 'Tvrdošín', 'Veľký Bysterec', 'Veľký Meder', 'Vinné', 'Vranov nad Topľou', 'Vrbové', 'Vráble', 'Vrútky', 'Vysoké Tatry', 'Vysoké Tatry - Nový Smokovec', 'Vyšné Ružbachy', 'Zlaté Moravce', 'Zliechov', 'Zvolen', 'Závodie', 'Čachtice', 'Čadca', 'Čierna nad Tisou', 'Ľubica', 'Šahy', 'Šamorín', 'Šaľa', 'Štrba', 'Štúrovo', 'Šurany', 'Žarnovica', 'Ždiar', 'Želiezovce', 'Žiar nad Hronom', 'Žilina']
# ```

# %%
# show One Call API call, response, account, apikey
# we will make direct call with requests module

import requests
from os import environ

owkey =  environ["OWM_APIKEY"]    # necessary for call

lat, lon = Stations_SK['Oravská Lesná']   # you can take your own place, but paste only from StaNames at above cell
URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,allerts&appid={owkey}&units=metric"

one_call_result = requests.get(URL)  # response object with many attributes and methods
wdict = one_call_result.json()       # you will see, this is what we need

# %%
# let's see, what we get
# print(f"keys:\n{wdict.keys()}", f"daily record:\n{wdict['daily'][0]}", 
#       f"hourly record:\n{wdict['hourly'][0]}", f"current weather:\n{wdict['current']}", sep='\n\n')

# %% [markdown]
# ### Vidíme neobvyklé hodnoty časových údajov pre kľúče ```"dt", "sunrise"```, ... Čas sa tu meria ako  ```timestamp```, čo je počet sekúnd od počiatku UNIX-ovej éry (1. jan. 1970). 
# ### Ukážeme, ako túto hodnotu konvertovať na čitateľnejší formát (dátum a čas).

# %%
from datetime import datetime

first_hourly = wdict['hourly'][0]
first_date = datetime.fromtimestamp(first_hourly['dt'])
# for string reprezentation we will use strftime method; we want the date and time in this format: 9. 9. 2022, 10:30
# nice help for formatting codes see at https://www.strfti.me/
#
# print (f"default: {first_date}", f'our format: {first_date.strftime("%-d. %-m. %Y, %-H:%M")}',sep='\n')

# %% [markdown]
# ### Inšpirovaní všetkým horeuvideným, editujeme v adresári ```working``` [pripravený notebook s názvom weather_functions](working/weather_functions.ipynb) a budeme ho postupne napĺňať funkciami pre získanie aktuálneho počasia, predpovedí na 48 hodin a 8 dní.

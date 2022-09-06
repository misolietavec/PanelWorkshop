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
# #### Naša konečná aplikácia sa trochu líši od tej, [na ktorú sme vás odkazovali](http://feelmath.eu:2022/Pocasie).
# #### Nebudeme sa zaoberať poslovenčením nadpisov, to pozorný čitateľ zvládne aj sám. :-)
# #### Ale prečo pri aktuálnom počasí niekedy nie je úplne aktuálny časový údaj?
# #### Aby sme sa vyhli prekročeniu bezplatného denného limitu 1000 volaní, zapisujeme údaje zo všetkých volaní v `sqlite` databáze. Podrobnosti pozrieme v notebooku [final/caching_weatherapi.](final/caching_weatherapi.ipynb) 

# %% [markdown]
# ### Nakoniec, odkazy na materiály, ktoré sme pre vás pripravili:
# - zdrojové súbory pre všetky notebooky sú na githube [https://github.com/misolietavec/PanelWorkshop](https://github.com/misolietavec/PanelWorkshop)
# - videá s tým, čo sme tu robili (pre tých, čo nemohli, alebo si to chcú osviežiť) sú na 
#   1. [https://feelmath.eu/PanelWorkshop/WeatherData.mp4](https://feelmath.eu/PanelWorkshop/WeatherData.mp4)
#   2. [https://feelmath.eu/PanelWorkshop/PlotWeather.mp4](https://feelmath.eu/PanelWorkshop/PlotWeather.mp4)
#   3. [https://feelmath.eu/PanelWorkshop/OneStation.mp4](https://feelmath.eu/PanelWorkshop/OneStation.mp4)
#   4. [https://feelmath.eu/PanelWorkshop/ChooseMeteoData.mp4](https://feelmath.eu/PanelWorkshop/ChooseMeteoData.mp4)

# %% [markdown]
# # <font size=7><center>Howgh.</center></font>

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:26:00 2023

@author: ildeniz
"""
#%%
import os

# Setting the working directory
path = os.getcwd()

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
os.chdir(dir_path)

#%%
%%time #Wall time: 5min 26s
from mal_scrapper import seasonal_anime_info
import pandas as pd

first = 2010
last = 2022

years = list(range(first, last+1))
seasons = ['winter', 'spring', 'summer', 'fall'] 

animes = pd.DataFrame()
for year in years:
    for season in seasons:
        animes_season = seasonal_anime_info(year, season)
        animes = pd.concat([animes, animes_season], ignore_index=True)
        
animes.to_csv('Data/animes_2010_-_2022.csv', index=False)

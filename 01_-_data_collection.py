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
'''
Scraping animes between 2010 winter season and 2022 fall season.
'''
from mal_scraper import seasonal_anime_info
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
#%%
%%time
'''
Scraping user data for the given animes.
Hint: Scraping info of 100 animes lasted 1h 33min 6s
                      1000 animes lasted 16h 13min 19s
For safe of time efficinecy I recommend to scrap data through multiple cloud slutions 
in smaller fractions (for example 100 titles at a time) and combine them later.
'''
from mal_scraper import user_updates_info
import pandas as pd

animes_2010_2022 = pd.read_csv('Data/info_animes_2010_-_2022.csv')
animes = animes_2010_2022['Mal_Id'] #[:100]

user_info = pd.DataFrame()
animes_scrapped = 0
for anime in animes:
    anime_scrapped = user_updates_info(anime)
    user_info = pd.concat([user_info, anime_scrapped], ignore_index=True)
    animes_scrapped += 1

user_info.to_csv('Data/users_info_animes_combined.csv', index=False)
#%%
# merging multiple files
import pandas as pd
import glob
import os

file_name = 'multi_combo_'

# identify the files to be merged
joined_files = os.path.join("Data/", f"{file_name}*.csv")
  
# list of joined files
joined_list = glob.glob(joined_files)
  
# merging the files
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)

    

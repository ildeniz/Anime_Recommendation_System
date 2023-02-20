# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:22:13 2023

@author: ildeniz
"""
#%%
import os

# Setting the working directory
path = os.getcwd()

real_path = os.path.realpath('__file__')
dir_path = os.path.dirname(real_path)
os.chdir(dir_path)
#%%
import pandas as pd
#from jikanpy import Jikan
import requests
import time # jikan API has a 'rate limiting': 30 requests per minute and 2 requests per second

def seasonal_anime_info(year, season):
    '''
    Returns anime infos* of the specified season
    year (int) – Year to get anime of.
    season (str) – Season to get anime of. Possible values are 'winter', 'spring', 'summer', and 'fall'.
    
    *Title (str), MyAnimeList ID (int), Score (float), Scored_by (int), Members (int), Favourited_by (int), Genre (comma seperated str)
    '''
    initial_response = requests.get("https://api.jikan.moe/v4/seasons/" + str(year) + "/" + season)
    season_info = initial_response.json()
    
    titles = []
    mal_ids = []
    scores = []
    scored_by = []
    members = []
    genres = []
    favorites = []
    ani_year = []
    ani_season = []
    
    for page in range(season_info['pagination']['last_visible_page']):    
        response = requests.get("https://api.jikan.moe/v4/seasons/" + str(year) + "/" + season + "?page=" + str(page+1))
        season_info = response.json()
        
        time.sleep(1)
        
        for i in range(len(season_info['data'])):
            if season_info['data'][i]['score'] == None: # excluding animes without score
                pass
            else:    
                titles.append(season_info['data'][i]['title'])
                mal_ids.append(season_info['data'][i]['mal_id'])
                scores.append(season_info['data'][i]['score'])
                scored_by.append(season_info['data'][i]['scored_by'])
                members.append(season_info['data'][i]['members'])
                favorites.append(season_info['data'][i]['favorites'])
                combined_genres=[]
                for genre in range(len(season_info['data'][i]['genres'])):
                    combined_genres.append(season_info['data'][i]['genres'][genre]['name'])
                combined_genres = ','.join(combined_genres)
                genres.append(combined_genres)
                ani_year.append(season_info['data'][i]['year'])
                ani_season.append(season_info['data'][i]['season'])
        
        time.sleep(1)
        
    anim_data = {'Title': titles, 
                 'Mal_Id': mal_ids, 
                 'Rating': scores,
                 'Scored_By':scored_by,
                 'Members':members,
                 'Favourited_by': favorites,
                 'Genre': genres,
                 'Year': ani_year,
                 'Season': ani_season,
                }
    df = pd.DataFrame(data = anim_data)
    return df


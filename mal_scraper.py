# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:22:13 2023

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
import pandas as pd
import requests
import time # Jikan API has a 'rate limiting': 30 requests per minute and 2 requests per second
            # hence we need the execution 'sleep'

def seasonal_anime_info(year: int, season: str):
    '''
    Returns anime infos* of the specified season
    year (int) – Year to get anime of.
    season (str) – Season to get anime of. Possible values are 'winter', 'spring', 'summer', and 'fall'.
    
    *Title (str), MyAnimeList ID (int), Score (float), Scored_by (int), Members (int), Favourited_by (int), Genre (comma seperated str)
    '''
    
    initial_url =  f"https://api.jikan.moe/v4/seasons/{year}/{season}"
    initial_response = requests.get(initial_url)
    season_info = initial_response.json()
    
    items = []
    for page in range(season_info['pagination']['last_visible_page']):    
        url = f'{initial_url}?page={page+1}'
        response = requests.get(url)
        season_info = response.json()
        
        time.sleep(1)
        
        for i in range(len(season_info['data'])):
            if not season_info['data'][i]['score']: # excluding animes without score
                continue
            combined_genres=[]
            for genre in range(len(season_info['data'][i]['genres'])):
                combined_genres.append(season_info['data'][i]['genres'][genre]['name'])
            combined_genres = ','.join(combined_genres)
            
            new_item = {'Title': season_info['data'][i]['title'], 
                        'Mal_Id': season_info['data'][i]['mal_id'], 
                        'Rating': season_info['data'][i]['score'],
                        'Scored_By': season_info['data'][i]['scored_by'],
                        'Members': season_info['data'][i]['members'],
                        'Favourited_by': season_info['data'][i]['favorites'],
                        'Genre': combined_genres,
                        'Year': season_info['data'][i]['year'],
                        'Season': season_info['data'][i]['season'],
                       }
            items.append(new_item)
        
        time.sleep(1)
        
    df = pd.DataFrame(items)
    return df

def user_updates_info(anime_id: int, pages = 5):
    '''
    Returns users' info, who rated a particular anime, from the 'userupdate' page of the anime
    anime_id (int)
    pages (int) = 5
    
    'User_name' (str), 'Score' (int), 'Status' (str), 'Anime_Id (int)'
    '''

    initial_url =  f"https://api.jikan.moe/v4/anime/{anime_id}/userupdates"
    items = []
    
    for page in range(5):    
        url = f'{initial_url}?page={page+1}'
        response = requests.get(url)
        time.sleep(1)
        user_info = response.json()
        
        if 'error' in user_info: # avoid "408 Request Timeout" error
            continue
        for i in range(len(user_info['data'])):
            if not user_info['data'][i]['score']: # exclude non-voting users
                continue
            new_item = {'User_Name': user_info['data'][i]['user']['username'], 
                        'Score': user_info['data'][i]['score'],
                        'Status': user_info['data'][i]['status'],
                        'Anime_Id': anime_id,
                       }
            items.append(new_item)
            
    
    # remove duplicated rows
    df = pd.DataFrame(items)
    duplicated_row = df[df.duplicated(keep = 'first')]
    df.drop(index = duplicated_row.index, axis = 0, inplace = True)
        
    return df
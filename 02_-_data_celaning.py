# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:12:27 2023

@author: ildeniz
"""
#%% Setting up the working directory
import os

path = os.getcwd()

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
os.chdir(dir_path)
#%% Loading packages and data sets
import pandas as pd

animes_info = pd.read_csv('Data/animes_2010_-_2022.csv')
users_info = pd.read_csv('Data/users_info_animes_combined.csv')

#%% Checking whether all the animes are scrapped
# number of animes scrapped successfully
len(users_info.Anime_Id.unique())

# 11 animes are missing, detect the mossong animes
missing_animes = pd.DataFrame(set(animes_info.Mal_Id.unique()) - set(users_info.Anime_Id.unique()))
missing_animes
# animes with ids 32353, 34566, 50250, 49515, 50060, 48365, 50607, 8336, 50418, 23539, and 42295 are missing.
# it turns out that it is not possible to scrap the data of these productions.

#%% Detecting fake and bot accounts
# Fake users and bot/troll accounts are well known issues for online calaogues with ranking system
# It is better to detect and drop them from the data set before they contaminate the results
# Search for users who scored more than 20 animes and have score mean of '1' and '10'
num_animes = users_info.User_Name.value_counts().sort_index()
mean_scores = users_info.groupby('User_Name').Score.mean().sort_index()

df = pd.merge(left=num_animes, right=mean_scores, left_index=True, right_index=True)
df.sort_values(by='User_Name', ascending=False)

suspicious_users = df.loc[(df.User_Name > 20)&
                          ((df.Score == 1)|
                           (df.Score == 10))
                          ].sort_values(by='User_Name', ascending=False).index.tolist()

# ZueiraBraba             531    1.0
# I_Am_A_God              319    1.0
# GoodM0rning             314    1.0
# PraiseGod               311    1.0
# NewWorkoutPlan          230    1.0
# kaidrok                 100   10.0
# JustKaede_               87    1.0
# PerfectGod               78   10.0
# Deabu123                 60   10.0
# GiwangSastri             60   10.0
# alialialh5678            58   10.0
# kingjoffery9             53    1.0
# 1a55bt60za               50   10.0
# Hi_no_Hana               50   10.0

users_info_cleaned = users_info.query(f"User_Name != {suspicious_users}")

#%% Detecting 'Dropped' animes with scores between 7-10 and drop them from the data set
users_info_cleaned.Status.value_counts()

users_info_cleaned = users_info_cleaned.query("Status != 'Plan to Watch'")

# Detecting 'Dropped' animes with high scores
users_info_cleaned.Status.value_counts()

index_names = users_info_cleaned.loc[(users_info_cleaned.Status == 'Dropped')&
                                     (users_info_cleaned.Score >= 7)].index

users_info_cleaned.drop(index_names, inplace = True)
users_info_cleaned.Status.value_counts()

#%% Detecting the missing values
animes_info.info()
animes_info.isnull().sum()
# 'Genre' has missing values

animes_info.loc[animes_info.Genre.isnull()== True]

# It is better to label them as 'NonClassified'
animes_info.fillna('NonClassified', inplace=True)
animes_info.Genre.value_counts() #'Genre' has to be one-hot-encoded


users_info_cleaned.info()
users_info_cleaned.isnull().sum()
# 'Status' has missing values

# Looks like the missing values are due to corrupted user data, we better drop them from the data set.
users_info_cleaned.loc[users_info_cleaned.Status.isnull()== True]

users_info_cleaned.dropna(inplace=True)

users_info_cleaned.User_Name.value_counts().ne(1).sum()
users_info_cleaned.User_Name.value_counts()
users_info_cleaned.User_Name.unique()

#%% One-hot-encoding 'Genre's

animes_info_cleaned = pd.concat([animes_info.drop('Genre', axis=1), animes_info['Genre'].str.get_dummies(sep=",")], axis=1)

#%% Combining anime and user infos
users_info_cleaned['Mal_Id'] = users_info_cleaned['Anime_Id']
users_info_cleaned = users_info_cleaned.drop('Anime_Id', axis=1)

mal_dataset = pd.merge(users_info_cleaned,
                       animes_info_cleaned, 
                       on = "Mal_Id", 
                       how = "inner"
                       )

mal_dataset.to_csv('Data/mal_data.csv', index=False)




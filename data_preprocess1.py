#script to preprocess full data
import ast
import pandas as pd
import numpy as np
import re, time
import warnings, requests
from bs4 import BeautifulSoup
import utils
from dateutil.parser import parse
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)


def get_month(x):
  '''helper function to get release month'''
    try:
        return month_order[x.month-1]
    except:
        return np.nan
    
def get_day(x):
  '''helper function to get release day'''
    try:
        return day_order[x.weekday()]
    except:
        return np.nan

#get metadata from the Movie Database
df_full = pd.read_csv('data/movies_metadata.csv')

#fix some errors in data
df_full.budget[df_full.title=='Dope'] = 7000000
df_full.budget[df_full.title=='The Letters'] = 20000000

#here is a dict to quickly get ids from movie titles and vice versa
title2id = {k:v for k, v in zip(df_full['title'], df_full['id'])}
id2title = {k:v for k, v in zip(df_full['id'], df_full['title'])}

# get openening weekend info scraped from the Box Office Mojo
weekend_df = pd.read_csv('data/opening_weekend_data.csv')
weekend_df.columns = ['title', 'weekend_rev', 'weekend_rev_mean']
weekend_df['num_theaters']= np.round(weekend_df['weekend_rev']/weekend_df['weekend_rev_mean'])

#merge data sets
df = df_full.set_index('title').join(weekend_df.set_index('title'), how='inner').drop_duplicates().reset_index()

#preprocess data
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df = df[df.budget >1000000]

df.drop(['adult', 'id', 'imdb_id', 'belongs_to_collection', 'homepage', 'original_title', 
               'poster_path', 'popularity', 'vote_average', 'vote_count', 'spoken_languages',
               'status', 'video', 'revenue', 'tagline', 'overview'], axis=1, inplace=True)

df['success'] = df['weekend_rev'] / df['budget']
df = df[~df['success'].isnull()].copy()
df = df[~df['release_date'].isnull()].copy()
df['release_date'] = df['release_date'].apply(parse)


month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

df['day'] = df['release_date'].apply(get_day)
df['month'] = df['release_date'].apply(get_month)
df['holiday'] = df['month'].apply(
    lambda x: 'Yes' if x in ['Jan', 'Feb', 'May', 'July', 'Sep', 'Oct', 'Nov', 'Dec'] else 'No'))
df['year'] = df['release_date'].apply(lambda x: x.year)

df['log_budget']= df['budget'].apply(np.log10)
df['log_weekend_rev']= df['weekend_rev'].apply(np.log10)
df['log_weekend_rev_mean']= df['weekend_rev_mean'].apply(np.log10)

#only include movies released in or after 2010
df2010 = df[df['year']>=2010].copy()
df2010.drop_duplicates(inplace=True)

#drop error-prone movies
df2010 = df2010[df2010.title != 'Camille Claudel 1915']
df2010 = df2010[df2010.title != 'Instructions Not Included']
df2010 = df2010[df2010.title != 'In Order of Disappearance trailer']
df2010.reset_index(inplace=True, drop=True)

#use ast.literal_eval to convert stringified dicts into usable dicts
df2010['production_countries'] = df2010['production_countries'].fillna('[]').apply(ast.literal_eval)
df2010['production_countries'] = df2010['production_countries'].apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

#only keep movies if the US is in the list of production countries 
index_US = []
for i in list(df2010.index):
    if 'United States of America' in df2010['production_countries'].iloc[i]:
        index_US.append(i)        
df2010US = df2010.iloc[index_US].reset_index(drop=True)

# get youtube trailer data
youtube_trailers = pd.read_csv('data/youtube_trailers.csv')

#merge with df2010US
df_merged = df2010US.merge(youtube_trailers, how='inner')

df_merged['production_companies'] = df_merged['production_companies'].fillna('[]').apply(ast.literal_eval)
df_merged['production_companies'] = df_merged['production_companies'].apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])


df_merged['genres'] = df_merged['genres'].fillna('[]').apply(ast.literal_eval).apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
df_merged.to_csv('data/data_since_2010.csv')

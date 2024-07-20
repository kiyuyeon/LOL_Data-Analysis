import matplotlib.pyplot as plt
import seaborn as sns # heatmap
import pydotplus
import os
import pandas as pd
import numpy as np
import pickle
import numpy as np
import json
import re 
import time
import ast
from pandas.io.json import _normalize
import json

# API 호출을 위해 requests 모듈을 사용
import requests



api_key = 'RGAPI-3576e661-885e-49d1-9fcc-59a8b7db1a5d'


grandmaster = 'https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=' + api_key
r = requests.get(grandmaster)#그마데이터 호출
league_df = pd.DataFrame(r.json())

league_df.reset_index(inplace=True)#수집한 그마데이터 index정리
league_entries_df = pd.DataFrame(dict(league_df['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df = pd.concat([league_df, league_entries_df], axis=1) #열끼리 결합

league_df = league_df.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df.info()


for i in range(len(league_df)):
    try:
        sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
        r = requests.get(sohwan)
        
        while r.status_code == 429:
            time.sleep(5)
            sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
            r = requests.get(sohwan)
            
        account_id = r.json()['accountId']
        league_df.iloc[i, -1] = account_id
    
    except:
        pass

for i in range(len(league_df)):
    try:
        sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
        r = requests.get(sohwan)
        
        while r.status_code == 429:
            time.sleep(5)
            sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
            r = requests.get(sohwan)
            
        account_id = r.json()['accountId']
        league_df.iloc[i, -1] = account_id
    
    except:
        pass


#13시즌의 데이터만을 이용할 것이며 league_df3 => 기존에 수집한 account_id가 있는 league_df
match_info_df = pd.DataFrame()
season = str(13)
for i in range(len(league_df)):
    try:
        match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df['account_id'].iloc[i]  +'?season=' + season + '&api_key=' + api_key
        r = requests.get(match0)
        
        while r.status_code == 429:
            time.sleep(5)
            match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df['account_id'].iloc[i]  +'?season=' + season + '&api_key=' + api_key
            r = requests.get(match0)
            
        match_info_df = pd.concat([match_info_df, pd.DataFrame(r.json()['matches'])])
    
    except:
        print(i)
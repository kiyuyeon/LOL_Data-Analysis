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

# API 에서 공통적으로 사용하는 텍스트를 선언
apiDefault = {
    'region': 'https://kr.api.riotgames.com',  # 한국서버를 대상으로 호출
    'key': 'RGAPI-3576e661-885e-49d1-9fcc-59a8b7db1a5d',  # API KEY 
}


api_key = 'RGAPI-3576e661-885e-49d1-9fcc-59a8b7db1a5d'

#챌린저 그랜드마스터 마스터 데이터 불러오기
grandmaster = F"{apiDefault['region']}/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key={apiDefault['key']}"
r = requests.get(grandmaster)#그마데이터 호출
league_df = pd.DataFrame(r.json())

league_df.reset_index(inplace=True)#수집한 그마데이터 index정리
league_entries_df = pd.DataFrame(dict(league_df['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df = pd.concat([league_df, league_entries_df], axis=1) #열끼리 결합

league_df = league_df.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df.info()
league_df.to_csv('그마데이터.csv',index=False,encoding = 'cp949')#중간저장

# 마스터 데이터
master = F"{apiDefault['region']}/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={apiDefault['key']}"
r = requests.get(master)#마스터데이터 호출
league_df_master = pd.DataFrame(r.json())

league_df_master.reset_index(inplace=True)#수집한 그마데이터 index정리
league_entries_df = pd.DataFrame(dict(league_df_master['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df_master = pd.concat([league_df_master, league_entries_df], axis=1) #열끼리 결합


league_df_master = league_df_master.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df_master.info()
league_df_master.to_csv('마스터데이터.csv',index=False,encoding = 'cp949')#중간저장

# 챌린저 데이터
challenger = F"{apiDefault['region']}/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={apiDefault['key']}"
r = requests.get(challenger)#챌린저데이터 호출
league_df_challenger = pd.DataFrame(r.json())

league_df_challenger.reset_index(inplace=True)#수집한 그마데이터 index정리
league_entries_df = pd.DataFrame(dict(league_df_challenger['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df_challenger = pd.concat([league_df_challenger, league_entries_df], axis=1) #열끼리 결합

league_df_challenger = league_df_challenger.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df_challenger.info()
league_df_challenger.to_csv('챌린저데이터.csv',index=False,encoding = 'cp949')#중간저장

tier_url = F"{apiDefault['region']}/lol/league/v4/positions/by-summoner/?api_key={apiDefault['key']}"
r2  = requests.get(tier_url)
r2.json()


challenger = F"{apiDefault['region']}/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={apiDefault['key']}"


for i in range(len(league_df_challenger)):
    try:
        # sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
        print('마스터 데이터 시작 ',i)
        master = F"{apiDefault['region']}/lol/summoner/v4/summoners/by-name/?api_key={apiDefault['key']}"+ league_df_challenger['summonerName'].iloc[i]

        r = requests.get(master)
        
        while r.status_code == 429:
            print('code 429')
            time.sleep(5)
            master = F"{apiDefault['region']}/lol/summoner/v4/summoners/by-name/?api_key={apiDefault['key']}"+ league_df_challenger['summonerName'].iloc[i]
            r = requests.get(master)
            
        account_id = r.json()['accountId']
        league_df_challenger.iloc[i, -1] = account_id
    
    except:
        pass
print('마스터 데이터 끝')
#13시즌의 데이터만을 이용할 것이며 league_df_challenger => 기존에 수집한 account_id가 있는 league_df
match_info_df_challenger = pd.DataFrame()
season = str(13)
for i in range(len(league_df_challenger)):
    print('마스터 13시즌 데이터 시작')
    try:
        match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df_challenger['account_id'].iloc[i]  +'?season=' + season + '&api_key=' + api_key
        r = requests.get(match0)
        
        while r.status_code == 429:
            print('code 429')
            time.sleep(5)
            match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df_challenger['account_id'].iloc[i]  +'?season=' + season + '&api_key=' + api_key
            r = requests.get(match0)
            
        match_info_df_challenger = pd.concat([match_info_df_challenger, pd.DataFrame(r.json()['matches'])])
    
    except:
        print(i)
print('마스터 13시즌 데이터 끝')
for i in range(len(match_info_df_challenger)):    
    print('마스터 최근게임')
    api_url='https://kr.api.riotgames.com/lol/match/v4/matches/' + str(match_info_df_challenger['gameId'].iloc[i]) + '?api_key=' + api_key
    r = requests.get(api_url)

    if r.status_code == 200: # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
        pass

    elif r.status_code == 429:
        print('api cost full : infinite loop start')
        print('loop location : ',i)
        start_time = time.time()

        while True: # 429error가 끝날 때까지 무한 루프
            if r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(api_url)
                print(r.status_code)

            elif r.status_code == 200: #다시 response 200이면 loop escape
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                break

    elif r.status_code == 503: # 잠시 서비스를 이용하지 못하는 에러
        print('service available error')
        start_time = time.time()

        while True:
            if r.status_code == 503 or r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(api_url)
                print(r.status_code)

            elif r.status_code == 200: # 똑같이 response가 정상이면 loop escape
                print('total error wait time : ', time.time() - start_time)
                print('recovery api cost')
                break
    elif r.status_code == 403: # api갱신이 필요
        print('you need api renewal')
        print('break')
        break

    # 위의 예외처리 코드를 거쳐서 내려왔을 때 해당 코드가 실행될 수 있도록 작성
    mat = pd.DataFrame(list(r.json().values()), index=list(r.json().keys())).T
    match_fin = pd.concat([match_fin,mat])

    match_fin.to_csv('정리데이터.csv',index=False,encoding = 'cp949')#중간저장





# for i in range(len(league_df_master)):
#     try:
#         # sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
#         print('마스터 데이터 시작 ',i)
#         master = F"{apiDefault['region']}/lol/summoner/v4/summoners/by-name/?api_key={apiDefault['key']}"+ league_df_master['summonerName'].iloc[i]

#         r = requests.get(master)
        
#         while r.status_code == 429:
#             print('code 429')
#             time.sleep(5)
#             master = F"{apiDefault['region']}/lol/summoner/v4/summoners/by-name/?api_key={apiDefault['key']}"+ league_df_master['summonerName'].iloc[i]
#             r = requests.get(master)
            
#         account_id = r.json()['accountId']
#         league_df_master.iloc[i, -1] = account_id
    
#     except:
#         pass
# print('마스터 데이터 끝')
# #13시즌의 데이터만을 이용할 것이며 league_df_master => 기존에 수집한 account_id가 있는 league_df
# match_info_df_master = pd.DataFrame()
# season = str(13)
# for i in range(len(league_df_master)):
#     print('마스터 13시즌 데이터 시작')
#     try:
#         match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df_master['account_id'].iloc[i]  +'?season=' + season + '&api_key=' + api_key
#         r = requests.get(match0)
        
#         while r.status_code == 429:
#             print('code 429')
#             time.sleep(5)
#             match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df_master['account_id'].iloc[i]  +'?season=' + season + '&api_key=' + api_key
#             r = requests.get(match0)
            
#         match_info_df_master = pd.concat([match_info_df_master, pd.DataFrame(r.json()['matches'])])
    
#     except:
#         print(i)
# print('마스터 13시즌 데이터 끝')
# for i in range(len(match_info_df_master)):    
#     print('마스터 최근게임')
#     api_url='https://kr.api.riotgames.com/lol/match/v4/matches/' + str(match_info_df_master['gameId'].iloc[i]) + '?api_key=' + api_key
#     r = requests.get(api_url)

#     if r.status_code == 200: # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
#         pass

#     elif r.status_code == 429:
#         print('api cost full : infinite loop start')
#         print('loop location : ',i)
#         start_time = time.time()

#         while True: # 429error가 끝날 때까지 무한 루프
#             if r.status_code == 429:

#                 print('try 10 second wait time')
#                 time.sleep(10)

#                 r = requests.get(api_url)
#                 print(r.status_code)

#             elif r.status_code == 200: #다시 response 200이면 loop escape
#                 print('total wait time : ', time.time() - start_time)
#                 print('recovery api cost')
#                 break

#     elif r.status_code == 503: # 잠시 서비스를 이용하지 못하는 에러
#         print('service available error')
#         start_time = time.time()

#         while True:
#             if r.status_code == 503 or r.status_code == 429:

#                 print('try 10 second wait time')
#                 time.sleep(10)

#                 r = requests.get(api_url)
#                 print(r.status_code)

#             elif r.status_code == 200: # 똑같이 response가 정상이면 loop escape
#                 print('total error wait time : ', time.time() - start_time)
#                 print('recovery api cost')
#                 break
#     elif r.status_code == 403: # api갱신이 필요
#         print('you need api renewal')
#         print('break')
#         break

#     # 위의 예외처리 코드를 거쳐서 내려왔을 때 해당 코드가 실행될 수 있도록 작성
#     mat = pd.DataFrame(list(r.json().values()), index=list(r.json().keys())).T
#     match_fin = pd.concat([match_fin,mat])

# match_fin.to_csv('정리데이터.csv',index=False,encoding = 'cp949')#중간저장

# for i in range(len(league_df)):
#     try:
#         sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
#         r = requests.get(sohwan)
        
#         while r.status_code == 429:
#             time.sleep(5)
#             sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
#             r = requests.get(sohwan)
            
#         account_id = r.json()['accountId']
#         league_df.iloc[i, -1] = account_id
    
#     except:
#         pass

# for i in range(len(league_df_challenger)):
#     try:
#         sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
#         r = requests.get(sohwan)
        
#         while r.status_code == 429:
#             time.sleep(5)
#             sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[i] + '?api_key=' + api_key 
#             r = requests.get(sohwan)
            
#         account_id = r.json()['accountId']
#         league_df.iloc[i, -1] = account_id
    
#     except:
#         pass
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
    'summonerName': 'ecrrd',  # 닉네임
}

grandmaster = F"{apiDefault['region']}/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?page=1?api_key={apiDefault['key']}"
r = requests.get(grandmaster)#그마데이터 호출
league_df = pd.DataFrame(r.json())

league_df.reset_index(inplace=True)#수집한 그마데이터 index정리
league_entries_df = pd.DataFrame(dict(league_df['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df = pd.concat([league_df, league_entries_df], axis=1) #열끼리 결합

league_df = league_df.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df.info()
league_df.to_csv('그마데이터2.csv',index=False,encoding = 'cp949')#중간저장
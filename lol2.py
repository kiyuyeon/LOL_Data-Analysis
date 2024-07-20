import requests
from urllib import parse
import time
 
api_key = "RGAPI-3576e661-885e-49d1-9fcc-59a8b7db1a5d"
request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-3576e661-885e-49d1-9fcc-59a8b7db1a5d"
}

def check_my_team(*args):
    current_players = []
    for n in range(0, 4):
        name = args[n]
        print(name)
        encoded_name = parse.quote(name)
        current_players.append(encoded_name)
        summoner_account_id = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encoded_name, headers=request_headers).json()["accountId"]
        win = 0
        for n in range(0, 10):
            get_latest_match_id = requests.get("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id, headers=request_headers).json()["matches"][n]["gameId"]
            get_match_info = requests.get("https://kr.api.riotgames.com/lol/match/v4/matches/" + str(get_latest_match_id), headers=request_headers).json()
            for i in range(0, 10):
                if get_match_info["participantIdentities"][i]["player"]["summonerName"] == name:
                    if get_match_info["participants"][i]["stats"]["win"] == True:
                        win += 1
            time.sleep(1)
        print(win)
        time.sleep(2)
            
        latest_players = []
        for n in range(0, 10):
            get_latest_match_id = requests.get("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id, headers=request_headers).json()["matches"][0]["gameId"]
            get_match_info = requests.get("https://kr.api.riotgames.com/lol/match/v4/matches/" + str(get_latest_match_id), headers=request_headers).json()
            latest_players.append(get_match_info["participantIdentities"][n]["player"]["summonerName"])
            time.sleep(1)
        print(latest_players)
        if len(set(current_players) & set(latest_players)) > 1:
            print(set(current_players) & set(latest_players))
        else:
            print("듀오가 없습니다")
        time.sleep(2)
 
check_my_team("내 팀원1","내 팀원2","내 팀원3", "내 팀원4")
 
def check_members():
    print("시작")
    live_game = requests.get("https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/E1AfcxGWK9MaVl7tn6uMcdFNLEFKh3gx3cAEhrm4Wq0iDQ", headers=request_headers)
    live_game = live_game.json()
    current_players = []
    print("진행중")
    print(live_game)
    for n in range(0, 10):
        print("??")
        name = parse.quote(live_game["participants"][n]["summonerName"])
        print(name)
        current_players.append(name)
        summoner_account_id = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name, headers=request_headers).json()["accountId"]
        get_latest_match_id = requests.get("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id, headers=request_headers).json()["matches"][0]["gameId"]
        get_match_info = requests.get("https://kr.api.riotgames.com/lol/match/v4/matches/" + str(get_latest_match_id), headers=request_headers).json()
        latest_players = []
        for n in range(0, 10):
            latest_players.append(get_match_info["participantIdentities"][n]["player"]["summonerName"])
            if len(set(current_players) & set(latest_players)) > 1:
                print(set(current_players) & set(latest_players))
        time.sleep(2)
 
check_members()
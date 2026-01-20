import os

import requests
from dotenv import load_dotenv

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")
BASE_URL = "https://euw1.api.riotgames.com"


def get_puuid_by_riot_id(game_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["puuid"]


def get_match_ids(puuid, count=10):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_match(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

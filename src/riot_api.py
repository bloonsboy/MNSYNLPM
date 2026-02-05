"""Riot Games API."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "").strip().strip('"').strip("'")
DEFAULT_TIMEOUT = 10

API_KEY = os.getenv("RIOT_API_KEY", "").strip().strip('"').strip("'")
if not API_KEY:
    raise RuntimeError(
        "RIOT_API_KEY non défini. export RIOT_API_KEY=... ou ajoutez-le dans .env"
    )

# Riot API accepte maintenant X-Riot-Token comme header principal
HEADERS = {"X-Riot-Token": API_KEY, "Accept": "application/json"}


def get_puuid_by_riot_id(game_name: str, tag_line: str) -> str:
    """Return the PUUID for a Riot ID given the game name and tag line."""
    url = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    if response.status_code == 401:
        raise RuntimeError("401 Unauthorized — clé RIOT_API_KEY invalide ou expirée.")
    response.raise_for_status()
    return response.json()["puuid"]


def get_match_ids(puuid: str, count: int = 10) -> list:
    """Retrieve a list of match IDs for a given PUUID."""
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    if response.status_code == 401:
        raise RuntimeError("401 Unauthorized — clé RIOT_API_KEY invalide ou expirée.")
    response.raise_for_status()
    return response.json()


def get_match(match_id: str) -> dict:
    """Fetch match details for a given match ID."""
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    if response.status_code == 401:
        raise RuntimeError("401 Unauthorized — clé RIOT_API_KEY invalide ou expirée.")
    response.raise_for_status()
    return response.json()

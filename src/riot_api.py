"""Riot Games API."""

import os

from dotenv import load_dotenv
import requests

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "").strip().strip('"').strip("'")
DEFAULT_TIMEOUT = 10

API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": API_KEY}


def get_puuid_by_riot_id(game_name: str, tag_line: str) -> str:
    """Return the PUUID for a Riot ID given the game name and tag line."""
    url = (
        f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/"
        f"{game_name}/{tag_line}"
    )
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()["puuid"]


def get_match_ids(puuid: str, count: int = 10) -> list:
    """Retrieve a list of match IDs for a given PUUID."""
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_match(match_id: str) -> dict:
    """Fetch match details for a given match ID."""
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()

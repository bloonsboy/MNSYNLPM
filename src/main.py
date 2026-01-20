import json

from riot_api import (
    get_match,
    get_match_ids,
    get_puuid_by_riot_id,
    get_summoner_by_name,
)

MATCHES_TO_FETCH = [
    "",
]

if __name__ == "__main__":
    for match_id in MATCHES_TO_FETCH:
        match = get_match(match_id)
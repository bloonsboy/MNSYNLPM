import json

# Liste des IDs de parties à traiter
MATCH_IDS = [
    # Ajoutez ici les IDs de parties à analyser
    # Exemple : "EUW1_1234567890"
]

from riot_api import get_match

if __name__ == "__main__":
    for match_id in MATCH_IDS:
        print(f"Récupération des infos pour {match_id}...")
        match = get_match(match_id)
        # Récupérer le timestamp du match (en secondes)
        timestamp = (
            match["info"]["gameStartTimestamp"] // 1000
            if "gameStartTimestamp" in match["info"]
            else None
        )
        from datetime import datetime

        if timestamp:
            date_str = datetime.utcfromtimestamp(timestamp).strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
        else:
            date_str = match_id
        filename = f"match_{date_str}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(match, f, ensure_ascii=False, indent=2)
        print(f"Match sauvegardé dans {filename}")

import json
from datetime import datetime
from pathlib import Path

from src.constant import MATCH_IDS
from src.export_match import process_match
from src.riot_api import get_match

if __name__ == "__main__":
    for name, match_id in MATCH_IDS.items():
        try:
            match = get_match(match_id)
            data = process_match(match)
            timestamp = match["info"].get("gameStartTimestamp", 0) // 1000
            date_str = (
                datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d_%H-%M-%S")
                if timestamp
                else name
            )
            safe_name = name.replace(" ", "_")
            filename = f"{safe_name}_{date_str}.json"
            out_dir = Path("data")
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / filename
            if out_file.exists():
                print(f"{out_file} existe déjà, passage au suivant.")
                continue
            with out_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Match filtré sauvegardé dans {out_file}")
        except Exception as e:
            print(f"Erreur pour {name} ({match_id}): {e}. Passage au suivant.")

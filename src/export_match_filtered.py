import json
import os
from datetime import datetime

from dotenv import load_dotenv

from riot_api import get_match

# Chargement de la variable VIRGULE depuis le .env
load_dotenv()
VIRGULE = json.loads(os.getenv("VIRGULE", "[]"))

# Mapping championId -> championName (extrait partiel, à compléter selon besoin)
CHAMPION_ID_TO_NAME = {
    266: "Aatrox",
    103: "Ahri",
    84: "Akali",
    166: "Akshan",
    12: "Alistar",
    32: "Amumu",
    34: "Anivia",
    1: "Annie",
    523: "Aphelios",
    22: "Ashe",
    136: "AurelionSol",
    268: "Azir",
    432: "Bard",
    200: "Belveth",
    53: "Blitzcrank",
    63: "Brand",
    201: "Braum",
    51: "Caitlyn",
    164: "Camille",
    69: "Cassiopeia",
    31: "Chogath",
    42: "Corki",
    122: "Darius",
    131: "Diana",
    119: "Draven",
    36: "DrMundo",
    245: "Ekko",
    60: "Elise",
    28: "Evelynn",
    81: "Ezreal",
    9: "Fiddlesticks",
    114: "Fiora",
    105: "Fizz",
    3: "Galio",
    41: "Gangplank",
    86: "Garen",
    150: "Gnar",
    79: "Gragas",
    104: "Graves",
    887: "Gwen",
    120: "Hecarim",
    74: "Heimerdinger",
    420: "Illaoi",
    39: "Irelia",
    427: "Ivern",
    40: "Janna",
    59: "JarvanIV",
    24: "Jax",
    126: "Jayce",
    202: "Jhin",
    222: "Jinx",
    145: "Kaisa",
    429: "Kalista",
    43: "Karma",
    30: "Karthus",
    38: "Kassadin",
    55: "Katarina",
    10: "Kayle",
    141: "Kayn",
    85: "Kennen",
    121: "Khazix",
    203: "Kindred",
    240: "Kled",
    96: "KogMaw",
    7: "Leblanc",
    64: "LeeSin",
    89: "Leona",
    876: "Lillia",
    127: "Lissandra",
    236: "Lucian",
    117: "Lulu",
    99: "Lux",
    54: "Malphite",
    90: "Malzahar",
    57: "Maokai",
    11: "MasterYi",
    21: "MissFortune",
    62: "Wukong",
    82: "Mordekaiser",
    25: "Morgana",
    267: "Nami",
    75: "Nasus",
    111: "Nautilus",
    518: "Neeko",
    76: "Nidalee",
    56: "Nocturne",
    20: "Nunu",
    2: "Olaf",
    61: "Orianna",
    516: "Ornn",
    80: "Pantheon",
    78: "Poppy",
    555: "Pyke",
    246: "Qiyana",
    133: "Quinn",
    497: "Rakan",
    33: "Rammus",
    421: "RekSai",
    526: "Rell",
    888: "Renata",
    58: "Renekton",
    107: "Rengar",
    92: "Riven",
    68: "Rumble",
    13: "Ryze",
    360: "Samira",
    113: "Sejuani",
    235: "Senna",
    147: "Seraphine",
    875: "Sett",
    35: "Shaco",
    98: "Shen",
    102: "Shyvana",
    27: "Singed",
    14: "Sion",
    15: "Sivir",
    72: "Skarner",
    37: "Sona",
    16: "Soraka",
    50: "Swain",
    517: "Sylas",
    134: "Syndra",
    223: "TahmKench",
    163: "Taliyah",
    91: "Talon",
    44: "Taric",
    17: "Teemo",
    412: "Thresh",
    18: "Tristana",
    48: "Trundle",
    23: "Tryndamere",
    4: "TwistedFate",
    29: "Twitch",
    77: "Udyr",
    6: "Urgot",
    110: "Varus",
    67: "Vayne",
    45: "Veigar",
    161: "Velkoz",
    711: "Vex",
    254: "Vi",
    234: "Viego",
    112: "Viktor",
    8: "Vladimir",
    106: "Volibear",
    19: "Warwick",
    498: "Xayah",
    101: "Xerath",
    5: "XinZhao",
    157: "Yasuo",
    777: "Yone",
    83: "Yorick",
    350: "Yuumi",
    154: "Zac",
    238: "Zed",
    221: "Zeri",
    115: "Ziggs",
    26: "Zilean",
    142: "Zoe",
    143: "Zyra",
}

# Liste des IDs de parties à traiter
MATCH_IDS = [
   "EUW1_7689627079"
]


def extract_team_info(team, bans):
    return {
        "bans": [
            {
                "championId": b["championId"],
                "championName": CHAMPION_ID_TO_NAME.get(
                    b["championId"], str(b["championId"])
                ),
            }
            for b in bans
        ],
        "baron": team.get("objectives", {}).get("baron", {}).get("kills", 0),
        "champion": team.get("objectives", {}).get("champion", {}).get("kills", 0),
        "dragon": team.get("objectives", {}).get("dragon", {}).get("kills", 0),
        "horde": team.get("objectives", {}).get("horde", {}).get("kills", 0),
        "inhibitor": team.get("objectives", {}).get("inhibitor", {}).get("kills", 0),
        "riftHerald": team.get("objectives", {}).get("riftHerald", {}).get("kills", 0),
        "tower": team.get("objectives", {}).get("tower", {}).get("kills", 0),
        "win": team.get("win", False),
    }


def extract_player_info(p):
    return {
        "teamPosition": p.get("teamPosition"),
        "Champion": {
            "champExperience": p.get("champExperience"),
            "champLevel": p.get("champLevel"),
            "championName": p.get("championName"),
        },
        "Damage": {
            "damageDealtToBuildings": p.get("damageDealtToBuildings"),
            "damageDealtToEpicMonsters": p.get("damageDealtToEpicMonsters"),
            "magicDamageDealtToChampions": p.get("magicDamageDealtToChampions"),
            "magicDamageTaken": p.get("magicDamageTaken"),
            "physicalDamageDealtToChampions": p.get("physicalDamageDealtToChampions"),
            "physicalDamageTaken": p.get("physicalDamageTaken"),
            "totalDamageDealtToChampions": p.get("totalDamageDealtToChampions"),
            "totalDamageTaken": p.get("totalDamageTaken"),
            "trueDamageDealtToChampions": p.get("trueDamageDealtToChampions"),
        },
        "Ping": {
            "dangerPings": p.get("dangerPings"),
            "enemyMissingPings": p.get("enemyMissingPings"),
            "enemyVisionPings": p.get("enemyVisionPings"),
            "getBackPings": p.get("getBackPings"),
            "holdPings": p.get("holdPings"),
            "needVisionPings": p.get("needVisionPings"),
            "onMyWayPings": p.get("onMyWayPings"),
            "pushPings": p.get("pushPings"),
            "retreatPings": p.get("retreatPings"),
            "visionClearedPings": p.get("visionClearedPings"),
            "allInPings": p.get("allInPings"),
            "assistMePings": p.get("assistMePings"),
            "basicPings": p.get("basicPings"),
        },
        "KDA": {
            "deaths": p.get("deaths"),
            "kills": p.get("kills"),
            "pentaKills": p.get("pentaKills"),
            "largestMultiKill": p.get("largestMultiKill"),
            "quadraKills": p.get("quadraKills"),
            "assists": p.get("assists"),
        },
        "First": {
            "firstBloodKill": p.get("firstBloodKill"),
            "firstBloodAssist": p.get("firstBloodAssist"),
            "firstTowerKill": p.get("firstTowerKill"),
            "firstTowerAssist": p.get("firstTowerAssist"),
        },
        "Stat game": {
            "goldEarned": p.get("goldEarned"),
            "itemsPurchased": p.get("itemsPurchased"),
            "totalAllyJungleMinionsKilled": p.get("totalAllyJungleMinionsKilled"),
            "totalEnemyJungleMinionsKilled": p.get("totalEnemyJungleMinionsKilled"),
            "totalTimeSpentDead": p.get("totalTimeSpentDead"),
            "turretTakedowns": p.get("turretTakedowns"),
            "wardsPlaced": p.get("wardsPlaced"),
            "wardsKilled": p.get("wardsKilled"),
            "visionWardsBoughtInGame": p.get("visionWardsBoughtInGame"),
            "visionScore": p.get("visionScore"),
        },
        "Spell": {
            "spell1Casts": p.get("spell1Casts"),
            "spell2Casts": p.get("spell2Casts"),
            "spell3Casts": p.get("spell3Casts"),
            "spell4Casts": p.get("spell4Casts"),
            "summoner1Casts": p.get("summoner1Casts"),
            "summoner1Id": p.get("summoner1Id"),
            "summoner2Casts": p.get("summoner2Casts"),
            "summoner2Id": p.get("summoner2Id"),
        },
    }


def process_match(match):
    info = match["info"]
    out = {
        "game": {
            "gameDuration": info.get("gameDuration"),
            "gameCreation": info.get("gameCreation"),
            "gameEndTimestamp": info.get("gameEndTimestamp"),
            "gameMode": info.get("gameMode"),
            "gameStartTimestamp": info.get("gameStartTimestamp"),
        }
    }
    # Trouver l'équipe de VIRGULE (bleue = 0-4, rouge = 5-9)
    participants = info["participants"]
    team1_names = [p["riotIdGameName"] for p in participants[:5]]
    team2_names = [p["riotIdGameName"] for p in participants[5:]]
    virgule_is_blue = any(name in VIRGULE for name in team1_names)
    if virgule_is_blue:
        virgule_team = info["teams"][0]
        virgule_bans = virgule_team.get("bans", [])
        enemy_team = info["teams"][1]
        enemy_bans = enemy_team.get("bans", [])
        virgule_players = participants[:5]
        enemy_players = participants[5:]
    else:
        virgule_team = info["teams"][1]
        virgule_bans = virgule_team.get("bans", [])
        enemy_team = info["teams"][0]
        enemy_bans = enemy_team.get("bans", [])
        virgule_players = participants[5:]
        enemy_players = participants[:5]
    out["virgule"] = extract_team_info(virgule_team, virgule_bans)
    out["enemy"] = extract_team_info(enemy_team, enemy_bans)
    # Ajouter les joueurs (tous)
    for p in participants:
        out[p["riotIdGameName"]] = extract_player_info(p)
    return out


if __name__ == "__main__":
    for match_id in MATCH_IDS:
        print(f"Récupération des infos pour {match_id}...")
        match = get_match(match_id)
        data = process_match(match)
        # Récupérer le timestamp du match (en secondes)
        timestamp = match["info"].get("gameStartTimestamp", 0) // 1000
        date_str = (
            datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d_%H-%M-%S")
            if timestamp
            else match_id
        )
        filename = f"match_{date_str}_filtered.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Match filtré sauvegardé dans {filename}")

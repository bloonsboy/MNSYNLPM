"""Export match data."""

import json
from datetime import datetime
from pathlib import Path

from .constant import CHAMPION_ID_TO_NAME, MATCH_IDS, VIRGULE
from .riot_api import get_match


def extract_team_info(team: dict, picks: list, bans: list) -> dict:
    """Extract team-level statistics, picks and bans."""
    objectives = team.get("objectives", {})
    return {
        "win": team.get("win", False),
        "kills": objectives.get("champion", {}).get("kills", 0),
        "tower": objectives.get("tower", {}).get("kills", 0),
        "inhibitor": objectives.get("inhibitor", {}).get("kills", 0),
        "dragon": objectives.get("dragon", {}).get("kills", 0),
        "horde": objectives.get("horde", {}).get("kills", 0),
        "riftHerald": objectives.get("riftHerald", {}).get("kills", 0),
        "baron": objectives.get("baron", {}).get("kills", 0),
        "picks": picks,
        "bans": [
            {
                "championId": b["championId"],
                "championName": CHAMPION_ID_TO_NAME.get(
                    b["championId"], str(b["championId"])
                ),
            }
            for b in bans
        ],
    }


def extract_player_info(p):
    """Extract player-level statistics."""
    team_position = p.get("teamPosition")
    if team_position == "UTILITY":
        team_position = "SUPPORT"

    return {
        "Position": team_position,
        "Champion": {
            "championName": p.get("championName"),
            "championExp": p.get("champExperience"),
            "championLevel": p.get("champLevel"),
            "gold": p.get("goldEarned"),
            "creeps": (p.get("totalMinionsKilled", 0) or 0)
            + (p.get("neutralMinionsKilled", 0) or 0),
            "turretTakedowns": p.get("turretTakedowns"),
            "itemsPurchased": p.get("itemsPurchased"),
            "totalTimeSpentDead": p.get("totalTimeSpentDead"),
            "wardsPlaced": p.get("wardsPlaced"),
            "wardsKilled": p.get("wardsKilled"),
            "visionWardsPlaced": p.get("visionWardsBoughtInGame"),
            "visionScore": p.get("visionScore"),
        },
        "Damage": {
            "totalDamageDealt": p.get("totalDamageDealtToChampions"),
            "physicalDamageDealt": p.get("physicalDamageDealtToChampions"),
            "magicDamageDealt": p.get("magicDamageDealtToChampions"),
            "trueDamageDealt": p.get("trueDamageDealtToChampions"),
            "totalDamageTaken": p.get("totalDamageTaken"),
            "physicalDamageTaken": p.get("physicalDamageTaken"),
            "magicDamageTaken": p.get("magicDamageTaken"),
            "trueDamageTaken": p.get("trueDamageTaken"),
            "damageDealtToBuildings": p.get("damageDealtToBuildings"),
            "damageDealtToEpicMonsters": p.get("damageDealtToEpicMonsters"),
        },
        "Ping": {
            "onMyWay": p.get("onMyWayPings"),
            "danger": p.get("dangerPings"),
            "getBack": p.get("getBackPings"),
            "enemyMissing": p.get("enemyMissingPings"),
            "assistMe": p.get("assistMePings"),
            "retreat": p.get("retreatPings"),
            "enemyVision": p.get("enemyVisionPings"),
            "hold": p.get("holdPings"),
            "needVision": p.get("needVisionPings"),
            "push": p.get("pushPings"),
            "visionCleared": p.get("visionClearedPings"),
            "allIn": p.get("allInPings"),
            "basic": p.get("basicPings"),
        },
        "KDA": {
            "kills": p.get("kills"),
            "deaths": p.get("deaths"),
            "assists": p.get("assists"),
            "doubleKills": p.get("doubleKills"),
            "tripleKills": p.get("tripleKills"),
            "pentaKills": p.get("pentaKills"),
            "quadraKills": p.get("quadraKills"),
            "largestMultiKill": p.get("largestMultiKill"),
        },
        "First": {
            "firstBlood": bool(
                p.get("firstBloodKill") or p.get("firstBloodAssist")
            ),
            "firstTower": bool(
                p.get("firstTowerKill") or p.get("firstTowerAssist")
            ),
        },
        "Spell": {
            "Q_spell": p.get("spell1Casts"),
            "W_spell": p.get("spell2Casts"),
            "E_spell": p.get("spell3Casts"),
            "R_spell": p.get("spell4Casts"),
            "summoner1Casts": p.get("summoner1Casts"),
            "summoner1Id": p.get("summoner1Id"),
            "summoner2Casts": p.get("summoner2Casts"),
            "summoner2Id": p.get("summoner2Id"),
        },
    }


def process_match(match):
    """Process a match and return a structure with game data."""
    info = match["info"]
    out = {
        "game": {
            "gameDuration": info.get("gameDuration"),
            "gameCreation": info.get("gameCreation"),
            "gameStartTimestamp": info.get("gameStartTimestamp"),
            "gameEndTimestamp": info.get("gameEndTimestamp"),
            "gameMode": info.get("gameMode"),
        }
    }
    participants = info["participants"]
    team1_names = [p["riotIdGameName"] for p in participants[:5]]
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

    virgule_picks = [p["championName"] for p in virgule_players]
    enemy_picks = [p["championName"] for p in enemy_players]
    out["virgule"] = extract_team_info(
        virgule_team, virgule_picks, virgule_bans
    )
    out["enemy"] = extract_team_info(
        enemy_team, enemy_picks, enemy_bans
    )

    for p in participants:
        out[p["riotIdGameName"]] = extract_player_info(p)
    return out
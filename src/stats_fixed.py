import glob
import json


def load_matches():
    matches = []
    for file in glob.glob("match_*.json"):
        with open(file) as f:
            matches.append(json.load(f))
    return matches


def basic_stats(matches):
    # Exemple : nombre de victoires/défaites de l'équipe
    win_count = 0
    loss_count = 0
    for match in matches:
        # À adapter selon la structure des données et votre équipe
        for participant in match["info"]["participants"]:
            if participant["win"]:
                win_count += 1
            else:
                loss_count += 1
    print(f"Victoires: {win_count}, Défaites: {loss_count}")


if __name__ == "__main__":
    matches = load_matches()
    basic_stats(matches)

import glob
import json

def basic_stats(matches):
    # Exemple : nombre de victoires/défaites de l'équipe
        # À adapter selon la structure des données et votre équipe
    import glob
    import json


        for participant in match['info']['participants']:
        matches = []
        for file in glob.glob("match_*.json"):
            with open(file) as f:
                matches.append(json.load(f))
        return matches


            if participant['win']:
                win_count += 1
            else:
                loss_count += 1
    print(f"Victoires: {win_count}, Défaites: {loss_count}")


def load_matches():
    matches = []
    for file in glob.glob("match_*.json"):
        with open(file) as f:
            matches.append(json.load(f))



    if __name__ == "__main__":
        matches = load_matches()
        basic_stats(matches)

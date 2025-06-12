import pandas as pd
import statbotics
import numpy as np
import os

'''base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "../data/2025_insights.csv")
pf = pd.read_csv(data_path)'''

def fetch_matches(event: str = None, team: int = None, year: int = None, limit: int = 500):
    sb = statbotics.Statbotics()
    matches = sb.get_matches(team=team, event=event, limit = limit)
    if year:
        matches = [m for m in matches if m['year'] == year]
    return matches
def fetch_match(match_key: str):
    sb = statbotics.Statbotics()
    match_data = sb.get_match(match=match_key)
    print(match_data)
    return match_data
def reading_frame(matches: list):
    rows = []
    for match in matches:
        match_key = ['key']
        for color in['red', 'blue']:
            alliance = match['alliances'][color]
            score = match['result'][f"{color}"]
def calculate_z_values(df, team_number):
    return None
#print(pf)
mf = fetch_match('2025isde1_sf11m1')
print(mf)
#matchs_frick = fetch_matches("2025isde1", 1690, 2025)
#print(matchs_frick)
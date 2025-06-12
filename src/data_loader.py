import pandas as pd

def load_match_data(filepath):
    df = pd.read_csv(filepath)

    df.columns = df.columns.str.strip()

    return df

def group_data_by_team(df):
    team_groups = {}
    for team, group in df.groupby("teamNumber"):
        team_groups[team] = group.reset_index(drop=True)
    return team_groups


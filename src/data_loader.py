import pandas as pd
import os

def load_match_data(filepath):
    df = pd.read_csv(filepath)

    df.columns = df.columns.str.strip()

    return df

def group_data_by_team(df):
    team_groups = {}
    for team, group in df.groupby("teamNumber"):
        team_groups[team] = group.reset_index(drop=True)
    return team_groups

def get_csv_from_user():
    while True:
        inputfile = input("Please enter the file path of your CSV file (type 'exit' to exit): ").strip()
        if inputfile.lower() == 'exit':
            print("CSV Loading cancelled")
            return None
        cleaned_path = inputfile.lstrip('&').strip()

        if cleaned_path.startswith('"') and cleaned_path.endswith('"'):
            cleaned_path = cleaned_path[1:-1]
        if cleaned_path.startswith("'") and cleaned_path.endswith("'"):
            cleaned_path = cleaned_path[1:-1]

        if not os.path.isfile(cleaned_path):
            print(f"File '{cleaned_path}' not found. Please check the path and try again.")
            continue

        if not cleaned_path.lower().endswith('.csv'):
            print("Invalid file. Please provide a valid .csv.")
            continue

        try:
            df = pd.read_csv(cleaned_path)
            print(f"\nLoaded '{cleaned_path}' successfully with {len(df)} rows.\n")
            return df
        except Exception as e:
            print(f"An error occurred while loading the file: {e}")
            continue
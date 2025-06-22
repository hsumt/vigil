import pandas as pd
import os

def analyze_team(team_number, data):
    if data is None:
        print(f"No data found for team {team_number}")
        return
    print(f"-----------Historical Data found for team {team_number}:------------")
    print(data)
    
def compare_teams(teams):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "../data/2025_insights.csv")
    pf = pd.read_csv(data_path)
    teams = [int(t) for t in teams]
    comparison_df = pf[pf['num'].isin(teams)]

    if comparison_df.empty:
        print("No matching teams found in the data.")
        return
    
    comparison_df = comparison_df.sort_values(by="total_epa", ascending=False)
    display_df = comparison_df[[
        "num", "team", "total_epa", "auto_epa", "teleop_epa", "endgame_epa",
        "rp_1_epa", "rp_2_epa", "rp_3_epa"
    ]].rename(columns={
        "num": "Team #",
        "team": "Team Name",
        "total_epa": "Total EPA",
        "auto_epa": "Auto",
        "teleop_epa": "Teleop",
        "endgame_epa": "Endgame",
        "rp_1_epa": "Auto RP",
        "rp_2_epa": "Coral RP",
        "rp_3_epa": "Barge RP"
    })

    # Display as table
    print("\nTeam Comparison:")
    print(display_df.to_string(index=False))
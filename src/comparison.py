import pandas as pd
import os
def write_output(use_streamlit, *args):
    if use_streamlit:
        import streamlit as st
        for arg in args:
            st.write(arg)
    else:
        for arg in args:
            print(arg)

def analyze_team(team_number, data, use_streamlit=True):
    if data is None:
        write_output(f"No data found for team {team_number}")
        return
    write_output(f"-----------Historical Data found for team {team_number}:------------")
    write_output(use_streamlit, data)
    
def compare_teams(teams, use_streamlit=True):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "../data/2025_insights.csv")
    pf = pd.read_csv(data_path)
    teams = [int(t) for t in teams]
    comparison_df = pf[pf['num'].isin(teams)]

    if comparison_df.empty:
        write_output("No matching teams found in the data.")
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
    write_output(use_streamlit, "\nTeam Comparison:")

    if use_streamlit:
        import streamlit as st
        st.dataframe(display_df)
    else:
        write_output(use_streamlit, display_df.to_string(index=False))
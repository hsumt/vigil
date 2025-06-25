import pandas as pd
import streamlit as st
import os
import colorama as cd
import random as rd

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "../data/2025_insights.csv")
    df = pd.read_csv(data_path)
    df["num"] = df["num"].astype(int)
    return df


def simulate_match(team_numbers, pf, use_streamlit=True):
    #this will come in as a list
    red_alliance = [int(team_numbers["red1"]), int(team_numbers["red2"]), int(team_numbers["red3"])]
    blue_alliance = [int(team_numbers["blue1"]), int(team_numbers["blue2"]), int(team_numbers["blue3"])]
    red_stats = {"auto_points": 0, "teleop_points": 0, "endgame_points": 0, 
                 "auto_rp": 0, "coral_rp": 0, "barge_rp": 0}
    blue_stats = {"auto_points": 0, "teleop_points": 0, "endgame_points": 0,
                  "auto_rp": 0, "coral_rp": 0, "barge_rp": 0}

    for team in red_alliance:
        row = pf[pf["num"] == team].iloc[0]
        team_auto_points = row["auto_epa"]
        team_teleop_points = row["teleop_epa"]
        team_endgame_points = row["endgame_epa"]
        if team_endgame_points > 12:
            team_endgame_points = 12
        red_stats["auto_points"] += team_auto_points
        red_stats["teleop_points"] += team_teleop_points
        red_stats["endgame_points"] += team_endgame_points
        red_stats["auto_rp"] += row["rp_1_epa"]
        red_stats["coral_rp"] += row["rp_2_epa"]
        red_stats["barge_rp"] += row["rp_3_epa"]


    for team in blue_alliance:
        row = pf[pf["num"] == team].iloc[0]  # get the row with the team mentioned
        team_auto_points = row["auto_epa"]
        team_teleop_points = row["teleop_epa"]
        team_endgame_points = row["endgame_epa"]
        if team_endgame_points > 12:
            team_endgame_points = 12
        blue_stats["auto_points"] += team_auto_points
        blue_stats["teleop_points"] += team_teleop_points
        blue_stats["endgame_points"] += team_endgame_points
        blue_stats["auto_rp"] += row["rp_1_epa"]
        blue_stats["coral_rp"] += row["rp_2_epa"]
        blue_stats["barge_rp"] += row["rp_3_epa"]

 #   print("Red Alliance Stats:")
  #  print(red_stats)
  #  print("Blue Alliance Stats:")
  #  print(blue_stats) test stuff

    red_total = red_stats["auto_points"] + red_stats["teleop_points"] + red_stats["endgame_points"]
    blue_total = blue_stats["auto_points"] + blue_stats["teleop_points"] + blue_stats["endgame_points"]
    red_alliance_display = []
    blue_alliance_display = []

    for team in red_alliance:
        team_name = pf[pf["num"] == team]["team"].values[0]
        red_alliance_display.append(f"{team} - {team_name}")

    for team in blue_alliance:
        team_name = pf[pf["num"] == team]["team"].values[0]
        blue_alliance_display.append(f"{team} - {team_name}")

    def write_output(*args):
        if use_streamlit:
            for arg in args:
                st.write(arg)
        else:
            for arg in args:
                print(arg)

    write_output("### Red Alliance:", red_alliance_display)
    write_output("### Blue Alliance:", blue_alliance_display)
    write_output("---")
    write_output("## Match Scores")
    write_output(f"**Red Alliance Total Score:** {int(red_total)}")
    write_output(f"**Blue Alliance Total Score:** {int(blue_total)}")
    write_output("---")
    write_output("### Detailed Scores")
    write_output(f"Red Alliance Auto Points: {round(red_stats['auto_points'], 1)}")
    write_output(f"Red Alliance Teleop Points: {round(red_stats['teleop_points'], 1)}")
    write_output(f"Red Alliance Endgame Points: {round(red_stats['endgame_points'], 1)}")
    write_output(f"Blue Alliance Auto Points: {round(blue_stats['auto_points'], 1)}")
    write_output(f"Blue Alliance Teleop Points: {round(blue_stats['teleop_points'], 1)}")
    write_output(f"Blue Alliance Endgame Points: {round(blue_stats['endgame_points'], 1)}")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

def plot_teams_performance(team_groups, team_numbers):
    plt.figure(figsize=(6*(len(team_numbers)), 3*(len(team_numbers))))

    xtick_labels = []
    x_positions = []
    team_match_labels = {}
    curr_pos = 0
    team_centers = {}  

    for team_number in team_numbers:
        team_df = team_groups[team_number].copy()
        team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
        grouped = team_df.groupby(['match', 'match_num']).mean(numeric_only=True).reset_index()
        grouped = grouped.sort_values(by='match_num').reset_index(drop=True)

        endgame_status = team_df.groupby(['match', 'match_num'])['endgame'].first().reset_index()
        grouped = grouped.merge(endgame_status, on=['match', 'match_num'], how='left')

        match_nums = grouped['match_num'].tolist()
        match_labels = [f"Q{n}" for n in match_nums]

        xpos = list(range(curr_pos, curr_pos + len(match_nums)))

        team_match_labels[team_number] = {
            'match_nums': match_nums,
            'auto': grouped['autoPoints'],
            'teleop': grouped['teleopPoints'],
            'endgame': grouped['endgame'],
            'x_positions': xpos
        }

        xtick_labels.extend(match_labels)
        x_positions.extend(xpos)

     
        team_centers[team_number] = np.mean(xpos)  # <-- ADDED

        curr_pos += len(match_nums) + 1
        xtick_labels.append("")
        x_positions.append(curr_pos - 1)


    if xtick_labels and xtick_labels[-1] == "":
        xtick_labels.pop()
        x_positions.pop()

    ax = plt.gca()
    bar_width = 0.5

    for team_number in team_numbers:
        data = team_match_labels[team_number]
        x = np.array(data['x_positions'])

        auto_vals = data['auto']
        teleop_vals = data['teleop']
        endgame_vals = []

        for status in data['endgame']:
            if isinstance(status, str):
                status = status.upper()
            if status == "DEEP":
                endgame_vals.append(12)
            elif status == "SHALLOW":
                endgame_vals.append(6)
            elif status == "NOT_ATTEMPTED":
                endgame_vals.append(0)
            else:
                endgame_vals.append(2)

        ax.bar(x, auto_vals, width=bar_width, color='purple', label='Auto')
        ax.bar(x, teleop_vals, width=bar_width, bottom=auto_vals, color='green', label='Teleop')
        ax.bar(x, endgame_vals, width=bar_width, bottom=(np.array(auto_vals) + np.array(teleop_vals)),
               color='orange', label='Endgame Bonus')


   # handles, labels = ax.get_legend_handles_labels()
   # by_label = dict(zip(labels, handles))
    #ax.legend(by_label.values(), by_label.keys())

    plt.title('Stacked Auto, Teleop, and Endgame Points per Match')
    #plt.xlabel('Match')
    plt.ylabel('Points')
    plt.grid(True, axis='y')


    plt.xticks(x_positions, xtick_labels, rotation=0)


    ylim = ax.get_ylim()
    y_offset = - (ylim[1] * 0.05) 
    for team_number, center_x in team_centers.items():
        ax.text(center_x, y_offset, f"Team {team_number}", ha='center', va='top', fontsize=10, color='black', transform=ax.transData)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close()
    summary_rows = []

    for team_number in team_numbers:
        team_df = team_groups[team_number].copy()
        avg_auto = team_df['autoPoints'].mean()
        avg_teleop = team_df['teleopPoints'].mean()

        climb_counts = team_df['endgame'].str.upper().fillna("OTHER").value_counts()
        deep = climb_counts.get("DEEP", 0)
        shallow = climb_counts.get("SHALLOW", 0)
        failed_deep = climb_counts.get("FAILED_DEEP", 0)
        park = climb_counts.get("PARKED", 0) + climb_counts.get("FAILED_SHALLOW", 0)

        summary_rows.append({
            "Team": team_number,
            "Avg Auto": round(avg_auto, 2),
            "Avg Teleop": round(avg_teleop, 2),
            "DEEP Climbs": deep,
            "SHALLOW Climbs": shallow,
            "FAILED DEEP": failed_deep,
            "PARK/FAILED SHALLOW": park
        })

    summary_df = pd.DataFrame(summary_rows)
    st.markdown("### Team Summary Table")
    st.table(summary_df)
    



def plot_team_performance(team_df, team_number):

    avg_auto = team_df['autoPoints'].mean()
    avg_teleop = team_df['teleopPoints'].mean()

    climb_counts = team_df['endgame'].str.upper().fillna("OTHER").value_counts()
    deep_count = climb_counts.get("DEEP", 0)
    shallow_count = climb_counts.get("SHALLOW", 0)
    park_count = climb_counts.get("PARKED", 0) + climb_counts.get("FAILED_SHALLOW", 0)
    failed_deep_count = climb_counts.get("FAILED_DEEP", 0)
    
    fig, ax = plt.subplots(figsize=(12,6))

    ax.bar("Auto + Tele", avg_auto, label='Auto Points', color="blue")    
    ax.bar("Auto + Tele", avg_teleop, bottom=avg_auto, label="Teleop Avg", color="green")

    # Separate bars for climb counts
    ax.bar("DEEP Climbs", deep_count, color="orange")
    ax.bar("SHALLOW Climbs", shallow_count, color="gold")
    ax.bar("FAILED DEEP Climbs", failed_deep_count, color="pink")
    ax.bar("Park", park_count, color="gray")

    ax.set_title(f"Team {team_number} – Average Points and Climb Attempts")
    ax.set_ylabel("Points / Match Count")
    ax.legend(loc='upper right')
    ax.grid(True, axis='y')

    st.pyplot(fig)
    plt.close(fig)

    summary_df = pd.DataFrame({
        "Metric": [
            "Avg Auto Points",
            "Avg Teleop Points",
            "DEEP Climbs",
            "SHALLOW Climbs",
            "FAILED DEEP Climbs",
            "Park/Failed SHALLOW Climbs"
        ],
        "Value": [
            round(avg_auto, 2),
            round(avg_teleop, 2),
            deep_count,
            shallow_count,
            failed_deep_count,
            park_count
        ]
    })

    st.markdown("### Summary Table")
    st.table(summary_df)



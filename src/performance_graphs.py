import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
def plot_teams_performance(team_groups, team_numbers):
    import matplotlib.pyplot as plt
    import streamlit as st

    plt.figure(figsize=(16, 8))
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']  # Max 6 teams

    for idx, team_number in enumerate(team_numbers):
        team_df = team_groups[team_number].copy()

        # Clean + group by match, average multiple reports
        team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
        grouped = team_df.groupby(['match', 'match_num']).mean(numeric_only=True).reset_index()
        grouped = grouped.sort_values(by='match_num')

        # X-axis will be string match labels, like Q1, Q2, etc.
        match_labels = grouped['match']
        auto_points = grouped['autoPoints']
        teleop_points = grouped['teleopPoints']

        # Plot lines with match names directly as x-axis
        plt.plot(match_labels, auto_points, marker='o', label=f'Team {team_number} - Auto', color=colors[idx])
        plt.plot(match_labels, teleop_points, marker='s', linestyle='--', label=f'Team {team_number} - Teleop', color=colors[idx])

    plt.title('Auto & Teleop Points per Match (Averaged Across Reports)')
    plt.xlabel('Match')
    plt.ylabel('Points')
    plt.xticks(rotation=45)  # Prevent label overlap
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)
    plt.close()




def plot_team_performance(team_df, team_number):
    team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
    df = team_df.sort_values(by='match_num')
    matches = df['match']
    auto_points = df['autoPoints']
    teleop_points = df['teleopPoints']
    
    plt.figure(figsize=(12,6))

    plt.plot(matches, auto_points, marker='o', label='Auto Points', color="blue")
    plt.plot(matches, teleop_points, marker='o', label='Teleop Points', color="green")

    plt.title(f"Team {team_number}'s Performance Across Recorded matches")
    plt.legend(loc='upper left', fontsize = 'small')
    plt.xlabel('Match Labels')
    plt.ylabel('Points (Auto/Tele, etc.)')
    plt.xticks(rotation = 45)

    st.pyplot(plt)
    plt.close()
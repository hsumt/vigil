import matplotlib.pyplot as plt
import numpy as np
def plot_teams_performance(team_groups, team_numbers):
    plt.figure(figsize=(16, 8))
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']  # Max 6 teams

    max_match_length = 0

    x_positions = []
    label_positions = []
    label_colors = []
    label_texts = []

    x_pos = 0

    for idx, team_number in enumerate(team_numbers):
        team_df = team_groups[team_number].copy()
        team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
        df = team_df.sort_values(by='match_num')

        matches = df['match']
        auto_points = df['autoPoints']
        teleop_points = df['teleopPoints']

        x = list(range(len(matches)))

        # Plot Auto Points
        plt.plot(x, auto_points, marker='o', label=f'Team {team_number} - Auto', color=colors[idx])

        # Plot Teleop Points with dashed line
        plt.plot(x, teleop_points, marker='s', linestyle='--', label=f'Team {team_number} - Teleop', color=colors[idx])

        # Collect x positions and label info
        x_positions.extend(x)
        label_positions.extend([-(idx + 1)] * len(matches))  # Each team gets its own label row
        label_colors.extend([colors[idx]] * len(matches))
        label_texts.extend(matches)

        if len(matches) > max_match_length:
            max_match_length = len(matches)

    plt.title('Auto & Teleop Points Comparison with Stacked Match Labels')
    plt.xlabel('Custom X-Axis')
    plt.ylabel('Points')
    plt.legend()
    plt.grid(True)

    for x, y, text, color in zip(x_positions, label_positions, label_texts, label_colors):
        plt.text(x, y, text, ha='center', va='center', fontsize=10, color=color)

    plt.ylim(bottom=min(label_positions) - 1)  # Add space for labels

    plt.tight_layout()
    plt.show()




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

    plt.show()
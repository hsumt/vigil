import matplotlib.pyplot as plt
import numpy as np
def plot_teams_performance(team_groups, team_numbers):
    plt.figure(figsize=(14,7))
    plt.subplot(1,2,1)
    for team_number in team_numbers:
        team_df = team_groups[team_number].copy()
        team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
        df = team_df.sort_values(by='match_num')
        matches = df['match']
        auto_points = df['autoPoints']
        plt.plot(matches, auto_points, marker='o', label=f"Team {team_number}")
    plt.title(f"Auto Point Comparison ({len(team_numbers)} teams)")
    plt.xlabel('Match')
    plt.ylabel("Auto Points")
    plt.legend()
    plt.xticks(rotation = 45)
    plt.subplot(1,2,2)
    for team_number in team_numbers:
        team_df = team_groups[team_number].copy()
        team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
        df = team_df.sort_values(by='match_num')
        matches = df['match']
        auto_points = df['autoPoints']
        plt.plot(matches, auto_points, marker='o', label=f"Team {team_number}")
    plt.title(f"TeleOp Point Comparison ({len(team_numbers)} teams)")
    plt.xlabel('Match')
    plt.ylabel("TeleOp Points")
    plt.legend()
    plt.xticks(rotation = 45)

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
import matplotlib.pyplot as plt
import numpy as np
def plot_team_performance(team_df, team_number):
    
    df = team_df.sort_values(by='match')
    matches = df['match']
    auto_points = df['autoPoints']
    teleop_points = df['teleopPoints']
    
    plt.figure(figsize=(12,6))

    plt.plot(matches, auto_points, marker='o', label='Auto Points', color="blue")
    plt.plot(matches, teleop_points, marker='o', label='Teleop Points', color="green")

    plt.show()
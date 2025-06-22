def detect_anomalies(team_df, underperformance_margin=0.8):
    "v1.0 of this function runs basic detection for <80%"
    anomalies = []

    avg_auto = team_df['autoPoints'].mean()
    avg_teleop = team_df['teleopPoints'].mean()

    for idx, row in team_df.iterrows():
        if row['autoPoints'] < underperformance_margin * avg_auto: 
            anomalies.append(f"Low Auto: {row['autoPoints']} vs. Normal Avg {round(avg_auto,1)} Auto in Match {row['match']}")
        if row['teleopPoints'] < underperformance_margin * avg_teleop: 
            anomalies.append(f"Low Teleop: {row['teleopPoints']} vs. Normal Avg {round(avg_teleop,1)} Teleop in Match {row['match']}")
        usually_deep = (team_df['endgame'] == 'DEEP').sum() >= len(team_df) / 2 #checks for majority rather than percent currently
    if usually_deep:
            for idx, row in team_df.iterrows():
                if not row['endgame'] == "DEEP":
                    anomalies.append(f"Endgame miss: Expected DEEP, got {row['endgame']} result instead in Match {row['match']}")
    return anomalies

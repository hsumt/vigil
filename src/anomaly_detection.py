def detect_anomalies(team_df, underperformance_margin=0.8):
    "v1.0 of this function runs basic detection, there's nothing like z-scores yet i just need to test. It tests for <80%"
    anomalies = []

    avg_auto = team_df['autoPoints'].mean()
    avg_teleop = team_df['teleopPoints'].mean()

    for idx, row in team_df.iterrows():
        if row['autoPoints'] < underperformance_margin * avg_auto: #should calc correctly
            anomalies.append(f"Low Auto: {row['autoPoints']} vs. Normal Avg {avg_auto} Auto in Match {row['match']}")
        if row['teleopPoints'] < underperformance_margin * avg_teleop: #should calc correctly
            anomalies.append(f"Low Teleop: {row['teleopPoints']} vs. Normal Avg {avg_teleop} Teleop in Match {row['match']}")
    
    return anomalies

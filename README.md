# Vigil

Vigil is a FRC robotics health monitor, anomaly detector, and predictive maintenance dashboard that monitors robotics teams' performance data over time - including reliability metrics, and detects when a team may be at risk of under/overperforming and what their current performance may be indicating.

Data usage you import the current 2025_insights.csv off of Statbotics and then whatever Lovat csvs you want to use.
Updated 6/21/2025: 


Old Update Log:
Updated 6/11/2025: Apparently Statbotics and API and the FMS do not record team specific data except for the endgame. issues 😭

Updated 6/12/2025: The new plan is to use Pandas to directly pull off the Raw Lovat data and to force its input
Updated 6/12/2025 2 hours later: Very happy we got a basic prototype of anomaly working. Should be MUCH easier to continue

Updated 6/16/2025 Performance Graphing. Viewing health trends works. Can compare teams now:
![image](https://github.com/user-attachments/assets/54714e7a-fd73-4a1b-b77b-8057580c2ccc)


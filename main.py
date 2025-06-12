from src.match_simulator import load_data, simulate_match
from src.data_loader import group_data_by_team, load_match_data
from src.anomaly_detection import detect_anomalies
from src.performance_graphs import plot_team_performance

def main():
    filepath = 'data/Lovat.csv'
    df = load_match_data(filepath)
    
    print("Loaded CSV, continuing: ")
    print(df.head())



    while True:
            print("Welcome to Vigil!")
            response = input("1: Upload CSV from Lovat\n2: \n3: View Health Trends\n4: Simulate Match \n5: Run Anomaly Detection on current data \n6: Exit \nWwhat would you like to do?   ")
            try:
                response = int(response)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
                continue

            if response == 1:
                break
            elif response == 2:
                print("Upload from NOMAD Master Sheet selected. (Feature coming soon!)")
            elif response == 3:
                print("Viewing Health Trends. (Feature coming soon!)")
            elif response == 4:
                pf = load_data()
                pf["num"] = pf["num"].astype(int)
                team_numbers = {}

                for alliance, i in [("Red Alliance", 1), ("Red Alliance", 2), ("Red Alliance", 3),
                                    ("Blue Alliance", 1), ("Blue Alliance", 2), ("Blue Alliance", 3)]:
                    while True:
                        team_input = input(f"Enter {alliance} Team {i} Number: ")
                        try:
                            team_int = int(team_input)
                        except ValueError:
                            print("Team number must be an integer.")
                            continue

                        if team_int in pf["num"].values:
                            key = f"{alliance.lower().split()[0]}{i}"
                            team_numbers[key] = team_int
                            break
                        else:
                            print("Team not found in data. Please re-enter.")

                simulate_match(team_numbers, pf)

            elif response == 5:
                print("Anomaly Detection selected . . .")
                team_groups = group_data_by_team(df)
                print(f"\nFound {len(team_groups)} teams in the {filepath}")
                
                target_team = input("Enter the team number to check for anomalies: ").strip()
                target_team = int(target_team)

                if target_team in team_groups:
                    print("---------------------------------------")
                    print("---------------------------------------")
                    print(f"\n Match List for Team {target_team}: ")
                    if target_team in team_groups:
                        print(f"\nTeam {target_team} Match Data: ")
                        print(team_groups[2056])
                    print("---------------------------------------")
                    print("---------------------------------------")
                    print(f"\n Anomalies detected for Team {target_team}: ")
                    anomalies = detect_anomalies(team_groups[target_team])
                    if anomalies:
                        for a in anomalies:
                            print(f"-{a}")
                    else:
                        print("No anomalies detected cuz they too busted")
                    print("---------------------------------------")
                    print("---------------------------------------")
                    print("\n Graphs based on data will be opening in a new window: ")
                    plot_team_performance(team_groups[target_team], target_team)




                #for team, team_df in team_groups.items():
                #print(f"Anomalies of the Daly Division of team {team}")
                #anomalies = detect_anomalies(team_df) ''' # This feeds the entire df in, for testing only. Usable later.
                
            
            elif response == 6:
                print("Goodbye!")
                exit()
            else:
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
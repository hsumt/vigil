from src.match_simulator import load_data, simulate_match
from src.data_loader import group_data_by_team, load_match_data
from src.anomaly_detection import detect_anomalies
from src.performance_graphs import plot_team_performance, plot_teams_performance
from src.api import get_team_data, get_team_events, get_team_event_performance
from src.comparison import analyze_team, compare_teams

def main():
    vigilactive = False
    while True:
        inputfile = input("Enter the filename of the .csv data you want to access. Do not write .csv at the end, only the name of the .csv filetype. Type 'Exit' if you want to cancel: ").strip()
        
        if inputfile.lower() == 'exit':
            print("CSV loading cancelled.")
            return  

        filepath = f'data/{inputfile}.csv'

        try:
            df = load_match_data(filepath)
            print("\nLoaded CSV successfully. Continuing...\n")
            print(df.head())
            vigilactive = True 
            break
        except FileNotFoundError:
            print(f"File '{filepath}' not found. Please make sure the file is in the 'data' folder and try again.")
        except Exception as e:
            print(f"An error occurred while loading the file: {e}")


    vigilactive == True

    while vigilactive:
            print("Welcome to Vigil!")
            response = input("1: Upload CSV from Lovat" \
            "\n2: Open Vigil Advisor " \
            "\n3: View Health Trends" \
            "\n4: Simulate Match " \
            "\n5: Run Anomaly Detection on current data " \
            "\n6: Get the matches of a team at an event and see history of the team overall " \
            "\n7:Compare six teams and their stats (2025) " \
            "\n8: Exit " \
            "\nWwhat would you like to do?   ")
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
                print("Viewing Health Trends...")
                team_groups = group_data_by_team(df)
                print(f"\nFound {len(team_groups)} teams in the {filepath}")
                while True:
                    trend_response = input("\n1: View team averages\n2: View performance graphs for all teams\n3: Compare 6 teams' performance graphs\n4: Back to main menu\nChoose an option: ")

                    try:
                        trend_response = int(trend_response)
                    except:
                        print("Invalid input. You must enter a number 1 and 3")
                        continue
                    if trend_response == 1:
                        print("\nTeam Averages:")
                        for team, team_df in team_groups.items():
                            avg_auto = team_df['autoPoints'].mean()
                            avg_tele = team_df['teleopPoints'].mean()
                            print(f"Team {team} - Avg Auto: {avg_auto:.2f}, Avg Teleop: {avg_tele:.2f}")

                    elif trend_response == 2:
                        print("\nPlotting Performance Graphs for All Teams...")
                        for team, team_df in team_groups.items():
                            print(f"Plotting Team {team}'s Performance...")
                            plot_team_performance(team_df, team)
                    elif trend_response == 3:
                        team_list_input = []
                        team_count = 1
                        while len(team_list_input) < 6:
                            team_input = input(f"Enter Team {team_count} Number (or press Enter to stop selecting any more teams)")
                            if team_input == "":
                                break #To clarify. This piece of code to break is to just cut it off if the user wants say only 4 teams
                            try:
                                team_int = int(team_input)
                            except ValueError:
                                print("Team int must be an integer")
                                continue
                            if team_int in team_groups:
                                if team_int not in team_list_input: #goal to check if unique!
                                    team_list_input.append(team_int)
                                    team_count += 1
                                else:
                                    print("Team has been input into the system in a previous response.")
                            else:
                                print("Team not found in current data sheet. Please re-enter")
                        if team_list_input:
                            print(f"Teams Inputted: {team_list_input}")
                            plot_teams_performance(team_groups, team_list_input)
                        else:
                            print("You didn't select any teams. Returning to the Health Trends Menu. Please input teams next time.")                    
                    elif trend_response == 4:
                        print("\nReturning to main menu...\n")
                        break

                    else:
                        print("Invalid selection. Please try again.")
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
                team_number = input("Enter a team number to load history: ")
                try:
                    team_number_int = int(team_number)
                except ValueError:
                    print("Team number must be an integer.")
                    continue

                history_data = get_team_data(team_number)
                if not history_data:
                    print("Team not found in search")
                    continue

                year = input("Enter a year: ")
                try:
                    year_int = int(year)
                except ValueError:
                    print("Year must be an integer.")
                    continue

                events = get_team_events(team_number, year_int)
                if not events:
                    print(f"No events found for team {team_number} in {year_int}.")
                    continue

                print(f"Events for {team_number} in {year_int}:")
                for event in events:
                    print(f"{event['name']} ({event['key']})")

                event_key = input("Please input the event key you want to search through: ")
                matches = None
                for event in events:
                    if event_key == event['key']:
                        matches = get_team_event_performance(f"frc{team_number}", event_key)
                        break

                if matches is None:
                    print("Event not found or no match data.")
                    return

                print(f"\nMatches for {team_number} at {event_key}:")
                for match in matches:
                    print("---------------------------------------------")
                    print(f"{match['comp_level']} {match['match_number']}")
                    print(f"{match['score_breakdown']}")
                    print("---------------------------------------------")
                    print("---------------------------------------------")
                analyze_team(team_number, history_data)
            elif response == 7:
                pf = load_data()  # Make sure pf is loaded here!
                teams = []
                for i in range(6):
                    while True:
                        t = input(f"Enter team {i+1}'s number: ")
                        try:
                            t_int = int(t)
                        except ValueError:
                            print("Team number must be an integer")
                            continue
                        if t_int in pf["num"].values:
                            teams.append(t_int)
                            break
                        else:
                            print(f"Team not found in data. Please re-enter.")
                compare_teams(teams)                
            elif response == 8:
                print("Goodbye!")
                vigilactive == False
                exit()
            else:
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
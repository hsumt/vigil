from src.match_simulator import load_data, simulate_match
from src.file_manager import upload_file, loaded_files

def upload_menu():
    while True:
        print("\nChoose a file to upload:")
        print("1: Overall Team Insights (all teams)")
        print("2: All Teams EPA Breakdown")
        print("3: Event Team Insights")
        print("4: Event EPA Breakdown")
        print("5: Event Alliance Insights")
        print("6: Event Strength of Schedule")
        print("7: Event Simulation")
        print("8: Go Back to Main Menu")

        choice = input("Your choice: ")

        if choice == '1':
            upload_file("Overall Insights", "2025_insights.csv")
        elif choice == '2':
            upload_file("All Teams EPA Breakdown", "2025_epa_breakdown.csv")
        elif choice == '3':
            upload_file("Event Team Insights", "2025isde1_team_insights.csv")
        elif choice == '4':
            upload_file("Event EPA Breakdown", "2025isde1_epa_breakdown.csv")
        elif choice == '5':
            upload_file("Event Alliance Insights", "2025isde1_alliance_insights.csv")
        elif choice == '6':
            upload_file("Event Strength of Schedule", "2025isde1_sos.csv")
        elif choice == '7':
            upload_file("Event Simulation", "2025isde1_simulation.csv")
        elif choice == '8':
            break
        else:
            print("Invalid selection. Please try again.")
def main():
    while True:
        print("Welcome to Vigil!")
        response = input("1: Upload CSV from Statbotics\n2: Upload CSV from NOMAD Master Sheet\n3: View Health Trends\n4: Simulate Match \n5: Run Anomaly Detection \n6: Exit \nWwhat would you like to do?   ")
        try:
            response = int(response)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            continue

        if response == 1:
            upload_menu()
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
            print("Anomaly Detection selected. (Feature coming soon!)")
        elif response == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
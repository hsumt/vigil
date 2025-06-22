import statbotics
import requests
import os
from dotenv import load_dotenv


load_dotenv()


statbotics_url = "https://api.statbotics.io/v3/team/"
def get_team_data(team_number):
    url = f"{statbotics_url}{team_number}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Response Status Code: {response.status_code}")
        print("The system ran into an error.")
        return None
    return response.json()

TBA_AUTH_KEY = os.getenv("TBA_AUTH_KEY")
tba_url = "https://www.thebluealliance.com/api/v3"

HEADERS = {
    "X-TBA-Auth-Key": TBA_AUTH_KEY
}
def get_team_events(team_number, year):
    team_key = f"frc{team_number}"
    url = f"{tba_url}/team/{team_key}/events/{year}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None
def get_team_event_performance(team_key, event_key):
    url = f"{tba_url}/team/{team_key}/event/{event_key}/matches"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

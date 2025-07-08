import streamlit as st
import pandas as pd
from src.match_simulator import load_data, simulate_match
from src.data_loader import group_data_by_team, load_match_data, get_csv_from_user
from src.anomaly_detection import detect_anomalies
from src.performance_graphs import plot_team_performance, plot_teams_performance
from src.api import get_team_data, get_team_events, get_team_event_performance
from src.comparison import analyze_team, compare_teams

# Streamlit app
st.set_page_config(page_title="Vigil: FRC Scouting Analyzer 6995", layout="wide")

# Persistent session state
if "current_df" not in st.session_state:
    st.session_state.current_df = load_data()
    if "num" in st.session_state.current_df.columns:
        st.session_state.current_df.rename(columns={"num": "teamNumber"}, inplace=True)

if "filepath" not in st.session_state:
    st.session_state.filepath = "Default Dataset"

st.title("Vigil: FRC Scouting Analyzer")

# Sidebar


st.sidebar.header("CSV Loader")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    st.session_state.current_df = pd.read_csv(uploaded_file)

    if 'teamNumber' in st.session_state.current_df.columns:
        st.session_state.current_df = st.session_state.current_df.dropna(subset=['teamNumber'])  # Drop rows where teamNumber is NaN
        st.session_state.current_df['teamNumber'] = st.session_state.current_df['teamNumber'].astype(int)

    st.session_state.filepath = uploaded_file.name
    st.sidebar.success(f"Loaded {uploaded_file.name} successfully!")

# Menu


menu = st.sidebar.selectbox("Select a Feature", [
    "Welcome",
    "Simulate Match",
    "Health Trends",
    "Anomaly Detection",
    "API: Team History & Matches",
    "Compare Teams"
])

df = st.session_state.current_df
team_groups = group_data_by_team(df)


# Welcomne


if menu == "Welcome":
    st.subheader("Welcome to Vigil 🚀")
    st.write(f"Current Dataset: `{st.session_state.filepath}`")
    st.write(f"Total teams in dataset: {len(team_groups)}")
    st.write("Select a feature from the sidebar to get started! WARNING: REMEMBER TO UPLOAD A CSV FILE FIRST")


#Simulate Match


elif menu == "Simulate Match":
    st.subheader("🔧 Match Simulator")
    pf = load_data()

    st.write("Select 3 Red Alliance teams and 3 Blue Alliance teams:")

    teams = pf['num'].unique()

    red1 = st.selectbox('Red 1', teams)
    red2 = st.selectbox('Red 2', teams)
    red3 = st.selectbox('Red 3', teams)
    blue1 = st.selectbox('Blue 1', teams)
    blue2 = st.selectbox('Blue 2', teams)
    blue3 = st.selectbox('Blue 3', teams)

    team_numbers = {
        "red1": red1, "red2": red2, "red3": red3,
        "blue1": blue1, "blue2": blue2, "blue3": blue3
    }

    if st.button("Simulate Match"):
        simulate_match(team_numbers, pf)



#Health Trends



elif menu == "Health Trends":
    st.subheader("📊 Health Trends")

    st.write(f"Total teams in dataset: {len(team_groups)}")

    trend_option = st.radio("Select an Option", [
        "View Team Averages",
        "View All Performance Graphs",
        "Compare Performance Graphs of 6 Teams"
    ])

    if trend_option == "View Team Averages":
        sort_option = st.selectbox("Sort By", ["Auto", "Teleop", "Team Number"])
        team_averages = []
        for team, team_df in team_groups.items():
            avg_auto = round(team_df['autoPoints'].mean(), 1)
            avg_tele = round(team_df['teleopPoints'].mean(), 1)
            team_averages.append({'Team': team, 'Avg Auto': avg_auto, 'Avg Teleop': avg_tele})

        if sort_option == "Auto":
            team_averages.sort(key=lambda x: x['Avg Auto'], reverse=True)
        elif sort_option == "Teleop":
            team_averages.sort(key=lambda x: x['Avg Teleop'], reverse=True)

        st.write(pd.DataFrame(team_averages))

    elif trend_option == "View All Performance Graphs":
        for team, team_df in team_groups.items():
            st.write(f"Team {team} Performance")
            plot_team_performance(team_df, team)

    elif trend_option == "Compare Performance Graphs of 6 Teams":
        selected_teams = st.multiselect("Select up to 6 Teams", df['teamNumber'].unique(), max_selections=6)
        if st.button("Plot Comparison"):
            if selected_teams:
                plot_teams_performance(team_groups, selected_teams)
            else:
                st.warning("Please select at least one team.")


#Anomaly Detection


elif menu == "Anomaly Detection":
    st.subheader("🚨 Anomaly Detection")

    target_team = st.number_input("Enter a Team Number", step=1)
    if st.button("Run Anomaly Detection"):
        if target_team in team_groups:
            anomalies = detect_anomalies(team_groups[target_team])
            #st.write("Detected Anomalies:")
            #if anomalies:
            #    for anomaly in anomalies:
            #        st.write(f"- {anomaly}")
            #else:
             #   st.success("No anomalies detected!")
            plot_team_performance(team_groups[target_team], target_team)
        else:
            st.warning("Team not found in the dataset.")


#API (TBA/Statbotics access)


elif menu == "API: Team History & Matches":
    st.subheader("🌐 API Lookup: Team History & Matches")

    team_number = st.number_input("Enter a Team Number", step=1)
    year = st.number_input("Enter a Year", step=1)
    events = get_team_events(team_number, year)
    if st.button("Search Team API History"):
        history_data = get_team_data(team_number)
        if history_data:
            st.write("Team History Data:")
            st.write(history_data)
        else:
            st.error("Team not found.")

    if st.button("Get Team Events"):

        if events:
            st.session_state.team_events = events
        else:
            st.session_state.team_events = []
            st.error(f"No events found for team {team_number} in {year}")
    if "team_events" in st.session_state and st.session_state.team_events:
            event_keys = [event['key'] for event in events]
            selected_event_key = st.selectbox("Select Event", event_keys, key="selected_event_key")
            if st.button("Get Matches for Selected Event"):
                matches = get_team_event_performance(f"frc{team_number}", selected_event_key)
                if matches:
                    st.write(f"Matches for {team_number} at {selected_event_key}:")
                    for match in matches:
                        st.write(f"{match['comp_level']} {match['match_number']}")
                        st.json(match['score_breakdown'])
                else:
                    st.warning("No matches found for this event.")


#Team Comparison


elif menu == "Compare Teams":
    st.subheader("🔍 Compare Teams")

    selected_teams = []
    pf = load_data()
    for i in range(6):
        team = st.number_input(f"Enter Team {i+1} Number", key=f'team_{i}', step=1)
        if team in pf["num"].values:
            selected_teams.append(team)

    if st.button("Compare Teams"):
        if selected_teams:
            compare_teams(selected_teams, use_streamlit=True)
        else:
            st.warning("Please input valid teams to compare.")

st.write("© Vigil Analyzer - Powered by Streamlit 🚀 - FRC Team 6995")
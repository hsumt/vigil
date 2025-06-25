# Vigil - FRC Scouting and Alliance Selection Assistant

Vigil is a local-host offline-ready Python FRC robotics match trend monitor, anomaly detector, predictive dashboard and alliance selection assistant tool. It processes performance data (from CSV files, Statbotics, TheBlueAlliance and manual inputs) to help analyze team metrics at events, thus providing informed details during alliance selection, picklist construction and match strategy.

## Current Features
- Simulate theoretical matchups between alliances
- Calculate average autonomous and teleoperated scores
- Priortize teams based on custom criteria (Auto/Tele)
- Import CSV functionality
- GUI and CLI support. Dual Mode.
- Offline Ready, works without internet after the initial setup and caching
- Trend Detection and Performance Analysis, able to plot the performance of teams across an event.

## Upcoming WIP Features
- ML model for additional analysis
- More support for different categories of graphing.

### Prereqs
- Internet (only for API based needs)
- Streamlit
- Pandas, NumPy
- Colorama
- Python 3.x
Please refer to the requirements.txt for the full-list of pip-related installations.


Data usage you import the current 2025_insights.csv off of Statbotics and then whatever Lovat csvs you want to use.

To use, clone the repo, create a venv, install the dependencies as previously mentioned and then to run CLI mode, just run main.py in terminal, and for GUI, do "streamlit run app.py" in powershell

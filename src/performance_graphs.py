import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def plot_teams_performance(team_groups, team_numbers):
    plt.figure(figsize=(6*(len(team_numbers)), 3*(len(team_numbers))))

    xtick_labels = []
    x_positions = []
    team_match_labels = {}
    curr_pos = 0
    team_centers = {}  

    for team_number in team_numbers:
        team_df = team_groups[team_number].copy()
        team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
        grouped = team_df.groupby(['match', 'match_num']).mean(numeric_only=True).reset_index()
        grouped = grouped.sort_values(by='match_num').reset_index(drop=True)

        endgame_status = team_df.groupby(['match', 'match_num'])['endgame'].first().reset_index()
        grouped = grouped.merge(endgame_status, on=['match', 'match_num'], how='left')

        match_nums = grouped['match_num'].tolist()
        match_labels = [f"Q{n}" for n in match_nums]

        xpos = list(range(curr_pos, curr_pos + len(match_nums)))

        team_match_labels[team_number] = {
            'match_nums': match_nums,
            'auto': grouped['autoPoints'],
            'teleop': grouped['teleopPoints'],
            'endgame': grouped['endgame'],
            'x_positions': xpos
        }

        xtick_labels.extend(match_labels)
        x_positions.extend(xpos)

        # Save center for this team's cluster
        team_centers[team_number] = np.mean(xpos)  # <-- ADDED

        curr_pos += len(match_nums) + 1
        xtick_labels.append("")
        x_positions.append(curr_pos - 1)

    # Remove final dummy label if present
    if xtick_labels and xtick_labels[-1] == "":
        xtick_labels.pop()
        x_positions.pop()

    ax = plt.gca()
    bar_width = 0.5

    for team_number in team_numbers:
        data = team_match_labels[team_number]
        x = np.array(data['x_positions'])

        auto_vals = data['auto']
        teleop_vals = data['teleop']
        endgame_vals = []

        for status in data['endgame']:
            if isinstance(status, str):
                status = status.upper()
            if status == "DEEP":
                endgame_vals.append(12)
            elif status == "SHALLOW":
                endgame_vals.append(6)
            elif status == "NOT_ATTEMPTED":
                endgame_vals.append(0)
            else:
                endgame_vals.append(2)

        ax.bar(x, auto_vals, width=bar_width, color='purple', label='Auto')
        ax.bar(x, teleop_vals, width=bar_width, bottom=auto_vals, color='green', label='Teleop')
        ax.bar(x, endgame_vals, width=bar_width, bottom=(np.array(auto_vals) + np.array(teleop_vals)),
               color='orange', label='Endgame Bonus')


   # handles, labels = ax.get_legend_handles_labels()
   # by_label = dict(zip(labels, handles))
    #ax.legend(by_label.values(), by_label.keys())

    plt.title('Stacked Auto, Teleop, and Endgame Points per Match')
    #plt.xlabel('Match')
    plt.ylabel('Points')
    plt.grid(True, axis='y')


    plt.xticks(x_positions, xtick_labels, rotation=0)


    ylim = ax.get_ylim()
    y_offset = - (ylim[1] * 0.05) 
    for team_number, center_x in team_centers.items():
        ax.text(center_x, y_offset, f"Team {team_number}", ha='center', va='top', fontsize=10, color='black', transform=ax.transData)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close()
    



def plot_team_performance(team_df, team_number):
    import matplotlib.pyplot as plt
    import streamlit as st

    # Ensure match_num sorting
    team_df['match_num'] = team_df['match'].str.extract(r'(\d+)').astype(int)
    df = team_df.sort_values(by='match_num')

    matches = df['match']
    auto_points = df['autoPoints']
    teleop_points = df['teleopPoints']
    endgame_vals = []
    for status in df['endgame']:
                if isinstance(status, str):
                    status = status.upper()
                if status == "DEEP":
                    endgame_vals.append(12)
                elif status == "SHALLOW":
                    endgame_vals.append(6)
                elif status == "NOT_ATTEMPTED":
                    endgame_vals.append(0)
                else:
                    endgame_vals.append(2)
    fig, ax = plt.subplots(figsize=(12,6))

    ax.bar(matches, auto_points, label='Auto Points', color="blue")
    ax.bar(matches, teleop_points, bottom=auto_points, label='Teleop Points', color="green")
    ax.bar(x, endgame_vals, width=bar_width, bottom=(np.array(auto_vals) + np.array(teleop_vals)),
               color='orange', label='Endgame Bonus')

    

    ax.set_title(f"Team {team_number}'s Performance Across Recorded Matches")
    ax.set_xlabel('Match Labels')
    ax.set_ylabel('Points (Stacked)')
    ax.legend(loc='upper left', fontsize='small')
    ax.set_xticks(range(len(matches)))
    ax.set_xticklabels(matches, rotation=45)

    st.pyplot(fig)
    plt.close(fig)





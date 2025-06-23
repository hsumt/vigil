import pandas as pd
import openai
import os
from dotenv import load_dotenv
import langchain

load_dotenv()

#OPEN_AI_AUTH_KEY = os.getenv("OPEN_AI_AUTH_KEY")

client = openai.OpenAI()



def ask_vigil(question, df, features):
    # For those reading, all this is is the prompt that sends scouting data context to GPT. Boring? Yeah its funny though
    system_prompt = f"""Your name is Vigil, an FRC (FIRST Robotics Competition) Alliance Selection Assistant. You serve FRC Team 6995 members, and your job is to help them do 3 things. First, to help them make clear, concise, and winning match strategy and insights before their next matches. Second, to help them make a preliminary picklist of potential first picks, second picks based on how their stats (including but not limited to coralL3, coral L1, netScores, notes) tell you how they perform. Third, help with alliance selection by analyzing the following scouting data. You can use the following columsn: {','.join(features)}.
    Each row is a team's data from the event. You must be precise. 
    Your reasoning must:
      - Use numerical comparisons when appropriate.
      - Analyze averages, minimums, maximums, and minimums greater than zero (min > 0) for key metrics like 'defends', 'autoPoints', etc.
      - For best defenders: focus on 'defends', 'driverAbility', and 'notes'.
      - For best autos: focus on 'autoPoints' with full stat breakdowns.
      - For reliability: focus on low 'netFails', low 'coralDrops', high 'driverAbility', and check 'notes' for qualitative insights.

      IMPORTANT:
      - Recommend specific team numbers based on the scouting data provided.
      - Never make up data. You MUST base your answers ONLY on the CSV data provided.

      Provide clear, actionable recommendations and practical advice.
    Here's a data sample:
    {df[features + ['teamNumber']].head(10).to_string(index=False)}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message['content']

def start_vigil_assistant(df):
    """ Chat Loop. I'll add further control comments here later, hence the multiline comment
    """
    features = ['role', 'coralPickup', 'algaePickup', 'teleopPoints', 'autoPoints', 'driverAbility', 'defends', 'coralPickups', 'algaePickups', 'coralDrops', 'algaeDrops', 'coralL1', 'coralL2', 'coralL3', 'coralL4', 'processorScores', 'netScores', 'netFails', 'notes']
    print("\nStarting Vigil AI")
    print("Ask questions pertaining to the data. For example, recommending alliance partners, the best defenders, teams to look at as sleepers, etc.")


    while True:
        user_input = input("Ask Vigil (or type 'exit' to return to the main menu): ")
        if user_input.lower() in ['exit', 'quit']:
            print("\n Exiting Vigil AI")
            break
        response = ask_vigil(user_input, df, features)
        print(f"\nVigil: {response}\n\n\n")


import pandas as pd

df = pd.read_csv("Daly2025.csv")


print(df.head())

features = ['autoPoints', 'teleopPoints']
import math
import pandas as pd

# Load the CSV file
file_path = r"c:\Users\Johan\PROJECTS\codewarsv5\CodewarsV5\teams\troop_ls.csv"
troops = pd.read_csv(file_path)

# Add Net DPS and Net Health columns
troops["Net DPS"] = troops["DPS"] * troops["Number"]
troops["Net Health"] = troops["Health"] * troops["Number"]

# Initialize the hits to kill table
hits_to_kill = pd.DataFrame(index=troops["Name"], columns=troops["Name"])

# Calculate hits to kill for each troop pair
for attacker in troops.itertuples():
    for defender in troops.itertuples():
        # Check if the attacker can target the defender
        if (attacker._11 == "No" and defender.Type == "Air"):  # Cannot target air
            hits_to_kill.at[attacker.Name, defender.Name] = "-"
        elif (attacker._12 == "No" and defender.Type == "Ground"):  # Cannot target ground
            hits_to_kill.at[attacker.Name, defender.Name] = "-"
        else:
            # Calculate hits to kill
            if attacker.DPS > 0:  # Ensure attacker DPS is not zero
                hits = math.ceil(defender.Health * defender.Number / (attacker.DPS * attacker.Number))
                hits_to_kill.at[attacker.Name, defender.Name] = hits
            else:
                hits_to_kill.at[attacker.Name, defender.Name] = "-"

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
print_full(hits_to_kill)
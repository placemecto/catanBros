import pandas as pd
# Assuming your CSV is already loaded into df and sorted
df = pd.read_csv("CatanReport_Cleaned.csv")
df = df.sort_values(by="Date", ascending=False)
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Define the dictionary to hold match history
match_history = {}

player_names = [col for col in df.columns if col not in ['Date', 'Year', 'Quarter']]
for i, row in df.iterrows():
    # Use the date as the key for each match
    match_date = row['Date']
    if match_date not in match_history:
        match_history[match_date] = []

    # Create a dictionary for this match's player scores, excluding date, year, quarter
    match_scores = {}
    for player in player_names:
        if row[player]>=2:
            match_scores[player] = row[player]
    
    # Append this match's scores to the match history under the correct date
    match_history[match_date].append(match_scores)

for date, matches in match_history.items():
    print(f"Games played on {date}:")
    
    # If there are multiple matches per date, iterate through each match
    for match in matches:
        player_scores = ", ".join([f"{player}: {score}" for player, score in match.items()])
        print(f"- Match with players and scores: {player_scores}")
    print("")  # Just to add a line break for better readability

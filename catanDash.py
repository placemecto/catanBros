import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def set_bg_image(image_file):
    """
    A function to set a full page background image.
    """
    with open(image_file, "rb") as file:
        bg_image = file.read()

    bg_image_encoded = base64.b64encode(bg_image).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image_encoded}");
            background-size: cover;
            opacity: .82;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Main", "2023 Award Recipients", "Enter a Game", "Match History", "Head to Head"])

# Set the background image
set_bg_image('CatanDark.png')
with tab1:
    # Load data
    df = pd.read_csv('CatanReport_Cleaned.csv')

    df = df.dropna(subset=['Date'])

    # Convert 'Date' column to datetime and extract year and quarter
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year.astype(int)  # Convert year to integer
    df['Quarter'] = df['Date'].dt.to_period('Q')

    # Initialize the Streamlit app
    st.title("Catan Power Rankings")

    # Dropdown to select the year
    year_options = ['Overall'] + sorted(df['Year'].unique(), reverse=True)
    year_selection = st.selectbox("Select Year:", year_options)
    def plot_catan_wins_over_time(df):
        """
        This method takes a DataFrame containing Catan game statistics and plots
        a line graph showing the total wins over time for each player with at least one win.
        """
        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Identify the player columns
        player_columns = df.columns.drop(['Date', 'Year', 'Quarter', 'Chelsea', 'Lydia','Eddie', 'Daniel', 'Austin'])

        # Creating a temporary DataFrame for win calculations
        temp_df = df[player_columns].applymap(lambda x: 1 if x in [10,11] else 0)
        temp_df['Date'] = df['Date']

        # Initialize a DataFrame to store cumulative wins over time
        cumulative_wins = pd.DataFrame()

        for player in player_columns:
            # Calculate cumulative wins over time (sort dates in descending order)
            temp_df_sorted = temp_df.sort_values(by='Date', ascending=False)
            cumulative_wins[player] = temp_df_sorted[player].cumsum()

        # Reverse the DataFrame to have ascending dates
        cumulative_wins = cumulative_wins.iloc[::-1]

        # Set the index to the Date column for plotting
        cumulative_wins.set_index(temp_df_sorted['Date'], inplace=True)

        # Plotting
        plt.figure(figsize=(10, 6))
        for player in player_columns:
            plt.plot(cumulative_wins.index, cumulative_wins[player], label=player)

        plt.title('Total Wins Over Time for Catan Players')
        plt.xlabel('Date')
        plt.ylabel('Total Wins')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt
    #Do i want charts for everything?
    def create_visualizations(data, df, year):
        # Set a modern color palette
        sns.set_palette("muted")
        
        # Total Wins Pie Chart - Only players with at least 1 win
        plt.figure(figsize=(8, 6))
        wins_data = data['Total Wins'][data['Total Wins'] > 0]
        labels = [f'{player}: {wins}' for player, wins in wins_data.items()]
        plt.pie(wins_data, labels=labels)
        plt.title(f"Total Wins Distribution {year} (Players with at least 1 win)")
        st.pyplot(plt)
        
        #Line graph for players wins over time
        fig = plot_catan_wins_over_time(df)
        st.pyplot(fig)


    # Games Played Bar Graph - Only for players with at least 1 game played
        plt.figure(figsize=(8, 6))
        games_played_data = data['Total Games Played'][data['Total Games Played'] > 1]
        sns.barplot(x=games_played_data.index, y=games_played_data)
        plt.title(f"Games Played {year}")
        st.pyplot(plt)

    # Function to calculate player statistics
    def calculate_player_stats(data):
        players = data.columns[1:-2]  # Exclude 'Date', 'Year', 'Quarter'
        stats = pd.DataFrame(index=players)
        stats['Total Games Played'] = data[players].notna().sum()
        stats['Avg Points/Game'] = data[players].mean()
        win_condition = data[players].isin([10, 11])
        stats['Total Wins'] = win_condition.sum()
        stats['Win Percentage'] = (stats['Total Wins'] / stats['Total Games Played']) * 100
        # Handle potential division by zero issue
        stats['Win Percentage'] = stats['Win Percentage'].fillna(0)
        return stats

    # Custom CSS to make radio buttons horizontal
    st.markdown("""
    <style>
    div.row-widget.stRadio > div{flex-direction:row;}
    </style>
    """, unsafe_allow_html=True)

    if year_selection == 'Overall':
        # Calculate stats for all years
        overall_stats = calculate_player_stats(df)
        st.header("Overall Statistics")
        # Create visualizations for overall data
        create_visualizations(overall_stats, df, 'Overall')

    if year_selection != "Overall":
        time_period = st.radio("Select Time Period:", ['Q1', 'Q2', 'Q3', 'Q4', 'Yearly'])

    if year_selection != 'Overall':
        if time_period == 'Yearly':
            # Calculate statistics for the entire year
            year_data = df[df['Year'] == int(year_selection)]
            stats = calculate_player_stats(year_data).sort_values(by="Win Percentage", ascending=False)
        else:
            # Calculate statistics for the selected quarter
            quarter = time_period[-1]  # Extract quarter number
            quarter_data = df[(df['Year'] == int(year_selection)) & (df['Quarter'].astype(str) == f"{year_selection}Q{quarter}")]
            stats = calculate_player_stats(quarter_data).sort_values(by="Win Percentage", ascending=False)
    # Display data for the selected time period
    if year_selection != "Overall":
        st.write(stats)
    else:
    # Calculate overall player statistics
        overall_stats = calculate_player_stats(df).sort_values(by="Win Percentage", ascending=False)
        st.header("Overall Player Statistics")
        st.write(overall_stats)

    # Additional interactivity and data displays can be added as needed
with tab2:
    set_bg_image('CatanDark.png')
    st.header("2023 Award Recipients")
    # Displaying the first award recipient
    st.subheader("Most Valuable Player")
    col1, col2 = st.columns(2)

    # First column for the image
    with col2:
        st.image("mike.png", width=310)
        st.image("jeremy.png", width=310)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.image("alec.png", width=310)
    # Second column for the text
    with col1:
        # Custom CSS to add a stroke to the text
        text_with_stroke = """
        <style>
        .colored-text {
            color: white; /* Change the color as needed */
            font-size: 15px;
            line-height: 2;
        }
        </style>
        <div class='colored-text'><b>Name:</b> Michael Bernetti</div>
                
        <div class='colored-text'><b>Win Percentage:</b> 46.29%</div>
        
        <div class='colored-text'><b>Total Wins (2023):</b> 13 </div>
        
        <div class='colored-text'><b>Preferred Color:</b> Blue</div>
        
        <div class='colored-text'><b>Bio:</b> Born in a quaint 4/6/9 settlement in the late 20th century to a family of sheep herders, Mike grew to become one of the most consistent players of the modern Catan era, cementing himself as one of the greats. His unpredictable style yielded massive success in 2023 and he looks to continue his dominance moving into the new year. Analysts attribute his success to his ability to think ahead and partly to sheer luck from the dice. In his free time, Mike enjoys watching sports and donating money to the wallets of his friends when on the golf course.</div>
        <div class='colored-text'><br></div>
        <div class='colored-text'><br></div>
        <div class='colored-text'><br></div>

        
        """

        
        text_with_stroke2 = """
        <style>
        .colored-text {
            color: white; /* Change the color as needed */
            font-size: 15px;
            line-height: 2;
        }
        </style>
        <div class='colored-text'><b>Name:</b> Jeremy Keyes</div>
                
        <div class='colored-text'><b>Attendance Percentage:</b> 100%</div>
        
        <div class='colored-text'><b>Total Wins (2023):</b> 13 </div>
        
        <div class='colored-text'><b>Preferred Color:</b> Red</div>
        
        <div class='colored-text'><b>Bio:</b> Hailing from a desert village north of the brick port, Mr. Keyes gained an appreciation for long roads at a young age. This life of laying pavement and establishing settlements has introduced him to a large network of like-minded people. In present day, Jeremy is the most reliable game facilitator in the West. He sets himself apart from rival gamemakers by being the first league commissioner to participate in every single game within his jurisdiction. Analysts are quick to point out that this does not directly correlate to skill level, as his win percentage hovers around the middle of the pack. What does 2024 hold in store for the man with most wins of all time?  </div>
        <div class='colored-text'><br></div>
        <div class='colored-text'><br></div>

        """
        
        text_with_stroke3 = """
        <style>
        .colored-text {
            color: white; /* Change the color as needed */
            font-size: 15px;
            line-height: 2;
        }
        </style>
        <div class='colored-text'><b>Name:</b>Alec</div>
                
        <div class='colored-text'><b>Attendance Percentage:</b> 26.7%%</div>
        
        <div class='colored-text'><b>Win Percentage:</b> 20% </div>
        
        <div class='colored-text'><b>Jacked off to Cam Newton Highlights:</b>[X] Yes [ ] No </div>
        
        <div class='colored-text'><b>Bio:</b>In the words of Catan journalist Lisa Salters, Alec's career was a "journey marked by early promise and unbridled confidence, followed by utter disappointment, failure, and despair when his luck ran dry". Alec felt like he was on top of the world at the end of Q1 2023, boasting a 40% win rate and high hopes in Panther's quarterback Bryce Young. When reality struck, it struck hard realizing that Young and himself shared one thing in common: they had 0 skill in the games that they play. His start to the 2023 season was as mediocre as it was brief, a veritable comet streaking across our game nights. When the understanding sank in that he had no strategy, sense of prophylaxis, or critical thinking skills, he quickly left the competitive scene, publicly attributing his disappearance to a new girlfriend that has later been proven to be completely fictional. Your virtual seat at the table remains as empty as our seltzers, but your legend continues to inspire tales of 'what could have been.' We raise our sheep and wheat in salute to your fleeting yet unforgettable Catan legacy.</div>
        <div class='colored-text'><br></div>
        <div class='colored-text'><br></div>
        <div class='colored-text'><br></div>
        """
        
        st.markdown(text_with_stroke, unsafe_allow_html=True)
        st.subheader("Love of the Game Award")
        st.markdown(text_with_stroke2, unsafe_allow_html=True)
        st.subheader("Stale Fart Award")
        st.markdown(text_with_stroke3, unsafe_allow_html=True)
with tab3:
    pwd = st.text_input("Please enter data custodian passcode.", type="password")
    if pwd == "5829":
        # Function to determine the quarter from a given date
        def get_quarter(date):
            month = date.month
            if month in [1, 2, 3]:
                return f"{date.year}Q1"
            elif month in [4, 5, 6]:
                return f"{date.year}Q2"
            elif month in [7, 8, 9]:
                return f"{date.year}Q3"
            else:
                return f"{date.year}Q4"

        # Streamlit page setup
        st.title("Catan Game Score Entry")

        # Load the CSV file
        df = pd.read_csv('CatanReport_Cleaned.csv')  # Update with the correct path

        # Create a form for data input
        with st.form("score_form", clear_on_submit=True):
            # Date picker
            date = st.date_input("Date", datetime.now())

            # Determine the number of columns based on the number of players
            # Adjust the number inside range() to control how many input fields per row you'd like
            columns = st.columns(4)  # For example, 4 columns for 4 input fields in a row

            scores = {}
            # Iterate over the player columns and create an input field in each column
            for i, column in enumerate(df.columns):
                if column not in ['Date', 'Year', 'Quarter', ]:  # Exclude non-player and metadata columns
                    with columns[i % len(columns)]:  # Cycle through the columns
                        # Use text_input with empty default for scores, allowing for non-entry
                        score_input = st.text_input(f"Score for {column}:", '', placeholder="DNP")
                        # Convert to int if not empty, else None
                        scores[column] = int(score_input) if score_input else None

            # Submit button
            submitted = st.form_submit_button("Submit")

            if submitted:
                # Determine year and quarter from the date
                year = date.year
                quarter = get_quarter(date)

                # Create a new row with the input data
                new_data = {
                    'Date': date.strftime('%Y-%m-%d'),
                    'Year': year,
                    'Quarter': f"{year}Q{quarter}"
                }
                new_data.update(scores)

                # Append to DataFrame and save to CSV
                new_df = df.append(new_data, ignore_index=True)
                new_df.to_csv('CatanReport_Cleaned.csv', index=False)  # Update with the correct path

                st.success("Data submitted successfully!")

        # Optionally, display the DataFrame
        st.write(df)
    elif pwd and pwd != "5829":
        st.write("Incorrect Passcode, please try again.")

with tab4:
    st.write(df)
with tab5:
    unnecessary_columns = ['Date', 'Year', 'Quarter']
    df.drop(columns=unnecessary_columns, inplace=True, errors='ignore')

    # Extract player names
    player_names = df.columns.tolist()

    # Streamlit app
    # Assuming the initial setup is done and df is loaded correctly

    # Streamlit app setup for the head-to-head statistics tab
    st.title('Player Head-to-Head Win Statistics')

    # Dropdown for selecting a player
    selected_player = st.selectbox('Select a Player:', player_names)

    # Button to calculate and display statistics
    if st.button('Show Statistics'):
        # Initialize dictionaries to hold statistics
        win_counts = {player: 0 for player in player_names if player != selected_player}
        total_games_with_each_player = {player: 0 for player in player_names if player != selected_player}
        lobby_sizes = {player: [] for player in player_names if player != selected_player}  # To track lobby sizes
        
        # Iterate through each game
        for _, row in df.iterrows():
            # Count non-NA (non-empty) entries for players in the game, ensuring we count at least 4 players
            players_in_game = max(4, row.notna().sum() - 3)  # Adjusted to ensure minimum lobby size of 4, -3 accounts for Date, Year, and Quarter columns

            if pd.notna(row[selected_player]):  # If the selected player played in the game
                max_score = row[player_names].max()  # Calculate max score among players only
                if row[selected_player] == max_score:  # If the selected player won
                    for player in win_counts.keys():
                        if pd.notna(row[player]):  # If another player was also in the game
                            win_counts[player] += 1
                            total_games_with_each_player[player] += 1
                            lobby_sizes[player].append(players_in_game)
                else:  # If the selected player didn't win but played
                    for player in total_games_with_each_player.keys():
                        if pd.notna(row[player]):  # If another player was also in the game
                            total_games_with_each_player[player] += 1
                            lobby_sizes[player].append(players_in_game)
        
        # Prepare data for DataFrame
        # Prepare data for DataFrame, keeping win percentages as numeric for sorting
        stats_data = [{
            'Player': player,
            'Games Played Together': total_games_with_each_player[player],
            'Wins': win_counts[player],
            'Win Percentage': win_counts[player] / total_games_with_each_player[player] * 100 if total_games_with_each_player[player] > 0 else 0,
            #'Average Lobby Size': sum(lobby_sizes[player]) / len(lobby_sizes[player]) if lobby_sizes[player] else 0
        } for player in player_names if player != selected_player and total_games_with_each_player[player] > 0]

        # Convert to DataFrame
        stats_df = pd.DataFrame(stats_data)

        # Sort the DataFrame by 'Win Percentage' in descending order
        stats_df = stats_df.sort_values(by='Win Percentage', ascending=False)

        # Convert 'Win Percentage' to string format with '%' for display after sorting
        stats_df['Win Percentage'] = stats_df['Win Percentage'].apply(lambda x: f"{x:.2f}%")

        # Display the sorted DataFrame
        st.dataframe(stats_df)

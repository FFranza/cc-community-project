import json
import pandas as pd
import data_collection

def extract_features(player_data): # Extract features from the player data
    features = {}
    features['current level'] = player_data['account']['level'] # Get the player's current level
    features['time_investment'] = player_data['global_stats']['solo']['minutesplayed'] # Total Minutes Played
    features['total_wins'] = player_data['global_stats']['solo']['placetop1'] # Total Wins in Solo
    features['win_percentage'] = player_data['global_stats']['solo'].get('winrate') # Winrate of Player
    features['kill/death'] = player_data['global_stats']['solo']['kd'] # KDA of Player
    features['kills'] = player_data['global_stats']['solo']['kills'] # Total Kills
    features['matchesplayed'] = player_data['global_stats']['solo']['matchesplayed'] # Total Matches Played

    return features

def calculate_level_changes(season_history):
    all_level_changes = []
    start_index = 0 

    while start_index < len(season_history):  
        if isinstance(season_history[start_index], dict) and 'level' in season_history[start_index]: 
            break
        elif start_index == 0: 
            print("Skipping initial element at index 0 (might not be a dictionary)")
        else:  
            print(f"Skipping non-dictionary element at index {start_index}")
        start_index += 1

    for i in range(start_index + 1, len(season_history)): 
        if isinstance(season_history[i], dict) and 'level' in season_history[i] and \
           isinstance(season_history[i-1], dict) and 'level' in season_history[i-1]: 
            current_level = season_history[i]['level']
            previous_level = season_history[i-1]['level']
            difference = current_level - previous_level
            all_level_changes.append(difference)

    return {"level_changes": all_level_changes}

def preprocess_data(all_games_data):
    features = extract_features(all_games_data) 
    seasons_level_changes = {}

    for season_data in all_games_data['accountLevelHistory']:
        season_num = season_data['season']
        if season_num not in seasons_level_changes:
            if 'season_history' in season_data:
                changes = calculate_level_changes(season_data['season_history'])
                if changes:
                    seasons_level_changes[season_num] = changes
            else:
                pass  
    return features, seasons_level_changes

def create_player_dataframe(player_stats, features, season_level_changes):
    index = ['current level', 'time_investment', 'total_wins', 'win_percentage', 'kill/death', 'kills', 'matchesplayed'] # Define the index list

    # Ensure that the features dictionary has the same number of keys as the index list
    if len(features) != len(index):
        raise ValueError("Length of features dictionary does not match length of index list")

    df = pd.DataFrame(index=index)  # Create the dataframe with the index
    
    relevant_stats = player_stats.get('global_stats', {}).get('solo', {}) 
    index = relevant_stats.keys()
   
    for stat in index:
        value = relevant_stats.get(stat, 0)
        if value is not None:
            df[stat] = value
    
    df['wins_per_hour'] = df['total_wins'] / (df['minutesplayed'] / 60)
    df['kills_per_match'] = df['kills'] / df['matchesplayed']
    df['average_placement'] = (df['placetop1'] + df.get('placetop5', 0) + df.get('placetop10', 0)) / df['matchesplayed']
    df['is_high_win_rate'] = df['win_percentage'] > 0.30

    return df


from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import data_collection as dc
import data_preprocessing as dp
import logging

def main():
    player_names = ['Ship', 'Queen Jessica176', 'Twitch Rapper', 'zvxa-CJT']
    platforms = ['pc', 'pc', 'pc', 'pc']

    for i, player_name in enumerate(player_names): 
        platform = platforms[i]

        try:
            player_stats = dc.get_player_stats(player_name, platform) # This will return a list of dictionaries
            
            if player_stats:
                features, seasons_level_changes = dp.preprocess_data(player_stats) # Pass the raw data
                df = dp.create_player_dataframe(player_stats, features, seasons_level_changes)  # Pass the processed data
                
                # Isolation Forest for anomaly detection
                X = df[['wins_per_hour', 'average_placement', 'kills_per_match', "kill/death"]]

                model = OneClassSVM(nu=0.005, kernel='rbf', gamma='scale')
                
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X) 
                
                model.fit(X_scaled)
                print("Scaled Data Sample:\n", X_scaled[:5])

                y_pred = model.predict(X_scaled)
                
                anomalies = X[y_pred == -1]  # Points labeled as -1 are considered outliers by DBSCAN

                print("Potential Anomalies:\n", anomalies)
                print("Number of Potential Anomalies:", anomalies.shape[0])

                # THIS IS FOR TESTING PURPOSES
                print("Preprocessed Features:\n", features)  # Use this to check if features are being extracted
                print(df)  # Use this to check if data frames are working

            else:
                logging.error("Failed to retrieve player stats for %s on %s", player_name, platform) # Log the error
        except Exception as e: 
            logging.error("An error occurred: %s", e) # Log the error

if __name__ == "__main__": # Check if the script is being run directly
    logging.basicConfig(level=logging.ERROR) # Set the logging level
    main() # Call the main function
import requests
import json
import os

# Use Environment Variables to secure links and API Key
api_key = os.getenv('API_key') 
base_url = os.getenv('API_global_player_stats')
lookup_url = os.getenv('API_account_id')

def get_account_id(player_name): # Function to find the account id of the player
    url = f"{lookup_url}?username={player_name}" # Base url + player_name
    headers = {'Authorization': api_key} # Uses api_key for authorization
    
    response = requests.get(url, headers=headers) # Requesting for the API

    if response.status_code == 200: # Checks if request is successful
        data = response.json() # Stores json in data variable
        account_id = data.get('account_id') # Gets the account id from the json
        
        if account_id:
            return account_id # Returns the account id
        else:
            print("Account ID not found.") # Error catch if Account ID was not found
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}") # Error catch if request was not successful

def get_player_stats(player_name, platform): # Function to get player stats after request of account id
    account_id = get_account_id(player_name) 

    if not account_id: # Checks if account id was found
        return None

    url = f"{base_url}?account={account_id}&platform={platform}" # Base url + account id + platform
    headers = {'Authorization': api_key} # Uses api_key for authorization
    params = {'account': account_id, 'platform': platform} # Parameters for account and platform for request

    response = requests.get(base_url, headers=headers, params=params) # Requesting for the API with parameters

    if response.status_code == 200: # Checks if request is successful
        data = response.json() # Stores json in data variable
        return data
    else:
        print(f"Error: {response.status_code}") # Error catch if request was not succesful
        return None

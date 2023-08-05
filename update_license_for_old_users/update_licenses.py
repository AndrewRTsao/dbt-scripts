import requests
import json
import os
import pandas as pd
import datetime
from dateutil.parser import parse

def main():

    # Retrieve relevant environment variables from env.sh for this script execution (needs to be pre-populated and sourced by end user)
    base_url = os.getenv('BASE_URL')
    account_id = os.getenv('ACCOUNT_ID')
    auth_token = os.getenv('API_KEY')
    days_to_cutoff = os.getenv('DAYS_TO_CUTOFF')

    # Create session headers for API calls
    headers = {'Authorization': f'Bearer {auth_token}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

    # Establish requests session object as we will be submitting multiple requests to API endpoints within this script
    session = requests.Session()
    session.headers.update(headers)
    print("printing session headers")
    print(session.headers)


    # Defining sub functions that will be called later in the script

    def retrieve_users_in_account(base_url, account_id):

         # Construct API endpoint to call
        url_endpoint = base_url + '/api/v2/accounts/' + account_id + '/users/'

        try:
            print("Attempting to retrieve list of users from account " + account_id)
            response = session.get(url_endpoint)
            response.raise_for_status()
            print(response)
            print("List of users in account retrieved")

            # Retrieve json payload
            users_payload = response.json()
            users = users_payload['data']

            return users
        except requests.exceptions.HTTPError as errh:
            print(errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            raise
        except requests.exceptions.Timeout as errt:
            print(errt)
            raise
        except requests.exceptions.RequestException as err:
            print(err)
            raise

    def check_if_user_is_inactive(last_login, days_to_cutoff):

        # Convert last_login to date
        last_login_date = parse(last_login).date()

        # Calculate how many days has it been since last login
        today = datetime.date.today()
        days_since_last_login = today - last_login_date

        print("checking if user is inactive")
        if days_since_last_login.days > int(days_to_cutoff):
            print("This user is considered inactive")
            return True
        else:
            print("This user should still be considered active")
            return False
        
    def update_inactive_user_license(base_url, account_id, license_id, payload):

        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v2/accounts/' + account_id + '/permissions/' + license_id

        try:
            print("Attempting to update license for user")
            response = session.post(url_endpoint, data=payload)
            response.raise_for_status()
            print(response)
            print("User license updated")
        
        except requests.exceptions.HTTPError as errh:
            print(errh)
            raise
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            raise
        except requests.exceptions.Timeout as errt:
            print(errt)
            raise
        except requests.exceptions.RequestException as err:
            print(err)
            raise


    # Retrieve list of current users in provided account
    users = retrieve_users_in_account(base_url, account_id)

    # Creating empty DF to store inactive users so we can output this data later
    inactive_users_df = pd.DataFrame(columns=['user_id', 'first_name', 'last_name', 'email', 'last_login'])
    
    # Iterate through users and check if user is inactive. If so, change license from "developer" to "read_only" (plus save the user info).
    for user in users:

        print("User ID: " + str(user['id']))
        print("First Name: " + user['first_name'])
        print("Last Name: " + user['last_name'])
        print("Email Address: " + user['email'])
        print("Last Login: " + user['last_login'])
        print("License Type: " + user['permissions'][0]['license_type'])
        print("License ID: " + str(user['permissions'][0]['id']))
        print("License State: " + str(user['permissions'][0]['state']))

        # Check if last login > cutoff period
        user_is_inactive = check_if_user_is_inactive(user['last_login'], days_to_cutoff)

        if user_is_inactive:

            print("User " + user['first_name'] + user['last_name'] + " with User ID " +  str(user['id']) + " is inactive!")
            
            # Storing user information in dataframe so we can store the output later
            user_data = {}

            user_data['user_id'] = user['id']
            user_data['first_name'] = user['first_name']
            user_data['last_name'] = user['last_name']
            user_data['email'] = user['email']
            user_data['last_login'] = user['last_login']

            user_df = pd.DataFrame(user_data, index=[0])

            # Appending this data to the inactive_users_df
            inactive_users_df = pd.concat([inactive_users_df, user_df], ignore_index=True)
            
            # Retrieve corresponding license id for inactive user
            license_id = user['permissions'][0]['id']
            
            # Construct license payload so we can update the license
            license_data = {}
            
            license_data['id'] = license_id
            license_data['license_type'] = 'read_only' # Assign read-only license to user
            license_data['user_id'] = user['id']
            license_data['account_id'] = int(account_id)
            license_data['state'] = user['permissions'][0]['state']

            # Converting object into JSON format
            json_payload = json.dumps(license_data)

            # Update ianctive user's license
            update_inactive_user_license(base_url, account_id, str(license_id), json_payload)

        else:

            print("User " + user['first_name'] + user['last_name'] + " with User ID " +  str(user['id']) + " is still active!")

        print("----------------------------------------")

    print("Done iterating through all users")

    # Output list of inactive users as a CSV file
    print("Printing out CSV file of inactive users")
    inactive_users_df.to_csv('inactive_users.csv', index=False)


if __name__ == "__main__":
    print("Kicking off update_licenses.py script!")
    main()
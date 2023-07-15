import os
import json
import requests
 

def main():

    # Retrieve relevant environment variables from env.sh for this script execution (needs to be prepopulated)
    base_url = os.getenv('BASE_URL')
    account_id = os.getenv('ACCOUNT_ID')
    source_project_id = os.getenv('SOURCE_PROJECT_ID')
    target_project_id = os.getenv('TARGET_PROJECT_ID')
    auth_token = os.getenv('API_KEY')

    # Create session headers for API calls
    headers = {'Authorization': f'Bearer {auth_token}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

    # Establish session object as we will be making multiple requests within this script
    session = requests.Session()
    session.headers.update(headers)
    print("printing session headers")
    print(session.headers)


    # sub functions

    def retrieve_environments_from_project(base_url, account_id, project_id):

        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v3/accounts/' + account_id + '/projects/' + project_id + '/environments/'

        try:
            print("Attempting to retrieve environments from project ID " + project_id)
            response = session.get(url_endpoint)
            response.raise_for_status()
            print(response)

            # Retrieve json payload
            environments_payload = response.json()
            environments = environments_payload['data']

            return environments
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

    def create_deployment_environment(base_url, account_id, project_id, payload):

        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v3/accounts/' + account_id + '/projects/' + project_id + '/environments/'

        try:
            print("Attempting to create deployment environment now")
            response = session.post(url_endpoint, data=payload)
            response.raise_for_status()
            print(response)
            
            # Retrieve resulting json payload so we can map old environment id to new environment id
            job_details = response.json()['data']
            return job_details
        
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
        
    
    def retrieve_jobs_from_project(base_url, account_id, project_id):
        
        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v2/accounts/' + account_id + '/jobs?project_id=' + project_id

        try:
            print("Attempting to retrieve jobs from project ID " + project_id)
            response = session.get(url_endpoint)
            response.raise_for_status()
            print(response)

            # Retrieve json payload
            jobs_payload = response.json()
            jobs = jobs_payload['data']

            return jobs
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

    def create_job_in_project(base_url, account_id, payload):

        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v2/accounts/' + account_id + '/jobs/'

        try:
            print("Attempting to create job in project now")
            response = session.post(url_endpoint, data=payload)
            response.raise_for_status()
            print(response)
            print("job creation done")
        
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

    def retrieve_env_vars_from_project(base_url, account_id, project_id):

        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v3/accounts/' + account_id + '/projects/' + project_id + '/environment-variables/environment/'

        try:
            print("Attempting to retrieve env vars from project ID " + project_id)
            response = session.get(url_endpoint)
            response.raise_for_status()
            print(response)

            # Retrieve json payload
            env_vars_payload = response.json()
            print("printing env_vars_payload")
            print(env_vars_payload)

            env_vars = env_vars_payload['data']

            print("printing env_vars")
            print(env_vars)
            print("checking type")
            print(type(env_vars))
            return env_vars

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

    def create_env_var_in_project(base_url, account_id, project_id, payload):

        # Construct API endpoint to call
        url_endpoint = base_url + '/api/v3/accounts/' + account_id + '/projects/' + project_id + "/environment-variables/bulk/"

        try:
            print("Attempting to create env var in project now")
            response = session.post(url_endpoint, data=payload)
            response.raise_for_status()
            print(response)
            print("env var creation done")
        
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
    

    
    
    # Retrieve environments from source project and port them to target project
    environments = retrieve_environments_from_project(base_url, account_id, source_project_id)

    # Create dict to map environment ID from source project to new environment ID created in target project (necessary later for porting jobs)
    environment_map = {}
    
    print("iterating through environments")
    for environment in environments:
        if environment['type'] == "deployment":
            print("Creating deployment environment " + environment['name'] + " for project ID " + target_project_id)

            # Constructing JSON body to pass in POST request
            print("Creating JSON body")

            data = {}          
            data['id'] = None
            data['account_id'] = environment['account_id']
            data['project_id'] = int(target_project_id)
            data['credentials_id'] = environment['credentials_id']
            data['name'] = environment['name']
            data['dbt_version'] = environment['dbt_version']
            data['type'] = environment['type']
            data['use_custom_branch'] = environment['use_custom_branch']
            data['custom_branch'] = environment['custom_branch']

            print("checking type before json dumps for envs")
            print(type(data))
            
            json_payload = json.dumps(data)
            print("printing json_payload")
            print(json_payload)
            print("checking type again")
            print(type(json_payload))

            new_environment = create_deployment_environment(base_url, account_id, target_project_id, json_payload)

            # Appending the source env id and new target env id as part of a dict
            old_env_id = environment['id']
            new_env_id = new_environment['id']
            print("old env ID: " + str(old_env_id))
            print("new env ID: " + str(new_env_id))
            environment_map[old_env_id] = new_env_id

        else:
            print("Skip - this is a development environment")
    
    print("printing env ID map dict")
    print(environment_map)
    

    # Retrieve jobs from source project and port them to target project
    jobs = retrieve_jobs_from_project(base_url, account_id, source_project_id)

    print("iterating through jobs")
    for job in jobs:
        
        print("checking old job payload from source")
        print(job)

        print("creating JSON body")
        data = {}
        
        # Need to make job id null when creating new job
        data['id'] = None
        
        # Copy relevant params from source job body for new target job payload
        data['account_id'] = job['account_id']
        data['project_id'] = int(target_project_id)

        # Calculating new env ID in target project for this job that maps to the old env ID in source project
        source_env_id = job['environment_id']
        target_env_id = environment_map[source_env_id]
        data['environment_id'] = target_env_id

        data['name'] = job['name']
        data['dbt_version'] = job['dbt_version']
        data['triggers'] = job['triggers']
        data['execute_steps'] = job['execute_steps']
        data['settings'] = job['settings']
        data['execution'] = job['execution']
        data['state'] = job['state']
        data['generate_docs'] = job['generate_docs']
        data['schedule'] = job['schedule']

        # convert to JSON
        json_payload = json.dumps(data)

        print("checking new job payload to use in target after updates")
        print(json_payload)

        print("but what is the type?")
        print(type(json_payload))

        print("Calling function now to create job " + job['name'] + " in target project ID " + target_project_id)

        create_job_in_project(base_url, account_id, json_payload)


    # Retrieve env vars from source project and port them to target project
    env_vars = retrieve_env_vars_from_project(base_url, account_id, source_project_id)
    variables = env_vars['variables']

    print("final check")
    print(variables)
    print(type(variables))

    print("iterating through individual variables to create")
    for variable in variables:

        print("creating JSON body for env var creation")
        data = {}

        # Copy necessary params from source env vars into new payload body in right structure

        data['name'] = variable
        data['ids'] = []
        data['new_name'] = variable

        # Environments with corresponding env values are nested so need to retrieve and loop through them

        nested_envs = variables[variable].items()
        for nested_env in nested_envs:

            # Storing environment name as key and associated nested dict value as env var value
            data[nested_env[0]] = nested_env[1]['value']

        print("printing data body")
        print(data)

        # Don't forget to nest this JSON body within a "parent" env_var body
        final_payload = {}
        final_payload['env_var'] = data

        print("checking final_payload")
        print(final_payload)


        # convert to JSON
        json_payload = json.dumps(final_payload)
        print("checking json_payload")
        print(json_payload)
        print(type(json_payload))
        
        # Create env var in target project
        create_env_var_in_project(base_url, account_id, target_project_id, json_payload)

    
    print("script complete - please check your new project")


if __name__ == "__main__":
    print("Kicking off migrate_project.py script")
    main()
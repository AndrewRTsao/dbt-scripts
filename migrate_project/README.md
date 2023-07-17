# Intro

This python script can be used to migrate a dbt project to a target new dbt project on the same dbt Cloud instance by using the [dbt Cloud Management APIs ](https://documenter.getpostman.com/view/14183654/UyxohieD#intro). 

# Getting Started

1. Clone this repo to where you plan to be executing the python script (e.g. local machine). If on a corporate network or behind a firewall, please make sure that the dbt Cloud instance is reachable by the script or you will run into network connectivity issues with the API calls.

2. Create a virtual environment and pip install requirements.txt

```sh
pip install --trusted-host pypip.python.org -r requirements.txt
```

3. Create a new project in your account / dbt Cloud instance by following the project creation workflow.

4. Fill out the environment variables in **env.sh** with the necessary information from your dbt Cloud instance and origin / target projects, then source the file. 

```sh
source env.sh
```

*Note: The values of the environment variables should be kept within existing double quotes.* 

5. Run the **migrate_project.py** script to kick off the migration process. This will copy all environments, jobs, and environment variables from the original project to the new target project (as specified in the **env.sh** file)

```sh
python migrate_project.py
```

*Note: The script itself should work but is also meant to serve as a starting template. Feel free to update the script accordingly if you wish to implement advanced logic.*

6. Please note that once the script completes, you will still need to input / update credentials in your target project. Please see the limitations described below. 

## Limitations of script / Post-script action items

While the script will copy over the environments, jobs, and environment variables, certain items will still need to be reviewed and updated manually. Please note the following:
- Connection settings and credentials for your new environments (in your target project)
- Environment variable overrides *at the job or profile level*
- Run history and other historical information will **not** be preserved between source and target projects

If the migration doesn't proceed as expected, you can delete the target project and start over. The original source project will not be touched or impacted by this script.


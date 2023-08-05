# Intro

This python script can be used to check whether users have exceeded a certain "threshold" (e.g. last_login_date > threshold) and automatically update the license type for these users from "developer" to "read_only". This sciprt was built using the [dbt Cloud Admin APIs](https://docs.getdbt.com/dbt-cloud/api-v2#/).

# Getting Started

1. Clone this repo locally to where you'll be executing the python script. If on a corporate network or behind a firewall, please make sure that the dbt Cloud instance is reachable by the script or you will run into potential network connectivity issues when executing the API calls.

2. Create a virtual environment and `pip install requirements.txt`

```she
pip install --trusted-host pypip.python.org -r requirements.txt
```

3. Fill out the environment variables in **env.sh** with the required information, then source the file.

```sh
source env.sh
```

4. Run the **update_licenses.py** script to kick off the license check automation.

```sh
python update_licenses.py
```

5. Once the script completes, besides updating the licenses for your inactive users, there will also be a resulting *inactive_users.csv* file, containing a list of all identified inactive users for your reference. 

This script is meant to only be a starting point. Please also reference the limitations below.

## Limitations of python script / post-script action items

A few things to note of with regards to this script (feel free to use it as a template):
- This script will only work on an individual account level. For multiple accounts, you will need to either update the environment variables accordingly and rerun it or implement an additional loop to iterate through the accounts as well. 
- This script will not check the existing license type of the identified inactive user. It shouldn't make much of a difference but it will reapply the read-only license to users who are considered inactive by the script. 
- There are no retry handling baked into the script. From a best practices standpoint, retries should be incorporated from a hardening perspective in case of transient failures. 
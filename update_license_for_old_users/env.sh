# Information about your dbt Cloud instance needed for script to run
export BASE_URL="" # Base URL for your dbt Cloud instance, e.g. https://cloud.getdbt.com
export ACCOUNT_ID="" # Account ID for your account. Check this by opening Account Settings and looking in URL
export API_KEY="" # API key / User token / Service token (to make API requests)
export DAYS_TO_CUTOFF=30 # Maximum number of days since last login before we consider an user "inactive" and downgrade their license (e.g. 30 days)
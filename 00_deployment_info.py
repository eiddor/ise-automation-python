# 00_deployment_info.py
#
# This script will gather deployment info from your ISE instance. Some of this may be interesting to you,
# but mostly it's just informational. I may modify this playbook in the future to gather
# some useful info that can be used by subsequent playbooks (policy and rule IDs),
# or maybe gather all of the data that we configure for comparison

import yaml  # import pyyaml package

# open the credentials yaml file and load it into data
with open('credentials.yaml') as f:
    data = yaml.safe_load(f)

# Pull in the Cisco ISE SDK
from ciscoisesdk import IdentityServicesEngineAPI

# define our API with credentials from credentials.yaml
api = IdentityServicesEngineAPI(username=data['ise_username'], 
                                password=data['ise_password'],
                                uses_api_gateway=True,
                                base_url='https://' + data['ise_hostname'],
                                version=data['ise_version'],
                                verify=data['ise_verify'])

# Get our deployment version and put it in a variable
ise_deployment_version = api.pull_deployment_info.get_version()

# Print the variable plus some deep thoughts
print("Suck it, Python " + ise_deployment_version.text)
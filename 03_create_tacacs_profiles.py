# 03_create_tacacs_profiles.py
#
# This file will create a TACACS profile and command set that will be assigned to authenticated users.
# For the purposes of this repo, the profile and command set are basic. It will simply assign privilege
# 15 and allow all commands for an authenticated user.

import yaml  # import pyyaml package

# open the yaml file and load it into data
with open('credentials.yaml') as f:
    data = yaml.safe_load(f)

# Pull in the Cisco ISE SDK
from ciscoisesdk import IdentityServicesEngineAPI

# define our API 
api = IdentityServicesEngineAPI(username=data['ise_username'], 
                                password=data['ise_password'],
                                uses_api_gateway=True,
                                base_url='https://' + data['ise_hostname'],
                                version=data['ise_version'],
                                verify=data['ise_verify'])


# Define our session attributes to send TACACS privilege 15
# I broke this out to separate lines to silence John
#
# Also, since we're name-dropping in comments, shoutout to Sue
# 
# https://twitter.com/sueinphilly/status/1457748734218055686?s=20
#
# 10 REM For Sue
# 20 PRINT Hi Sue
# 30 GOTO 20

attributes = {"sessionAttributeList": [{"type": "MANDATORY", 
                                        "name": "priv-lvl", 
                                        "value": "15"}, 
                                        {"type": "MANDATORY", 
                                        "name": "max_priv_lvl", 
                                        "value": "15"}]}

# Create a new TACACS profile called "PermitAllShell" which will give TACACS privilege 15
api.tacacs_profile.create_tacacs_profile(name="PermitAllShell",
                                        description="Permit all",
                                        session_attributes=attributes
                                        )

# Create a new TACACS command set called "PermitAllCommands" which will allow all commands
api.tacacs_command_sets.create_tacacs_command_sets(name="PermitAllCommands",
                                        description="PermitAllCommands Command Set",
                                        permit_unmatched=True
                                        )
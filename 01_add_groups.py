# 01_add_groups.py
#
# This file will create user identity groups in the internal ISE identity store.
# You should not need to modify this file as it will dynamically read all of the groups
# from groupsandusers.yaml.

import yaml  # import pyyaml package

# open the credentials.yaml file and load it into data
with open('credentials.yaml') as f:
    data = yaml.safe_load(f)

# open the groupsandusers.yaml file and load it into groups
with open('groupsandusers.yaml') as g:
    groups = yaml.safe_load(g)

# Pull in the Cisco ISE SDK
from ciscoisesdk import IdentityServicesEngineAPI

# define our API with credentials from credentials.yaml
api = IdentityServicesEngineAPI(username=data['ise_username'], 
                                password=data['ise_password'],
                                uses_api_gateway=True,
                                base_url='https://' + data['ise_hostname'],
                                version=data['ise_version'],
                                verify=data['ise_verify'])

# iterate through the list of groups and create them using the information in credentials.yaml
for groupname in groups['usergroups']:
        api.identity_groups.create_identity_group(name=groupname['name'], 
                                                description=groupname['desc'],
                                                parent="NAC Group:NAC:IdentityGroups:User Identity Groups")
        print("Creating group:", groupname['name'])
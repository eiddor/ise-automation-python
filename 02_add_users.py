# 02_add_users.py
#
# This file will create users and assign them to the appropriate groups.  It should be run after
# 01_add_groups.py as it will query ISE for the created groups and their corresponding ids.
# You should not need to modify this file as it will dynamically read all of the users and groups
# from groupsandusers.yaml.
#
# The group name to group id matching and variable assignment is kind of irritating, but..... 
#
# Actually it's more that ISE requires a group id instead of a group name when creating a user.

import yaml  # import pyyaml package

# open the yaml file and load it into data
with open('credentials.yaml') as f:
    data = yaml.safe_load(f)

# open the groupsandusers.yaml file and load it into groups
with open('groupsandusers.yaml') as g:
    groups = yaml.safe_load(g)

# Pull in the Cisco ISE SDK
from ciscoisesdk import IdentityServicesEngineAPI

# define our API 
api = IdentityServicesEngineAPI(username=data['ise_username'], 
                                password=data['ise_password'],
                                uses_api_gateway=True,
                                base_url='https://' + data['ise_hostname'],
                                version=data['ise_version'],
                                verify=data['ise_verify'])

# We're going to iterate through the list of users and create them using the information in credentials.yaml,
# but first we need to get the group id for each group
for groupname in groups['userlist']:
        groupinfo = api.identity_groups.get_identity_group_by_name(name=groupname['groups']).response
        groupid = groupinfo.IdentityGroup.id
        api.internal_user.create_internal_user(name=groupname['name'],
                                                first_name=groupname['firstname'],
                                                last_name=groupname['lastname'],
                                                description=groupname['description'],
                                                password=groups['default_password'],
                                                change_password=False,
                                                identity_groups=groupid,
                                                password_idstore="Internal Users")
        print("Creating user:", groupname['name'])
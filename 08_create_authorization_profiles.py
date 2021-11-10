# 08_create_authorization_profiles.py
#
# This file will create authorization profiles for wired and wireless network access users.
# The reason we need to have separate profiles for wired and wireless is because Cisco WLCs
# accept a different RADIUS attribute for VLAN assignments than Cisco switches.  Please don't ask me why.
#
# All data for the profiles (names and VLANs) is pulled from the policy.yaml file and then there will be
# a wired and wireless profile created for each.
#
# I'm using a different way to wrap strings around a variable in the description field below
# because apparently the way I've been doing it is some old way and Google failed me
#
# You should not have to edit this file unless you want to add more fields or customize further.

import yaml  # import pyyaml package

# open the yaml file and load it into data
with open('credentials.yaml') as f:
    data = yaml.safe_load(f)

# open the policy.yaml file and load it into the policy variable
with open('policy.yaml') as g:
    policy = yaml.safe_load(g)

# Pull in the Cisco ISE SDK
from ciscoisesdk import IdentityServicesEngineAPI

# define our API 
api = IdentityServicesEngineAPI(username=data['ise_username'], 
                                password=data['ise_password'],
                                uses_api_gateway=True,
                                base_url='https://' + data['ise_hostname'],
                                version=data['ise_version'],
                                verify=data['ise_verify'])

# We'll use this set this so that we don't try to create duplicate profiles (the script will break)
already_created = set()

# iterate through policies in policy.yaml to create each profile
# I probably should have done this in one loop - I'll come back and fix that later.
for policies in policy['policies']:
    if policies['policy'] not in already_created: # check for duplicate

# some VLAN data for our command
        vlandata = {
                    "nameID" : policies['vlan'],
                    "tagID" : 1
                }

# Create our wired profiles               
        api.authorization_profile.create_authorization_profile(name=policies['policy'] + "_wired", 
                                            description="wired profile for " + policies['policy'] + " users - automated",
                                            access_type="ACCESS_ACCEPT",
                                            authz_profile_type="SWITCH",
                                            easywired_session_candidate=False,
                                            profile_name="Cisco",
                                            service_template=False,
                                            track_movement=False,
                                            vlan=vlandata
                                            )
        print("Creating Authorization Profile: " + policies['policy'] + "_wired")
        already_created.add(policies['policy']) # add the policy to our set for duplicate checking

# We'll use this set this so that we don't try to create duplicate profiles (the script will break)
already_created = set()

# Iterate through policies in policy.yaml to create each profile
for policies in policy['policies']:
    if policies['policy'] not in already_created: # check for duplicate

# Some attribute data for our command
        attributedata = [{
                "leftHandSideDictionaryAttribue" : {
                    "AdvancedAttributeValueType" : "AdvancedDictionaryAttribute",
                    "dictionaryName" : "Airespace",
                    "attributeName" : "Airespace-Interface-Name"
                },
                "rightHandSideAttribueValue" : {
                    "AdvancedAttributeValueType" : "AttributeValue",
                    "value" : policies['vlan']
                }
        }]

# Create our wireless profiles  
        api.authorization_profile.create_authorization_profile(name=policies['policy'] + "_wireless", 
                                            description="wireless profile for " + policies['policy'] + " users - automated",
                                            access_type="ACCESS_ACCEPT",
                                            authz_profile_type="SWITCH",
                                            easywired_session_candidate=False,
                                            profile_name="Cisco",
                                            service_template=False,
                                            track_movement=False,
                                            advanced_attributes=attributedata
                                            )
        print("Creating Authorization Profile: " + policies['policy'] + "_wireless")
        already_created.add(policies['policy']) # add the policy to our set for duplicate checking
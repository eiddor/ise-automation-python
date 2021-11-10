# 12_access_point_profiling.py
#
# This file will create authorization profiles and policies that will detect Cisco Access Points
# and place them in a VLAN.
#
# It relies on the Guest workflow configured earlier in order to profile the AP during the GuestRedirect flow.
#
# You probably want to enable Change of Authorization (CoA) in ISE so that the AP can be re-authorized after it is
# profiled.
#
# The VLAN that the AP will be placed on is defined in policy.yaml
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

# First we have to get the information for all device admin policy sets
policysets = api.network_access_policy_set.get_network_access_policy_sets()

# Then we have to pull the policy ID for the Default policy set
policyId = policysets.response.response[0].id

# create our policy rule object, or array, or list, or dictionary, or whatever.
# Jose told me to use underscores in my variable names
#
ap_policy_rule = {
    "default" : False,
    "name" : "CiscoAccessPoint",
    "rank" : 8,
    "condition" : {
        "conditionType" : "ConditionAttributes",
        "isNegate" : False,
        "dictionaryName" : "EndPoints",
        "attributeName" : "EndPointPolicy",
        "operator" : "equals",
        "attributeValue" : "Cisco-Device:Cisco-Access-Point"
    }
}

vlan_data = {
            "nameID" : policy['accesspoint']['vlan'],
            "tagID" : 1
        }

# Create our Cisco Access point authz profile and rule
api.authorization_profile.create_authorization_profile(name="CiscoAccessPoint", 
                                    description="Cisco Access point profile",
                                    access_type="ACCESS_ACCEPT",
                                    authz_profile_type="SWITCH",
                                    easywired_session_candidate=False,
                                    profile_name="Cisco",
                                    service_template=False,
                                    track_movement=False,
                                    vlan=vlan_data,
                                    )

api.network_access_authorization_rules.create_network_access_authorization_rule(policy_id=policyId,
                                                                                profile=["CiscoAccessPoint"],
                                                                                rule=ap_policy_rule 
                                                                                )
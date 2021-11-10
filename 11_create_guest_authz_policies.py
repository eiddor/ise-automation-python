# 11_create_guest_authz_policies.py
#
# This file will create authorization policies required for a wired guest workflow in ISE.
#
# See the comments in 10_create_guest_authz_profiles.py for more info about the wired guest workflow.
#
# The way the rules are ordered, any wired non-authenticated devices or clients will hit the GuestRedirect rule
# and get limited network access in the Guest VLAN.
#
# This will allow a wired user to access the guest portal and authenticate before being put back into
# the process and hitting the GuestAccess rule.
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

# In earlier scripts I used some really convoluted ways to get this stupid condition ID.  
# This way is much simpler
# Get the Wired_MAB network access condition ID and set it to a variable
wiredmab = api.network_access_conditions.get_network_access_condition_by_name(name="Wired_MAB")

# Oh crap I just remembered that I could have used this method for some of the previous scripts
wiredmabId = wiredmab.response.response.id

# create our policy rule object, or array, or list, or dictionary, or whatever.
guestredirectrule = {
    "default" : False,
    "name" : "GuestRedirect",
    "rank" : 9,
    "condition" : {
        "conditionType" : "ConditionReference",
        "isNegate" : False,
        "name" : "Wired_MAB",
        "id" : wiredmabId
    }
}

guestaccessrule =  {
    "default" : False,
    "name" : "GuestAccess",
    "rank" : 8,
    "condition" : {
        "conditionType" : "ConditionAndBlock",
        "isNegate" : False,
        "children" : [ {
            "conditionType" : "ConditionAttributes",
            "isNegate" : False,
            "dictionaryName" : "IdentityGroup",
            "attributeName" : "Name",
            "operator" : "equals",
            "attributeValue" : "Endpoint Identity Groups:GuestEndpoints"
            }, {
            "conditionType" : "ConditionReference",
            "isNegate" : False,
            "name" : "Wired_MAB",
            "id" : wiredmabId
        } ]
    }
}

# Create rules for Guest Redirect and Guest Access
api.network_access_authorization_rules.create_network_access_authorization_rule(policy_id=policyId,
                                                                                security_group=policy['guest']['sgt'],
                                                                                profile=["GuestAccess"],
                                                                                rule=guestaccessrule
                                                                                )

api.network_access_authorization_rules.create_network_access_authorization_rule(policy_id=policyId,
                                                                                security_group=policy['guest']['sgt'],
                                                                                profile=["GuestRedirect"],
                                                                                rule=guestredirectrule
                                                                                )

# 09_create_authorization_policies.py
#
# This file will create authorization policies in the "Default" policy set for wired and wireless network
# access users.
#
# All data for the profiles (names, groups, VLANs, and SGTs) is pulled from the policy.yaml file and there will be
# a wired and wireless policy created for each entry.
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

# First we have to get the information for all network access policy sets
policysets = api.network_access_policy_set.get_network_access_policy_sets()

# Then we have to pull the policy ID for the Default policy set
policyId = policysets.response.response[0].id

# Then we use the policy ID to grab all of the network access authc rules
rulesets = api.network_access_authentication_rules.get_network_access_authentication_rules(policy_id=policyId)

# Now we need some condition and rule IDs
# This is still stupid, everything is still stupid, I still hate JSON
# I am still probably doing this wrong (I was)
# I still don't care
defaultruleId = [x['rule.id'] for x in rulesets.response.response if x['rule.name'] == 'Default']
dot1xruleId = [x['rule.id'] for x in rulesets.response.response if x['rule.name'] == 'Dot1X']

# Some people, including Brooks from Twitter, think 
# that
# multiline comments ma
# ke things unreadable.

# These IDs are nested so we have to do some stupid crap to get them - I learned later on that there's a better
# way to get these values, but I'm leaving it here for posterity
#
# iterate through all of the condition children in the response to find the conditions that we want
# 
# I had to use try/except here because not every element had a "children" attribute, so we ignore those ones
for z in range(len(rulesets.response.response)):
    try:
        wireddot1xcondId = [y['id'] for y in rulesets.response.response[z].rule.condition.children if y['name'] == 'Wired_802.1X']
        wirelessdot1xcondId = [y['id'] for y in rulesets.response.response[z].rule.condition.children if y['name'] == 'Wireless_802.1X']
    except AttributeError: pass

for policies in policy['policies']:

# create our policy rule object, or array, or list, or dictionary, or whatever.

    wiredpolicyrule = {
        "default" : False,
        "name" : policies['usergroup'] + "_users_wired",
        "rank" : 1,
        "condition" : {
            "conditionType" : "ConditionAttributes",
            "isNegate" : False,
            "dictionaryName" : "IdentityGroup",
            "attributeName" : "Name",
            "operator" : "equals",
            "attributeValue" : "User Identity Groups:" + policies['usergroup']
        }
    }

    wirelesspolicyrule =  {
        "default" : False,
        "name" : policies['usergroup'] + "_users_wireless",
        "rank" : 0,
        "condition" : {
            "conditionType" : "ConditionAndBlock",
            "isNegate" : False,
            "children" : [ {
                "conditionType" : "ConditionAttributes",
                "isNegate" : False,
                "dictionaryName" : "IdentityGroup",
                "attributeName" : "Name",
                "operator" : "equals",
                "attributeValue" : "User Identity Groups:" + policies['usergroup']
                }, {
                "conditionType" : "ConditionReference",
                "isNegate" : False,
                "name" : "Wireless_802.1X",
                "id" : wirelessdot1xcondId[0],
            } ]
        }
    }

# Create rules for both wireless and wired users because some of our devices expect different RADIUS attributes
    api.network_access_authorization_rules.create_network_access_authorization_rule(policy_id=policyId,
                                                                                    security_group=policies['sgt'],
                                                                                    profile=[policies['policy'] + "_wireless"],
                                                                                    rule=wirelesspolicyrule
                                                                                    )

    api.network_access_authorization_rules.create_network_access_authorization_rule(policy_id=policyId,
                                                                                    security_group=policies['sgt'],
                                                                                    profile=[policies['policy'] + "_wired"],
                                                                                    rule=wiredpolicyrule
                                                                                    )
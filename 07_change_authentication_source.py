# 07_change_authentication_source.py
#
# This file will simply change the identity source of the default and dot1x network access policy to use
# internal users instead of all user stores, similar to 04_change_tacacs_authc_source.py
#
# It's not strictly necessary to do this, but it can sometimes speed up authc for a lab environment
# that doesn't have to talk to an AD or LDAP for network access user information.
#
# This was the most annoying playbook to develop because there are some things that we need
# from ISE (policy id and a bunch of rule/condition ids) in order to change the setting.  To get these
# values I had to create some really ugly and irritating JSON filters and use loops.  
# There was probably an easier way to get the values (narrator: THERE WAS),
# but I'm new to all of this nonsense and it's all I could come up with on my own.
#
# ISE's API also required a bunch of seemingly random fields to be sent all so we can set
# this: identitySourceName: "Internal Users"

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

# First we have to get the information for all device admin policy sets
policysets = api.network_access_policy_set.get_network_access_policy_sets()

# Then we have to pull the policy ID for the Default policy set
policyId = policysets.response.response[0].id

# Then we use the policy ID to grab all of the device administration authc rules
rulesets = api.network_access_authentication_rules.get_network_access_authentication_rules(policy_id=policyId)

# Now we need some condition and rule IDs
# This is stupid, everything is stupid, I hate JSON
# I am probably also doing this wrong (yep)
# I don't care
defaultruleId = [x['rule.id'] for x in rulesets.response.response if x['rule.name'] == 'Default']
dot1xruleId = [x['rule.id'] for x in rulesets.response.response if x['rule.name'] == 'Dot1X']

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

# But wait, the ISE API needs some mandatory fields for some reason
defaultruledata = {
                "default": True, 
                "name": "Default",
                "rank": 2
                }

dot1xruledata = {
                "default": False, 
                "name": "Dot1X",
                "rank": 1,
                "condition" : {
                    "conditionType" : "ConditionOrBlock",
                    "isNegate" : False,
                    "children" : [ {
                        "conditionType" : "ConditionReference",
                        "name" : "Wired_802.1X",
                        "id" : wireddot1xcondId[0],
                        }, {
                        "conditionType" : "ConditionReference",
                        "name" : "Wireless_802.1X",
                        "id" : wirelessdot1xcondId[0],
                        } ]
                    }
                }

# And now, after all of that work, we can change the identity source in the default and dot1x authc policies to "Internal Users"
# I had to add the if_* rules because the ISE API changed between 3.1 and 3.1p1 and now they're mandatory
# for some ridiculous reason 
api.network_access_authentication_rules.update_network_access_authentication_rule_by_id(id=defaultruleId[0],
                                                                                            policy_id=policyId,
                                                                                            if_auth_fail="REJECT",
                                                                                            if_user_not_found="REJECT",
                                                                                            if_process_fail="DROP",                                                                                            
                                                                                            rule=defaultruledata,
                                                                                            identity_source_name="Internal Users")

api.network_access_authentication_rules.update_network_access_authentication_rule_by_id(id=dot1xruleId[0],
                                                                                            policy_id=policyId,
                                                                                            if_auth_fail="REJECT",
                                                                                            if_user_not_found="REJECT",
                                                                                            if_process_fail="DROP",                                                                                            
                                                                                            rule=dot1xruledata,
                                                                                            identity_source_name="Internal Users")

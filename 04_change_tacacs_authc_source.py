# 04_change_tacacs_authc_source.py
#
# This file will simply change the identity source of the default device administration policy to use
# internal users instead of all user stores
#
# It's not strictly necessary to do this, but it can sometimes speed up authc for a lab environment
# that isn't talking to an AD or LDAP for device administrator user information.
#
# This was also the second most annoying script to develop because there are two settings that we need
# from ISE (policy id and rule id) in order to change the setting.  ISE's API also required a bunch of
# seemingly random fields to be sent all so we can set this: identitySourceName: "Internal Users"

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
policysets = api.device_administration_policy_set.get_device_admin_policy_sets()

# Then we have to pull the policy ID for the Default policy set
policyId = policysets.response.response[0].id

# Then we use the policy ID to grab all of the device administration authc rules
rulesets = api.device_administration_authentication_rules.get_device_admin_authentication_rules(policy_id=policyId)

# And finally we pull the rule ID from the "Default" policy set rule
ruleId = rulesets.response.response[0].rule.id

# But wait, the ISE API needs some mandatory fields for some reason
mandatorydata = {
                "default": True, 
                "name": "Default"
                }

# And now, after all of that work, we can change the identity source in the default authc policy to "Internal Users"
# I had to add the if_* rules because the ISE API changed between 3.1 and 3.1p1 and now they're mandatory
# for some ridiculous reason 
api.device_administration_authentication_rules.update_device_admin_authentication_rule_by_id(id=ruleId,
                                                                                            policy_id=policyId, 
                                                                                            if_auth_fail="REJECT",
                                                                                            if_user_not_found="REJECT",
                                                                                            if_process_fail="DROP",
                                                                                            rule=mandatorydata,
                                                                                            identity_source_name="Internal Users")
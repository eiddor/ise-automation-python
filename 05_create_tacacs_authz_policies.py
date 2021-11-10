# 05_create_tacacs_authz_policies.py
#
# This file will create an authorization policy rule in the default device administation policy set
# that will authorize anyone in the "netadmin" user group and assign them privilege 15 in TACACS
# for device administration

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

# declare our rule and condition data because we have to pass it all in one big chunky dictionary/
# array/list/blob/whatever
ruledata = {
        "default" : False,
        "name" : "AdminAccess",
        "rank" : 0,
        "condition" : {
            "conditionType" : "ConditionAttributes",
            "isNegate" : False,
            "dictionaryName" : "IdentityGroup",
            "attributeName" : "Name",
            "operator" : "equals",
            "attributeValue" : "User Identity Groups:netadmin"
        }
    }

# Create our device administration authz rule
api.device_administration_authorization_rules.create_device_admin_authorization_rule(policy_id=policyId,
                                                                                    commands=[ "PermitAllCommands" ],
                                                                                    profile="PermitAllShell",
                                                                                    rule=ruledata)
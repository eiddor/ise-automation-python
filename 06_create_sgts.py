# 06_create-sgts.py
#
# This file will create Scalable Group Tags (SGTs) in ISE that can be used for policy
# with Cisco Software-Defined Access.
#
# In a typical SD-Access environment these SGTs would be created with Cisco DNA Center, so this
# script isn't strictly necessary, however these SGTs need to exist before the authorization policies
# are created.
#
# Either way, you should not need to modify this file - You should list your SGTs in policy.yaml
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

# iterate through the list of SGTs in policy.yaml and create each one
for sgtlist in policy['sgtvars']:
        api.security_groups.create_security_group(name=sgtlist['sgtname'], 
                                                description=sgtlist['sgtdesc'],
                                                value=-1)
        print("Creating SGT:", sgtlist['sgtname'])
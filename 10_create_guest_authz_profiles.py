# 10_create_guest_authz_profiles.py
#
# This file will create authorization profiles required for a wired guest workflow in ISE.
#
# There are two profiles for this workflow:
#
# 1) The first profile (GuestRedirect) allows unauthenticted users/devices onto the network with limited
# connectivity in the Guest VLAN allowing them to only connect to ISE to access the guest portal
#
# 2) Once the user authenticates with the guest portal, the second profile (GuestAccess) will allow them
# full network access in the Guest VLAN.
#
# This workflow services two purposes:
#
# 1) Wired guest users will receive a guest portal to be allowed access to the network
#
# 2) Allow other devices limited network access so that ISE can profile them, specifically access points for the
# later scripts
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

# create our profile object, or array, or list, or dictionary, or whatever.

vlandata = {
            "nameID" : policy['guest']['vlan'],
            "tagID" : 1
        }

webredirectdata = {
        "WebRedirectionType" : "CentralizedWebAuth",
        "acl" : policy['guest']['redirectacl'],
        "portalName" : "Self-Registered Guest Portal (default)",
        "staticIPHostNameFQDN" : data['ise_hostname'],
        "displayCertificatesRenewalMessages" : True
        }

# Create the Guest Redirect profile
api.authorization_profile.create_authorization_profile(name="GuestRedirect", 
                                    description="Guest Redirect profile",
                                    access_type="ACCESS_ACCEPT",
                                    authz_profile_type="SWITCH",
                                    easywired_session_candidate=False,
                                    profile_name="Cisco",
                                    service_template=False,
                                    track_movement=False,
                                    vlan=vlandata,
                                    web_redirection=webredirectdata
                                    )

# Create the Guest Access profile
api.authorization_profile.create_authorization_profile(name="GuestAccess", 
                                    description="Guest Access profile",
                                    access_type="ACCESS_ACCEPT",
                                    authz_profile_type="SWITCH",
                                    easywired_session_candidate=False,
                                    profile_name="Cisco",
                                    service_template=False,
                                    track_movement=False,
                                    vlan=vlandata,
                                    )
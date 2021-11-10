# Python Scripts for Cisco Identity Services Engine (ISE)

A set of [Python](https://www.python.org/) scripts to configure a freshly installed Cisco Identity Services Engine (ISE) for simple operation; in my case, a basic [Cisco Software-Defined Access](https://www.cisco.com/c/en/us/solutions/enterprise-networks/software-defined-access/index.html) environment.

> **Note:** This repo is my second shot at automating ISE, and is mostly the same as my [Ansible project](https://github.com/eiddor/ise-automation-ansible) in terms of functionality.  I even used the same YAML settings files so you can use either method without any modification.
### Features
These scripts will configure the following in ISE:

* local user groups (`01_add_groups.py`)
* local user identities (`02_add_users.py`)
* a simple TACACS profile and command set for privilege 15 access (`03_create_tacacs_profiles.py`)
* TACACS policies in the default policy set (`05_create_tacacs_authz_policies.py`)
* Scalable Group Tags (SGT) to allow our authentication rules to work (`06_create_sgts.py`)
* network access authorization rules to places users in the appropriate VLANs (wired and wireless) (`08_create_authorization_profiles.py`)
* network access policies to authorize users and assign SGTs (`09_create_authorization_policies.py`)
* a complete wired guest workflow with redirection, portal, and SGT(`10_create_guest_authz_profiles.py` & `11_create_guest_authz_policies.py`)
* Cisco access point profiling (using the wired guest flow) and authorization profiles (`12_access_point_profiling.py`)

The ISE resources that are configured with these scripts are enough to support a basic Cisco SD-Access network including:

* TACACS authentication for network devices
* dot1x authentication and authorization for multiple users
* wired guest access
* multiple Scalable Group Tags (SGTs)
* Cisco access point profiling and authorization

### Background

I administer a lab environment that is used to demonstrate Cisco Software-Defined Access for customers.  When new versions of [Cisco ISE](https://www.cisco.com/c/en/us/products/security/identity-services-engine/index.html) or [DNA Center](https://www.cisco.com/c/en/us/products/cloud-systems-management/dna-center/index.html) are released, I do a fresh installation of both so that I can test the new versions with the lab workflow.  This involves installing each piece of software and then configuring them both to the point where I can start going through the lab guide.

After watching a demo of the collections in [this repo](https://github.com/hosukw/20210928-IBN-Demo) that use Terraform and Ansible to spin-up and configure ISE in AWS, I was inspired to setup something similar to assist in my configuration process when testing new versions.

I started with almost zero API experience beyond installing Postman on my workstation in the past and never using it.  Prior to this project I had run exactly one Ansible playbook in my life, and that was six years ago.  Needless to say, I was (and still am) completely green with this stuff, so it was a complete learning experience for me, especially not having a background in code or data structures.

Once I got the [Ansible collection](https://github.com/eiddor/ise-automation-ansible) done, I decided to teach myself Python the hard way by converting everything into Python scripts. It was a challenge because I had zero Python experience, but I got it done in a couple of days with the help of Google.

As a bonus: You will notice some snark in the script comments as well, which stemmed from some frustrations that I ran into while learning.  Some, but not all, of these comments were copied from the companion Ansible playbooks, because the frustrations were mostly the same.
### Requirements

#### Server
* [Cisco Identity Services Engine](https://www.cisco.com/c/en/us/products/security/identity-services-engine/index.html) (ISE) 3.1 or higher

> **Note:** Some of these scripts may work with ISE 3.0, but 3.1 is required for the policy stuff.
#### Workstation
* [Python](https://www.python.org/) 3.6+
* [Cisco ISE SDK v1.0.0](https://github.com/CiscoISE/ciscoisesdk)+

### Quick Start

If you just want to see these in action, you can run them against a Cisco DevNet [ISE 3.1 APIs, Ansible, and Automation](https://devnetsandbox.cisco.com/RM/Diagram/Index/ad4bb2ae-bb67-4d93-9f0d-2a6a04792e2e?diagramType=Topology) sandbox instance without any customization:

* On your local workstation install [requirements](#requirements) above:

**Cisco ISE SDK:**
> `sudo pip install ciscoisesdk`

* Reserve a sandbox in DevNet and connect to it per their instructions

* In ISE, enable **ERS** and **Open API** settings in: _Administration | Settings | API Settings | API Service Settings_

![ISE API Settings](images/ise_api.png)

* Run the scripts one at a time like this:

> `$ python 01_add_groups.py` 

> `$ python 02_add_users.py` 

> `$ python 03_create_tacacs_profiles.py`

* You can verify the changes in the ISE GUI after each script if you're curious
### Usage Notes

Although my use-case for these scripts involves a fresh deployment of ISE to support a Cisco SD-Access topology, they can absolutely be modified and used in a brownfield ISE environment without SDA.

I'm going to try to make the project self-documenting via comments as best I can, but here's a rough guide to get started:

`credentials.yaml` - Contains the ISE deployment information such as hostname, username, and password

`groupsandusers.yaml` - Contains the internal identity groups and users that will be configured by the scripts

`policy.yaml` - Contains the policy/profile information that will be configured by the scripts

* I developed these scripts using Cisco DevNet's [ISE 3.1 APIs, Ansible, and Automation](https://devnetsandbox.cisco.com/RM/Diagram/Index/ad4bb2ae-bb67-4d93-9f0d-2a6a04792e2e?diagramType=Topology) sandbox, so they should be useable there without any modification (See [Quick Start](#quick-start) section)

### Other ISE Settings

One day I will post a summary of some of the ISE settings that I change to make my life a little easier following an install.  These settings will be pretty specific to a lab environment and not suggested for production.
### TODO

* better documentation
* better optimization of the scripts
* result feedback from the scripts
* error checking and handling
* clean up the scripts to match the Python style guide (Hi, Jose!)
* add more optional fields to make this useful in the real world
* redo this whole mess in Python before I retire (**NOTE**: I DID IT)

### Acknowledgements

Google.

I also want to give a shoutout to the developers of the [Cisco ISE SDK](https://github.com/CiscoISE/ciscoisesdk).  It made things much much easier for me.
### Questions?

Please open an issue if you have any questions or suggestions.  

I developed these scripts for my own use, so I do want to keep them as clean as I can, but if you think they can be improved or optimized, feel free to submit a PR.


#!/usr/bin/python

# Copyright: (c) 2022, Ruben van Komen <rubenvankomen@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: librenms_get
short_description: Executes GET operations on API endpoints.
version_added: "1.0.0"
description: Executes GET operations on API endpoints.
author: Ruben van Komen (@Walkablenormal)

options:
    api_url:
        description: URL of the LibreNMS-server which needs to be queried.
        required: true
        type: str
    api_token:
        description: API-token that should be used for authenticating to the LibreNMS API.
        required: true
        type: str
    endpoint:
        description: The endpoint (and optional filters) which needs to be queried.
        required: true
        type: str
    ssl_verify:
        description: Sets if the host should check if the SSL-certificate of the LibreNMS-server is valid.
        required: false
        type: bool
'''

EXAMPLES = r'''
tasks:
- name: Get a list of all devices.
  local_action:
    module: walkablenormal.librenms.librenms_get
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices

- name: Get a list of graphs of the device called 'server1'.
  local_action:
    module: walkablenormal.librenms.librenms_get
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices/server1/graphs

- name: Get a list of ports of the device called 'server1'.
  local_action:
    module: walkablenormal.librenms.librenms_get
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices/server1/ports
'''

RETURN = r'''
data:
    description: The data returned by the GET-request.
    returned: On success
'''


from ansible.module_utils.basic import AnsibleModule
import requests


def get_data(api_url, api_token, endpoint, ssl_verify):
    if not ssl_verify:
        ssl_verify = False
    headers = {
        "X-Auth-Token": api_token
    }
    url = f"{api_url}/api/v0/{endpoint}"
    response = requests.get(url, headers=headers, verify=ssl_verify)
    if response.status_code != 200:
        raise ValueError(f"Failed to get {endpoint} from LibreNMS API")
    return response.json()


def run_module():
    module_args = {
        "api_url": {"type": "str", "required": True},
        "api_token": {"type": "str", "required": True},
        "endpoint": {"type": "str", "required": True},
        "ssl_verify": {"type": "bool", "required": False}
    }
    module = AnsibleModule(argument_spec=module_args)
    try:
        data = get_data(module.params["api_url"], module.params["api_token"], module.params["endpoint"], module.params.get("ssl_verify"))
        module.exit_json(changed=False, data=data)
    except Exception as e:
        module.fail_json(msg=str(e))


run_module()

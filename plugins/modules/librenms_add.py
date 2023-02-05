#!/usr/bin/python

# Copyright: (c) 2022, Ruben van Komen <rubenvankomen@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: librenms_add
short_description: Executes POST operations on API endpoints.
version_added: "1.0.0"
description: Executes POST operations on API endpoints.
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
        description: The endpoint which needs to be queried.
        required: true
        type: str
    json_data:
        description: JSON-data which needs to be parsed to the LibreNMS API.
        required: false
        type: str
    ssl_verify:
        description: Sets if the host should check if the SSL-certificate of the LibreNMS-server is valid.
        required: false
        type: bool
'''

EXAMPLES = r'''
tasks:
- name: Add a devices called 'server1' that should be polled using SNMPv1 with 'public' as community.
  local_action:
    module: walkablenormal.librenms.librenms_add
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices
    json_data: {"hostname":"server1","version":"v1","community":"public"}
'''

RETURN = r'''
data:
    description: The data returned by the POST-request.
    returned: On success
'''

from ansible.module_utils.basic import AnsibleModule
import json
import requests


def post_data(api_url, api_token, endpoint, json_data=None, ssl_verify):
    if not ssl_verify:
        ssl_verify = False
    headers = {
        "X-Auth-Token": api_token
    }
    url = f"{api_url}/api/v0/{endpoint}"
    if json_data:
        headers["Content-Type"] = "application/json"
        json_data = json_data.replace("'", '"')
        response = requests.post(url, headers=headers, json=json.loads(json_data), verify=ssl_verify)
    else:
        response = requests.post(url, headers=headers)
    if response.status_code not in [200, 500]:
        if response.status_code == 500 and 'already exists' not in response.json["message"]:
            raise ValueError(f"Failed to query {endpoint}")
        else:
            pass
    return response.json()


def run_module():
    module_args = {
        "api_url": {"type": "str", "required": True},
        "api_token": {"type": "str", "required": True},
        "endpoint": {"type": "str", "required": True},
        "json_data": {"type": "str", "required": False},
        "ssl_verify": {"type": "bool", "required": False}
    }
    module = AnsibleModule(argument_spec=module_args)
    try:
        data = post_data(module.params["api_url"], module.params["api_token"], module.params["endpoint"], module.params.get("json_data"), module.params.get("ssl_verify"))
        if 'already exists' not in data['message']:
            module.exit_json(changed=True, data=data)
        else:
            module.exit_json(changed=False, data=data)
    except Exception as e:
        module.fail_json(msg=str(e))


run_module()

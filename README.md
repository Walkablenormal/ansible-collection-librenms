# Walkablenormal.librenms

The LibreNMS collection is a set of Ansible modules that allow you to interact with the LibreNMS API. This collection contains modules for the GET, DELETE, and POST operations, giving you the ability to retrieve, delete, and create data in your LibreNMS installation.

With the LibreNMS collection, you can automate tasks such as monitoring the health of your network devices, updating device configurations, and managing alerts. The collection also makes it easy to integrate LibreNMS with other automation tools, such as Ansible Tower, allowing you to manage your network infrastructure more efficiently.

## Installation

To use the LibreNMS collection, you will need to have a LibreNMS installation and an API token. The collection also requires that you have Python3.x (libs: requests and json) and Ansible 2.9 or later installed on your system. Once you have these prerequisites, you can install the collection by running the following command:

`ansible-galaxy collection install walkablenormal.librenms`

Once the collection is installed, you can use the modules in your playbooks. The modules take a number of parameters, such as the API URL, API token, and endpoint, allowing you to specify the details of the operation you wish to perform.

## Modules

The `librenms_get` module allows you to retrieve information about a specific resource or a list of resources from your LibreNMS installation. This can be useful for monitoring the health of your network devices or retrieving information about alerts.

The `librenms_delete` module allows you to delete a specific resource or a list of resources from your LibreNMS installation. This can be useful for removing outdated or unnecessary data.

The `librenms_add` module allows you to create new resources or update existing resources in your LibreNMS installation. This can be useful for adding new devices to your network or updating device configurations.

## Usage

### librenms_get

```yaml
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
```

### librenms_delete

```yaml
tasks:
- name: Delete a device called 'server1'.
  local_action:
    module: walkablenormal.librenms.librenms_delete
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices/server1

- name: Delete a component with ID 4459 from the device called 'server1'.
  local_action:
    module: walkablenormal.librenms.librenms_delete
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices/server1/components/4459
```

### librenms_add

```yaml
tasks:
- name: Add a devices called 'server1' that should be polled using SNMPv1 with 'public' as community.
  local_action:
    module: walkablenormal.librenms.librenms_add
    api_url: http://librenms.example
    api_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    endpoint: devices
    json_data: {"hostname":"server1","version":"v1","community":"public"}
```

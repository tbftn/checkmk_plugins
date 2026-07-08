#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Clouds

# sample output:
# <<<vmware_avi_cloud:sep(0)>>>
# {
#     'name': 'Default-Cloud', 
#     'state': 'CLOUD_STATE_PLACEMENT_READY'
# },
# {...}


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service


def discover_vmware_avi_cloud(section):
    for cloud in section:
        yield Service(item = f"{cloud['name']}")


def check_vmware_avi_cloud(item, params, section):

    map_state = {
        "CLOUD_STATE_FAILED": {"cmk": params['state_failed'], "str": "Failed"},
        "CLOUD_STATE_IN_PROGRESS": {"cmk": params['state_in_progress'], "str": "In progress"},
        "CLOUD_STATE_PLACEMENT_READY": {"cmk": 0, "str": "Ready"},
    }

    for cloud in section:

        if f"{cloud['name']}" != item:
            continue

        # state
        yield from yield_mapped_result(cloud['state'], map_state, "State")

    return None


agent_section_vmware_avi_cloud = AgentSection(
    name = "vmware_avi_cloud",
    parse_function = parse_python_literal,
)


check_plugin_vmware_avi_cloud = CheckPlugin(
    name = "vmware_avi_cloud",
    service_name = "Avi Cloud %s",
    discovery_function = discover_vmware_avi_cloud,
    check_function = check_vmware_avi_cloud,
    check_default_parameters = {
        "state_failed": 2,
        "state_in_progress": 1,
    },
    check_ruleset_name = "vmware_avi_cloud",
)

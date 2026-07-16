#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Nodes

# sample output:
# <<<vmware_avi_node:sep(0)>>>
# {
#     'name': '1.2.3.4', 
#     'state': 'CLUSTER_ACTIVE', 
#     'role': 'CLUSTER_LEADER', 
#     'uptime': 22286802.046232
# },
# {...}


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_list, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, render


def discover_vmware_avi_node(section):
    for node in section:
        yield Service(item = f"{node['name']}")


def check_vmware_avi_node(item, section):

    map_role = {
        "CLUSTER_FOLLOWER": {"cmk": 0, "str": "Follower"},
        "CLUSTER_LEADER": {"cmk": 0, "str": "Leader"},
    }

    map_state = {
        "CLUSTER_ACTIVE": {"cmk": 0, "str": "Active"},
        "CLUSTER_STARTING": {"cmk": 1, "str": "Starting"},
    }

    for node in section:

        if f"{node['name']}" != item:
            continue
        
        # state
        yield from yield_mapped_result(node['state'], map_state, "State")

        # role
        yield from yield_mapped_result(node['role'], map_role, "Role")
        
        # uptime
        yield from check_levels(
            node['uptime'],
            label="Up since",
            render_func=lambda v: f'{render.timespan(v)}',
            metric_name="uptime",
        )

    return None


agent_section_vmware_avi_node = AgentSection(
    name = "vmware_avi_node",
    parse_function = parse_python_literal_list,
)


check_plugin_vmware_avi_node = CheckPlugin(
    name = "vmware_avi_node",
    service_name = "Avi Node %s",
    discovery_function = discover_vmware_avi_node,
    check_function = check_vmware_avi_node,
)

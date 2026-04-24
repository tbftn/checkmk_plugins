#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
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

import ast
import itertools


from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_node(string_table):

    parsed = []
    flatlist = list(itertools.chain.from_iterable(string_table))
    
    for f in flatlist:
        i = ast.literal_eval(f)
        parsed.append(i)

    return parsed


def discover_vmware_avi_node(section):
    for node in section:
        yield Service(item = f"{node['name']}")


def check_vmware_avi_node(item, section):

    map_role = {
        "CLUSTER_FOLLOWER": "Follower",
        "CLUSTER_LEADER": "Leader",
    }

    map_state = {
        "CLUSTER_ACTIVE": {"cmk": 0, "str": "Active"},
    }

    for node in section:

        if f"{node['name']}" != item:
            continue
        
        # State
        if node['state'] in map_state:
            yield Result(state=State(map_state[node['state']]["cmk"]), summary=f"State: {map_state[node['state']]["str"]}")
        else:
            yield Result(state=State(3), summary=f"State: {node['state']}")

        # Role
        yield Result(state=State.OK, summary=f"Role: {map_role.get(node['role'], node['role'])}")
        
        # Uptime
        yield from check_levels(
            node['uptime'],
            label="Up since",
            render_func=lambda v: f'{render.timespan(v)}',
            metric_name="uptime",
        )

    return None


agent_section_vmware_avi_node = AgentSection(
    name = "vmware_avi_node",
    parse_function = parse_vmware_avi_node,
)


check_plugin_vmware_avi_node = CheckPlugin(
    name = "vmware_avi_node",
    service_name = "Avi Node %s",
    discovery_function = discover_vmware_avi_node,
    check_function = check_vmware_avi_node,
)

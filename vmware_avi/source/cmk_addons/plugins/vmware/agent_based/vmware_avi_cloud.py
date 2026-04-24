#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
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

import ast
import itertools


from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_cloud(string_table):

    parsed = []
    flatlist = list(itertools.chain.from_iterable(string_table))
    
    for f in flatlist:
        i = ast.literal_eval(f)
        parsed.append(i)

    return parsed


def discover_vmware_avi_cloud(section):
    for cloud in section:
        yield Service(item = f"{cloud['name']}")


def check_vmware_avi_cloud(item, section):

    map_state = {
        "CLOUD_STATE_PLACEMENT_READY": {"cmk": 0, "str": "Ready"},
    }

    for cloud in section:

        if f"{cloud['name']}" != item:
            continue

        # State
        if cloud['state'] in map_state:
            yield Result(state=State(map_state[cloud['state']]["cmk"]), summary=f"State: {map_state[cloud['state']]["str"]}")
        else:
            yield Result(state=State(3), summary=f"State: {cloud['state']}")

    return None


agent_section_vmware_avi_cloud = AgentSection(
    name = "vmware_avi_cloud",
    parse_function = parse_vmware_avi_cloud,
)


check_plugin_vmware_avi_cloud = CheckPlugin(
    name = "vmware_avi_cloud",
    service_name = "Avi Cloud %s",
    discovery_function = discover_vmware_avi_cloud,
    check_function = check_vmware_avi_cloud,
)

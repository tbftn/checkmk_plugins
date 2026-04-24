#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Cluster

# sample output:
# <<<vmware_avi_cluster:sep(0)>>>
# {
#     'version': '30.2.2(9108) 2024-09-04 20:26:19 UTC', 
#     'patch': '2p5', 
#     'state': 'CLUSTER_UP_HA_ACTIVE', 
#     'uptime': 22286802.045929, 
#     'services': [
#         {'name': 'federated_datastore', 'state': 'CLUSTER_ACTIVE'},
#         {...}
#     ]
# }


import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_cluster(string_table):

    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_cluster(section):
    yield Service()


def check_vmware_avi_cluster(section):
    
    map_state = {
        "CLUSTER_UP_HA_ACTIVE": {"cmk": 0, "str": "Active"},
    }

    # State
    if section['state'] in map_state:
        yield Result(state=State(map_state[section['state']]["cmk"]), summary=f"State: {map_state[section['state']]["str"]}")
    else:
        yield Result(state=State(3), summary=f"State: {section['state']}")

    # Version
    yield Result(state=State.OK, summary=f"Version: {section['version']}, Patch: {section['patch']}")

    # Uptime
    yield from check_levels(
        section['uptime'],
        label="Up since",
        render_func=lambda v: f'{render.timespan(v)}',
        metric_name="uptime",
    )

    # Services: print only services there are no active
    crit_services = []
    for s in section['services']:
        if s['state'] != "CLUSTER_ACTIVE":
            crit_services.append(s['name'])
    if len(crit_services) > 0:   
        yield Result(state=State.CRIT, summary=f"{len(crit_services)} failed: {crit_services}")

    return
        

agent_section_vmware_avi_cluster = AgentSection(
    name = "vmware_avi_cluster",
    parse_function = parse_vmware_avi_cluster,
)


check_plugin_vmware_avi_cluster = CheckPlugin(
    name = "vmware_avi_cluster",
    service_name = "Avi Cluster",
    discovery_function = discover_vmware_avi_cluster,
    check_function = check_vmware_avi_cluster,
)

#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Site Engines CPU

# sample output:
# <<<vmware_avi_se_mem:sep(0)>>>
# {
#     'mem_usage': 51.0, 
#     'con_mem_usage': 3.0, 
#     'dyn_mem_usage': 62.32417239225484
# }


import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_se_mem(string_table):
    
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_se_mem(section):
    yield Service()


def check_vmware_avi_se_mem(params, section):
    
    map_mem = {
        "mem_usage": "Memory usage",
        "con_mem_usage": "Connection memory usage",
        "dyn_mem_usage": "Dynamic memory usage",
    }

    for m in map_mem:
        if m in section:
            yield from check_levels(
                section[m],
                label=map_mem[m],
                levels_upper=params[m],
                render_func=lambda v: f'{render.percent(v)}',
                metric_name=f"vmware_avi_se_{m}",
                boundaries=(0, 100)
            )


agent_section_vmware_avi_se_mem = AgentSection(
    name = "vmware_avi_se_mem",
    parse_function = parse_vmware_avi_se_mem,
)


check_plugin_vmware_avi_se_mem = CheckPlugin(
    name = "vmware_avi_se_mem",
    service_name = "Avi Memory",
    discovery_function = discover_vmware_avi_se_mem,
    check_function = check_vmware_avi_se_mem,
    check_default_parameters={
        "mem_usage": ("fixed", (80, 90)),
        "con_mem_usage": ("fixed", (80, 90)),
        "dyn_mem_usage": ("fixed", (80, 90)),
    },
    check_ruleset_name = "vmware_avi_se_mem",
)

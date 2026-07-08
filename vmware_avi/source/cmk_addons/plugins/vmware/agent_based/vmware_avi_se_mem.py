#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
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


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, render


def discover_vmware_avi_se_mem(section):
    yield Service()


def check_vmware_avi_se_mem(params, section):
    
    map_mem = {
        "mem_usage": "Memory",
        "con_mem_usage": "Connection memory",
        "dyn_mem_usage": "Dynamic memory",
    }

    for m in map_mem:
        if section.get(m, None) != None:
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
    parse_function = parse_python_literal,
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

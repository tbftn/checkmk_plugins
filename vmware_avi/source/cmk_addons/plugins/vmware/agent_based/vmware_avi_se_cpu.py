#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Site Engines CPU

# sample output:
# <<<vmware_avi_se_cpu:sep(0)>>>
# {
#     'cpu_usage': 0.0
# }


import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_se_cpu(string_table):
    
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_se_cpu(section):
    yield Service()


def check_vmware_avi_se_cpu(params, section):
    
    yield from check_levels(
        section['cpu_usage'],
        label="Total CPU",
        levels_upper=params["util"],
        render_func=lambda v: f'{render.percent(v)}',
        metric_name="util", # buildin checkmk metric
        boundaries=(0, 100)
    )


agent_section_vmware_avi_se_cpu = AgentSection(
    name = "vmware_avi_se_cpu",
    parse_function = parse_vmware_avi_se_cpu,
)


check_plugin_vmware_avi_se_cpu = CheckPlugin(
    name = "vmware_avi_se_cpu",
    service_name = "Avi CPU utilization",
    discovery_function = discover_vmware_avi_se_cpu,
    check_function = check_vmware_avi_se_cpu,
    check_default_parameters={
        "util": ("fixed", (80.0, 90.0)),
    },
    check_ruleset_name = "vmware_avi_se_cpu",
)

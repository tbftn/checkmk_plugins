#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Site Engines Health Score

# sample output:
# <<<vmware_avi_se_health:sep(0)>>>
# {
#     'health_score': 100.0, 
#     'anomaly_penalty': 0.0, 
#     'resources_penalty': 0.0, 
#     'performance_score': 100.0, 
#     'security_penalty': 0.0
# }


import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_se_health(string_table):
    
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_se_health(section):
    yield Service()


def check_vmware_avi_se_health(params, section):
    
    map_scores_l = {
        "health_score": "Health Score",
        "performance_score": "Performance"
    }

    map_scores_u = {
        "resources_penalty": "Resource Penalty",
        "anomaly_penalty": "Anomaly Penalty",
        "security_penalty": "Security Penalty"
    }

    for s in map_scores_l:
        yield from check_levels(
            section[s],
            label=map_scores_l[s],
            levels_lower=params[s],
            render_func=lambda v: f'{render.percent(v)}',
            metric_name=f"vmware_avi_{s}",
            boundaries=(0, 100)
        )

    for s in map_scores_u:
        yield from check_levels(
            section[s],
            label=map_scores_u[s],
            levels_upper=params[s],
            render_func=lambda v: f'{render.percent(v)}',
            metric_name=f"vmware_avi_{s}",
            boundaries=(0, 100)
        )


agent_section_vmware_avi_se_health = AgentSection(
    name = "vmware_avi_se_health",
    parse_function = parse_vmware_avi_se_health,
)


check_plugin_vmware_avi_se_health = CheckPlugin(
    name = "vmware_avi_se_health",
    service_name = "Avi Health",
    discovery_function = discover_vmware_avi_se_health,
    check_function = check_vmware_avi_se_health,
    check_default_parameters = {
        "health_score": ("fixed", (90, 60)),
        "performance_score": ("fixed", (90, 60)),
        "resources_penalty": ("fixed", (10, 50)),
        "anomaly_penalty": ("fixed", (10, 50)),
        "security_penalty": ("fixed", (10, 50)),
    },
    check_ruleset_name = "vmware_avi_se_health",
)

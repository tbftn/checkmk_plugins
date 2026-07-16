#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
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


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_dict, yield_health_score
from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service


def discover_vmware_avi_se_health(section):
    yield Service()


def check_vmware_avi_se_health(params, section):
    yield from yield_health_score(params['health_score'], section)
    

agent_section_vmware_avi_se_health = AgentSection(
    name = "vmware_avi_se_health",
    parse_function = parse_python_literal_dict,
)


check_plugin_vmware_avi_se_health = CheckPlugin(
    name = "vmware_avi_se_health",
    service_name = "Avi Health",
    discovery_function = discover_vmware_avi_se_health,
    check_function = check_vmware_avi_se_health,
    check_default_parameters = {
        "health_score": {
            "health_score": ("fixed", (85.0, 60.0)),
            "performance_score": ('no_levels', None),
            "resources_penalty": ('no_levels', None),
            "anomaly_penalty": ('no_levels', None),
            "security_penalty": ('no_levels', None),
        }
    },
    check_ruleset_name = "vmware_avi_se_health",
)

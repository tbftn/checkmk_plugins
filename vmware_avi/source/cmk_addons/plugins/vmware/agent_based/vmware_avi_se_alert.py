#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer Site Engine - Alerts

# sample output:
# <<<vmware_avi_se_alert:sep(0)>>>
# {
#     'low': 0, 
#     'medium': 0, 
#     'high': 0
# }


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service


def parse_vmware_avi_se_alert(string_table):

    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_se_alert(section):
    yield Service()


def check_vmware_avi_se_alert(params, section):

    map_alarms = {
        "low": "Low Alarms",
        "medium": "Medium Alarms",
        "high": "High Alarms"
    }

    for a in map_alarms:
        yield from check_levels(
            section[a],
            label=map_alarms[a],
            render_func=lambda v: f'{int(v)}',
            levels_upper=params[a],
        )


agent_section_vmware_avi_se_alert = AgentSection(
    name = "vmware_avi_se_alert",
    parse_function = parse_python_literal,
)


check_plugin_vmware_avi_se_alert = CheckPlugin(
    name = "vmware_avi_se_alert",
    service_name = "Avi Alerts",
    discovery_function = discover_vmware_avi_se_alert,
    check_function = check_vmware_avi_se_alert,
    check_default_parameters = {
        "low": ("fixed", (1, 1)),
        "medium": ("fixed", (1, 1)),
        "high": ("fixed", (1, 1)),
    },
    check_ruleset_name = "vmware_avi_se_alert",
)

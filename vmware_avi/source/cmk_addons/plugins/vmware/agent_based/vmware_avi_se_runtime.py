#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Service Engine Runtime

# sample output:
# <<<vmware_avi_se_runtime:sep(0)>>>
# {
#     'state': 'OPER_UP',
#     'power_state': 'SE_POWER_ON',
#     'version': '30.2.2(9108) 2024-09-04 20:26:19 UTC',
#     'license_state': 'LICENSE_STATE_LICENSED'
# }

import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_se_runtime(string_table):
    
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed

def discover_vmware_avi_se_runtime(section):
    yield Service()


def check_vmware_avi_se_runtime(section):
    
    if section['state'] == "OPER_UP":
        yield Result(state=State.OK, summary=f"State: {section['state']}")
    else:
        yield Result(state=State.CRIT, summary=f"State: {section['state']}")

    if section['power_state'] == "SE_POWER_ON":
        yield Result(state=State.OK, summary=f"Power: {section['power_state']}")
    else:
        yield Result(state=State.CRIT, summary=f"Power: {section['power_state']}")

    if section['license_state'] == "LICENSE_STATE_LICENSED":
        yield Result(state=State.OK, summary=f"License: {section['license_state']}")
    else:
        yield Result(state=State.WARN, summary=f"License: {section['license_state']}")

    yield Result(state=State.OK, summary=f"Version: {section['version']}")
    

agent_section_vmware_avi_se_runtime = AgentSection(
    name = "vmware_avi_se_runtime",
    parse_function = parse_vmware_avi_se_runtime,
)


check_plugin_vmware_avi_se_runtime = CheckPlugin(
    name = "vmware_avi_se_runtime",
    service_name = "Avi Runtime",
    discovery_function = discover_vmware_avi_se_runtime,
    check_function = check_vmware_avi_se_runtime,
)

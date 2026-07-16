#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
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


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_dict, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, State, Result


def discover_vmware_avi_se_runtime(section):
    yield Service()


def check_vmware_avi_se_runtime(section):
    
    map_state = {
        "OPER_UP": {"cmk": 0, "str": "Up"},
        "OPER_DONW": {"cmk": 2, "str": "Down"},
    }

    map_power_state = {
        "SE_POWER_ON": {"cmk": 0, "str": "On"},
    }

    map_license_state = {
        "LICENSE_STATE_LICENSED": {"cmk": 0, "str": "Ok"},
    }

    # state
    yield from yield_mapped_result(section['state'], map_state, "State")

    # power state
    yield from yield_mapped_result(section['power_state'], map_power_state, "Power")

    # license state
    yield from yield_mapped_result(section['license_state'], map_license_state, "License")

    # version
    yield Result(state=State.OK, summary=f"Version: {section['version']}")
    

agent_section_vmware_avi_se_runtime = AgentSection(
    name = "vmware_avi_se_runtime",
    parse_function = parse_python_literal_dict,
)


check_plugin_vmware_avi_se_runtime = CheckPlugin(
    name = "vmware_avi_se_runtime",
    service_name = "Avi Runtime",
    discovery_function = discover_vmware_avi_se_runtime,
    check_function = check_vmware_avi_se_runtime,
)

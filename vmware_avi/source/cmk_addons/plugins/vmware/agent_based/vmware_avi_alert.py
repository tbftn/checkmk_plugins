#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Alerts

# sample output:
# <<<vmware_avi_alert:sep(0)>>>
# {
#     'level': 'ALERT_MEDIUM', 
#     'state': 'ALERT_STATE_ON', 
#     'time': '2026-04-23 03:21:12', 
#     'summary': 'System-Controller-Alert System Alert Triggered', 
#     'obj_name': 'NSX Advanced Load Balancer'
# },
# {...}


import ast
import itertools

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, State, Result


def parse_vmware_avi_alert(string_table):

    parsed = []
    flatlist = list(itertools.chain.from_iterable(string_table))
    
    for f in flatlist:
        i = ast.literal_eval(f)
        parsed.append(i)

    return parsed


def discover_vmware_avi_alert(section):
    yield Service()


def check_vmware_avi_alert(section):
    
    map_status = {
        "ALERT_LOW": "Low",
        "ALERT_MEDIUM": "Medium",
        "ALERT_HIGH": "High",
    }

    if len(section) == 0:
        yield Result(state=State.OK, summary=f"No alerts")
        return
    for a in section:
        yield Result(state=State.CRIT, summary=f"{a['time']}: [{map_status.get(a['level'], a['level'])}] {a['obj_name']}: {a['summary']}")

    return
        

agent_section_vmware_avi_alert = AgentSection(
    name = "vmware_avi_alert",
    parse_function = parse_vmware_avi_alert,
)


check_plugin_vmware_avi_alert = CheckPlugin(
    name = "vmware_avi_alert",
    service_name = "Avi Alerts",
    discovery_function = discover_vmware_avi_alert,
    check_function = check_vmware_avi_alert,
)

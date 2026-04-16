#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-16
# License: GNU General Public License v2
#
# Check: ExtremeCloud IQ Controller - Access Points

# sample output:
# <<<netextreme_xiq_controller_ap:sep(0)>>>
# [
#     {
#         'name': 'AP 044', 
#         'power': 5.663, 
#         'uptime': 15728467, 
#         'clients': 23, 
#         'ipAddress': '192.168.1.1', 
#         'hardwareType': 'AP4000-WW', 
#         'serialNumber': '0400Serial123', 
#         'softwareVersion': '10.15.1.0-038R', 
#         'macAddress': 'AA:BB:CC:DD:EE:FF', 
#         'description': 'Secret Description', 
#         'status': 'InService'
#     },
#     {...},
# ]


import ast
import itertools

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_netextreme_xiq_controller_ap(string_table):

    parsed = []
    flatlist = list(itertools.chain.from_iterable(string_table))
    
    for f in flatlist:
        i = ast.literal_eval(f)
        parsed.append(i)

    return parsed


def discover_netextreme_xiq_controller_ap(section):
    for ap in section:
        if ap['status'] != 'Unknown':
            yield Service(item = f"{ap['name']}")


def check_netextreme_xiq_controller_ap(item, params, section):

    map_status = {
        "critical": "Critical",
        "InService": "In-Service",
        "InServiceTrouble": "In-Service Trouble",
        "Unknown": "Unknown",
        "UpgradeFailed": "Upgrade Failed",
        "Upgrading": "Upgrading",
    }
    
    map_inv_keys = {
        "ipAddress": "IP Address", 
        "hardwareType": "Model", 
        "serialNumber": "Serial Number", 
        "softwareVersion": "Version", 
        "macAddress": "MAC Address", 
        "description": "Description"
    }

    for ap in section:

        if f"{ap['name']}" != item:
            continue
        
        inv_data = ""
        for key in map_inv_keys:
            if ap.get(key, "") != "":
                inv_data += f"\n{map_inv_keys[key]}: {ap[key]}"
            
        if len(inv_data) > 0:
            inv_data = "AP Info:" + inv_data

        # status: InServce, Upgrading, UpgradeFailed, Unknown, critical
        if ap['status'] == 'InService':
            yield Result(state=State(params["state_ap_inservice"]), summary=f"Status: {map_status.get(ap['status'])}")
        
        else:
            if ap['status'] == 'Upgrading':
                yield Result(state=State(params["state_ap_uprading"]), summary=f"Status: {map_status.get(ap['status'])}", details=inv_data)
            elif ap['status'] == 'UpgradeFailed':
                yield Result(state=State(params["state_ap_upgradefailed"]), summary=f"Status: {map_status.get(ap['status'])}", details=inv_data)
            elif ap['status'] == 'InServiceTrouble':
                yield Result(state=State(params["state_ap_inservicetrouble"]), summary=f"Status: {map_status.get(ap['status'])}", details=inv_data)
            elif ap['status'] == 'critical':
                yield Result(state=State(params["state_ap_critical"]), summary=f"Status: {map_status.get(ap['status'])}", details=inv_data)
            else:
                yield Result(state=State.UNKNOWN, summary=f"Status: {ap['status']}")
            return None

        # uptime
        yield from check_levels(
            ap['uptime'],
            label="Uptime",
            render_func=lambda v: f'{render.timespan(v)}',
            metric_name="netextreme_xiq_controller_uptime",
            boundaries=(0, None)
        )

        # clients
        yield from check_levels(
            ap['clients'],
            label="Clients",
            levels_upper=params["ap_clients_levels_upper"],
            render_func=lambda v: int(v),
            metric_name="netextreme_xiq_controller_ap_clients",
            boundaries=(0, None)
        )

        # power
        # If Power <= 0, then this hardware type can't read the power.
        # Typical Extreme Networks: simply outputting 0 for a value that can't be determined...
        if ap['power'] > 0:
            yield from check_levels(
                ap['power'],
                label="Power",
                levels_upper=params["ap_power_levels_upper"],
                render_func=lambda v: f'{v} W',
                metric_name="netextreme_xiq_controller_ap_power",
                boundaries=(0, None)
            )
            
        # ap inv infos
        yield Result(state=State.OK, notice=inv_data)
 
    return None


agent_section_netextreme_xiq_controller_ap = AgentSection(
    name = "netextreme_xiq_controller_ap",
    parse_function = parse_netextreme_xiq_controller_ap,
)


check_plugin_netextreme_xiq_controller_ap = CheckPlugin(
    name = "netextreme_xiq_controller_ap",
    service_name = "AP %s",
    discovery_function = discover_netextreme_xiq_controller_ap,
    check_function = check_netextreme_xiq_controller_ap,
    check_default_parameters = {
        "state_ap_inservice": 0,
        "state_ap_uprading": 0,
        "state_ap_inservicetrouble": 1,
        "state_ap_upgradefailed": 2,
        "state_ap_critical": 2,
        "ap_clients_levels_upper": ('no_levels', None),
        "ap_power_levels_upper": ('no_levels', None),
    },
    check_ruleset_name = "netextreme_xiq_controller_ap",
)

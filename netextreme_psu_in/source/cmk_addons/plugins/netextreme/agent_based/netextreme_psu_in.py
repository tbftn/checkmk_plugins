#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-01
# License: GNU General Public License v2
#
# Check: Extreme Networks Power Supply Input


from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    startswith,
    Metric,
    OIDEnd,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State
)

from typing import Dict, List, Optional, Tuple, Union
import math


# .1.3.6.1.4.1.1916.1.1.1.27.1.2.1 2 --> EXTREME-SYSTEM-MIB::extremePowerSupplyStatus.1
# .1.3.6.1.4.1.1916.1.1.1.27.1.2.2 2 --> EXTREME-SYSTEM-MIB::extremePowerSupplyStatus.2
# .1.3.6.1.4.1.1916.1.1.1.27.1.9.1 66480 --> EXTREME-SYSTEM-MIB::extremePowerSupplyInputPowerUsage.1
# .1.3.6.1.4.1.1916.1.1.1.27.1.9.2 33970 --> EXTREME-SYSTEM-MIB::extremePowerSupplyInputPowerUsage.2
# .1.3.6.1.4.1.1916.1.1.1.27.1.11.1 -3 --> EXTREME-SYSTEM-MIB::extremePowerSupplyInputPowerUsageUnitMultiplier.1
# .1.3.6.1.4.1.1916.1.1.1.27.1.11.2 -3 --> EXTREME-SYSTEM-MIB::extremePowerSupplyInputPowerUsageUnitMultiplier.2


def parse_netextreme_psu_in(string_table):
    
    parsed = []
    
    for psu_index, psu_status, psu_usage_str, psu_factor_str in string_table:
        
        psu = {}
        
        power = float(psu_usage_str) * pow(10, int(psu_factor_str))
        
        psu = {
            'index': psu_index,    
            'status': int(psu_status),
            'power': round(power, 2)
        }
        
        parsed.append(psu)

    return parsed


def discover_netextreme_psu_in(section):
    for psu in section:
        if psu['status'] != 1: # notPresent: no power supply inserted
            yield Service(item = f"Input {psu['index']}")


def check_netextreme_psu_in(item, params, section):

    for psu in section:

        if f"Input {psu['index']}" != item:
            continue

        if psu['status'] == 1: # notPresent
            yield Result(state=State.UNKNOWN, summary='Empty - No Power supply available')
        
        elif psu['status'] == 2: # poweredOn: print power, if available
            
            if psu['power'] > 0:
            
                yield from check_levels(
                    psu['power'],
                    label="Power",
                    levels_upper=params["levels_upper"],
                    render_func=lambda v: f'{v} W',
                    metric_name="power",
                    boundaries=(0, None)
                )
                
            else: # Some switches do not provide any performance information
                yield Result(state=State.OK, summary='Powered On')

        elif psu['status'] == 3: # presentNotOK
            yield Result(state=State(params["psu_failed"]), summary='Failed - Power supply and power available, but an error has occurred!')

        elif psu['status'] == 4: # poweredOff
            yield Result(state=State(params["psu_powered_off"]), summary='Powered Off - Power supply available, but no power!')

        else: # undefined
            yield Result(state=State.UNKNOWN, summary='Undefined state of Power Supply')
            
        return


snmp_section_netextreme_psu_in = SimpleSNMPSection(
    name = "netextreme_psu_in",
    parse_function = parse_netextreme_psu_in,
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Extreme"),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.1916.1.1.1.27.1',
        oids=[
            OIDEnd(),   # Power Supply Index
            "2",        # extremePowerSupplyStatus { notPresent(1), presentOK(2), presentNotOK(3) poweredOff(4)}
            "9",        # extremePowerSupplyInputPowerUsage
            "11",       # extremePowerSupplyInputPowerUsageUnitMultiplier
        ]
    )
)


check_plugin_netextreme_psu_in = CheckPlugin(
    name = "netextreme_psu_in",
    service_name = "Power Supply %s",
    discovery_function = discover_netextreme_psu_in,
    check_function = check_netextreme_psu_in,
    check_default_parameters = {
        "levels_upper": ('fixed', (110.0, 120.0)), # This levels a recomended by the manufactorer
        "psu_powered_off": 2,
        "psu_failed": 2,
    },
    check_ruleset_name = "netextreme_psu_in",
)

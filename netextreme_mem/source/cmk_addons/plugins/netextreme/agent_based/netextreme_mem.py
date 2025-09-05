#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-05
# License: GNU General Public License v2
#
# Check: Extreme Networks Memory Usage

# SNMP walk:
# .1.3.6.1.4.1.1916.1.32.2.2.1.1.1 1 --> EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemSlotId.1
# .1.3.6.1.4.1.1916.1.32.2.2.1.2.1 8388608 --> EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemTotal.1
# .1.3.6.1.4.1.1916.1.32.2.2.1.3.1 7031304 --> EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemFree.1
# .1.3.6.1.4.1.1916.1.32.2.2.1.4.1 495720 --> EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemUsage.1
# .1.3.6.1.4.1.1916.1.32.2.2.1.5.1 861584 --> EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorUserUsage.1


from cmk.agent_based.v2 import check_levels, CheckPlugin, get_value_store, Metric, render, Result, Service, SimpleSNMPSection, SNMPTree, startswith, State
from cmk.plugins.lib.size_trend import size_trend


def parse_netextreme_mem(string_table):

    if len(string_table) > 0:

        # convert values in Bytes
        mem = {
            'total': int(string_table[0][0]) * 1024,
            'free': int(string_table[0][1]) * 1024 ,
            'system': int(string_table[0][2]) * 1024,
            'user': int(string_table[0][3]) * 1024,
        }

        # calc summary used mem
        mem['sum'] = mem['system'] + mem['user']

        # calc percent of summary used mem
        mem['sum_perc'] = (mem['sum'] / mem['total']) * 100

    return mem


def discover_netextreme_mem(section):
    yield Service()


def check_netextreme_mem(params, section):
    
    # Output like classic checkmk: Used: %s%s - %s of %s (warn/crit at ..%/..%)
    # always ok, only for info :)
    yield Result(state=State.OK, summary=f"Memory: {round(section['sum_perc'], 2)}% - {render.bytes(section['sum'])} of {render.bytes(section['total'])}")
    
    # only print, if service is warn or crit
    yield from check_levels(
        section['sum_perc'],
        levels_upper=params["levels"],
        metric_name="netextreme_mem_sum_perc",
        render_func=lambda v: f'{v:.2f} %',
        label="Used",
        boundaries=(0, 100),
        notice_only=True,
    )
    
    # in the summary, indicate the trend and the time when the memory runs full. No diagrams or similar
    # hard coded, nothing adjustable in Wato in case this feature is removed in a future version
    yield from size_trend(
        value_store=get_value_store(),
        value_store_key="Memory",
        resource="memory",
        levels={
            'trend_range': 24
        },
        used_mb=section['sum'] / 1024 / 1024,
        size_mb=section['total'] / 1024 / 1024,
        timestamp=None,
    )

    # metrics
    yield Metric(value=section['system'], name="netextreme_mem_system", boundaries=(0, None))
    yield Metric(value=section['user'], name="netextreme_mem_user", boundaries=(0, None))
    yield Metric(value=section['sum'], name="netextreme_mem_sum",boundaries=(0, None))


snmp_section_netextreme_mem = SimpleSNMPSection(
    name = "netextreme_mem",
    parse_function = parse_netextreme_mem,
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Extreme"),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.1916.1.32.2.2.1',
        oids=[
            "2.1", # EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemTotal
            "3.1", # EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemFree
            "4.1", # EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorSystemUsage
            "5.1", # EXTREME-SOFTWARE-MONITOR-MIB::extremeMemoryMonitorUserUsage	
        ]
    )
)


check_plugin_netextreme_mem = CheckPlugin(
    name = "netextreme_mem",
    service_name = "Memory",
    discovery_function = discover_netextreme_mem,
    check_function = check_netextreme_mem,
    check_default_parameters = {
        "levels": ('fixed', (80.0, 90.0)),
    },
    check_ruleset_name = "netextreme_mem",
)

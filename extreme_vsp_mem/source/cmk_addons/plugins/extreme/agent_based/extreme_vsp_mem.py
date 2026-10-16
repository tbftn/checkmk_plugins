#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-10-15
# License: GNU General Public License v2
#
# Check: Extreme VSP Memory Usage

# SNMP walk:
# .1.3.6.1.4.1.2272.1.85.10.1.1.2.1 8 --> RAPID-CITY::rcKhiSlotCpuCurrentUtil.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.3.1 3 --> RAPID-CITY::rcKhiSlotCpu5MinAve.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.4.1 5 --> RAPID-CITY::rcKhiSlotCpu5MinHi.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.5.1 "07 EA 0A 0D 0C 31 21 00 " --> RAPID-CITY::rcKhiSlotCpu5MinHiTime.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.6.1 2197744 --> RAPID-CITY::rcKhiSlotMemUsed.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.7.1 14170656 --> RAPID-CITY::rcKhiSlotMemFree.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.8.1 13 --> RAPID-CITY::rcKhiSlotMemUtil.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.9.1 13 --> RAPID-CITY::rcKhiSlotMem5MinAve.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.10.1 13 --> RAPID-CITY::rcKhiSlotMem5MinHi.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.11.1 "07 EA 06 1E 0A 14 14 00 " --> RAPID-CITY::rcKhiSlotMem5MinHiTime.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.12.1 0 --> RAPID-CITY::rcKhiSlotUsedFbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.13.1 3072 --> RAPID-CITY::rcKhiSlotFreeFbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.14.1 0 --> RAPID-CITY::rcKhiSlotNoFbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.15.1 0 --> RAPID-CITY::rcKhiSlotNetStackSysFreeMbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.16.1 0 --> RAPID-CITY::rcKhiSlotNetStackDataFreeMbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.17.1 0 --> RAPID-CITY::rcKhiSlotNetStackSysUsedMbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.18.1 0 --> RAPID-CITY::rcKhiSlotNetStackDataUsedMbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.19.1 0 --> RAPID-CITY::rcKhiSlotNetStackSysSocketMbuf.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.20.1 0 --> RAPID-CITY::rcKhiSlotQHigh.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.21.1 0 --> RAPID-CITY::rcKhiSlotQNormal.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.22.1 0 --> RAPID-CITY::rcKhiSlotFreeQEntries.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.23.1 0 --> RAPID-CITY::rcKhiSlotCpu1MinAve.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.24.1 0 --> RAPID-CITY::rcKhiSlotCpu1MinHi.1
# .1.3.6.1.4.1.2272.1.85.10.1.1.25.1 "00 00 00 00 00 00 00 00 00 00 00 " --> RAPID-CITY::rcKhiSlotCpu1MinHiTime.1


from cmk.agent_based.v2 import check_levels, CheckPlugin, get_value_store, Metric, render, Result, Service, SimpleSNMPSection, SNMPTree, contains, State
from cmk.plugins.lib.size_trend import size_trend


def parse_extreme_vsp_mem(string_table):
    mem = {}
    
    if len(string_table) > 0:
        # convert values in Bytes
        mem = {
            "used": int(string_table[0][0]) * 1024,
            "free": int(string_table[0][1]) * 1024,
        }

        # calc total mem
        mem['total'] = mem['used'] + mem['free']

        # calc percent of summary used mem
        mem['used_perc'] = (mem['used'] / mem['total']) * 100

    return mem


def discover_extreme_vsp_mem(section):
    if len(section) > 0:
        yield Service()


def check_extreme_vsp_mem(params, section):
    
    # always ok, only for info :)
    yield Result(state=State.OK, summary=f"Memory: {round(section['used_perc'], 2)}% - {render.bytes(section['used'])} of {render.bytes(section['total'])}")
    
    # only print, if service is warn or crit
    yield from check_levels(
        section['used_perc'],
        levels_upper=params["levels"],
        metric_name="extreme_vsp_mem_sum_perc",
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
        used_mb=section['used'] / 1024 / 1024,
        size_mb=section['total'] / 1024 / 1024,
        timestamp=None,
    )

    # metrics
    yield Metric(value=section['used'], name="extreme_vsp_mem_used",boundaries=(0, None))


snmp_section_extreme_vsp_mem = SimpleSNMPSection(
    name = "extreme_vsp_mem",
    parse_function = parse_extreme_vsp_mem,
    detect = contains(".1.3.6.1.2.1.1.1.0", "FabricEngine"),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.2272.1.85.10.1.1',
        oids=[
            "6.1", # RAPID-CITY::rcKhiSlotMemUsed
            "7.1", # RAPID-CITY::rcKhiSlotMemFree
        ]
    )
)


check_plugin_extreme_vsp_mem = CheckPlugin(
    name = "extreme_vsp_mem",
    service_name = "Memory",
    discovery_function = discover_extreme_vsp_mem,
    check_function = check_extreme_vsp_mem,
    check_default_parameters = {
        "levels": ('fixed', (80.0, 90.0)),
    },
    check_ruleset_name = "extreme_vsp_mem",
)

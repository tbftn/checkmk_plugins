#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Site Engines Interface

# sample output:
# <<<vmware_avi_se_if:sep(0)>>>
# {
#     'throughput': 221602.96000000002,
#     'rx_packets': 47.94333333333334,
#     'tx_packets': 51.76,
#     'rx_bits': 108877.44,
#     'tx_bits': 112725.52000000002
# }


import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_se_if(string_table):
    
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_se_if(section):
    yield Service()


def check_vmware_avi_se_if(section):

    yield from check_levels(
        section['throughput'],
        label="Throughput",
        render_func=lambda v: f'{render.networkbandwidth(v/8)}',
        metric_name="vmware_avi_throughput",
    )

    yield from check_levels(
        section['rx_bits'],
        label="In",
        render_func=lambda v: f'{render.networkbandwidth(v/8)}',
        metric_name="vmware_avi_se_if_rx_bits",
    )

    yield from check_levels(
        section['tx_bits'],
        label="Out",
        render_func=lambda v: f'{render.networkbandwidth(v/8)}',
        metric_name="vmware_avi_se_if_tx_bits",
    )

    yield from check_levels(
        section['rx_packets'],
        label="RX packtes",
        render_func=lambda v: f'{round(v, 2)} packets/s',
        metric_name="vmware_avi_se_if_rx_packtes",
        notice_only=True,
    )

    yield from check_levels(
        section['tx_packets'],
        label="TX packets",
        render_func=lambda v: f'{round(v, 2)} packets/s',
        metric_name="vmware_avi_se_if_tx_packtes",
        notice_only=True,
    )

    

agent_section_vmware_avi_se_if = AgentSection(
    name = "vmware_avi_se_if",
    parse_function = parse_vmware_avi_se_if,
)


check_plugin_vmware_avi_se_if = CheckPlugin(
    name = "vmware_avi_se_if",
    service_name = "Avi Interface",
    discovery_function = discover_vmware_avi_se_if,
    check_function = check_vmware_avi_se_if,
)

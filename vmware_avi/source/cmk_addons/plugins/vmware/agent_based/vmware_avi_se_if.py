#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
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


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, render


def discover_vmware_avi_se_if(section):
    yield Service()


def check_vmware_avi_se_if(section):

    yield from check_levels(
        section['throughput'],
        label="Throughput",
        render_func=lambda v: f'{render.networkbandwidth(v/8)}',
        metric_name="if_total_bps", # build-in checkmk metric
    )

    yield from check_levels(
        section['rx_bits'],
        label="In",
        render_func=lambda v: f'{render.networkbandwidth(v/8)}',
        metric_name="if_in_bps", # build-in checkmk metric
    )

    yield from check_levels(
        section['tx_bits'],
        label="Out",
        render_func=lambda v: f'{render.networkbandwidth(v/8)}',
        metric_name="if_out_bps", # build-in checkmk metric
    )

    yield from check_levels(
        section['rx_packets'],
        label="Input packtes",
        render_func=lambda v: f'{round(v, 2)} packets/s',
        metric_name="if_in_pkts", # build-in checkmk metric
        notice_only=True,
    )

    yield from check_levels(
        section['tx_packets'],
        label="Output packtes",
        render_func=lambda v: f'{round(v, 2)} packets/s',
        metric_name="if_out_pkts", # build-in checkmk metric
        notice_only=True,
    )


agent_section_vmware_avi_se_if = AgentSection(
    name = "vmware_avi_se_if",
    parse_function = parse_python_literal,
)


check_plugin_vmware_avi_se_if = CheckPlugin(
    name = "vmware_avi_se_if",
    service_name = "Avi Interface",
    discovery_function = discover_vmware_avi_se_if,
    check_function = check_vmware_avi_se_if,
)

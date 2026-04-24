#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Site Engines Heartbeat

# sample output:
# <<<vmware_avi_se_hb:hb(0)>>>
# {
#     'hb_misses': 0, 
#     'num_outstanding_hb': 0, 
#     'last_hb_req_sent': 3.015833, 
#     'last_hb_resp_recv': 3.015864
# }


import itertools
import json

from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_se_hb(string_table):
    
    flatlist = list(itertools.chain.from_iterable(string_table))
    parsed = json.loads(" ".join(flatlist).replace("'", "\""))
    return parsed


def discover_vmware_avi_se_hb(section):
    yield Service()


def check_vmware_avi_se_hb(params, section):

    yield from check_levels(
        section['hb_misses'],
        label="HB misses",
        levels_upper=("fixed", (1, 10)),
        render_func=lambda v: f'{int(v)}',
        metric_name="vmware_avi_se_hb_misses",
        boundaries=(0, 100)
    )

    yield from check_levels(
        section['hb_outstanding'],
        label="HB outstanding",
        levels_upper=("fixed", (1, 10)),
        render_func=lambda v: f'{int(v)}',
        metric_name="vmware_avi_se_hb_outstanding",
        boundaries=(0, 100)
    )

    yield from check_levels(
        section['last_hb_req_sent'],
        label="Last request",
        levels_upper=params['last_hb_req_sent'],
        render_func=lambda v: f'{round(v, 2)} s',
        metric_name="vmware_avi_se_hb_last_req_age",
        boundaries=(0, 100)
    )

    yield from check_levels(
        section['last_hb_resp_recv'],
        label="Last response",
        levels_upper=params['last_hb_resp_recv'],
        render_func=lambda v: f'{round(v, 2)} s',
        metric_name="vmware_avi_se_hb_last_resp_age",
        boundaries=(0, 100)
    )


agent_section_vmware_avi_se_hb = AgentSection(
    name = "vmware_avi_se_hb",
    parse_function = parse_vmware_avi_se_hb,
)


check_plugin_vmware_avi_se_hb = CheckPlugin(
    name = "vmware_avi_se_hb",
    service_name = "Avi Heartbeat",
    discovery_function = discover_vmware_avi_se_hb,
    check_function = check_vmware_avi_se_hb,
    check_default_parameters={
        "last_hb_req_sent": ("fixed", (30.0, 60.0)),
        "last_hb_resp_recv": ("fixed", (30.0, 60.0)),
    },
    check_ruleset_name = "vmware_avi_se_hb",
)

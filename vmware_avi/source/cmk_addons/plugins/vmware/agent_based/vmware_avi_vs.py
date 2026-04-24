#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Virtual Serivces

# sample output:
# <<<vmware_avi_vs:sep(0)>>>
# {
#     'name': 'domain-c8--kube-system-kube-apiserver-lb-svc',
#     'enabled': True,
#     'state': 'OPER_UP', 
#     'health_score': 100.0, 
#     'num_se_requested': 2, 
#     'num_se_assigned': 2, 
#     'service_engine': [
#         {
#             'uuid': 'se-005056b77158', 
#             'primary': True, 
#             'standby': False, 
#             'connected': True, 
#             'mgmt_ip': {'addr': '10.99.33.23', 'type': 'V4'}, 
#             'active_on_cloud': True, 
#             'active_on_se': True, 
#             'url': 'https://10.99.33.11/api/serviceengine/se-005056b77158'
#         }, 
#         {...}
#     ], 
#     'alert': {'low': 0, 'medium': 0, 'high': 0}, 
#     'rps': 0.0, 
#     'cps': 0.0083333333, 
#     'open_conns': 5.0, 
#     'throughput': 12502.7555555556
# }


import ast
import itertools


from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_vs(string_table):

    parsed = []
    flatlist = list(itertools.chain.from_iterable(string_table))
    
    for f in flatlist:
        i = ast.literal_eval(f)
        parsed.append(i)

    return parsed


def discover_vmware_avi_vs(section):
    for vs in section:
        if vs['enabled'] == True:
            yield Service(item = f"{vs['name']}")


def check_vmware_avi_vs(item, params, section):

    map_state = {
        "OPER_UP": {"cmk": 0, "str": "Up"},
        "OPER_DOWN": {"cmk": 2, "str": "Down"}
    }

    for vs in section:

        if f"{vs['name']}" != item:
            continue

        # State
        if vs['state'] in map_state:
            yield Result(state=State(map_state[vs['state']]["cmk"]), summary=f"State: {map_state[vs['state']]["str"]}")
        else:
            yield Result(state=State(3), summary=f"State: {vs['state']}")
        
        # Healt Score: for virtual services only the health data...
        yield from check_levels(
            vs['health_score'],
            label="Health Score",
            levels_lower=params['health_score_levels_lower'],
            render_func=lambda v: f'{render.percent(v)}',
            metric_name="vmware_avi_health_score",
            boundaries=(0, 100)
        )

        # Service Engines requested/assigend, only print id assigned is lower than requested
        if vs['num_se_assigned'] < vs['num_se_requested']:
            yield Result(state=State(params['state_lower_se_avail_as_req']), summary=f"Service Engines requested/assigend: {vs['num_se_requested']}/{vs['num_se_assigned']}")

        # check service engines data...
        for se in vs['service_engine']:
            if se['connected'] != True:
                yield Result(state=State(params['state_se_not_connected']), summary=f"Service Engine {se['uuid']} not connected")

        # Requests per Second
        yield from check_levels(
            vs['rps'],
            label="RPS",
            render_func=lambda v: f'{round(v, 2)}/s',
            metric_name="vmware_avi_rps",
        )

        # Connections per Second
        yield from check_levels(
            vs['cps'],
            label="CPS",
            render_func=lambda v: f'{round(v, 2)}/s',
            metric_name="vmware_avi_cps",
        )

        # Open Connections
        yield from check_levels(
            vs['open_conns'],
            label="Open connections",
            render_func=lambda v: f'{v}',
            metric_name="vmware_avi_open_conns",
        )

        # Throughput
        yield from check_levels(
            vs['throughput'],
            label="Throughput",
            render_func=lambda v: f'{render.networkbandwidth(v/8)}',
            metric_name="vmware_avi_throughput",
        )
        
        # Alerts
        if vs['alert']['low'] > 0:
            yield Result(state=State.CRIT, summary=f"Low Alarms: {len(vs['alert']['low'])}", notice_only=True)
        if vs['alert']['medium'] > 0:
            yield Result(state=State.CRIT, summary=f"Medium Alarms: {len(vs['alert']['medium'])}", notice_only=True)
        if vs['alert']['high'] > 0:
            yield Result(state=State.CRIT, summary=f"High Alarms: {len(vs['alert']['high'])}", notice_only=True)

    return None


agent_section_vmware_avi_vs = AgentSection(
    name = "vmware_avi_vs",
    parse_function = parse_vmware_avi_vs,
)


check_plugin_vmware_avi_vs = CheckPlugin(
    name = "vmware_avi_vs",
    service_name = "Avi VS %s",
    discovery_function = discover_vmware_avi_vs,
    check_function = check_vmware_avi_vs,
    check_default_parameters = {
        "state_lower_se_avail_as_req": 1, # WARN
        "state_se_not_connected": 2, # CRIT
        "health_score_levels_lower": ("fixed", (90, 60)), # in %
    },
    check_ruleset_name = "vmware_avi_vs",
)

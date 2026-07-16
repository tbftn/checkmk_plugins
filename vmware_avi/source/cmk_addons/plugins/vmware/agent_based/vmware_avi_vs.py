#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Virtual Serivces

# sample output:
# <<<vmware_avi_vs:sep(0)>>>
# {
#     'name': 'VS-01', 
#     'enabled': True, 
#     'state': 'OPER_UP', 
#     'health_score': {
#         'health_score': 78.0, 
#         'anomaly_penalty': 0.0, 
#         'resources_penalty': 16.0, 
#         'performance_score': 94.0, 
#         'security_penalty': 0.0
#     }, 
#     'num_se_requested': 2, 
#     'num_se_assigned': 2, 
#     'pools': ['/api/pool/pool-12345678-1234-abcd-1a2b-0123456789ab'], 
#     'service_engine': [
#         {
#             'uuid': 'se-0a1b2c3d4e5f', 
#             'primary': True, 
#             'standby': False, 
#             'connected': True, 
#             'mgmt_ip': {
#                 'addr': '1.2.3.4', 
#                 'type': 'V4'
#             }, 
#             'active_on_cloud': True, 
#             'active_on_se': True, 
#             'url': 'https://1.2.3.0/api/serviceengine/se-0a1b2c3d4e5f'
#         }, 
#         {...}
#     ], 
#     'metrics': {
#         'l4_server_avg_total_rtt': 2.1071428571, 
#         'l7_client_avg_resp_4xx_avi_errors': 0.0, 
#         'l7_client_avg_complete_responses': 13.8033333333, 
#         'l7_client_avg_client_data_transfer_time': 2498.4535073409, 
#         'l7_client_pct_response_errors': 11.180874185, 
#         'l7_client_avg_resp_5xx_avi_errors': 0.0, 
#         'l4_client_max_open_conns': 183.0, 
#         'l4_client_avg_lossy_connections': 0.0, 
#         'l4_client_avg_total_rtt': 1.2971576227, 
#         'l4_client_avg_complete_conns': 2.5833333333, 
#         'l4_client_avg_errored_connections': 0.0033333333, 
#         'l4_client_avg_bandwidth': 2402090.933333333, 
#         'l4_client_pct_connection_errors': 0.1290322581, 
#         'l7_server_avg_application_response_time': 27.9376878929, 
#         'l7_server_avg_resp_5xx_errors': 0.79, 
#         'l7_server_avg_resp_4xx_errors': 0.7533333333
#     }
# },
# {...}


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_list, yield_health_score, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def discover_vmware_avi_vs(section):
    for vs in section:
        if vs.get("enabled") is True:
            yield Service(item=vs['name'])


def check_vmware_avi_vs(item, params, section):

    map_state = {
        "OPER_UP": {"cmk": 0, "str": "Up"},
        "OPER_DOWN": {"cmk": params['state_vs_down'], "str": "Down"}
    }

    for vs in section:

        if vs['name'] != item:
            continue

        # state
        yield from yield_mapped_result(vs['state'], map_state, "State")

        if vs['state'] == "OPER_DOWN":
            continue

        # health score
        yield from yield_health_score(params['health_score'], vs['health_score'])

        # service engines requested/assigend, only in summary if assigned is lower than requested
        if vs['num_se_assigned'] < vs['num_se_requested']:
            yield Result(state=State(params['state_lower_se_avail_as_req']), summary=f"Service Engines requested/assigned: {vs['num_se_requested']}/{vs['num_se_assigned']}")
        else:
            yield Result(state=State(0), notice=f"Service Engines requested/assigned: {vs['num_se_requested']}/{vs['num_se_assigned']}")

        # pool count - only for information
        yield Result(state=State(0), notice=f"Pools: {len(vs['pools'])}")

        # check service engines data...
        for se in vs['service_engine']:
            if se['connected'] != True:
                yield Result(state=State(params['state_se_not_connected']), summary=f"Service Engine {se['uuid']} not connected")

        # METRICS
        metric_specs = {
            "l4_client_avg_total_rtt": {"label": "Client RTT", "render_func": lambda v: f"{render.time_offset(v)}"},
            "l4_server_avg_total_rtt": {"label": "Server RTT", "render_func": lambda v: f"{render.time_offset(v)}"},
            "l7_server_avg_application_response_time": {"label": "App Response", "render_func": lambda v: f"{render.time_offset(v)}"},
            "l7_client_avg_client_data_transfer_time": {"label": "Data Transfer", "render_func": lambda v: f"{render.time_offset(v)}"},
            "l4_client_avg_bandwidth": {"label": "Throughput", "render_func": lambda v: f"{render.networkbandwidth(v/8)}"},
            "l4_client_max_open_conns": {"label": "Open Connections", "render_func": lambda v: f"{v}"},
            "l4_client_avg_complete_conns": {"label": "Connections", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l4_client_avg_lossy_connections": {"label": "Lossy connections", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l4_client_avg_errored_connections": {"label": "Bad connections", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l4_client_pct_connection_errors": {"label": "Connection errors", "render_func": lambda v: f"{render.percent(v)}", "boundaries": (0, 100)},
            "l7_client_avg_complete_responses": {"label": "Requests", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_server_avg_resp_4xx_errors": {"label": "4xx errors", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_server_avg_resp_5xx_errors": {"label": "5xx errors", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_client_avg_resp_4xx_avi_errors": {"label": "Avi 4xx errors", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_client_avg_resp_5xx_avi_errors": {"label": "Avi 5xx errors", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_client_pct_response_errors": {"label": "Request errors", "render_func": lambda v: f"{render.percent(v)}", "boundaries": (0, 100)},
        }

        end_to_end_metric_names = (
            "l4_client_avg_total_rtt",
            "l4_server_avg_total_rtt",
            "l7_server_avg_application_response_time",
            "l7_client_avg_client_data_transfer_time",
        )

        vs_metrics = dict(vs.get("metrics") or {})

        has_end_to_end_data = any(
            vs_metrics.get(metric_name) is not None
            for metric_name in end_to_end_metric_names
        )

        if has_end_to_end_data:
            for metric_name in end_to_end_metric_names:
                if vs_metrics.get(metric_name) is None:
                    vs_metrics[metric_name] = 0.0

        for metric_name, spec in metric_specs.items():
            value = vs_metrics.get(metric_name)
        
            if value is None:
                continue

            yield from check_levels(
                value,
                levels_upper=params.get(f"{metric_name}_upper"),
                levels_lower=params.get(f"{metric_name}_lower"),
                metric_name=spec.get("metric_name", f"vmware_avi_vs_{metric_name}"),
                render_func=spec["render_func"],
                label=spec["label"],
                boundaries=spec.get("boundaries"),
                notice_only=spec.get("notice_only", True),
            )
        
        
        if has_end_to_end_data:
            end_to_end_time = sum(
                vs_metrics[metric_name]
                for metric_name in end_to_end_metric_names
            )

            yield from check_levels(
                end_to_end_time,
                label="End to End time",
                render_func=render.time_offset,
                metric_name="vmware_avi_vs_end_to_end_time",
                notice_only=True,
            )

    return None


agent_section_vmware_avi_vs = AgentSection(
    name = "vmware_avi_vs",
    parse_function = parse_python_literal_list,
)


check_plugin_vmware_avi_vs = CheckPlugin(
    name = "vmware_avi_vs",
    service_name = "Avi VS %s",
    discovery_function = discover_vmware_avi_vs,
    check_function = check_vmware_avi_vs,
    check_default_parameters = {
        "state_vs_down": 2,
        "state_lower_se_avail_as_req": 1,
        "state_se_not_connected": 2,
        "health_score": {
            "health_score": ("fixed", (85.0, 60.0)),
            "performance_score": ('no_levels', None),
            "resources_penalty": ('no_levels', None),
            "anomaly_penalty": ('no_levels', None),
            "security_penalty": ('no_levels', None),
        }
    },
    check_ruleset_name = "vmware_avi_vs",
)

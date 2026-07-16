#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Pools

# sample output:
# <<<vmware_avi_pool:sep(0)>>>
# {
#     'name': 'Pool-Name-01', 
#     'uuid': 'pool-12345678-1234-abcd-1a2b-0123456789ab', 
#     'enabled': True, 
#     'state': 'OPER_UP', 
#     'num_servers': 16, 
#     'num_servers_enabled': 16, 
#     'num_servers_up': 6,
#     'num_servers_down': 10,
#     'num_servers_disabled': 0,
#     'health_score': {
#         'health_score': 100.0, 
#         'anomaly_penalty': 0.0, 
#         'resources_penalty': 0.0, 
#         'performance_score': 100.0, 
#         'security_penalty': 0.0
#     }, 
#     'alert': {
#         'low': 0, 
#         'medium': 0, 
#         'high': 0
#     }, 
#     'virtualservices': ['/api/virtualservice/virtualservice-12345678-1234-abcd-1a2b-0123456789ab'], 
#     'metrics': {
#         'l7_server_avg_application_response_time': 8.71264367816092, 
#         'l7_server_pct_response_errors': 0.0, 
#         'l7_server_avg_resp_4xx_errors': 0.0, 
#         'l7_server_avg_resp_5xx_errors': 0.0, 
#         'l7_server_avg_complete_responses': 0.29, 
#         'l4_server_avg_total_rtt': 2.625, 
#         'l4_server_avg_bandwidth': 8267.279999999999, 
#         'l4_server_avg_errored_connections': 0.0, 
#         'l4_server_avg_complete_conns': 0.02666666666666667, 
#         'l4_server_max_open_conns': 14.0, 
#         'l4_server_avg_lossy_connections': 0.0
#     }
# }
# {...}


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_list, yield_health_score, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def discover_vmware_avi_pool(section):
    for pool in section:
        if pool.get("enabled") is True and pool.get("state") != "OPER_UNUSED": # if unused, no data available...
            yield Service(item=pool['name'])


def check_vmware_avi_pool(item, params, section):

    map_state = {
        "OPER_UP": {"cmk": 0, "str": "Up"},
        "OPER_DOWN": {"cmk": params['state_pool_down'], "str": "Down"},
        "OPER_UNUSED": {"cmk": 3, "str": "Unused"}
    }

    for pool in section:

        if pool['name'] != item:
            continue

        # state
        yield from yield_mapped_result(pool['state'], map_state, "State")

        if pool['state'] == "OPER_DOWN":
            continue

        # health score
        yield from yield_health_score(params['health_score'], pool['health_score'])

        # servers
        servers = {
            "num_servers": {"label": "Servers", "render_func":  lambda v: f"{v}"},
            "num_servers_up": {"label": "Servers up", "render_func":  lambda v: f"{v}"},
            "num_servers_down": {"label": "Servers down", "render_func":  lambda v: f"{v}"},
            "num_servers_disabled": {"label": "Servers disbaled", "render_func":  lambda v: f"{v}"},
        }

        for num_server, spec in servers.items():
            value = pool.get(num_server)

            if value is None:
                continue

            yield from check_levels(
                value,
                levels_upper=spec.get("levels_upper"),
                levels_lower=spec.get("levels_lower"),
                metric_name=spec.get("metric_name",f"vmware_avi_pool_{num_server}"),
                render_func=spec["render_func"],
                label=spec["label"],
                boundaries=spec.get("boundaries"),
                notice_only=spec.get("notice_only", True),
            )

        # virtual services, only for info
        yield Result(state=State(0), notice=f"Virtual Services: {len(pool['virtualservices'])}")

        # METRICS
        metric_specs = {
            "l4_server_avg_total_rtt": {"label": "Server RTT", "render_func": lambda v: f"{render.time_offset(v)}"},
            "l7_server_avg_application_response_time": {"label": "App Response", "render_func": lambda v: f"{render.time_offset(v)}"},
            "l4_server_avg_bandwidth": {"label": "Throughput", "render_func": lambda v: f"{render.networkbandwidth(v/8)}"},
            "l4_server_max_open_conns": {"label": "Open Connections", "render_func": lambda v: f"{v}"},
            "l4_server_avg_complete_conns": {"label": "New Connections", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l4_server_avg_lossy_connections": {"label": "Lossy connections", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l4_server_avg_errored_connections": {"label": "Bad connections", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_server_avg_complete_responses": {"label": "Requests", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_server_avg_resp_4xx_errors": {"label": "4xx errors", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_server_avg_resp_5xx_errors": {"label": "5xx errors", "render_func": lambda v: f"{round(v, 2)}/s"},
            "l7_server_pct_response_errors": {"label": "Request errors", "render_func": lambda v: f"{render.percent(v)}", "boundaries": (0, 100)},
        }

        end_to_end_metric_names = (
            "l4_server_avg_total_rtt",
            "l7_server_avg_application_response_time",
        )

        pool_metrics = dict(pool.get("metrics") or {})

        has_end_to_end_data = any(
            pool_metrics.get(metric_name) is not None
            for metric_name in end_to_end_metric_names
        )

        if has_end_to_end_data:
            for metric_name in end_to_end_metric_names:
                if pool_metrics.get(metric_name) is None:
                    pool_metrics[metric_name] = 0
        
        for metric_name, spec in metric_specs.items():
            value = pool_metrics.get(metric_name)

            if value is None:
                continue

            yield from check_levels(
                value,
                levels_upper=params.get(f"{metric_name}_upper"),
                levels_lower=params.get(f"{metric_name}_lower"),
                metric_name=spec.get("metric_name", f"vmware_avi_pool_{metric_name}"),
                render_func=spec["render_func"],
                label=spec["label"],
                boundaries=spec.get("boundaries"),
                notice_only=spec.get("notice_only", True),
            )

        if has_end_to_end_data:
            end_to_end_time = sum(
                pool_metrics[metric_name]
                for metric_name in end_to_end_metric_names
            )

            yield from check_levels(
                end_to_end_time,
                label="End to End time",
                render_func=render.time_offset,
                metric_name="vmware_avi_pool_end_to_end_time",
                notice_only=True,
            )

        # alerts
        for severity in ("low", "medium", "high"):
            count = pool.get("alert", {}).get(severity, 0)

            if count > 0:
                yield Result(
                    state=State.CRIT,
                    summary=f"{severity.title()} Alarms: {count}",
                    notice_only=True,
                )
                
    return None


agent_section_vmware_avi_pool = AgentSection(
    name = "vmware_avi_pool",
    parse_function = parse_python_literal_list,
)


check_plugin_vmware_avi_pool = CheckPlugin(
    name = "vmware_avi_pool",
    service_name = "Avi Pool %s",
    discovery_function = discover_vmware_avi_pool,
    check_function = check_vmware_avi_pool,
    check_default_parameters = {
        "state_pool_down": 2,
        "health_score": {
            "health_score": ("fixed", (85.0, 60.0)),
            "performance_score": ("no_levels", None),
            "resources_penalty": ("no_levels", None),
            "anomaly_penalty": ("no_levels", None),
            "security_penalty": ("no_levels", None),
        },
    },
    check_ruleset_name = "vmware_avi_pool",
)

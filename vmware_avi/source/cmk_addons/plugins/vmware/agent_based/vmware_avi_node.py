#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-09-23
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Nodes

# sample output:
# <<<vmware_avi_node:sep(0)>>>
# {
#     'name': '1.2.3.4', 
#     'state': 'CLUSTER_ACTIVE', 
#     'role': 'CLUSTER_LEADER', 
#     'uptime': 22286802.046232,
#     'metrics': {
#         'controller_stats_avg_cpu_usage': 3.5, 
#         'controller_stats_avg_mem_usage': 64.0, 
#         'controller_stats_avg_disk_write_bytes': 223596.167, 
#         'controller_stats_avg_disk_read_bytes': 0.0, 
#         'controller_stats_avg_disk_usage': 51.0,
#     }
# },
# {...}


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_list, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, render


def discover_vmware_avi_node(section):
    for node in section:
        yield Service(item = f"{node['name']}")


def check_vmware_avi_node(item, params, section):

    map_role = {
        "CLUSTER_FOLLOWER": {"cmk": params['state_role_follower'], "str": "Follower"},
        "CLUSTER_LEADER": {"cmk": params['state_role_leader'], "str": "Leader"},
    }

    map_state = {
        "CLUSTER_ACTIVE": {"cmk": 0, "str": "Active"},
        "CLUSTER_STARTING": {"cmk": params['state_starting'], "str": "Starting"},
    }

    for node in section:

        if f"{node['name']}" != item:
            continue
        
        # state
        yield from yield_mapped_result(node['state'], map_state, "State")

        # role
        yield from yield_mapped_result(node['role'], map_role, "Role")
        
        # METRICS
        metric_specs = {
            "controller_stats_avg_cpu_usage": {"label": "CPU", "render_func": lambda v: f"{render.percent(v)}", "notice_only": False},
            "controller_stats_avg_disk_read_bytes": {"label": "Disk read", "render_func": lambda v: f"{render.iobandwidth(v)}"},
            "controller_stats_avg_disk_usage": {"label": "Disk Usage", "render_func": lambda v: f"{render.percent(v)}"},
            "controller_stats_avg_disk_write_bytes": {"label": "Disk write", "render_func": lambda v: f"{render.iobandwidth(v)}"},
            #"controller_stats_avg_mem_buffered": {"label": "Buffered memory", "render_func": lambda v: f"{render.bytes(v)}"},
            #"controller_stats_avg_mem_cached": {"label": "Cached memory", "render_func": lambda v: f"{render.bytes(v)}"},
            "controller_stats_avg_mem_usage": {"label": "Memory", "render_func": lambda v: f"{render.percent(v)}", "notice_only": False},
            #"controller_stats_avg_num_backend_servers": {"label": "Backend Servers", "render_func": lambda v: f"{v}"},
            #"controller_stats_avg_total_se_throughput": {"label": "SE Throughput", "render_func": lambda v: f"{render.networkbandwidth(v/8)}"},
            #"controller_stats_sum_total_se_bytes": {"label": "SE total bytes", "render_func": lambda v: f"{render.bytes(v)}"},
            #"controller_stats_sum_total_vs_bytes": {"label": "VS total bytes", "render_func": lambda v: f"{render.bytes(v)}"},
            #"controller_stats_sum_total_vs_client_bytes": {"label": "VS client bytes", "render_func": lambda v: f"{render.bytes(v)}"},
        }

        node_metrics = dict(node.get("metrics") or {})

        for metric_name, spec in metric_specs.items():
            value = node_metrics.get(metric_name)
        
            if value is None:
                continue

            yield from check_levels(
                value,
                levels_upper=params.get(f"{metric_name}_upper"),
                levels_lower=params.get(f"{metric_name}_lower"),
                metric_name=spec.get("metric_name", f"vmware_avi_node_{metric_name}"),
                render_func=spec["render_func"],
                label=spec["label"],
                boundaries=spec.get("boundaries"),
                notice_only=spec.get("notice_only", True),
            )

        # uptime
        yield from check_levels(
            node['uptime'],
            label="Up since",
            render_func=lambda v: f'{render.timespan(v)}',
            metric_name="vmware_avi_node_uptime",
        )

    return None


agent_section_vmware_avi_node = AgentSection(
    name = "vmware_avi_node",
    parse_function = parse_python_literal_list,
)


check_plugin_vmware_avi_node = CheckPlugin(
    name = "vmware_avi_node",
    service_name = "Avi Node %s",
    discovery_function = discover_vmware_avi_node,
    check_function = check_vmware_avi_node,
    check_default_parameters = {
        "state_role_follower": 0,
        "state_role_leader": 0,
        "state_starting": 1,
        "controller_stats_avg_cpu_usage_upper": ("fixed", (80.0, 90.0)),
        "controller_stats_avg_disk_usage_upper": ("fixed", (80.0, 90.0)),
        "controller_stats_avg_mem_usage_upper": ("fixed", (80.0, 90.0)),
    },
    check_ruleset_name = "vmware_avi_node",
)

#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Graphing: VMware Avi Load Balancer - Pools


from cmk.graphing.v1 import graphs, metrics, Title


UNIT_BITS_PER_SECOND = metrics.Unit(metrics.SINotation("bit/s"))
UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(""))
UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation("/s"), metrics.StrictPrecision(2))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())


# End to End timing
metric_vmware_avi_pool_l4_server_avg_total_rtt = metrics.Metric(
    name = "vmware_avi_pool_l4_server_avg_total_rtt",
    title = Title("Server RTT"),
    unit = UNIT_TIME,
    color = metrics.Color.LIGHT_BLUE,
)

metric_vmware_avi_pool_l7_server_avg_application_response_time = metrics.Metric(
    name = "vmware_avi_pool_l7_server_avg_application_response_time",
    title = Title("App response"),
    unit = UNIT_TIME,
    color = metrics.Color.ORANGE,
)

metric_vmware_avi_pool_end_to_end_time = metrics.Metric(
    name = "vmware_avi_pool_end_to_end_time",
    title = Title("End to End time"),
    unit = UNIT_TIME,
    color = metrics.Color.GRAY,
)

graph_vmware_avi_pool_end_to_end = graphs.Graph(
    name = "vmware_avi_pool_end_to_end",
    title = Title("End to End timing"),
    simple_lines=["vmware_avi_pool_end_to_end_time"],
    compound_lines=[
        "vmware_avi_pool_l4_server_avg_total_rtt", 
        "vmware_avi_pool_l7_server_avg_application_response_time",
    ],
)

# Throughput
metric_vmware_avi_pool_l4_server_avg_bandwidth = metrics.Metric(
    name = "vmware_avi_pool_l4_server_avg_bandwidth",
    title = Title("Throughput"),
    unit = UNIT_BITS_PER_SECOND,
    color = metrics.Color.LIGHT_BLUE
)

# Open connections
metric_vmware_avi_pool_l4_server_max_open_conns = metrics.Metric(
    name = "vmware_avi_pool_l4_server_max_open_conns",
    title = Title("Open Connections"),
    unit = UNIT_NUMBER,
    color = metrics.Color.DARK_BLUE,
)

# New Connections
metric_vmware_avi_pool_l4_server_avg_complete_conns = metrics.Metric(
    name = "vmware_avi_pool_l4_server_avg_complete_conns",
    title = Title("New Connections"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.LIGHT_GREEN,
)

metric_vmware_avi_pool_l4_server_avg_lossy_connections = metrics.Metric(
    name = "vmware_avi_pool_l4_server_avg_lossy_connections",
    title = Title("Lossy connections"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.ORANGE,
)

metric_vmware_avi_pool_l4_server_avg_errored_connections = metrics.Metric(
    name = "vmware_avi_pool_l4_server_avg_errored_connections",
    title = Title("Bad connections"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.RED,
)

graph_vmware_avi_pool_avg_conns = graphs.Graph(
    name = "vmware_avi_pool_avg_conns",
    title = Title("New Connections"),
    compound_lines=[
        "vmware_avi_pool_l4_server_avg_errored_connections",
        "vmware_avi_pool_l4_server_avg_lossy_connections", 
        "vmware_avi_pool_l4_server_avg_complete_conns", 
    ],
)

# Requests
metric_vmware_avi_pool_l7_server_avg_complete_responses = metrics.Metric(
    name = "vmware_avi_pool_l7_server_avg_complete_responses",
    title = Title("Requests"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.LIGHT_GREEN,
)

metric_vmware_avi_pool_l7_server_avg_resp_4xx_errors = metrics.Metric(
    name = "vmware_avi_pool_l7_server_avg_resp_4xx_errors",
    title = Title("4xx errors"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.RED,
)

metric_vmware_avi_pool_l7_server_avg_resp_5xx_errors = metrics.Metric(
    name = "vmware_avi_pool_l7_server_avg_resp_5xx_errors",
    title = Title("5xx errors"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.ORANGE,
)

graph_vmware_avi_pool_avg_resp = graphs.Graph(
    name = "vmware_avi_pool_avg_resp",
    title = Title("Requests"),
    compound_lines=[
        "vmware_avi_pool_l7_server_avg_resp_5xx_errors",
        "vmware_avi_pool_l7_server_avg_resp_4xx_errors", 
        "vmware_avi_pool_l7_server_avg_complete_responses", 
    ],
)

metric_vmware_avi_pool_l7_server_pct_response_errors = metrics.Metric(
    name = "vmware_avi_pool_l7_server_pct_response_errors",
    title = Title("Request errors"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.RED,
)

# Errors - Grph from requetes
graph_vmware_avi_pool_errors = graphs.Graph(
    name = "vmware_avi_pool_errors",
    title = Title("Errors"),
    simple_lines=[
        "vmware_avi_pool_l7_server_pct_response_errors",
    ],
)

# Servers
servers = {
            "num_servers": {"label": "Servers", "render_func":  lambda v: f"{v}"},
            "num_servers_up": {"label": "Servers up", "render_func":  lambda v: f"{v}"},
            "num_servers_down": {"label": "Servers down", "render_func":  lambda v: f"{v}"},
            "num_servers_disabled": {"label": "Servers disbaled", "render_func":  lambda v: f"{v}"},
        }

metric_vmware_avi_pool_num_servers = metrics.Metric(
    name = "vmware_avi_pool_num_servers",
    title = Title("Servers"),
    unit = UNIT_NUMBER,
    color = metrics.Color.BLACK,
)

metric_vmware_avi_pool_num_servers_up = metrics.Metric(
    name = "vmware_avi_pool_num_servers_up",
    title = Title("Servers up"),
    unit = UNIT_NUMBER,
    color = metrics.Color.GREEN,
)

metric_vmware_avi_pool_num_servers_down = metrics.Metric(
    name = "vmware_avi_pool_num_servers_down",
    title = Title("Servers down"),
    unit = UNIT_NUMBER,
    color = metrics.Color.RED,
)

metric_vmware_avi_pool_num_servers_disabled = metrics.Metric(
    name = "vmware_avi_pool_num_servers_disabled",
    title = Title("Servers disabled"),
    unit = UNIT_NUMBER,
    color = metrics.Color.GRAY,
)

graph_vmware_avi_pool_num_servers = graphs.Graph(
    name = "vmware_avi_pool_num_servers",
    title = Title("Servers"),
    simple_lines=["vmware_avi_pool_num_servers"],
    compound_lines=[
        "vmware_avi_pool_num_servers_up", 
        "vmware_avi_pool_num_servers_down",
        "vmware_avi_pool_num_servers_disabled",
    ],
)
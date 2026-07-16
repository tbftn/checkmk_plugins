#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Graphing: VMware Avi Load Balancer - Virtual Services


from cmk.graphing.v1 import graphs, metrics, Title


UNIT_BITS_PER_SECOND = metrics.Unit(metrics.SINotation("bit/s"))
UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(""))
UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation("/s"), metrics.StrictPrecision(2))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())


# End to End timing
metric_vmware_avi_vs_l4_client_avg_total_rtt = metrics.Metric(
    name = "vmware_avi_vs_l4_client_avg_total_rtt",
    title = Title("Client RTT"),
    unit = UNIT_TIME,
    color = metrics.Color.LIGHT_GREEN,
)

metric_vmware_avi_vs_l4_server_avg_total_rtt = metrics.Metric(
    name = "vmware_avi_vs_l4_server_avg_total_rtt",
    title = Title("Server RTT"),
    unit = UNIT_TIME,
    color = metrics.Color.LIGHT_BLUE,
)

metric_vmware_avi_vs_l7_server_avg_application_response_time = metrics.Metric(
    name = "vmware_avi_vs_l7_server_avg_application_response_time",
    title = Title("App response"),
    unit = UNIT_TIME,
    color = metrics.Color.ORANGE,
)

metric_vmware_avi_vs_l7_client_avg_client_data_transfer_time = metrics.Metric(
    name = "vmware_avi_vs_l7_client_avg_client_data_transfer_time",
    title = Title("Data transfer"),
    unit = UNIT_TIME,
    color = metrics.Color.PURPLE,
)

metric_vmware_avi_vs_end_to_end_time = metrics.Metric(
    name = "vmware_avi_vs_end_to_end_time",
    title = Title("End to End time"),
    unit = UNIT_TIME,
    color = metrics.Color.GRAY,
)

graph_vmware_avi_vs_end_to_end = graphs.Graph(
    name = "vmware_avi_vs_end_to_end",
    title = Title("End to End timing"),
    simple_lines=["vmware_avi_vs_end_to_end_time"],
    compound_lines=[
        "vmware_avi_vs_l4_client_avg_total_rtt", 
        "vmware_avi_vs_l4_server_avg_total_rtt", 
        "vmware_avi_vs_l7_server_avg_application_response_time", 
        "vmware_avi_vs_l7_client_avg_client_data_transfer_time",
    ],
)

# Throughput
metric_vmware_avi_vs_l4_client_avg_bandwidth = metrics.Metric(
    name = "vmware_avi_vs_l4_client_avg_bandwidth",
    title = Title("Throughput"),
    unit = UNIT_BITS_PER_SECOND,
    color = metrics.Color.LIGHT_GREEN
)

# Open connections
metric_vmware_avi_vs_l4_client_max_open_conns = metrics.Metric(
    name = "vmware_avi_vs_l4_client_max_open_conns",
    title = Title("Open Connections"),
    unit = UNIT_NUMBER,
    color = metrics.Color.LIGHT_BLUE,
)

# Connections
metric_vmware_avi_vs_l4_client_avg_complete_conns = metrics.Metric(
    name = "vmware_avi_vs_l4_client_avg_complete_conns",
    title = Title("Connections"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.LIGHT_BLUE,
)

metric_vmware_avi_vs_l4_client_avg_lossy_connections = metrics.Metric(
    name = "vmware_avi_vs_l4_client_avg_lossy_connections",
    title = Title("Lossy connections"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.ORANGE,
)

metric_vmware_avi_vs_l4_client_avg_errored_connections = metrics.Metric(
    name = "vmware_avi_vs_l4_client_avg_errored_connections",
    title = Title("Bad connections"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.RED,
)

graph_vmware_avi_vs_avg_conns = graphs.Graph(
    name = "vmware_avi_vs_avg_conns",
    title = Title("Connections"),
    compound_lines=[
        "vmware_avi_vs_l4_client_avg_errored_connections",
        "vmware_avi_vs_l4_client_avg_lossy_connections", 
        "vmware_avi_vs_l4_client_avg_complete_conns", 
    ],
)

metric_vmware_avi_vs_l4_client_pct_connection_errors = metrics.Metric(
    name = "vmware_avi_vs_l4_client_pct_connection_errors",
    title = Title("Connection errors"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.DARK_BLUE,
)

# Requests
metric_vmware_avi_vs_l7_client_avg_complete_responses = metrics.Metric(
    name = "vmware_avi_vs_l7_client_avg_complete_responses",
    title = Title("Requests"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.LIGHT_GREEN,
)

metric_vmware_avi_vs_l7_server_avg_resp_4xx_errors = metrics.Metric(
    name = "vmware_avi_vs_l7_server_avg_resp_4xx_errors",
    title = Title("4xx errors"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.RED,
)

metric_vmware_avi_vs_l7_server_avg_resp_5xx_errors = metrics.Metric(
    name = "vmware_avi_vs_l7_server_avg_resp_5xx_errors",
    title = Title("5xx errors"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.ORANGE,
)

metric_vmware_avi_vs_l7_client_avg_resp_4xx_avi_errors = metrics.Metric(
    name = "vmware_avi_vs_l7_client_avg_resp_4xx_avi_errors",
    title = Title("Avi 4xx errors"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.GRAY,
)

metric_vmware_avi_vs_l7_client_avg_resp_5xx_avi_errors = metrics.Metric(
    name = "vmware_avi_vs_l7_client_avg_resp_5xx_avi_errors",
    title = Title("Avi 5xx errors"),
    unit = UNIT_PER_SECOND,
    color = metrics.Color.PURPLE,
)

graph_vmware_avi_vs_avg_resp = graphs.Graph(
    name = "vmware_avi_vs_avg_resp",
    title = Title("Requests"),
    compound_lines=[
        "vmware_avi_vs_l7_client_avg_resp_5xx_avi_errors",
        "vmware_avi_vs_l7_client_avg_resp_4xx_avi_errors",
        "vmware_avi_vs_l7_server_avg_resp_5xx_errors",
        "vmware_avi_vs_l7_server_avg_resp_4xx_errors", 
        "vmware_avi_vs_l7_client_avg_complete_responses", 
    ],
)

metric_vmware_avi_vs_l7_client_pct_response_errors = metrics.Metric(
    name = "vmware_avi_vs_l7_client_pct_response_errors",
    title = Title("Request errors"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.RED,
)

# Errors - Graph from connections and requetes
graph_vmware_avi_vs_errors = graphs.Graph(
    name = "vmware_avi_vs_errors",
    title = Title("Errors"),
    simple_lines=[
        "vmware_avi_vs_l4_client_pct_connection_errors",
        "vmware_avi_vs_l7_client_pct_response_errors",
    ],
)
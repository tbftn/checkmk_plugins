#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-09-23
# License: GNU General Public License v2
#
# Graphing: VMware Avi Load Balancer - Nodes


from cmk.graphing.v1 import graphs, metrics, perfometers, Title


UNIT_BYTES_PER_SECOND = metrics.Unit(metrics.IECNotation("B/s"))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())


# CPU
metric_vmware_avi_node_controller_stats_avg_cpu_usage = metrics.Metric(
    name = "vmware_avi_node_controller_stats_avg_cpu_usage",
    title = Title("CPU"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.GREEN,
)

perfometer_vmware_avi_node_controller_stats_avg_cpu_usage = perfometers.Perfometer(
    name="vmware_avi_node_controller_stats_avg_cpu_usage",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(100)),
    segments=["vmware_avi_node_controller_stats_avg_cpu_usage"],
)


# DISK IO
metric_vmware_avi_node_controller_stats_avg_disk_read_bytes = metrics.Metric(
    name = "vmware_avi_node_controller_stats_avg_disk_read_bytes",
    title = Title("Disk read"),
    unit = UNIT_BYTES_PER_SECOND,
    color = metrics.Color.GREEN,
)

metric_vmware_avi_node_controller_stats_avg_disk_write_bytes = metrics.Metric(
    name = "vmware_avi_node_controller_stats_avg_disk_write_bytes",
    title = Title("Disk write"),
    unit = UNIT_BYTES_PER_SECOND,
    color = metrics.Color.BLUE,
)

graph_vmware_avi_node_disk_throughput = graphs.Bidirectional(
    name="vmware_avi_node_disk_throughput",
    title=Title("Disk throughput"),
    upper=graphs.Graph(
        name="disk_read_throughput",
        title=Title("Read throughput"),
        compound_lines=["vmware_avi_node_controller_stats_avg_disk_read_bytes"],
    ),
    lower=graphs.Graph(
        name="disk_write_throughput",
        title=Title("Write throughput"),
        compound_lines=["vmware_avi_node_controller_stats_avg_disk_write_bytes"],
    ),
)


# Disk usage
metric_vmware_avi_node_controller_stats_avg_disk_usage = metrics.Metric(
    name = "vmware_avi_node_controller_stats_avg_disk_usage",
    title = Title("Disk usage"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.CYAN,
)


# Memory
metric_vmware_avi_node_controller_stats_avg_mem_usage = metrics.Metric(
    name = "vmware_avi_node_controller_stats_avg_mem_usage",
    title = Title("Memory"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.YELLOW,
)


# Uptime
metric_vmware_avi_node_uptime = metrics.Metric(
    name="vmware_avi_node_uptime",
    title=Title("Uptime"),
    unit=UNIT_TIME,
    color=metrics.Color.DARK_YELLOW,
)

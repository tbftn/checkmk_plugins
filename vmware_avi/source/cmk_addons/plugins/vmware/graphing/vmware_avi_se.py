#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Graphing: VMware Avi Load Balancer - Service Engines


from cmk.graphing.v1 import graphs, metrics, perfometers, Title


UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(""))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())


# Heartbeat
metric_vmware_avi_se_hb_misses = metrics.Metric(
    name = "vmware_avi_se_hb_misses",
    title = Title("HB misses"),
    unit = UNIT_NUMBER,
    color = metrics.Color.RED
)

metric_vmware_avi_se_hb_outstanding = metrics.Metric(
    name = "vmware_avi_se_hb_outstanding",
    title = Title("HB outstanding"),
    unit = UNIT_NUMBER,
    color = metrics.Color.ORANGE
)

metric_vmware_avi_se_hb_last_req_age = metrics.Metric(
    name = "vmware_avi_se_hb_last_req_age",
    title = Title("Last request"),
    unit = UNIT_TIME,
    color = metrics.Color.GRAY
)

metric_vmware_avi_se_hb_last_resp_age = metrics.Metric(
    name = "vmware_avi_se_hb_last_resp_age",
    title = Title("Last response"),
    unit = UNIT_TIME,
    color = metrics.Color.BLUE
)

graph_vmware_avi_se_hb_errors = graphs.Graph(
    name = "vmware_avi_se_hb_errors",
    title = Title("Heartbeat Errors"),
    simple_lines=["vmware_avi_se_hb_misses", "vmware_avi_se_hb_outstanding"],
)

graph_vmware_avi_se_hb_time = graphs.Graph(
    name = "vmware_avi_se_hb_time",
    title = Title("Heartbeat Timing"),
    simple_lines=["vmware_avi_se_hb_last_req_age", "vmware_avi_se_hb_last_resp_age"],
)

perfometer_vmware_avi_se_hb_time = perfometers.Stacked(
    name='perfometer_vmware_avi_se_hb_time',
    upper=perfometers.Perfometer(
        name='perfometer_vmware_avi_se_hb_time_upper',
        segments=['vmware_avi_se_hb_last_req_age'],
        focus_range=perfometers.FocusRange(lower=perfometers.Closed(0), upper=perfometers.Open(60))
    ),
    lower=perfometers.Perfometer(
        name='perfometer_vmware_avi_se_hb_time_lower',
        segments=['vmware_avi_se_hb_last_resp_age'],
        focus_range=perfometers.FocusRange(lower=perfometers.Closed(0), upper=perfometers.Open(60))
    ))

# Memory
metric_vmware_avi_se_mem_usage = metrics.Metric(
    name = "vmware_avi_se_mem_usage",
    title = Title("Memory usage"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.YELLOW,
)

metric_vmware_avi_se_con_mem_usage = metrics.Metric(
    name = "vmware_avi_se_con_mem_usage",
    title = Title("Connection memory usage"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.LIGHT_GREEN,
)

metric_vmware_avi_se_dyn_mem_usage = metrics.Metric(
    name = "vmware_avi_se_dyn_mem_usage",
    title = Title("Dynamic memory usage"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.DARK_BLUE,
)

perfometer_vmware_avi_se_mem_usage = perfometers.Perfometer(
    name='perf_vmware_avi_se_mem_usage',
    focus_range = perfometers.FocusRange(perfometers.Closed(0), perfometers.Closed(100)),
    segments = ["vmware_avi_se_mem_usage"],
)
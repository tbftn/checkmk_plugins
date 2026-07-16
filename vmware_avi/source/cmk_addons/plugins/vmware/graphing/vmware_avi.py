#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Graphing: VMware Avi Load Balancer


from cmk.graphing.v1 import graphs, metrics, perfometers, Title


UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(""))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())


# Cert
metric_vmware_avi_cert_time = metrics.Metric(
    name = "vmware_avi_cert_time",
    title = Title("Remaining certificate validity time"),
    unit = UNIT_TIME,
    color = metrics.Color.YELLOW
)

perfometer_vmware_avi_cert_time = perfometers.Perfometer(
    name='perf_vmware_avi_cert_time',
    focus_range=perfometers.FocusRange(lower=perfometers.Closed(0), upper=perfometers.Open(31536000)),
    segments = ["vmware_avi_cert_time"],
)

# Health Score
metric_vmware_health_health_score = metrics.Metric(
    name = "vmware_avi_health_health_score",
    title = Title("Health score"),
    unit = UNIT_NUMBER,
    color = metrics.Color.GREEN
)

metric_vmware_avi_health_performance_score = metrics.Metric(
    name = "vmware_avi_health_performance_score",
    title = Title("Performance score"),
    unit = UNIT_NUMBER,
    color = metrics.Color.BLUE
)

metric_vmware_avi_health_resources_penalty = metrics.Metric(
    name = "vmware_avi_health_resources_penalty",
    title = Title("Resource penalty"),
    unit = UNIT_NUMBER,
    color = metrics.Color.ORANGE
)

metric_vmware_avi_health_anomaly_penalty = metrics.Metric(
    name = "vmware_avi_health_anomaly_penalty",
    title = Title("Anomaly penalty"),
    unit = UNIT_NUMBER,
    color = metrics.Color.RED
)

metric_vmware_avi_health_security_penalty = metrics.Metric(
    name = "vmware_avi_health_security_penalty",
    title = Title("Security penalty"),
    unit = UNIT_NUMBER,
    color = metrics.Color.PURPLE
)

graph_vmware_avi_health = graphs.Graph(
    name = "vmware_avi_health",
    title = Title("Health score"),
    simple_lines=["vmware_avi_health_performance_score"],
    compound_lines=[
        "vmware_avi_health_health_score",
        "vmware_avi_health_resources_penalty",
        "vmware_avi_health_anomaly_penalty",
        "vmware_avi_health_security_penalty",
    ],
)

perfometer_health_health_score = perfometers.Perfometer(
    name='perf_vmware_avi_health_health_score',
    focus_range = perfometers.FocusRange(perfometers.Closed(0), perfometers.Closed(100)),
    segments = ["vmware_avi_health_health_score"],
)
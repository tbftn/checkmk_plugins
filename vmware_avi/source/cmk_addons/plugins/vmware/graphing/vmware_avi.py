#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Graphing: VMware Avi Load Balancer


from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Bidirectional, Graph
from cmk.graphing.v1.metrics import Color, DecimalNotation, IECNotation, Metric, SINotation, StrictPrecision, TimeNotation, Unit
from cmk.graphing.v1.perfometers import Bidirectional as bi, Closed, FocusRange, Open, Stacked, Perfometer

# Avi Cert
metric_vmware_avi_cert_time = Metric(
    name = "vmware_avi_cert_time",
    title = Title("Remaining certificate validity time"),
    unit = Unit(TimeNotation()),
    color = Color.YELLOW
)

perfometer_vmware_avi_cert_time = Perfometer(
    name='perf_vmware_avi_cert_time',
    focus_range=FocusRange(lower=Closed(0), upper=Open(31536000)),
    segments = ["vmware_avi_cert_time"],
)

# Avi Health Score
metric_vmware_health_score = Metric(
    name = "vmware_avi_health_score",
    title = Title("Health Score"),
    unit = Unit(DecimalNotation("%")),
    color = Color.GREEN
)

metric_vmware_avi_performance_score = Metric(
    name = "vmware_avi_performance_score",
    title = Title("Performance"),
    unit = Unit(DecimalNotation("%")),
    color = Color.LIGHT_GREEN
)

metric_vmware_avi_resources_penalty = Metric(
    name = "vmware_avi_resources_penalty",
    title = Title("Resource Penalty"),
    unit = Unit(DecimalNotation("%")),
    color = Color.ORANGE
)

metric_vmware_avi_anomaly_penalty = Metric(
    name = "vmware_avi_anomaly_penalty",
    title = Title("Anomaly Penalty"),
    unit = Unit(DecimalNotation("%")),
    color = Color.RED
)

metric_vmware_avi_security_penalty = Metric(
    name = "vmware_avi_security_penalty",
    title = Title("Security Penalty"),
    unit = Unit(DecimalNotation("%")),
    color = Color.PURPLE
)

perfometer_vmware_avi_health_score = Perfometer(
    name='perf_vmware_avi_health_score',
    focus_range = FocusRange(Closed(0), Closed(100)),
    segments = ["vmware_avi_health_score"],
)

# Avi SE Heartbeat
metric_vmware_avi_se_hb_misses = Metric(
    name = "vmware_avi_se_hb_misses",
    title = Title("HB misses"),
    unit = Unit(DecimalNotation("")),
    color = Color.RED
)

metric_vmware_avi_se_hb_outstanding = Metric(
    name = "vmware_avi_se_hb_outstanding",
    title = Title("HB outstanding"),
    unit = Unit(DecimalNotation("")),
    color = Color.ORANGE
)

metric_vmware_avi_se_hb_last_req_age = Metric(
    name = "vmware_avi_se_hb_last_req_age",
    title = Title("Last request"),
    unit = Unit(TimeNotation()),
    color = Color.GRAY
)

metric_vmware_avi_se_hb_last_resp_age = Metric(
    name = "vmware_avi_se_hb_last_resp_age",
    title = Title("Last response"),
    unit = Unit(TimeNotation()),
    color = Color.BLUE
)

graph_vmware_avi_se_hb_errors = Graph(
    name = "vmware_avi_se_hb_errors",
    title = Title("Heartbeat Errors"),
    simple_lines=["vmware_avi_se_hb_misses", "vmware_avi_se_hb_outstanding"],
)

graph_vmware_avi_se_hb_time = Graph(
    name = "vmware_avi_se_hb_time",
    title = Title("Heartbeat Timing"),
    simple_lines=["vmware_avi_se_hb_last_req_age", "vmware_avi_se_hb_last_resp_age"],
)

perfometer_vmware_avi_se_hb_time = Stacked(
    name='perfometer_vmware_avi_se_hb_time',
    upper=Perfometer(
        name='perfometer_vmware_avi_se_hb_time_upper',
        segments=['vmware_avi_se_hb_last_req_age'],
        focus_range=FocusRange(lower=Closed(0), upper=Open(60))
    ),
    lower=Perfometer(
        name='perfometer_vmware_avi_se_hb_time_lower',
        segments=['vmware_avi_se_hb_last_resp_age'],
        focus_range=FocusRange(lower=Closed(0), upper=Open(60))
    ))

# Avi SE Interface
metric_vmware_avi_se_if_throughput = Metric(
    name = "vmware_avi_throughput",
    title = Title("Throughput"),
    unit = Unit(SINotation("bit/s")),
    color = Color.YELLOW
)

metric_vmware_avi_se_if_rx_packtes = Metric(
    name = "vmware_avi_se_if_rx_packtes",
    title = Title("Input packtes"),
    unit = Unit(DecimalNotation("/s"), StrictPrecision(2)),
    color = Color.GREEN
)

metric_vmware_avi_se_if_tx_packtes = Metric(
    name = "vmware_avi_se_if_tx_packtes",
    title = Title("Output packtes"),
    unit = Unit(DecimalNotation("/s"), StrictPrecision(2)),
    color = Color.BLUE
)

metric_vmware_avi_se_if_rx_bits = Metric(
    name = "vmware_avi_se_if_rx_bits",
    title = Title("Input bandwith"),
    unit = Unit(SINotation("bit/s")),
    color = Color.GREEN
)

metric_vmware_avi_se_if_tx_bits = Metric(
    name = "vmware_avi_se_if_tx_bits",
    title = Title("Output bandwith"),
    unit = Unit(SINotation("bit/s")),
    color = Color.BLUE
)

graph_vmware_avi_se_if_bits = Bidirectional(
    name = "vmware_avi_se_if_bandwith",
    title = Title("Bandwith"),
    upper = Graph(
        name="upper",
        title=Title("Input bandwith"),
        compound_lines=["vmware_avi_se_if_rx_bits"],
    ),
    lower = Graph(
        name="lower",
        title=Title("Output bandwith"),
        compound_lines=["vmware_avi_se_if_tx_bits"],
    )
)

graph_vmware_avi_se_if_packtes = Bidirectional(
    name = "vmware_avi_se_if_packtes",
    title = Title("Packets"),
    upper = Graph(
        name="upper",
        title=Title("Input packtes"),
        simple_lines=["vmware_avi_se_if_rx_packtes"],
    ),
    lower = Graph(
        name="lower",
        title=Title("Output packtes"),
        simple_lines=["vmware_avi_se_if_tx_packtes"],
    )
)

perfometer_vmware_avi_se_if_bandwith = bi(
    name='perfometer_vmware_avi_se_if_bandwith',
    left=Perfometer(
        name='perfometer_vmware_avi_se_if_bandwith_upper',
        segments=['vmware_avi_se_if_rx_bits'],
        focus_range=FocusRange(lower=Closed(0), upper=Open(1000000))
    ),
    right=Perfometer(
        name='perfometer_vmware_avi_se_if_bandwith_lower',
        segments=['vmware_avi_se_if_tx_bits'],
        focus_range=FocusRange(lower=Closed(0), upper=Open(1000000))
    ))

# Avi SE Mem
metric_vmware_avi_se_mem_usage = Metric(
    name = "vmware_avi_se_mem_usage",
    title = Title("Memory usage"),
    unit = Unit(DecimalNotation("%")),
    color = Color.YELLOW,
)

metric_vmware_avi_se_con_mem_usage = Metric(
    name = "vmware_avi_se_con_mem_usage",
    title = Title("Connection memory usage"),
    unit = Unit(DecimalNotation("%")),
    color = Color.LIGHT_GREEN,
)

metric_vmware_avi_se_dyn_mem_usage = Metric(
    name = "vmware_avi_se_dyn_mem_usage",
    title = Title("Dynamic memory usage"),
    unit = Unit(DecimalNotation("%")),
    color = Color.DARK_BLUE,
)

perfometer_vmware_avi_se_mem_usage = Perfometer(
    name='perf_vmware_avi_se_mem_usage',
    focus_range = FocusRange(Closed(0), Closed(100)),
    segments = ["vmware_avi_se_mem_usage"],
)

# Other
metric_vmware_avi_open_conns = Metric(
    name = "vmware_avi_open_conns",
    title = Title("Open Connections"),
    unit = Unit(DecimalNotation("")),
    color = Color.LIGHT_BLUE,
)

metric_vmware_avi_rps = Metric(
    name = "vmware_avi_rps",
    title = Title("Requests per second"),
    unit = Unit(DecimalNotation("/s"), StrictPrecision(2)),
    color = Color.LIGHT_GREEN,
)

metric_vmware_avi_cps = Metric(
    name = "vmware_avi_cps",
    title = Title("Connections per second"),
    unit = Unit(DecimalNotation("/s"), StrictPrecision(2)),
    color = Color.LIGHT_BLUE,
)

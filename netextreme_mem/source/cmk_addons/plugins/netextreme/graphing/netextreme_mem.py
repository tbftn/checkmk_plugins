#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-05
# License: GNU General Public License v2
#
# Graphing: Extreme Networks Memory Usage


from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph
from cmk.graphing.v1.metrics import Color, DecimalNotation, IECNotation, Metric, Unit
from cmk.graphing.v1.perfometers import Closed, FocusRange, Perfometer


metric_netextreme_mem_sum = Metric(
    name = "netextreme_mem_sum",
    title = Title("Total"),
    unit = Unit(IECNotation("B")),
    color = Color.LIGHT_GREEN,
)


metric_netextreme_mem_system = Metric(
    name = "netextreme_mem_system",
    title = Title("System"),
    unit = Unit(IECNotation("B")),
    color = Color.ORANGE,
)


metric_netextreme_mem_user = Metric(
    name = "netextreme_mem_user",
    title = Title("User"),
    unit = Unit(IECNotation("B")),
    color = Color.GREEN,
)


metric_netextreme_mem_sum_perc = Metric(
    name = "netextreme_mem_sum_perc",
    title = Title("Total memory in %"),
    unit = Unit(DecimalNotation("%")),
    color = Color.BLUE,
)


graph_netextreme_mem_combined = Graph(
    name = "netextreme_mem",
    title = Title("Memory"),
    simple_lines=["netextreme_mem_sum"],
    compound_lines=["netextreme_mem_system", "netextreme_mem_user"],
)


perfometer_netextreme_mem_sum_perc = Perfometer(
    name = "netextreme_mem_sum_perc",
    focus_range = FocusRange(Closed(0), Closed(100)),
    segments = ["netextreme_mem_sum_perc"],
)

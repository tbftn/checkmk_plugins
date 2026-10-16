#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-10-15
# License: GNU General Public License v2
#
# Graphing: Extreme VSP Memory Usage


from cmk.graphing.v1 import metrics, perfometers, Title


UNIT_BYTES = metrics.Unit(metrics.IECNotation("B"))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))


metric_extreme_vsp_mem_used = metrics.Metric(
    name = "extreme_vsp_mem_used",
    title = Title("Used memory"),
    unit = UNIT_BYTES,
    color = metrics.Color.LIGHT_GREEN,
)

metric_extreme_vsp_mem_sum_perc = metrics.Metric(
    name = "extreme_vsp_mem_sum_perc",
    title = Title("Used memory in %"),
    unit = UNIT_PERCENTAGE,
    color = metrics.Color.BLUE,
)

perfometer_extreme_vsp_mem_sum_perc = perfometers.Perfometer(
    name = "extreme_vsp_mem_sum_perc",
    focus_range = perfometers.FocusRange(perfometers.Closed(0), perfometers.Closed(100)),
    segments = ["extreme_vsp_mem_sum_perc"],
)

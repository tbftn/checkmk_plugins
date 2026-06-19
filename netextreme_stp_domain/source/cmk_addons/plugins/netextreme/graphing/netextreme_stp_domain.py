#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-19
# License: GNU General Public License v2
#
# Graphing: Extreme Networks STP Domain


from cmk.graphing.v1 import Title, metrics, perfometers


metric_netextreme_stp_domain_top_changes = metrics.Metric(
    name="netextreme_stp_domain_top_changes",
    title=Title("STP topology changes"),
    color=metrics.Color.BLUE,
    unit=metrics.Unit(metrics.DecimalNotation(""))
)

metric_netextreme_stp_domain_top_changes_rate = metrics.Metric(
    name="netextreme_stp_domain_top_changes_rate",
    title=Title("STP topology change rate"),
    color=metrics.Color.YELLOW,
    unit=metrics.Unit(metrics.DecimalNotation("/min"))
)

metric_netextreme_stp_domain_top_last_change = metrics.Metric(
    name="netextreme_stp_domain_top_last_change",
    title=Title("Time since last STP topology change"),
    color=metrics.Color.GREEN,
    unit=metrics.Unit(metrics.TimeNotation())
)


perfometer_netextreme_stp_domain_top_changes_rate = perfometers.Perfometer(
    name="perfometer_netextreme_stp_domain_top_changes_rate",
    segments=["netextreme_stp_domain_top_changes_rate"],
    focus_range=perfometers.FocusRange(lower=perfometers.Closed(0), upper=perfometers.Open(10))
)

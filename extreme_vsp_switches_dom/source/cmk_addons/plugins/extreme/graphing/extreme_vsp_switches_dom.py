#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-11-04
# License: GNU General Public License v2
#
# Graphing: Extreme VSP Optical Modules (SFP)



from cmk.graphing.v1 import metrics, perfometers, graphs, Title


UNIT_TEMPERATURE = metrics.Unit(metrics.DecimalNotation("°C"))
UNIT_VOLTAGE = metrics.Unit(metrics.DecimalNotation("V"))
UNIT_AMPERE = metrics.Unit(metrics.SINotation("A"))
UNIT_DBM = metrics.Unit(metrics.DecimalNotation("dBm"))


metric_extreme_vsp_switches_dom_temperature = metrics.Metric(
    name = "extreme_vsp_switches_dom_temperature",
    title = Title("Temperature"),
    unit = UNIT_TEMPERATURE,
    color = metrics.Color.ORANGE,
)

metric_extreme_vsp_switches_dom_voltage = metrics.Metric(
    name = "extreme_vsp_switches_dom_voltage",
    title = Title("Voltage"),
    unit = UNIT_VOLTAGE,
    color = metrics.Color.ORANGE,
)

metric_extreme_vsp_switches_dom_bias = metrics.Metric(
    name = "extreme_vsp_switches_dom_bias",
    title = Title("Bias"),
    unit = UNIT_AMPERE,
    color = metrics.Color.LIGHT_ORANGE,
)

metric_extreme_vsp_switches_dom_tx_power = metrics.Metric(
    name = "extreme_vsp_switches_dom_tx_power",
    title = Title("TX power"),
    unit = UNIT_DBM,
    color = metrics.Color.GREEN,
)

metric_extreme_vsp_switches_dom_rx_power = metrics.Metric(
    name = "extreme_vsp_switches_dom_rx_power",
    title = Title("RX power"),
    unit = UNIT_DBM,
    color = metrics.Color.BLUE,
)


perfometer_dom = perfometers.Stacked(
    name='perfometer_extreme_vsp_switches_dom_optical_power',
    upper=perfometers.Perfometer(
        name='perfometer_extreme_vsp_switches_dom_optical_power_lower',
        segments=['extreme_vsp_switches_dom_tx_power'],
        focus_range=perfometers.FocusRange(lower=perfometers.Closed(-40), upper=perfometers.Open(10))
    ),
    lower=perfometers.Perfometer(
        name='perfometer_extreme_vsp_switches_dom_optical_power_upper',
        segments=['extreme_vsp_switches_dom_rx_power'],
        focus_range=perfometers.FocusRange(lower=perfometers.Closed(-40), upper=perfometers.Open(10))
    ),
)
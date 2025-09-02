#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-01
# License: GNU General Public License v2
#
# Graphing: Extreme Networks Optical Modules (SFP)


from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Unit
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer, Stacked


metric_netextreme_rx_signal_power = Metric(
    name='netextreme_input_signal_power',
    title=Title('Input power'),
    color=Color.GREEN,
    unit=Unit(DecimalNotation("dBm")),
)


metric_netextreme_tx_signal_power = Metric(
    name='netextreme_output_signal_power',
    title=Title('Output power'),
    color=Color.BLUE,
    unit=Unit(DecimalNotation("dBm")),
)


perfometer_dom = Stacked(
    name='perfometer_dom',
    upper=Perfometer(
        name='perfometer_dom_upper',
        segments=['netextreme_input_signal_power'],
        focus_range=FocusRange(lower=Closed(-40), upper=Open(30))
    ),
    lower=Perfometer(
        name='perfometer_dom_lower',
        segments=['netextreme_output_signal_power'],
        focus_range=FocusRange(lower=Closed(-40), upper=Open(30))
    ))

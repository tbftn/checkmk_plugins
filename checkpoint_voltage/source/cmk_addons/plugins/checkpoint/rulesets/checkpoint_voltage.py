#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-21
# License: GNU General Public License v2
#
# Ruleset: Check Point Voltage


from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    ServiceState,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostAndItemCondition,
    Topic,
)


def _parameter_form_checkpoint_voltage():
    return Dictionary(
        elements={
            "state_sensor_out_of_range": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if the voltage sensor is out of range"),
                    help_text=Help("Default monitoring state if the voltage sensor is out of range."),
                    prefill=DefaultValue(2)
                )
            ),
            "state_reading_error": DictElement(
                parameter_form=ServiceState(
                    title=Title("Status if the voltage sensor has a reading error"),
                    help_text=Help("Default monitoring state if the voltage sensor has a reading error."),
                    prefill=DefaultValue(3)
                )
            ),
            "performance_data": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Performance data"),
                    label=Label("Enable performance data"),
                    prefill=DefaultValue(value=False)
                )
            )
        }
    )


rule_spec_checkpoint_voltage = CheckParameters(
    name="checkpoint_voltage",
    title=Title("Check Point Voltage"),
    topic=Topic.POWER,
    condition = HostAndItemCondition(item_title=Title("Voltage")),
    parameter_form=_parameter_form_checkpoint_voltage,
)

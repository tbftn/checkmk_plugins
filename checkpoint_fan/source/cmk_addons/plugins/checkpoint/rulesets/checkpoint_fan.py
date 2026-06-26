#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-23
# License: GNU General Public License v2
#
# Ruleset: Check Point Fan


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


def _parameter_form_checkpoint_fan():
    return Dictionary(
        elements={
            "state_sensor_out_of_range": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the fan sensor is out of range"),
                    help_text=Help("Default monitoring state if the fan sensor is out of range."),
                    prefill=DefaultValue(2)
                )
            ),
            "state_reading_error": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the fan sensor has a reading error"),
                    help_text=Help("Default monitoring state if the fan sensor has a reading error."),
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


rule_spec_checkpoint_fan = CheckParameters(
    name="checkpoint_fan",
    title=Title("Check Point Fan"),
    topic=Topic.ENVIRONMENTAL,
    condition = HostAndItemCondition(item_title=Title("Fan")),
    parameter_form=_parameter_form_checkpoint_fan,
)

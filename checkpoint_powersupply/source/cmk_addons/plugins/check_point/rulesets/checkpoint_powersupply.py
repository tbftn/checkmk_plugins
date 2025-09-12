#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-12
# License: GNU General Public License v2
#
# Ruleset: Checkpoint Power Supply


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
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


def _parameter_form_checkpoint_powersupply():
    return Dictionary(
        elements={
            'psu_not_up': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if Power Supply is not "OK", "Present" or "Up"'),
                    help_text=Help('Default monitoring state if the Power Supply is not "OK", "Present" or "Up".'),
                    prefill=DefaultValue(2)
                )
            ),
        }
    )


rule_spec_netextreme_psu_in = CheckParameters(
    name='checkpoint_powersupply',
    title=Title('Check Point Power Supply'),
    topic=Topic.NETWORKING,
    condition = HostAndItemCondition(item_title=Title("Power Supply")),
    parameter_form=_parameter_form_checkpoint_powersupply,
)

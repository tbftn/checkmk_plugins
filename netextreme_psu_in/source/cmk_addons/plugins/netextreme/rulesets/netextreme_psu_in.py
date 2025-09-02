#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-01
# License: GNU General Public License v2
#
# Ruleset: Extreme Networks Power Supply Input


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    ServiceState,
    SimpleLevels,
    migrate_to_integer_simple_levels,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostAndItemCondition,
    Topic,
)


def _parameter_form_netextreme_psu_in():
    return Dictionary(
        elements={
            'levels_upper': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Power Supply Input upper levels'),
                    help_text=Help('Set the upper levels for power in W.'),
                    form_spec_template=Integer(unit_symbol='W'),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(110.0, 120.0)),
                )
            ),
            'psu_powered_off': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if Power Supply is "Powered Off"'),
                    help_text=Help('Default monitoring state if the Power Supply is present but has no power.'),
                    prefill=DefaultValue(2)
                )
            ),
            'psu_failed': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if Power Supply is "Failed"'),
                    help_text=Help('Default monitoring state if the Power Supply and power are present, but an error has occurred.'),
                    prefill=DefaultValue(2)
                )
            ),
        }
    )


rule_spec_netextreme_psu_in = CheckParameters(
    name='netextreme_psu_in',
    title=Title('Extreme Power Supply Input'),
    topic=Topic.NETWORKING,
    condition = HostAndItemCondition(item_title=Title("Power Supply Input")),
    parameter_form=_parameter_form_netextreme_psu_in,
)

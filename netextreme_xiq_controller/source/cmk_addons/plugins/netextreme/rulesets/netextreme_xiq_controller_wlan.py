#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-16
# License: GNU General Public License v2
#
# Ruleset: ExtremeCloud IQ Controller - WLANs


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    LevelsType,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostAndItemCondition,
    Topic,
)


def _parameter_form_netextreme_xiq_controller_wlan():
    return Dictionary(
        elements={
            'levels_upper': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Maximum Number of clients'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol='Clients'),
                    prefill_levels_type = DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(100, 200)),
                )
            ),
        }
    )


rule_spec_netextreme_xiq_controller_wlan = CheckParameters(
    name='netextreme_xiq_controller_wlan',
    title=Title('ExtremeCloud IQ Controller WLAN Clients'),
    topic=Topic.NETWORKING,
    condition = HostAndItemCondition(item_title=Title("WLAN")),
    parameter_form=_parameter_form_netextreme_xiq_controller_wlan,
)

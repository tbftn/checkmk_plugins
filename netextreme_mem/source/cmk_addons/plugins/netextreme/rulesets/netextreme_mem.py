#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-05
# License: GNU General Public License v2
#
# Ruleset: Extreme Networks Memory Usage


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, Integer, LevelDirection, Percentage, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_netextreme_mem():

    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels for the memory usage"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                )
            ),
        }
    )


rule_spec_netextreme_dom = CheckParameters(
    name="netextreme_mem",
    title=Title("Extreme Memory usage"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_netextreme_mem,
    condition=HostCondition(),
)

#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-10-15
# License: GNU General Public License v2
#
# Ruleset: Extreme VSP Memory Usage


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, LevelDirection, Percentage, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_extreme_vsp_mem():

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


rule_spec_extreme_vsp_mem = CheckParameters(
    name="extreme_vsp_mem",
    title=Title("Extreme VSP Memory usage"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_extreme_vsp_mem,
    condition=HostCondition(),
)

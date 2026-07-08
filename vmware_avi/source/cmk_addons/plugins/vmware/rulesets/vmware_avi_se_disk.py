#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Service Engines Disk


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    LevelsType,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)


def parameter_form_vmware_avi_se_disk():
    return Dictionary(
        elements={
            "usage": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper Levels for Disk usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(80.0, 90.0)),
                )
            )
        }
    )


rule_spec_vmware_avi_se_disk = CheckParameters(
    name="vmware_avi_se_avi",
    title=Title("VMware Avi Service Engine Disk"),
    topic=Topic.VIRTUALIZATION,
    condition = HostCondition(),
    parameter_form=parameter_form_vmware_avi_se_disk,
)

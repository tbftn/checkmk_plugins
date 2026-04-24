#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Service Engines CPU


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


def parameter_form_vmware_avi_se_cpu():
    return Dictionary(
        elements={
            'util': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Upper Levels for total CPU utilization'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(80.0, 90.0)),
                )
            )
        }
    )


rule_spec_vmware_avi_se_cpu = CheckParameters(
    name='vmware_avi_se_cpu',
    title=Title('VMware Avi Service Engine CPU Usage'),
    topic=Topic.VIRTUALIZATION,
    condition = HostCondition(),
    parameter_form=parameter_form_vmware_avi_se_cpu,
)

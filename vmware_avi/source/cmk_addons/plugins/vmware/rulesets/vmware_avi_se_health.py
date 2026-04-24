#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Service Engines Health


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


def parameter_form_vmware_avi_se_health():
    return Dictionary(
        elements={
            "health_score": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower Health Score levels"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(90.0, 60.0)),
                )
            ),
            "performance_score": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower Performance Score levels"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(90.0, 60.0)),
                )
            ),
            "resources_penalty": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper Resource Penalty levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(10.0, 50.0)),
                )
            ),
            "anomaly_penalty": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper Anomaly Penalty levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(10.0, 50.0)),
                )
            ),
            "security_penalty": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper Security Penalty levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(10.0, 50.0)),
                )
            ),
        }
    )


rule_spec_vmware_avi_se_health = CheckParameters(
    name='vmware_avi_se_health',
    title=Title('VMware Avi Service Engine Health'),
    topic=Topic.VIRTUALIZATION,
    condition = HostCondition(),
    parameter_form=parameter_form_vmware_avi_se_health,
)

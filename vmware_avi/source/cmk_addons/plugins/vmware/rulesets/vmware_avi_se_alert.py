#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Service Engines Alerts


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    LevelsType,
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostCondition,
    Topic,
)


def parameter_form_vmware_avi_se_alert():
    return Dictionary(
        elements={
            'low': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Low Alerts'),
                    help_text=Help('Set the thresholds for the number of low alarms.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1, 1)),
                )
            ),
            'medium': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Medium Alerts'),
                    help_text=Help('Set the thresholds for the number of medium alarms.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1, 1)),
                )
            ),
            'high': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('High Alerts'),
                    help_text=Help('Set the thresholds for the number of high alarms.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1, 1)),
                )
            ),
        }
    )


rule_spec_vmware_avi_se_alert = CheckParameters(
    name='vmware_avi_se_alert',
    title=Title('VMware Avi Service Engine Alerts'),
    topic=Topic.VIRTUALIZATION,
    condition = HostCondition(),
    parameter_form=parameter_form_vmware_avi_se_alert,
)

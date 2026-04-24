#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Virtual Services


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    LevelsType,
    Percentage,
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostAndItemCondition,
    Topic,
)


def parameter_form_vmware_avi_vs():
    return Dictionary(
        elements={
            'state_lower_se_avail_as_req': DictElement(
                parameter_form=ServiceState(
                    title=Title('Status when more Service Engines are requested than available'),
                    help_text=Help('Status when more Service Engines are requested than available.'),
                    prefill=DefaultValue(1)
                )
            ),
            'state_se_not_connected': DictElement(
                parameter_form=ServiceState(
                    title=Title('Status when one or more Service Engines are not connected'),
                    help_text=Help('Status when one or more Service Engines are not connected.'),
                    prefill=DefaultValue(2)
                )
            ),
            'health_score_levels_lower': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Lower Healt Score levels'),
                    help_text=Help('Set the lower levels for the Health Score.'),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(90.0, 60.0)),
                )
            ),
        }
    )


rule_spec_vmware_avi_vs = CheckParameters(
    name='vmware_avi_vs',
    title=Title('VMware Avi Virtual Services'),
    topic=Topic.VIRTUALIZATION,
    condition = HostAndItemCondition(item_title=Title("Avi VS")),
    parameter_form=parameter_form_vmware_avi_vs,
)

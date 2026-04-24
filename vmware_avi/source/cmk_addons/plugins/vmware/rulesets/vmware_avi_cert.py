#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Certificates


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    LevelsType,
    SimpleLevels,
    TimeSpan,
    TimeMagnitude,
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def parameter_form_vmware_avi_cert():
    return Dictionary(
        elements={
            'days_until_expire': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Days until expiration'),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.DAY]),
                    prefill_fixed_levels=DefaultValue(value=(90.0 * 86400, 30.0 * 86400))
                )
            ),
        }
    )


rule_spec_vmware_avi_cert = CheckParameters(
    name="vmware_avi_cert",
    title=Title("VMware Avi Certificates"),
    topic=Topic.VIRTUALIZATION,
    parameter_form=parameter_form_vmware_avi_cert,
    condition=HostAndItemCondition(item_title=Title("Avi Cert")),
)

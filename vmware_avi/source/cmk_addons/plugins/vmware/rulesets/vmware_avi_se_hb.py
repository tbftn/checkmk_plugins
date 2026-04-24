#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Service Engines Heartbeat


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    LevelsType,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)


def parameter_form_vmware_avi_se_hb():
    return Dictionary(
        elements={
            "last_hb_req_sent": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Maximal age of last HB request"),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_fixed_levels=DefaultValue(value=(30.0, 60.0))
                )
            ),
            "last_hb_resp_recv": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Maximal age of last HB response"),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_fixed_levels=DefaultValue(value=(30.0, 60.0))
                )
            ),
        }
    )


rule_spec_vmware_avi_se_hb = CheckParameters(
    name="vmware_avi_se_hb",
    title=Title("VMware Avi Service Engine Heartbeat"),
    topic=Topic.VIRTUALIZATION,
    condition = HostCondition(),
    parameter_form=parameter_form_vmware_avi_se_hb,
)

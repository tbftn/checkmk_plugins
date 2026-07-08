#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Clouds


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    ServiceState,
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def parameter_form_vmware_avi_cloud():
    return Dictionary(
        elements={
            "state_failed": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when Cloud state is Failed"),
                    prefill=DefaultValue(2)
                ),
            ),
            "state_in_progress": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when Cloud state is In progress"),
                    prefill=DefaultValue(1)
                ),
            )
        }
    )


rule_spec_vmware_avi_cert = CheckParameters(
    name="vmware_avi_cloud",
    title=Title("VMware Avi Clouds"),
    topic=Topic.VIRTUALIZATION,
    parameter_form=parameter_form_vmware_avi_cloud,
    condition=HostAndItemCondition(item_title=Title("Avi Cloud")),
)

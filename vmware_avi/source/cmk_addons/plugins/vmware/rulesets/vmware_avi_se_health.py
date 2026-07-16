#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-15
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Service Engines Health


from cmk_addons.plugins.vmware.lib.vmware_avi import param_health_score
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import Dictionary
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def parameter_form_vmware_avi_se_health():
    return Dictionary(
        elements={
            "health_score": param_health_score()
        }
    )


rule_spec_vmware_avi_se_health = CheckParameters(
    name='vmware_avi_se_health',
    title=Title('VMware Avi Service Engine Health'),
    topic=Topic.VIRTUALIZATION,
    condition = HostCondition(),
    parameter_form=parameter_form_vmware_avi_se_health,
)

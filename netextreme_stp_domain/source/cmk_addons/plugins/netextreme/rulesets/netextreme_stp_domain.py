#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-19
# License: GNU General Public License v2
#
# Ruleset: Extreme Networks STP Domain


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    LevelsType,
    ServiceState,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostAndItemCondition,
    Topic,
)


def _parameter_form_netextreme_stp_domain():
    return Dictionary(
        elements={
            'top_changes_rate': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Topology changes rate'),
                    help_text=Help('Set the upper levels for Topology changes rate.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/min'),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            'last_top_change': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Last topology change'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_fixed_levels=DefaultValue(value=(180, 120)),
                )
            ),
            'state_bridge_not_root': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if the bridge is not the root brigde'),
                    help_text=Help('Default monitoring state if the bridge is not the root brigde.'),
                    prefill=DefaultValue(0)
                )
            ),
            'state_rstp_not_enabled': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if RSTP is not enabled'),
                    help_text=Help('Default monitoring state if RSTP is not enabled.'),
                    prefill=DefaultValue(1)
                )
            ),
            'state_rrfailover_not_enabled': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if Rapid Root Failover is not enabled'),
                    help_text=Help('Default monitoring state if Rapid Root Failover is not enabled.'),
                    prefill=DefaultValue(1)
                )
            ),
        }
    )


rule_spec_netextreme_stp_domain = CheckParameters(
    name='netextreme_stp_domain',
    title=Title('Extreme STP Domain'),
    topic=Topic.NETWORKING,
    condition = HostAndItemCondition(item_title=Title("STP Domain")),
    parameter_form=_parameter_form_netextreme_stp_domain,
)

#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Pools


from cmk_addons.plugins.vmware.lib.vmware_avi import param_health_score
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    LevelDirection,
    LevelsType,
    Percentage,
    ServiceState,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)

def parameter_form_vmware_avi_pool():
    return Dictionary(
        elements={
            "state_pool_down": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when pool status is Down"),
                    prefill=DefaultValue(2)
                )
            ),
            "health_score": param_health_score(),
            "l4_server_avg_total_rtt_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Server RTT"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5, 10)),
                )
            ),
            "l7_server_avg_application_response_time_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("App response"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5, 10)),
                )
            ),
            "l4_server_max_open_conns_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Open connections"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(10, 20)),
                )
            ),
            "l4_server_avg_complete_conns_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("New connections rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l4_server_avg_lossy_connections_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lossy connections rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l4_server_avg_errored_connections_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Bad connections rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l7_server_avg_complete_responses_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Requests rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l7_server_avg_resp_4xx_errors_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("4xx errors rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l7_server_avg_resp_5xx_errors_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("5xx errors rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l7_server_pct_response_errors_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Request errors"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5.0, 10.0)),
                )
            ),
        }
    )

rule_spec_vmware_avi_pool = CheckParameters(
    name="vmware_avi_pool",
    title=Title("VMware Avi Pools"),
    topic=Topic.VIRTUALIZATION,
    condition = HostAndItemCondition(item_title=Title("Avi Pool")),
    parameter_form=parameter_form_vmware_avi_pool,
)

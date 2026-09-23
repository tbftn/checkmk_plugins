#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Virtual Services


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


def parameter_form_vmware_avi_vs():
    return Dictionary(
        elements={
            "state_vs_down": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when VS is Down"),
                    prefill=DefaultValue(2)
                )
            ),
            "state_vs_resources": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when VS have problems with there resources"),
                    prefill=DefaultValue(2)
                )
            ),
            "state_vs_partitioned": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when VS is Partitioned"),
                    prefill=DefaultValue(1)
                )
            ),
            "state_vs_creating": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when VS is Creating"),
                    prefill=DefaultValue(1)
                )
            ),
            "state_lower_se_avail_as_req": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when more Service Engines are requested than available"),
                    prefill=DefaultValue(1)
                )
            ),
            "state_se_not_connected": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when one or more Service Engines are not connected"),
                    prefill=DefaultValue(2)
                )
            ),
            "health_score": param_health_score(),
            "l4_client_avg_total_rtt_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Client RTT"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5, 10)),
                )
            ),
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
                    title=Title("App response time"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5, 10)),
                )
            ),
            "l7_client_avg_client_data_transfer_time_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Data transfer time"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(displayed_magnitudes=[TimeMagnitude.SECOND]),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5, 10)),
                )
            ),
            "l4_client_max_open_conns_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Open connections"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(10, 20)),
                )
            ),
            "l4_client_avg_complete_conns_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Connections rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l4_client_avg_lossy_connections_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lossy connections rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l4_client_avg_errored_connections_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Bad connections rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l4_client_pct_connection_errors_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Connections errors"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(5.0, 10.0)),
                )
            ),
            "l7_client_avg_complete_responses_upper": DictElement(
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
            "l7_client_avg_resp_4xx_avi_errors_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Avi 4xx errors rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol='/s'),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(1.0, 2.0)),
                )
            ),
            "l7_client_avg_resp_5xx_avi_errors_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Avi 5xx errors rate"),
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


rule_spec_vmware_avi_vs = CheckParameters(
    name="vmware_avi_vs",
    title=Title("VMware Avi Virtual Services"),
    topic=Topic.VIRTUALIZATION,
    condition = HostAndItemCondition(item_title=Title("Avi VS")),
    parameter_form=parameter_form_vmware_avi_vs,
)

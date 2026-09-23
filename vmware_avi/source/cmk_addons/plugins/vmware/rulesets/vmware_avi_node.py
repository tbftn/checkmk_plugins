#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-09-23
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer - Nodes


from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    LevelsType,
    Percentage,
    ServiceState,
    SIMagnitude,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)


def parameter_form_vmware_avi_node():
    return Dictionary(
        elements={
            "state_role_follower": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when Node is role Follower"),
                    prefill=DefaultValue(0)
                )
            ),
            "state_role_leader": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when Node is role Leader"),
                    prefill=DefaultValue(0)
                )
            ),
            "state_starting": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when Node is Starting"),
                    prefill=DefaultValue(1)
                )
            ),
            "controller_stats_avg_cpu_usage_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("CPU usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(80.0, 90.0)),
                )
            ),
            "controller_stats_avg_disk_read_bytes_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Disk read throughput per second"),
                    form_spec_template=DataSize(
                        displayed_magnitudes=[SIMagnitude.KILO, SIMagnitude.MEGA, SIMagnitude.TERA],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((50_000_000, 100_000_000)),
                )
            ),
            "controller_stats_avg_disk_write_bytes_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Disk write throughput per second"),
                    form_spec_template=DataSize(
                        displayed_magnitudes=[SIMagnitude.KILO, SIMagnitude.MEGA, SIMagnitude.TERA],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((50_000_000, 100_000_000)),
                )
            ),
            "controller_stats_avg_disk_usage_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Disk usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(80.0, 90.0)),
                )
            ),
            "controller_stats_avg_mem_usage_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Memory usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_levels_type=DefaultValue(LevelsType.FIXED),
                    prefill_fixed_levels=DefaultValue(value=(80.0, 90.0)),
                )
            ),
        }
    )


rule_spec_vmware_avi_node = CheckParameters(
    name="vmware_avi_node",
    title=Title("VMware Avi Nodes"),
    topic=Topic.VIRTUALIZATION,
    condition = HostAndItemCondition(item_title=Title("Avi Node")),
    parameter_form=parameter_form_vmware_avi_node,
)

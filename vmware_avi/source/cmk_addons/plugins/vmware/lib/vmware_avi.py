#!/usr/bin/env python3
#-*- encoding: utf-8
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-16
# License: GNU General Public License v2
#
# Lib: VMware Avi Load Balancer


import ast
import itertools

from cmk.agent_based.v2 import check_levels, State, Result
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, LevelDirection, LevelsType, Float, SimpleLevels


def parse_python_literals(string_table):
    """Parse all non-empty entries from a Checkmk string_table."""
    flat = [
        line.strip()
        for line in itertools.chain.from_iterable(string_table)
        if line.strip()
    ]

    return [ast.literal_eval(line) for line in flat]


def parse_python_literal_dict(string_table):
    parsed = parse_python_literals(string_table)

    if not parsed:
        return {}

    return parsed[0]


def parse_python_literal_list(string_table):
    return parse_python_literals(string_table)


def yield_mapped_result(value, mapping, label):
    if value is None:
        yield Result(
            state=State(0),
            summary=f"{label}: N/A",
        )
        return

    if value in mapping:
        yield Result(
            state=State(mapping[value]['cmk']),
            summary=f"{label}: {mapping[value]['str']}",
        )
    else:
        yield Result(
            state=State(3),
            summary=f"{label}: {value}",
        )


# health score
def yield_health_score(params, values):
    
    scores = {
        "health_score": {"label": "Health score", "levels_lower": params.get("health_score", None), "notice_only": False},
        "performance_score": {"label": "Performance score", "levels_lower": params.get("performance_score", None)},
        "resources_penalty": {"label": "Resource penalty", "levels_upper": params.get("resources_penalty", None)},
        "anomaly_penalty": {"label": "Anomaly penalty", "levels_upper": params.get("anomaly_penalty", None)},
        "security_penalty": {"label": "Security penalty", "levels_upper": params.get("security_penalty", None)},
    }

    for s in scores:
        if values.get(s, None) != None:
            yield from check_levels(
                values[s],
                levels_upper=scores[s].get("levels_upper", None),
                levels_lower=scores[s].get("levels_lower", None),
                metric_name=f"vmware_avi_health_{s}",
                render_func=lambda v: f"{v}",
                label=scores[s]['label'],
                boundaries=(0, 100),
                notice_only=scores[s].get("notice_only", True)
            )

def param_health_score():
    return DictElement(
        parameter_form=Dictionary(
            title=Title("Health score"),
            elements = {
                "health_score": DictElement(
                    parameter_form=SimpleLevels(
                        title=Title("Lower Health score levels"),
                        level_direction=LevelDirection.LOWER,
                        form_spec_template=Float(),
                        prefill_levels_type=DefaultValue(LevelsType.FIXED),
                        prefill_fixed_levels=DefaultValue(value=(85.0, 60.0)),
                    )
                ),
                "performance_score": DictElement(
                    parameter_form=SimpleLevels(
                        title=Title("Lower Performance score levels"),
                        level_direction=LevelDirection.LOWER,
                        form_spec_template=Float(),
                        prefill_levels_type=DefaultValue(LevelsType.NONE),
                        prefill_fixed_levels=DefaultValue(value=(85.0, 60.0)),
                    )
                ),
                "resources_penalty": DictElement(
                    parameter_form=SimpleLevels(
                        title=Title("Upper Resource penalty levels"),
                        level_direction=LevelDirection.UPPER,
                        form_spec_template=Float(),
                        prefill_levels_type=DefaultValue(LevelsType.NONE),
                        prefill_fixed_levels=DefaultValue(value=(10.0, 50.0)),
                    )
                ),
                "anomaly_penalty": DictElement(
                    parameter_form=SimpleLevels(
                        title=Title("Upper Anomaly penalty levels"),
                        level_direction=LevelDirection.UPPER,
                        form_spec_template=Float(),
                        prefill_levels_type=DefaultValue(LevelsType.NONE),
                        prefill_fixed_levels=DefaultValue(value=(10.0, 50.0)),
                    )
                ),
                "security_penalty": DictElement(
                    parameter_form=SimpleLevels(
                        title=Title("Upper Security penalty levels"),
                        level_direction=LevelDirection.UPPER,
                        form_spec_template=Float(),
                        prefill_levels_type=DefaultValue(LevelsType.NONE),
                        prefill_fixed_levels=DefaultValue(value=(10.0, 50.0)),
                    )
                ),
            }
        )
    )
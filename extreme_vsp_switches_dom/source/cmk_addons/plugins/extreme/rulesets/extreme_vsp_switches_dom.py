#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-11-04
# License: GNU General Public License v2
#
# Ruleset: Extreme VSP Optical Modules (SFP)


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    FixedValue,
    LevelDirection,
    LevelsType,
    SimpleLevels,
    migrate_to_float_simple_levels,
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _custom_levels_form(dom_title, unit_symbol):
    return Dictionary(
        elements={
            "upper_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title(f"Upper levels for the {dom_title}"),
                    migrate=migrate_to_float_simple_levels,
                    form_spec_template=Float(unit_symbol=unit_symbol),
                    level_direction=LevelDirection.UPPER,
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(0.0, 0.0)),
                )
            ),
            "lower_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title(f"Lower levels for the {dom_title}"),
                    migrate=migrate_to_float_simple_levels,
                    form_spec_template=Float(unit_symbol=unit_symbol),
                    level_direction=LevelDirection.LOWER,
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=DefaultValue(value=(0.0, 0.0)),
                )
            ),
        }
    )


def _sensor_dom(dom_title, unit_symbol):
    return DictElement(
        parameter_form=CascadingSingleChoice(
            title=Title(dom_title),
            help_text=Help("Check the status of the " + dom_title + " sensor. \'Use device levels\': Use levels that are specified by device." + \
                    "You can check there levles on the cli from the extreme device with the command <show pluggable-optical-modules detail [port]>. " + \
                    "\'Use the following levels\': Use custom levels. Here you can specify custom thresholds or no thresholds (always up)."),
            prefill=DefaultValue("device"),
            elements=[
                CascadingSingleChoiceElement(
                    name="device",
                    title=Title("Use device levels"),
                    parameter_form=FixedValue(value=None),
                ),
                CascadingSingleChoiceElement(
                    name="custom",
                    title=Title("Use the following levels"),
                    parameter_form=_custom_levels_form(dom_title, unit_symbol),
                ),
            ],
        )
    )


def _parameter_extreme_vsp_switches_dom():
    return Dictionary(
        elements={
            "rx": _sensor_dom("RX Power", "dBm"),
            "tx": _sensor_dom("TX Power", "dBm"),
            "temp": _sensor_dom("Temperature", "°C"),
            "bias": _sensor_dom("Bias", "mA"),
            "volt": _sensor_dom("Voltage", "V"),
        }
    )


rule_spec_extreme_vsp_switches_dom = CheckParameters(
    name="extreme_vsp_switches_dom",
    title=Title("Extreme VSP Digital Optical Monitoring (DOM)"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_extreme_vsp_switches_dom,
    condition=HostAndItemCondition(item_title=Title("DOM Port")),
)

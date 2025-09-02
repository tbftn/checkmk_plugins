#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-01
# License: GNU General Public License v2
#
# Ruleset: Extreme Networks Optical Modules (SFP)


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    SimpleLevels,
    FixedValue,
    LevelDirection,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    Float,
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _custom_levels_form(dom_title):
    return Dictionary(
        elements={
            "upper_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title(f"Upper levels for the {dom_title}"),
                    form_spec_template=Float(unit_symbol='dBm'),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(0.0, 0.0)),
                )
            ),
            "lower_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title(f"Lower levels for the {dom_title}"),
                    form_spec_template=Float(unit_symbol='dBm'),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue(value=(0.0, 0.0)),
                )
            ),
        }
    )


def _sensor_dom(dom_title):
    # Auswahl: no (immer OK), device (Geräte-Grenzen), custom (eigene Grenzwerte)
    return DictElement(
        parameter_form=CascadingSingleChoice(
            title=Title(dom_title),
            help_text=Help("Check the status of the " + dom_title + " sensor. \'Use device levels\': Use levels that are specified by device." + \
                    "You can check there levles on the cli from the extreme device with the command <show port [port] tranceiver information detail>. " + \
                    "\'Use the following levels\': Use levels that are specified by device. Here you can specify custom thresholds or no thresholds (always up)."),
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
                    parameter_form=_custom_levels_form(dom_title),
                ),
            ],
        )
    )


def _parameter_netextreme_dom():
    return Dictionary(
        elements={
            "input_power": _sensor_dom("Input Power (RX)"),
            "output_power": _sensor_dom("Output Power (TX)"),
        }
    )


rule_spec_netextreme_dom = CheckParameters(
    name="netextreme_dom",
    title=Title("Extreme Digital Optical Monitoring (DOM)"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_netextreme_dom,
    condition=HostAndItemCondition(item_title=Title("DOM Port")),
)

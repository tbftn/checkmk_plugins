#!/usr/bin/env python3
#-*- encoding: utf-8
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer


from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, DictElement, Dictionary, MultipleChoice, MultipleChoiceElement, String, Password, validators
from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent


def _valuespec_special_agent_vmware_avi():
    
    return Dictionary(
        elements={
            "username": DictElement(
                parameter_form=String(
                    title=Title("Username"),
                    help_text=Help("User ID for API access"),
                ),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    help_text=Help("Password for the user"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "tenant": DictElement(
                parameter_form=String(
                    title=Title("Tenant"),
                    help_text=Help("Used tenant. Default is 'admin'"),
                ),
                required=True,
            ),
            #"verify_ssl": DictElement(
            #    parameter_form=BooleanChoice(
            #        title=Title("Verify SSL"),
            #        help_text=Help("Use SSL"),
            #        label=Label("Verify SSL"),
            #    )
            #),
            "sections": DictElement(
                parameter_form=MultipleChoice(
                    title=Title("Get information about..."),
                    help_text=Help(
                        "Alerts: Found in the web interface at: Operations > Alerts > All Alerts. "
                        "Certificates: Found in the web interface at: Templates > Security > SSL/TLS Certificates. "
                        "Clouds: Found in the web interface at: Infrastructure > Clouds. "
                        "Cluster and Nodes: Found in the web interface at: Infrastructure > Controller > Nodes. "
                        "Serice Engines: Found in the web interface at: Infrastructure > Dashboard. "
                        "Virtual Services: Found in the web interface at: Applications > Virtual Services."
                    ),
                    elements=[
                        MultipleChoiceElement(
                            name="alert", title=Title("Alerts"),
                        ),
                        MultipleChoiceElement(
                            name="certificate", title=Title("Certificates"),
                        ),
                        MultipleChoiceElement(
                            name="cloud", title=Title("Clouds"),
                        ),
                        MultipleChoiceElement(
                            name="cluster", title=Title("Cluster and Nodes"),
                        ),
                        MultipleChoiceElement(
                            name="service_engine", title=Title("Service Engines (monitor hosts with piggyback data)"),
                        ),
                        MultipleChoiceElement(
                            name="virtual_service", title=Title("Virtual Services"),
                        ),
                    ],
                    prefill=DefaultValue(
                        [
                            "alert",
                            "certificate",
                            "cluster",
                            "cloud",
                            "service_engine",
                            "virtual_service",
                        ]
                    ),
                    show_toggle_all=True,
                ),
            ),
        },
    )


rule_spec_vmware_avi = SpecialAgent(
    name="vmware_avi",
    title=Title("VMware Avi Load Balancer"),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_special_agent_vmware_avi,
)
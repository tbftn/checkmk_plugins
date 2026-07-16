#!/usr/bin/env python3
#-*- encoding: utf-8
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-15
# License: GNU General Public License v2
#
# Ruleset: VMware Avi Load Balancer


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, MultipleChoice, MultipleChoiceElement, String, Password, validators
from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent


def _valuespec_special_agent_vmware_avi():
    
    return Dictionary(
        elements={
            "username": DictElement(
                parameter_form=String(
                    title=Title("Username"),
                    help_text=Help("Username of the account used to access the Avi REST API."),
                ),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    help_text=Help("Password of the account used to access the Avi REST API."),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "tenant": DictElement(
                parameter_form=String(
                    title=Title("Tenant"),
                    help_text=Help("Avi tenant to query. Use 'admin' for the default administrative tenant."),
                ),
                required=True,
            ),
            "version": DictElement(
                parameter_form=String(
                    title=Title("Api-Version"),
                    help_text=Help(
                        "API schema version sent to the Avi Controller in the "
                        "X-Avi-Version HTTP header, for example '30.2.7'. "
                        "This version does not need to match the installed "
                        "Controller version. Keep the version against which "
                        "the special agent was tested unless you intentionally "
                        "want to use a newer API schema."
                    ),
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
                        "Select the Avi object types that the special agent "
                        "should retrieve and monitor. "
                        "Alerts are available in the Avi web interface under "
                        "Operations > Alerts > All Alerts. "
                        "Certificates are available under "
                        "Templates > Security > SSL/TLS Certificates. "
                        "Clouds are available under Infrastructure > Clouds. "
                        "Controller clusters and nodes are available under "
                        "Infrastructure > Controller > Nodes. "
                        "Pools are available under Applications > Pools. "
                        "Service Engines are available under "
                        "Infrastructure > Dashboard. "
                        "Virtual Services are available under "
                        "Applications > Virtual Services."
                    ),
                    elements=[
                        MultipleChoiceElement(
                            name="alert", title=Title("Alerts (This feature will be deprecated in a future version)"),
                        ),
                        MultipleChoiceElement(
                            name="certificate", title=Title("Certificates"),
                        ),
                        MultipleChoiceElement(
                            name="cloud", title=Title("Clouds"),
                        ),
                        MultipleChoiceElement(
                            name="cluster", title=Title("Controller cluster and nodes"),
                        ),
                        MultipleChoiceElement(
                            name="pool", title=Title("Pools"),
                        ),
                        MultipleChoiceElement(
                            name="service_engine", title=Title("Service Engines (provide piggyback monitoring data)"),
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
                            "pool",
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
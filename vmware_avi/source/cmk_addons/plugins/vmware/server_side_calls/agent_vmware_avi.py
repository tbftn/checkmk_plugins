#!/usr/bin/env python3
#-*- encoding: utf-8
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Side Server Call: VMware Avi Load Balancer


from cmk.server_side_calls.v1 import HostConfig, Secret, SpecialAgentConfig, SpecialAgentCommand
from pydantic import BaseModel


class AgentVMwareAviLoadBalancer(BaseModel):
    username: str
    password: Secret
    tenant: str
    #verify_ssl: bool
    sections: list = None


def _agent_arguments(params: AgentVMwareAviLoadBalancer, host_config: HostConfig):
    
    args = [
        "--server", host_config.primary_ip_config.address, 
        "--username", params.username, 
        "--password", params.password.unsafe(),
        "--tenant", params.tenant,
        #"--verify_ssl", params.verify_ssl,
    ]

    if params.sections is not None:
        args += ["--sections", ",".join(params.sections)]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_vmware_avi = SpecialAgentConfig(
    name="vmware_avi",
    parameter_parser=AgentVMwareAviLoadBalancer.model_validate,
    commands_function=_agent_arguments,
)
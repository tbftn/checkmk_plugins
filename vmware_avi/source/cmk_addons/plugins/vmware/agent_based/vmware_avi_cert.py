#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-04-24
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Certificates

# sample output:
# <<<vmware_avi_cert:sep(0)>>>
# {
#     'name': 'System-Default-Cert', 
#     'status': 'SSL_CERTIFICATE_FINISHED', 
#     'ocsp_error_status': 'OCSP_ERR_CERTSTATUS_DISABLED', 
#     'expire_status': 'SSL_CERTIFICATE_GOOD', 
#     'not_before': '2025-08-01 07:36:19',
#     'not_after': '2035-07-30 07:36:19',
#     'diff_not_after': 292698023.755681,
#     'self_signed': True
# },
# {...}


import ast
import itertools


from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def parse_vmware_avi_cert(string_table):

    parsed = []
    flatlist = list(itertools.chain.from_iterable(string_table))
    
    for f in flatlist:
        i = ast.literal_eval(f)
        parsed.append(i)

    return parsed


def discover_vmware_avi_cert(section):
    for cert in section:
        yield Service(item = f"{cert['name']}")


def check_vmware_avi_cert(item, params, section):

    for cert in section:

        if f"{cert['name']}" != item:
            continue
        
        # Status
        if cert['status'] == "SSL_CERTIFICATE_FINISHED":
            yield Result(state=State.OK, summary=f"Status: {cert['status']}")
        else:
            yield Result(state=State.CRIT, summary=f"Status: {cert['status']}")

        # Valid until
        yield Result(state=State.OK, summary=f"Valid until: {cert['not_after']}")
        
        # Days expire
        yield from check_levels(
            cert['diff_not_after'],
            label="Time until expire",
            levels_lower=params['days_until_expire'],
            render_func=lambda v: f'{render.time_offset(v)}',
            metric_name="vmware_avi_cert_time",
        )

        # self-signed
        yield Result(state=State.OK, summary=f"Self signed: {"Yes" if cert['self_signed'] else "No"}")

    return None


agent_section_vmware_avi_cert = AgentSection(
    name = "vmware_avi_cert",
    parse_function = parse_vmware_avi_cert,
)


check_plugin_vmware_avi_cert = CheckPlugin(
    name = "vmware_avi_cert",
    service_name = "Avi Cert %s",
    discovery_function = discover_vmware_avi_cert,
    check_function = check_vmware_avi_cert,
    check_default_parameters = {
        "days_until_expire": ("fixed", (7776000, 2592000)), # 90 days, 30 days
    },
    check_ruleset_name = "vmware_avi_cert",
)

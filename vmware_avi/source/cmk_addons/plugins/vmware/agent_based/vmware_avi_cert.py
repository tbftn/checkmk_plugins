#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-23
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Certificates

# sample output:
# <<<vmware_avi_cert:sep(0)>>>
# {
#     'name': 'System-Default-Cert', 
#     'ocsp_error_status': 'OCSP_ERR_CERTSTATUS_DISABLED', 
#     'expire_status': 'SSL_CERTIFICATE_GOOD', 
#     'not_before': '2025-08-01 07:36:19',
#     'not_after': '2035-07-30 07:36:19',
#     'diff_not_after': 292698023.755681,
#     'self_signed': True
# },
# {...}


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal_list, yield_mapped_result
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, State, render, Result


def discover_vmware_avi_cert(section):
    for cert in section:
        yield Service(item = f"{cert['name']}")


def check_vmware_avi_cert(item, params, section):

    map_expire_state = {
        "SSL_CERTIFICATE_GOOD": {"cmk": 0, "str": "Good"},
        "SSL_CERTIFICATE_EXPIRY_WARNING": {"cmk": params['state_expire_warning'], "str": "Warning"},
        "SSL_CERTIFICATE_EXPIRED": {"cmk": params['state_expired'], "str": "Expired"},
    }

    for cert in section:

        if f"{cert['name']}" != item:
            continue
        
        # expire state
        yield from yield_mapped_result(cert['expire_status'], map_expire_state, "Expire state")

        # valid until
        yield Result(state=State.OK, summary=f"Valid until: {cert['not_after']}")
        
        # days expire
        yield from check_levels(
            cert['diff_not_after'],
            label="Time until expire",
            levels_lower=params['days_until_expire'],
            render_func=lambda v: f'{render.time_offset(v)}',
            metric_name="vmware_avi_cert_time",
        )

        # self-signed
        if cert['self_signed']:
            yield Result(state=State(params['state_self_signed']), summary=f"Self-signed: Yes")
        else:
            yield Result(state=State.OK, summary="Self-signed: No")

    return None


agent_section_vmware_avi_cert = AgentSection(
    name = "vmware_avi_cert",
    parse_function = parse_python_literal_list,
)


check_plugin_vmware_avi_cert = CheckPlugin(
    name = "vmware_avi_cert",
    service_name = "Avi Cert %s",
    discovery_function = discover_vmware_avi_cert,
    check_function = check_vmware_avi_cert,
    check_default_parameters = {
        "days_until_expire": ("fixed", (2592000, 604800)), # 30 days, 7 days
        "state_self_signed": 1,
        "state_expire_warning": 1,
        "state_expired": 2,
    },
    check_ruleset_name = "vmware_avi_cert",
)

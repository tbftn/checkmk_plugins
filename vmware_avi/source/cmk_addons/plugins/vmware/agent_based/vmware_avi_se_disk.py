#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
# License: GNU General Public License v2
#
# Check: VMware Avi Load Balancer - Site Engines Filesystem

# sample output:
# <<<vmware_avi_se_disk:sep(0)>>>
# {
#     'disk_usage': 60.0
# }


from cmk_addons.plugins.vmware.lib.vmware_avi import parse_python_literal
from cmk.agent_based.v2 import AgentSection, check_levels, CheckPlugin, Service, render


def discover_vmware_avi_se_disk(section):
    yield Service()


def check_vmware_avi_se_disk(params, section):
    
    yield from check_levels(
        section['disk_usage'],
        label="Usage",
        levels_upper=params["usage"],
        render_func=lambda v: f'{render.percent(v)}',
        metric_name="fs_used_percent", # build checkmk metric
        boundaries=(0, 100)
    )


agent_section_vmware_avi_se_disk = AgentSection(
    name = "vmware_avi_se_disk",
    parse_function = parse_python_literal,
)


check_plugin_vmware_avi_se_disk = CheckPlugin(
    name = "vmware_avi_se_disk",
    service_name = "Avi Disk",
    discovery_function = discover_vmware_avi_se_disk,
    check_function = check_vmware_avi_se_disk,
    check_default_parameters={
        "usage": ("fixed", (80.0, 90.0)),
    },
    check_ruleset_name = "vmware_avi_se_disk",
)

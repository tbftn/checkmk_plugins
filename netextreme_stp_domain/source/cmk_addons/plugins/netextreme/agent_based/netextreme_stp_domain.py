#!/usr/bin/env python3
# 
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-19
# License: GNU General Public License v2
#
# Check: Extreme Networks STP Domain

# SNMP walk:
# .1.3.6.1.4.1.1916.1.17.1.1.2.1 s0 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainStpdName.1
# .1.3.6.1.4.1.1916.1.17.1.1.3.1 1 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainStpEnabled.1
# .1.3.6.1.4.1.1916.1.17.1.1.4.1 1 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainRstpEnabled.1
# .1.3.6.1.4.1.1916.1.17.1.1.5.1 0 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainStpdTag.1
# .1.3.6.1.4.1.1916.1.17.1.1.6.1 50 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainNumPorts.1
# .1.3.6.1.4.1.1916.1.17.1.1.7.1 "1A 2B 3C 4D 5E 6F 7A 8B " --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainBridgeId.1
# .1.3.6.1.4.1.1916.1.17.1.1.8.1 8192 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainBridgePriority.1
# .1.3.6.1.4.1.1916.1.17.1.1.9.1 "1A 2B 3C 4D 5E 6F 7A 8B " --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainDesignatedRoot.1
# .1.3.6.1.4.1.1916.1.17.1.1.10.1 0 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainRootPortIfIndex.1
# .1.3.6.1.4.1.1916.1.17.1.1.11.1 0 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainRootCost.1
# .1.3.6.1.4.1.1916.1.17.1.1.12.1 2 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainRRFailoverEnabled.1
# .1.3.6.1.4.1.1916.1.17.1.1.13.1 2000 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainMaxAge.1
# .1.3.6.1.4.1.1916.1.17.1.1.14.1 200 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainHelloTime.1
# .1.3.6.1.4.1.1916.1.17.1.1.15.1 1500 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainForwardDelay.1
# .1.3.6.1.4.1.1916.1.17.1.1.16.1 2000 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainBridgeMaxAge.1
# .1.3.6.1.4.1.1916.1.17.1.1.17.1 200 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainBridgeHelloTime.1
# .1.3.6.1.4.1.1916.1.17.1.1.18.1 1500 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainBridgeForwardDelay.1
# .1.3.6.1.4.1.1916.1.17.1.1.19.1 100 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainHoldTime.1
# .1.3.6.1.4.1.1916.1.17.1.1.20.1 1476 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainTopChanges.1
# .1.3.6.1.4.1.1916.1.17.1.1.21.1 8331200 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainTimeSinceTopologyChange.1
# .1.3.6.1.4.1.1916.1.17.1.1.22.1 1 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainRowStatus.1
# .1.3.6.1.4.1.1916.1.17.1.1.23.1 0 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainPortInstance.1
# .1.3.6.1.4.1.1916.1.17.1.1.24.1 --> EXTREME-STP-EXTENSIONS-MIB::extremeStpDomainStpdDescription.1


import time

from cmk.agent_based.v2 import (
    check_levels, 
    CheckPlugin, 
    get_rate, 
    get_value_store, 
    render, 
    Result, 
    Service, 
    SimpleSNMPSection, 
    SNMPTree, 
    startswith, 
    State
)


def parse_netextreme_stp_domain(string_table):
    parsed = []

    for name, stp_enabled, rstp_enabled, bridge_id, des_root, rr_failover_enabled, top_changes, time_since_top_change in string_table:
        
        stp_domain = {
            "name": name,
            "stp_enabled": stp_enabled == "1",
            "rstp_enabled": rstp_enabled == "1",
            "is_root": bridge_id == des_root,
            "rr_failover_enabled": rr_failover_enabled == "1",
            "top_changes": int(top_changes),
            "top_last_change": int(int(time_since_top_change) / 100),
        }

        parsed.append(stp_domain)

    return parsed


def discover_netextreme_stp_domain(section):
    for stp_domain in section:
        if stp_domain['stp_enabled']:
            yield Service(item=stp_domain["name"])


def check_netextreme_stp_domain(item, params, section):

    for stp_domain in section:

        if f"{stp_domain['name']}" != item:
            continue

        if stp_domain["is_root"]:
            yield Result(state=State.OK, summary="Bridge is root")
        else:
            yield Result(state=State(params["state_bridge_not_root"]), summary='Bridge is not root')

        # Topology change - count
        yield from check_levels(
            stp_domain["top_changes"],
            label="Topology changes",
            render_func=lambda v: f"{v}",
            metric_name="netextreme_stp_domain_top_changes",
            boundaries=(0, None)
        )

        # topology changes - rate: topology changes/min
        try:
            rate = get_rate(
                value_store=get_value_store(),
                key=f"top_changes.{item}",
                time=time.time(),
                value=stp_domain["top_changes"],
                raise_overflow=True,
            )

            if rate is not None:
                yield from check_levels(
                    rate * 60, # /s --> /min
                    label="Topology changes rate",
                    levels_upper=params["top_changes_rate"],
                    render_func=lambda v: f"{v:.2f}/min",
                    metric_name="netextreme_stp_domain_top_changes_rate",
                    boundaries=(0, None),
                    notice_only=True # only show, if warn or crit
                )
        except Exception:
            yield Result(state=State.OK, summary="Topology changes rate: Result available on second check execution")

        # since last topology change
        if stp_domain['top_last_change'] == 0 and stp_domain["top_changes"] == 0: # The switch hasn't had a single topology change since the reboot
            yield Result(state=State.OK, summary="Last topology change: Never since reboot")
        else:
            yield from check_levels(
                stp_domain['top_last_change'],
                label="Last topology change",
                levels_lower=params["last_top_change"],
                render_func=lambda v: f'{render.timespan(v)}',
                metric_name="netextreme_stp_domain_top_last_change",
                boundaries=(0, None),
            )

        # rstp enabled
        if not stp_domain['rstp_enabled']:
            yield Result(state=State(params["state_rstp_not_enabled"]), notice='RSTP not enabled')

        # rrfailover enabled
        if not stp_domain['rr_failover_enabled']:
            yield Result(state=State(params["state_rrfailover_not_enabled"]), notice='Rapid Root Failover not enabled')

        return


snmp_section_netextreme_stp_domain = SimpleSNMPSection(
    name = "netextreme_stp_domain",
    parse_function = parse_netextreme_stp_domain,
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Extreme"),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.1916.1.17.1.1',
        oids=[
            "2",    # extremeStpDomainStpdName
            "3",    # extremeStpDomainStpEnabled
            "4",    # extremeStpDomainRstpEnabled
            #"5",    # extremeStpDomainStpdTag
            #"6",    # extremeStpDomainNumPorts
            "7",    # extremeStpDomainBridgeId
            #"8",    # extremeStpDomainBridgePriority
            "9",    # extremeStpDomainDesignatedRoot
            #"10",   # extremeStpDomainRootPortIfIndex
            #"11",   # extremeStpDomainRootCost
            "12",   # extremeStpDomainRRFailoverEnabled
            #"13",   # extremeStpDomainMaxAge
            #"14",   # extremeStpDomainHelloTime
            #"15",   # extremeStpDomainForwardDelay
            #"16",   # extremeStpDomainBridgeMaxAge
            #"17",   # extremeStpDomainBridgeHelloTime
            #"18",   # extremeStpDomainBridgeForwardDelay
            #"19",   # extremeStpDomainHoldTime
            "20",   # extremeStpDomainTopChanges
            "21",   # extremeStpDomainTimeSinceTopologyChange
            #"22",   # extremeStpDomainRowStatus
            #"23",   # extremeStpDomainPortInstance
            #"24",   # extremeStpDomainStpdDescription
        ]
    )
)


check_plugin_netextreme_stp_domain = CheckPlugin(
    name = "netextreme_stp_domain",
    service_name = "STP Domain %s",
    discovery_function = discover_netextreme_stp_domain,
    check_function = check_netextreme_stp_domain,
    check_default_parameters = {
        "top_changes_rate": ("fixed", (1.0, 2.0)),
        "last_top_change": ('no_levels', None),
        "state_bridge_not_root": 0,
        "state_rstp_not_enabled": 1,
        "state_rrfailover_not_enabled": 1,
    },
    check_ruleset_name = "netextreme_stp_domain",
)

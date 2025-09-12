#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-12
# License: GNU General Public License v2
#
# Check: Checkpoint Power Supply

# SNMP walk
# .1.3.6.1.4.1.2620.1.6.7.9.1.1.1.1.0 1 --> CHECKPOINT-MIB::powerSupplyIndex.1.0
# .1.3.6.1.4.1.2620.1.6.7.9.1.1.1.2.0 2 --> CHECKPOINT-MIB::powerSupplyIndex.2.0
# .1.3.6.1.4.1.2620.1.6.7.9.1.1.2.1.0 Up --> CHECKPOINT-MIB::powerSupplyStatus.1.0
# .1.3.6.1.4.1.2620.1.6.7.9.1.1.2.2.0 Up --> CHECKPOINT-MIB::powerSupplyStatus.2.0


from cmk.agent_based.v2 import all_of, any_of, CheckPlugin, equals, startswith, Result, Service, SimpleSNMPSection, SNMPTree, State


def parse_checkpoint_powersupply(string_table):
    
    parsed = []
    
    for index, status in string_table:
        
        parsed.append({
            'index': index,
            'status': status,
        })

    return parsed


def discover_checkpoint_powersupply(section):
    for psu in section:
        yield Service(item = f"{psu['index']}")


def check_checkpoint_powersupply(item, params, section):

    for psu in section:

        if f"{psu['index']}" != item:
            continue

        if psu['status'] in ['OK', 'Present', 'Up']:
            yield Result(state=State.OK, summary=f"Status: {psu['status']}")
        else:
            yield Result(state=params['psu_not_up'], summary=f"Status: {psu['status']}")

        return


snmp_section_checkpoint_powersupply = SimpleSNMPSection(
    name = "checkpoint_powersupply",
    parse_function = parse_checkpoint_powersupply,
    detect=any_of(
        startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.2620'),
        all_of(
            equals('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.8072.3.2.10'),
            equals('.1.3.6.1.4.1.2620.1.6.1.0', 'SVN Foundation'),
        )
    ),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.2620.1.6.7.9.1.1',
        oids=[
            "1",    # powerSupplyIndex
            "2",    # powerSupplyStatus
        ]
    )
)


check_plugin_checkpoint_powersupply = CheckPlugin(
    name = "checkpoint_powersupply",
    service_name = "Power Supply %s",
    discovery_function = discover_checkpoint_powersupply,
    check_function = check_checkpoint_powersupply,
    check_default_parameters = {
        "psu_not_up": 2,
    },
    check_ruleset_name = "checkpoint_powersupply",
)

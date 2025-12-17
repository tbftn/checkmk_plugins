#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-12-15
# License: GNU General Public License v2
#
# Check: VMware AVI Load Balancer - Service Engine

# SNMP walk
# .1.3.6.1.4.1.45468.2.2.1.2.2 se-01
# .1.3.6.1.4.1.45468.2.2.1.2.3 se-02
# .1.3.6.1.4.1.45468.2.2.1.2.4 se-03
# .1.3.6.1.4.1.45468.2.2.1.2.5 se-04
# .1.3.6.1.4.1.45468.2.2.1.2.6 se-05
# .1.3.6.1.4.1.45468.2.2.1.2.7 se-06
# .1.3.6.1.4.1.45468.2.2.1.2.8 se-07
# .1.3.6.1.4.1.45468.2.2.1.2.9 se-08
# .1.3.6.1.4.1.45468.2.2.1.2.10 se-09
# .1.3.6.1.4.1.45468.2.2.1.2.11 se-0a
# .1.3.6.1.4.1.45468.2.2.1.3.2 name-01
# .1.3.6.1.4.1.45468.2.2.1.3.3 name-02
# .1.3.6.1.4.1.45468.2.2.1.3.4 name-03
# .1.3.6.1.4.1.45468.2.2.1.3.5 name-04
# .1.3.6.1.4.1.45468.2.2.1.3.6 name-05
# .1.3.6.1.4.1.45468.2.2.1.3.7 name-08
# .1.3.6.1.4.1.45468.2.2.1.3.8 name-09
# .1.3.6.1.4.1.45468.2.2.1.3.9 name-08
# .1.3.6.1.4.1.45468.2.2.1.3.10 name-09
# .1.3.6.1.4.1.45468.2.2.1.3.11 name-0a
# .1.3.6.1.4.1.45468.2.2.1.4.2 1
# .1.3.6.1.4.1.45468.2.2.1.4.3 1
# .1.3.6.1.4.1.45468.2.2.1.4.4 1
# .1.3.6.1.4.1.45468.2.2.1.4.5 1
# .1.3.6.1.4.1.45468.2.2.1.4.6 1
# .1.3.6.1.4.1.45468.2.2.1.4.7 1
# .1.3.6.1.4.1.45468.2.2.1.4.8 1
# .1.3.6.1.4.1.45468.2.2.1.4.9 1
# .1.3.6.1.4.1.45468.2.2.1.4.10 1
# .1.3.6.1.4.1.45468.2.2.1.4.11 1
# .1.3.6.1.4.1.45468.2.2.1.5.2 192.168.2.1
# .1.3.6.1.4.1.45468.2.2.1.5.3 192.168.2.2
# .1.3.6.1.4.1.45468.2.2.1.5.4 192.168.2.3
# .1.3.6.1.4.1.45468.2.2.1.5.5 192.168.2.4
# .1.3.6.1.4.1.45468.2.2.1.5.6 192.168.2.5
# .1.3.6.1.4.1.45468.2.2.1.5.7 192.168.2.6
# .1.3.6.1.4.1.45468.2.2.1.5.8 192.168.2.7
# .1.3.6.1.4.1.45468.2.2.1.5.9 192.168.2.8
# .1.3.6.1.4.1.45468.2.2.1.5.10 192.168.2.9
# .1.3.6.1.4.1.45468.2.2.1.5.11 192.168.2.10
# .1.3.6.1.4.1.45468.2.2.1.6.2 1
# .1.3.6.1.4.1.45468.2.2.1.6.3 1
# .1.3.6.1.4.1.45468.2.2.1.6.4 1
# .1.3.6.1.4.1.45468.2.2.1.6.5 1
# .1.3.6.1.4.1.45468.2.2.1.6.6 1
# .1.3.6.1.4.1.45468.2.2.1.6.7 1
# .1.3.6.1.4.1.45468.2.2.1.6.8 1
# .1.3.6.1.4.1.45468.2.2.1.6.9 1
# .1.3.6.1.4.1.45468.2.2.1.6.10 1
# .1.3.6.1.4.1.45468.2.2.1.6.11 1


from cmk.agent_based.v2 import any_of, CheckPlugin, OIDEnd, startswith, Result, Service, SimpleSNMPSection, SNMPTree, State


def parse_vmware_alb_service_engine(string_table):
    
    parsed = []
    
    for index, uuid, name, addr, status in string_table:
        
        parsed.append({
            'index': index,
            'uuid': uuid,
            'name': name,
            'addr': addr,
            'status': int(status),
        })

    return parsed


def discover_vmware_alb_service_engine(section):
    for service_engine in section:
        yield Service(item = f"{service_engine['name']}")


def check_vmware_alb_service_engine(item, section):

    map_status = {
        1: "Ok",
        2: "Down",
    }

    for service_engine in section:

        if f"{service_engine['name']}" != item:
            continue
        
        # status
        if service_engine['status'] == 1:
            yield Result(state=State.OK, summary=f"Status: {map_status.get(service_engine['status'])}")
        elif service_engine['status'] == 2:
            yield Result(state=State.CRIT, summary=f"Status: {map_status.get(service_engine['status'])}")
        else:
            yield Result(state=State.UNKNOWN, summary=f"Status: Unknown ({service_engine['status']})")

        # ip
        yield Result(state=State.OK, summary=f"IP: {service_engine['addr']}")
        
        # uuid
        yield Result(state=State.OK, summary=f"UUID: {service_engine['uuid']}")

        return


snmp_section_vmware_alb_service_engine = SimpleSNMPSection(
    name = "vmware_alb_service_engine",
    parse_function = parse_vmware_alb_service_engine,
    detect=any_of(
        startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.45468')
    ),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.45468.2.2.1',
        oids=[
            OIDEnd(),   # Service Engine Index
            "2",        # aviServiceEngineUUID
            "3",        # aviServiceEngineName
            #"4",       # aviServiceEngineAddrType
            "5",        # aviServiceEngineAddr
            "6",        # aviServiceEngineStatus
        ]
    )
)


check_plugin_vmware_alb_service_engine = CheckPlugin(
    name = "vmware_alb_service_engine",
    service_name = "Service Engine %s",
    discovery_function = discover_vmware_alb_service_engine,
    check_function = check_vmware_alb_service_engine,
)

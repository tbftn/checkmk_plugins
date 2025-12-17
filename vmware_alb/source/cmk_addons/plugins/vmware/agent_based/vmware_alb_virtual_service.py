#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-12-15
# License: GNU General Public License v2
#
# Check: VMware AVI Load Balancer - Virtual Service

# SNMP walk
# .1.3.6.1.4.1.45468.2.3.1.2.2 virtualservice-1
# .1.3.6.1.4.1.45468.2.3.1.2.4 virtualservice-2
# .1.3.6.1.4.1.45468.2.3.1.2.6 virtualservice-3
# .1.3.6.1.4.1.45468.2.3.1.2.8 virtualservice-4
# .1.3.6.1.4.1.45468.2.3.1.2.12 virtualservice-5
# .1.3.6.1.4.1.45468.2.3.1.2.14 virtualservice-6
# .1.3.6.1.4.1.45468.2.3.1.2.28 virtualservice-7
# .1.3.6.1.4.1.45468.2.3.1.2.30 virtualservice-8
# .1.3.6.1.4.1.45468.2.3.1.3.2 domain-c8--name-1
# .1.3.6.1.4.1.45468.2.3.1.3.4 domain-c8--name-2
# .1.3.6.1.4.1.45468.2.3.1.3.6 domain-c8--name-3
# .1.3.6.1.4.1.45468.2.3.1.3.8 domain-c8--name-4
# .1.3.6.1.4.1.45468.2.3.1.3.12 domain-c8--name-5
# .1.3.6.1.4.1.45468.2.3.1.3.14 domain-c8--name-6
# .1.3.6.1.4.1.45468.2.3.1.3.28 domain-c8--name-7
# .1.3.6.1.4.1.45468.2.3.1.3.30 domain-c8--name-8
# .1.3.6.1.4.1.45468.2.3.1.4.2 1
# .1.3.6.1.4.1.45468.2.3.1.4.4 1
# .1.3.6.1.4.1.45468.2.3.1.4.6 1
# .1.3.6.1.4.1.45468.2.3.1.4.8 1
# .1.3.6.1.4.1.45468.2.3.1.4.12 1
# .1.3.6.1.4.1.45468.2.3.1.4.14 1
# .1.3.6.1.4.1.45468.2.3.1.4.28 1
# .1.3.6.1.4.1.45468.2.3.1.4.30 1
# .1.3.6.1.4.1.45468.2.3.1.5.2 192.168.1.1
# .1.3.6.1.4.1.45468.2.3.1.5.4 192.168.1.2
# .1.3.6.1.4.1.45468.2.3.1.5.6 192.168.1.3
# .1.3.6.1.4.1.45468.2.3.1.5.8 192.168.1.4
# .1.3.6.1.4.1.45468.2.3.1.5.12 192.168.1.5
# .1.3.6.1.4.1.45468.2.3.1.5.14 192.168.1.6
# .1.3.6.1.4.1.45468.2.3.1.5.28 192.168.1.7
# .1.3.6.1.4.1.45468.2.3.1.5.30 192.168.1.8
# .1.3.6.1.4.1.45468.2.3.1.6.2 1
# .1.3.6.1.4.1.45468.2.3.1.6.4 1
# .1.3.6.1.4.1.45468.2.3.1.6.6 1
# .1.3.6.1.4.1.45468.2.3.1.6.8 1
# .1.3.6.1.4.1.45468.2.3.1.6.12 1
# .1.3.6.1.4.1.45468.2.3.1.6.14 1
# .1.3.6.1.4.1.45468.2.3.1.6.28 1
# .1.3.6.1.4.1.45468.2.3.1.6.30 2


from cmk.agent_based.v2 import any_of, CheckPlugin, OIDEnd, startswith, Result, Service, SimpleSNMPSection, SNMPTree, State


def parse_vmware_alb_virtual_service(string_table):
    
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


def discover_vmware_alb_virtual_service(section):
    for virtual_service in section:
        yield Service(item = f"{virtual_service['name']}")


def check_vmware_alb_virtual_service(item, section):

    map_status = {
        1: "Ok",
        2: "Down",
    }

    for virtual_service in section:

        if f"{virtual_service['name']}" != item:
            continue
        
        # status
        if virtual_service['status'] == 1:
            yield Result(state=State.OK, summary=f"Status: {map_status.get(virtual_service['status'])}")
        elif virtual_service['status'] == 2:
            yield Result(state=State.CRIT, summary=f"Status: {map_status.get(virtual_service['status'])}")
        else:
            yield Result(state=State.UNKNOWN, summary=f"Status: Unknown ({virtual_service['status']})")

        # ip
        yield Result(state=State.OK, summary=f"IP: {virtual_service['addr']}")
        
        # uuid
        yield Result(state=State.OK, summary=f"UUID: {virtual_service['uuid']}")

        return


snmp_section_vmware_alb_virtual_service = SimpleSNMPSection(
    name = "vmware_alb_virtual_service",
    parse_function = parse_vmware_alb_virtual_service,
    detect=any_of(
        startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.45468')
    ),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.45468.2.3.1',
        oids=[
            OIDEnd(),   # Controller Index
            "2",        # aviVirtualServiceUUID
            "3",        # aviVirtualServiceName
            #"4",       # aviVirtualServiceAddrType
            "5",        # aviVirtualServiceAddr
            "6",        # aviVirtualServiceStatus
        ]
    )
)


check_plugin_vmware_alb_virtual_service = CheckPlugin(
    name = "vmware_alb_virtual_service",
    service_name = "Virtual Service %s",
    discovery_function = discover_vmware_alb_virtual_service,
    check_function = check_vmware_alb_virtual_service,
)

#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-12-15
# License: GNU General Public License v2
#
# Check: VMware AVI Load Balancer - NSX Advanced Load Balancer Controller

# SNMP walk
# .1.3.6.1.4.1.45468.2.1.1.2.1 01
# .1.3.6.1.4.1.45468.2.1.1.2.2 02
# .1.3.6.1.4.1.45468.2.1.1.2.3 03
# .1.3.6.1.4.1.45468.2.1.1.3.1 192.168.3.1
# .1.3.6.1.4.1.45468.2.1.1.3.2 192.168.3.2
# .1.3.6.1.4.1.45468.2.1.1.3.3 192.168.3.3
# .1.3.6.1.4.1.45468.2.1.1.4.1 1
# .1.3.6.1.4.1.45468.2.1.1.4.2 1
# .1.3.6.1.4.1.45468.2.1.1.4.3 1
# .1.3.6.1.4.1.45468.2.1.1.5.1 192.168.3.1
# .1.3.6.1.4.1.45468.2.1.1.5.2 192.168.3.2
# .1.3.6.1.4.1.45468.2.1.1.5.3 192.168.3.3
# .1.3.6.1.4.1.45468.2.1.1.6.1 1
# .1.3.6.1.4.1.45468.2.1.1.6.2 1
# .1.3.6.1.4.1.45468.2.1.1.6.3 1


from cmk.agent_based.v2 import any_of, CheckPlugin, OIDEnd, startswith, Result, Service, SimpleSNMPSection, SNMPTree, State


def parse_vmware_alb_controller(string_table):
    
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


def discover_vmware_alb_controller(section):
    for controller in section:
        yield Service(item = f"{controller['name']}")


def check_vmware_alb_controller(item, section):

    map_status = {
        1: "Ok",
        2: "Down",
    }

    for controller in section:

        if f"{controller['name']}" != item:
            continue
        
        # status
        if controller['status'] == 1:
            yield Result(state=State.OK, summary=f"Status: {map_status.get(controller['status'])}")
        elif controller['status'] == 2:
            yield Result(state=State.CRIT, summary=f"Status: {map_status.get(controller['status'])}")
        else:
            yield Result(state=State.UNKNOWN, summary=f"Status: Unknown ({controller['status']})")

        # ip
        yield Result(state=State.OK, summary=f"IP: {controller['addr']}")
        
        # uuid
        yield Result(state=State.OK, summary=f"UUID: {controller['uuid']}")

    return


snmp_section_vmware_alb_controller = SimpleSNMPSection(
    name = "vmware_alb_controller",
    parse_function = parse_vmware_alb_controller,
    detect=any_of(
        startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.45468')
    ),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.45468.2.1.1',
        oids=[
            OIDEnd(),   # Controller Index
            "2",        # aviControllerUUID
            "3",        # aviControllerName
            #"4",       # aviControllerAddrType
            "5",        # aviControllerAddr
            "6",        # aviControllerStatus
        ]
    )
)


check_plugin_vmware_alb_controller = CheckPlugin(
    name = "vmware_alb_controller",
    service_name = "Controller %s",
    discovery_function = discover_vmware_alb_controller,
    check_function = check_vmware_alb_controller,
)

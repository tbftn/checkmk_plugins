#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2025-09-01
# License: GNU General Public License v2
#
# Check: Extreme Networks Optical Modules (SFP)


from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    CheckResult,
    startswith,
    DiscoveryResult,
    Metric,
    OIDEnd,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPSection,
    SNMPTree,
    State,
    StringTable
)

import math


def _convert_microwatt_to_decibel_milliwatt(microwatt):
    microwatt = int(microwatt)
    
    if microwatt <= 0:
        return -40
    else:
        dbm = 10 * math.log10(microwatt/1000)

    dbm = round(dbm, 2)
    return dbm


def parse_netextreme_dom(string_table):

    parsed = []

    # get data from all sensors
    if len(string_table[0]) <= 0:
        return []

    sensors = {}
    for s_id, s_type, scale, precision, value, operStatus in string_table[0]:
        
        s_id = int(s_id)
        s_type = int(s_type)
        operStatus = int(operStatus)
        
        # only sensors from type 6 (watt)
        if s_type == 6:
            
            parsed_value = int(value) * float("1e-%s" % precision)

            sensors[s_id] = {
                'value': parsed_value,
                'status': operStatus,
            }

    # get alarms and thresholds
    alarms = {}
    for a_id, state, highAlarm, highWarning, lowWarning, lowAlarm in string_table[2]:
        
        if highAlarm == '0' and highWarning == '0' and lowWarning == '0' and lowAlarm == '0':
            continue
    
        alarms[int(a_id)] = {
            'state': int(state),
            'highAlarm': int(highAlarm),
            'highWarning': int(highWarning),
            'lowWarning': int(lowWarning),
            'lowAlarm': int(lowAlarm)
        }
        
    # get interfaces (ports)
    interfaces = {}
    for if_id, adminStatus in string_table[3]:
        if int(if_id) < 2000: # only detect physical ports
            if_id = int(if_id) - 1000 # 1015 --> 15
            
            interfaces[int(if_id)] = {
                'adminStatus': int(adminStatus),
            }

    # parse 'physicals', merge all sensors to one physical port
    for s_id, descr, containedIn in string_table[1]:

        if int(containedIn) < 4 or int(containedIn) > 199:
            continue

        # detect name and channel from description
        # channel = 0, if there are no channels in this transceiver
        descr = descr.replace(' Sensor', '').replace('SFP ', '')
        
        if 'Channel' in descr:
            descr_split = descr
            channel = int(descr_split.split(' ')[-1])
            name = descr.replace(' Channel ', '').replace(str(channel), '')
        else:
            channel = 0
            name = descr
        
        s_id = int(s_id)
        found_dom = False
        
        # containedIn specifies the port ID on which a sensor is located
        # Strangely, this is always +3 too high, therefore -3
        containedIn = int(containedIn) - 3
        
        # a service for each port and each channel...

        # check whether the respective port has already been created by another sensor
        for dom in parsed:
            if dom['port'] == containedIn and dom['channel'] == channel: # found port in dict --> no add port, but append the current sensor to this port
                found_dom = True
                
                # add the current sensor and alarms for this sensor to the current dict...
                if s_id in sensors and s_id in alarms: # Wenn nicht, dann wurde der Sensor auch nicht erfasst --> Alles weitere verwerfen
                    dom['sensors'][name] = sensors.get(s_id)
                    dom['sensors'][name]['alarms'] = alarms.get(s_id)
                
                    # summary state of this port, is one sensor status == 1, then summary state = 1
                    if dom['sensors'][name]['status'] == 1:
                        dom['status'] = 1
                break
            
        if found_dom == False: # add a new dom and append the current sensor to this port
            
            dom = {
                'port': containedIn,
                'channel': channel,
                'ifAdminStatus': interfaces.get(containedIn)['adminStatus'],
                'status': 3, # it is assumed that all sensors are unavailable
                'sensors': {}
            }

            # add the current sensor and alarms for this sensor to the current dict...
            if s_id in sensors and s_id in alarms: # Wenn nicht, dann wurde der Sensor auch nicht erfasst --> Alles weitere verwerfen

                dom['sensors'][name] = sensors.get(s_id)
                dom['sensors'][name]['alarms'] = alarms.get(s_id)
            
                # summary state of this port, is one sensor status == 1, then summary state = 1
                if dom['sensors'][name]['status'] == 1:
                    dom['status'] = 1
        
                # port is new --> append port to parsed
                parsed.append(dom)
                
    return parsed


def discover_netextreme_dom(section):
    for dom in section:
        if dom['status'] == 1 and dom['ifAdminStatus'] != 2:
            if dom['channel'] == 0:
                yield Service(item=str(dom['port']))
            else:
                yield Service(item=str(dom['port']) + ' Channel ' + str(dom['channel']))


def check_netextreme_dom(item, params, section):

    for dom in section:
        if dom['channel'] == 0:
            if str(dom['port']) != item:
                continue
        else:
            if (str(dom['port']) + ' Channel ' + str(dom['channel'])) != item:
                continue

        # print all values from the dict
        for sensor in dom['sensors']:

            # create tmp variables
            value = dom['sensors'][sensor]['value']
            alarms = dom['sensors'][sensor]['alarms']
            
            # current state of the sensor
            cst_state = alarms['state']
            
            # 28-06-2024: Check thredsholds from the sensor, if are all four thredsholds 0,
            # then an error reading this sensor --> Discard this sensor...
            if 'lowAlarm' in alarms and 'lowWarning' in alarms and 'highWarning' in alarms and 'highAlarm' in alarms:
                if alarms['lowAlarm'] == 0 and alarms['lowWarning'] == 0 and alarms['highWarning'] == 0 and alarms['highAlarm'] == 0:
                    continue
            
            # convert values from rx and tx sensors from mW to dBm
            if 'RX Power' in sensor or 'TX Power' in sensor:
                value = _convert_microwatt_to_decibel_milliwatt(value)
                alarms['lowAlarm'] = _convert_microwatt_to_decibel_milliwatt(alarms['lowAlarm'])
                alarms['lowWarning'] = _convert_microwatt_to_decibel_milliwatt(alarms['lowWarning'])
                alarms['highWarning'] = _convert_microwatt_to_decibel_milliwatt(alarms['highWarning'])
                alarms['highAlarm'] = _convert_microwatt_to_decibel_milliwatt(alarms['highAlarm'])

            if 'RX Power' in sensor:
                metric_name="netextreme_input_signal_power"
                choice, payload = params["input_power"]
            else:
                metric_name="netextreme_output_signal_power"
                choice, payload = params["output_power"]

            # create output message for checkmk

            # Use levels from device
            # If the device's thresholds are used to determine the status, the check_levels
            # function is not used and is not compared with the device's values. Instead,
            # the device's status is evaluated (.1.3.6.1.4.1.5624.1.2.85.1.2.1.1.1).
            # This is also due to the fact that, for lower thresholds, check_levels only 
            # changes the state below the specified threshold. However, in this case, it is 
            # necessary that the status change occurs at, for example, -20, and not at -20.1.
            if choice == 'device':
            
                low_message = '%s: %s dBm (warn/crit below at %s/%s dBm)' %(sensor, value, alarms['lowWarning'], alarms['lowAlarm'])
                high_message = '%s: %s dBm (warn/crit at %s/%s dBm)' %(sensor, value, alarms['highWarning'], alarms['highAlarm'])
                
                if cst_state == 2: # lowAlarm
                    yield Result(state=State.CRIT, summary = low_message)
                elif cst_state == 3: # lowWarning
                    yield Result(state=State.WARN, summary = low_message)
                elif cst_state == 4: # normal
                    yield Result(state=State.OK, summary = '%s: %s dBm' %(sensor, value))
                elif cst_state == 5: # highWarning
                    yield Result(state=State.CRIT, summary = high_message)
                elif cst_state == 6: # highAlarm
                    yield Result(state=State.CRIT, summary = high_message)
                else: # unknown
                    yield Result(state=State.UNKNOWN, summary='%s: %s dBm (Unknown State %s)' %(sensor, value, cst_state))
                    
                yield Metric(value=value,name=metric_name)

            elif choice == 'custom':
                yield from check_levels(
                    value,
                    label=sensor,
                    levels_upper=payload.get('upper_levels', None),
                    levels_lower=payload.get('lower_levels', None),
                    render_func=lambda v: f'{v} dBm',
                    metric_name=metric_name
                )

    return None

snmp_section_netextreme_dom = SNMPSection(
    name = "netextreme_dom_base_config",
    parse_function = parse_netextreme_dom,
    detect = startswith(".1.3.6.1.2.1.1.1.0", "Extreme"),
    fetch = [
        SNMPTree(
            base = '.1.3.6.1.2.1.99.1.1.1',
            oids = [
                OIDEnd(), # Gives the last number from an oid; is the ID for the sensor
                '1',    # entPhySensorType {other(1), unknown(2), voltsAC(3), voltsDC(4), amperes(5), watts(6), hertz(7), celsius(8), percentRH(9), 1rpm(10), cmm(11), truthvalue(12)}
                '2',    # entPhySensorScale {yocto(1), zepto(2), atto(3), femto(4), pico(5), nano(6), micro(7), milli(8), units(9), kilo(10), mega(11), giga(12), tera(13), exa(14), peta(15), zetta(16), yotta(17)}
                '3',    # entPhySensorPrecision
                '4',    # entPhySensorValue
                '5',    # entPhySensorOperStatus {ok(1), unavailable(2), nonoperational(3)}
            ],
        ),
        SNMPTree(
            base = '.1.3.6.1.2.1.47.1.1.1.1',
            oids = [
                OIDEnd(), # Gives the last number from an oid; is the ID for the sensor
                '2',    # entPhysicalDescr
                '4',    # entPhysicalContainedIn
            ],
        ),
        SNMPTree(
            base = '.1.3.6.1.4.1.5624.1.2.85.1.2.1.1',
            oids = [
                OIDEnd(), # Gives the last number from an oid; is the ID for the sensor
                '1',    # etsysEntitySfpSensorState {unknown(1), lowAlarm(2), lowWarning(3), normal(4), highWarning(5), highAlarm(6)}
                '2',    # etsysEntitySfpSensorHighAlarm; Threshold for HighAlarm
                '3',    # etsysEntitySfpSensorHighWarning; Threshold for HighWarning
                '4',    # etsysEntitySfpSensorLowWarning; Threshold for LowWarning
                '5',    # etsysEntitySfpSensorLowAlarm; Threshold for LowAlarm
            ],
        ),
        SNMPTree(
            base = '.1.3.6.1.2.1.2.2.1',
            oids = [
                OIDEnd(), # Gives the last number from an oid; is the portID
                '7', # ifAdminStatus INTEGER {up(1), down(2), testing(3)}
            ],
        ),
    ]
)

check_plugin_netextreme_dom = CheckPlugin(
    name = "netextreme_dom",
    sections = ["netextreme_dom_base_config"],
    service_name = "DOM Port %s",
    discovery_function = discover_netextreme_dom,
    check_function = check_netextreme_dom,
    check_default_parameters= {
        'input_power': ('device', None),
        'output_power': ('device', None),
    },  
    check_ruleset_name = "netextreme_dom",
)

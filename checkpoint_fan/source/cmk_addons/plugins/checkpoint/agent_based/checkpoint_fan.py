#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-23
# License: GNU General Public License v2
#
# Check: Check Point Fan


from cmk.agent_based.v2 import (
    all_of,
    any_of,
    CheckPlugin,
    equals,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    State
)


# .1.3.6.1.4.1.2620.1.6.7.8.2.1.2.1.0 CPU FAN1 --> CHECKPOINT-MIB::fanSpeedSensorName.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.2.2.0 CPU FAN2 --> CHECKPOINT-MIB::fanSpeedSensorName.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.2.3.0 CPU FAN3 (unused) --> CHECKPOINT-MIB::fanSpeedSensorName.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.3.1.0 6279.0000 --> CHECKPOINT-MIB::fanSpeedSensorValue.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.3.2.0 5672.0000 --> CHECKPOINT-MIB::fanSpeedSensorValue.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.3.3.0 0.0000 --> CHECKPOINT-MIB::fanSpeedSensorValue.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.4.1.0 RPM --> CHECKPOINT-MIB::fanSpeedSensorUnit.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.4.2.0 RPM --> CHECKPOINT-MIB::fanSpeedSensorUnit.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.4.3.0 RPM --> CHECKPOINT-MIB::fanSpeedSensorUnit.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.5.1.0 fan --> CHECKPOINT-MIB::fanSpeedSensorType.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.5.2.0 fan --> CHECKPOINT-MIB::fanSpeedSensorType.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.5.3.0 fan --> CHECKPOINT-MIB::fanSpeedSensorType.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.6.1.0 0 --> CHECKPOINT-MIB::fanSpeedSensorStatus.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.6.2.0 0 --> CHECKPOINT-MIB::fanSpeedSensorStatus.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.2.1.6.3.0 0 --> CHECKPOINT-MIB::fanSpeedSensorStatus.3.0


def parse_checkpoint_fan(string_table):
    
    parsed = []
    
    for name, value, unit, status in string_table:

        # check if "unused" in name and rpm == 0 -> the remove this fan, because is unused
        if "(unused)" in name and float(value) == 0:
            continue

        # check if " Fan" in name -> then remove this
        # Remove not FAN or others...
        name = name.replace(" Fan", "").strip()

        fan = {
            "name": name,    
            "value": float(value),
            "unit": unit,
            "status": int(status),
        }
        
        parsed.append(fan)

    return parsed


def discover_checkpoint_fan(section):
    for fan in section:
        yield Service(item = fan['name'])


def check_checkpoint_fan(item, params, section):
    
    for fan in section:

        if fan['name'] != item:
            continue

        if fan['status'] in [0, 1]:
            
            # status
            if fan['status'] == 0: # sensor not out of range
                yield Result(state=State.OK, notice="Status: Sensor in range")

            else: # sensor is out of range
                yield Result(state=State(params['state_sensor_out_of_range']), summary="Status: Sensor is out of range")

            # value
            yield Result(state=State.OK, summary=f"Speed: {round(fan['value'], 2)} RPM")

            # metric (only if enabled in ruleset)
            if params["performance_data"]:
                yield Metric(name="fan", value=fan['value'], boundaries=(0, None))

        elif fan['status'] == 2:
            yield Result(state=State(params['state_reading_error']), summary="Status: Reading error")

        else:
             yield Result(state=State.UNKNOWN, summary="Status: Undefined state")

        return
  

snmp_section_checkpoint_fan = SimpleSNMPSection(
    name = "checkpoint_fan",
    parse_function = parse_checkpoint_fan,
    detect=any_of(
        startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.2620'),
        all_of(
            equals('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.8072.3.2.10'),
            equals('.1.3.6.1.4.1.2620.1.6.1.0', 'SVN Foundation'),
        )
    ),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.2620.1.6.7.8.2.1',
        oids=[
            "2",    # fanSpeedSensorName
            "3",    # fanSpeedSensorValue
            "4",    # fanSpeedSensorUnit
            #"5",    # fanSpeedSensorType
            "6",    # fanSpeedSensorStatus "Sensor is out of range TRUE(1), FALSE(0), READING ERROR(2)"
        ]
    )
)


check_plugin_checkpoint_fan = CheckPlugin(
    name = "checkpoint_fan",
    service_name = "Fan %s",
    discovery_function = discover_checkpoint_fan,
    check_function = check_checkpoint_fan,
    check_default_parameters = {
        "state_sensor_out_of_range": 2,
        "state_reading_error": 3,
        "performance_data": False,
    },
    check_ruleset_name = "checkpoint_fan",
)

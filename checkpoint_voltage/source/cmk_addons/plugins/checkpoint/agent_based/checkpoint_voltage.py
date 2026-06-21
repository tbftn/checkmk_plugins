#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-06-21
# License: GNU General Public License v2
#
# Check: Check Point Voltage


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


# .1.3.6.1.4.1.2620.1.6.7.8.3.1.1.1.0 1 --> CHECKPOINT-MIB::voltageSensorIndex.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.1.2.0 2 --> CHECKPOINT-MIB::voltageSensorIndex.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.1.3.0 3 --> CHECKPOINT-MIB::voltageSensorIndex.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.2.1.0 Voltage 3V3 --> CHECKPOINT-MIB::voltageSensorName.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.2.2.0 Voltage 1V8 --> CHECKPOINT-MIB::voltageSensorName.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.2.3.0 Voltage 0V99 --> CHECKPOINT-MIB::voltageSensorName.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.3.1.0 3.2956 --> CHECKPOINT-MIB::voltageSensorValue.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.3.2.0 1.8320 --> CHECKPOINT-MIB::voltageSensorValue.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.3.3.0 0.9900 --> CHECKPOINT-MIB::voltageSensorValue.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.4.1.0 Volt --> CHECKPOINT-MIB::voltageSensorUnit.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.4.2.0 Volt --> CHECKPOINT-MIB::voltageSensorUnit.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.4.3.0 Volt --> CHECKPOINT-MIB::voltageSensorUnit.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.5.1.0 voltage --> CHECKPOINT-MIB::voltageSensorType.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.5.2.0 voltage --> CHECKPOINT-MIB::voltageSensorType.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.5.3.0 voltage --> CHECKPOINT-MIB::voltageSensorType.3.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.6.1.0 0 --> CHECKPOINT-MIB::voltageSensorStatus.1.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.6.2.0 0 --> CHECKPOINT-MIB::voltageSensorStatus.2.0
# .1.3.6.1.4.1.2620.1.6.7.8.3.1.6.3.0 0 --> CHECKPOINT-MIB::voltageSensorStatus.3.0


def parse_checkpoint_voltage(string_table):
    
    parsed = []
    
    for name, value, unit, status in string_table:

        # check if "Voltage" in name -> then remove this
        if "voltage" in name.lower():
            name = name.replace("Voltage", "").replace("voltage", "").strip()

        voltage = {
            "name": name,    
            "value": float(value),
            "unit": unit,
            "status": int(status),
        }
        
        parsed.append(voltage)

    return parsed


def discover_checkpoint_voltage(section):
    for voltage in section:
        if voltage['status'] in [0, 1, 2]: # notPresent: no power supply inserted
            yield Service(item = voltage['name'])


def check_checkpoint_voltage(item, params, section):
    
    for voltage in section:

        if voltage['name'] != item:
            continue

        if voltage['status'] in [0, 1]:
            
            # status
            if voltage['status'] == 0: # sensor not out of range
                yield Result(state=State.OK, notice="Status: Sensor in range")

            else: # sensor is out of range
                yield Result(state=State(params['state_sensor_out_of_range']), summary="Status: Sensor is out of range")

            # value
            yield Result(state=State.OK, summary=f"Voltage: {round(voltage['value'], 2)} V")

            # metric (only if enabled in ruleset)
            if params["performance_data"]:
                yield Metric(name="voltage", value=voltage['value'], boundaries=(0, None))

            # Metric(name: str, value: float, *, levels: tuple[float | None, float | None] | None = None, boundaries: tuple[float | None, float | None] | None = None)

        elif voltage['status'] == 2:
            yield Result(state=State(params['state_reading_error']), summary="Status: Reading error")

        else:
             yield Result(state=State.UNKNOWN, summary="Status: Undefined state")

        return
  

snmp_section_checkpoint_voltage = SimpleSNMPSection(
    name = "checkpoint_voltage",
    parse_function = parse_checkpoint_voltage,
    detect=any_of(
        startswith('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.2620'),
        all_of(
            equals('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.4.1.8072.3.2.10'),
            equals('.1.3.6.1.4.1.2620.1.6.1.0', 'SVN Foundation'),
        )
    ),
    fetch = SNMPTree(
        base ='.1.3.6.1.4.1.2620.1.6.7.8.3.1',
        oids=[
            #"1",    # voltageSensorIndex
            "2",    # voltageSensorName
            "3",    # voltageSensorValue
            "4",    # voltageSensorUnit
            #"5",    # voltageSensorType
            "6",    # voltageSensorStatus "Sensor is out of range TRUE(1), FALSE(0), READING ERROR(2)"
        ]
    )
)


check_plugin_checkpoint_voltage = CheckPlugin(
    name = "checkpoint_voltage",
    service_name = "Voltage %s",
    discovery_function = discover_checkpoint_voltage,
    check_function = check_checkpoint_voltage,
    check_default_parameters = {
        "state_sensor_out_of_range": 2,
        "state_reading_error": 3,
        "performance_data": False,
    },
    check_ruleset_name = "checkpoint_voltage",
)

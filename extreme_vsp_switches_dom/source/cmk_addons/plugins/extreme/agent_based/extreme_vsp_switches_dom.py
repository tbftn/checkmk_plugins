#!/usr/bin/env python3
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-11-04
# License: GNU General Public License v2
#
# Check: Extreme VSP Optical Modules (SFP)

# Extreme Fabric Engine DOM monitoring (SFP and 4-channel QSFP)
# Fabric Engine reports DOM values in 1/10000 of the displayed unit,
# except bias current, which is converted to amperes for Checkmk.
# Optical power is already in dBm (contrary to the published MIB).

from cmk.agent_based.v2 import (
    CheckPlugin,
    OIDEnd,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    check_levels,
    contains,
)


def _check_dom_sensor(sensor, sensor_name, params, metric_name, label, render_func, boundaries=None):
    """Apply device or custom thresholds and export the metric."""

    choice, custom = params.get(sensor_name, ("device", None))

    if choice == "device":
        levels_upper = ("fixed", (sensor["high_warning"], sensor["high_alarm"]))
        levels_lower = ("fixed", (sensor["low_warning"], sensor["low_alarm"]))

    elif choice == "custom":
        custom = custom or {}

        levels_upper = custom.get("upper_levels", ("no_levels", None))
        levels_lower = custom.get("lower_levels", ("no_levels", None))

        if sensor_name == "bias":
            levels_upper = _convert_custom_bias_levels(levels_upper)
            levels_lower = _convert_custom_bias_levels(levels_lower)

    elif choice == "no_levels":
        levels_upper = ("no_levels", None)
        levels_lower = ("no_levels", None)

    else:
        yield Result(state=State.UNKNOWN, summary=f"{label}: invalid level configuration {choice!r}")
        return

    yield from check_levels(
        sensor["value"],
        levels_upper=levels_upper,
        levels_lower=levels_lower,
        metric_name=metric_name,
        label=label,
        render_func=render_func,
        boundaries=boundaries,
    )


def _convert_custom_bias_levels(levels):
    """Convert ruleset bias thresholds from mA to A."""

    if levels is None or levels[0] == "no_levels":
        return levels

    if levels[0] == "fixed":
        warn, crit = levels[1]
        return ("fixed", (warn / 1000, crit / 1000))

    return levels


def _decode_ddm_status(data):
    flags = {
        0: "DDM OK",
        1: "Checksum error",
        2: "I2C read error",
        3: "Threshold error",
        4: "Calibration error",
        5: "Avaya checksum error",
    }
    raw = data.encode("latin-1")
    return [
        description
        for bit, description in flags.items()
        if bit // 8 < len(raw) and raw[bit // 8] & (0x80 >> (bit % 8))
    ]


def _parse_dom_sensor(value, high_alarm, low_alarm, high_warning, low_warning, status, scale):
    """Convert raw SNMP values into a DOM sensor dictionary."""

    return {
        "value": int(value) / scale,
        "high_alarm": int(high_alarm) / scale,
        "low_alarm": int(low_alarm) / scale,
        "high_warning": int(high_warning) / scale,
        "low_warning": int(low_warning) / scale,
        "status": int(status),
    }


def parse_extreme_vsp_switches_dom(string_table):

    # Map interface indexes to their administrative status
    interfaces_admin = {}

    for if_index, admin_status in string_table[0]:
        interfaces_admin[if_index] = int(admin_status)

    # Map interface indexes to their names
    interfaces = {}

    for if_index, if_name in string_table[1]:
        interfaces[if_index] = if_name.strip()

    parsed = {}

    # Read optical module data
    for row in string_table[2]:
        (
            tra_id, ddm_status, supports_ddm, module_type,
            # Temperature: OIDs 17-21
            temp, temp_ha, temp_la, temp_hw, temp_lw,
            # Voltage: OIDs 22-26
            volt, volt_ha, volt_la, volt_hw, volt_lw,
            # Shared bias thresholds: OIDs 27-31
            bias, bias_ha, bias_la, bias_hw, bias_lw,
            # Shared TX thresholds: OIDs 32-36
            tx, tx_ha, tx_la, tx_hw, tx_lw,
            # Shared RX thresholds: OIDs 37-41
            rx, rx_ha, rx_la, rx_hw, rx_lw,
            # Module sensor status: OIDs 52-56
            temp_status, volt_status, bias_status, tx_status, rx_status,
            # QSFP bias readings: OIDs 59-62
            bias_1, bias_2, bias_3, bias_4,
            # QSFP TX readings: OIDs 63-66
            tx_1, tx_2, tx_3, tx_4,
            # QSFP RX readings: OIDs 67-70
            rx_1, rx_2, rx_3, rx_4,
            # QSFP bias status: OIDs 71-74
            bias_status_1, bias_status_2, bias_status_3, bias_status_4,
            # QSFP TX status: OIDs 75-78
            tx_status_1, tx_status_2, tx_status_3, tx_status_4,
            # QSFP RX status: OIDs 79-82
            rx_status_1, rx_status_2, rx_status_3, rx_status_4,
        ) = row

        # SNMP TruthValue: true(1), false(2).
        if supports_ddm != "1":
            continue

        if_name = interfaces.get(tra_id, tra_id)

        sensors = {
            "temp": _parse_dom_sensor(temp, temp_ha, temp_la, temp_hw, temp_lw, temp_status, scale=10000),
            "volt": _parse_dom_sensor(volt, volt_ha, volt_la, volt_hw, volt_lw, volt_status, scale=10000),
        }

        channels = {}
        channel_readings = [
            (bias_1, tx_1, rx_1, bias_status_1, tx_status_1, rx_status_1),
            (bias_2, tx_2, rx_2, bias_status_2, tx_status_2, rx_status_2),
            (bias_3, tx_3, rx_3, bias_status_3, tx_status_3, rx_status_3),
            (bias_4, tx_4, rx_4, bias_status_4, tx_status_4, rx_status_4),
        ]

        # The current firmware exposes these OIDs even for SFPs and DACs.
        # The tested QSFP28 identifies itself as 100GbLR4 and has active
        # channel bias/TX readings; the single-channel SFPs report zeros.
        # Do not use RX != 0: an unplugged fiber has a valid low RX value.
        is_multichannel = (
            "LR4" in module_type.upper()
            or "QSFP" in module_type.upper()
            or (
                all(int(reading[0]) > 0 for reading in channel_readings)
                and all(int(reading[1]) != 0 for reading in channel_readings)
            )
        )

        if is_multichannel:
            for channel_number, readings in enumerate(channel_readings, start=1):
                ch_bias, ch_tx, ch_rx, ch_bias_status, ch_tx_status, ch_rx_status = readings
                # A supported channel with a legitimate zero reading must not
                # be skipped. The QSFP type selects the four physical lanes.
                channels[str(channel_number)] = {
                    "bias": _parse_dom_sensor(ch_bias, bias_ha, bias_la, bias_hw, bias_lw, ch_bias_status, scale=10000000),
                    "tx": _parse_dom_sensor(ch_tx, tx_ha, tx_la, tx_hw, tx_lw, ch_tx_status, scale=10000),
                    "rx": _parse_dom_sensor(ch_rx, rx_ha, rx_la, rx_hw, rx_lw, ch_rx_status, scale=10000),
                }
        else:
            # Ordinary SFP: keep the existing five-metric DOM service.
            sensors["bias"] = _parse_dom_sensor(bias, bias_ha, bias_la, bias_hw, bias_lw, bias_status, scale=10000000)
            sensors["tx"] = _parse_dom_sensor(tx, tx_ha, tx_la, tx_hw, tx_lw, tx_status, scale=10000)
            sensors["rx"] = _parse_dom_sensor(rx, rx_ha, rx_la, rx_hw, rx_lw, rx_status, scale=10000)

        parsed[if_name] = {
            "index": tra_id,
            "admin_status": interfaces_admin.get(tra_id),
            "module_type": module_type,
            "states": _decode_ddm_status(ddm_status),
            "sensors": sensors,
            "channels": channels,
        }

    return parsed


def discover_extreme_vsp_switches_dom(section):
    
    for if_name, dom in section.items():
        
        # Only discover administratively enabled ports
        # IF-MIB::ifAdminStatus: up(1), down(2), testing(3)
        if dom["admin_status"] != 1:
            continue

        # Main transceiver service
        yield Service(item=if_name)

        # Additional services for optical channels
        for channel in dom["channels"]:
            yield Service(item=f"{if_name} Channel {channel}")


def check_extreme_vsp_switches_dom(item, params, section):
    
    # Match the full interface name first. " Channel " is only parsed when
    # there is no corresponding module item.
    dom = section.get(item)
    channel = None

    if dom is None and " Channel " in item:
        if_name, channel = item.rsplit(" Channel ", 1)
        dom = section.get(if_name)
        if dom is None or channel not in dom["channels"]:
            return
    elif dom is None:
        return

    if dom["admin_status"] != 1:
        return

    #if "DDM OK" not in dom["states"]:
    #    yield Result(state=State.CRIT, summary=f"DDM states: {dom['states']}")

    if channel is None:
        sensors = dom["sensors"]
        yield from _check_dom_sensor(sensors["temp"], "temp", params, "extreme_vsp_switches_dom_temperature", "Temperature", lambda value: f"{value:.2f} °C")
        yield from _check_dom_sensor(sensors["volt"], "volt", params, "extreme_vsp_switches_dom_voltage", "Voltage", lambda value: f"{value:.4f} V")
    else:
        sensors = dom["channels"][channel]

    if "bias" in sensors:
        yield from _check_dom_sensor(sensors["bias"], "bias", params, "extreme_vsp_switches_dom_bias", "Bias", lambda value: f"{value * 1000:.3f} mA", boundaries=(0, None))
        yield from _check_dom_sensor(sensors["tx"], "tx", params, "extreme_vsp_switches_dom_tx_power", "TX Power", lambda value: f"{value:.2f} dBm")
        yield from _check_dom_sensor(sensors["rx"], "rx", params, "extreme_vsp_switches_dom_rx_power", "RX Power", lambda value: f"{value:.2f} dBm")


snmp_section_extreme_vsp_switches_dom = SNMPSection(
    name="extreme_vsp_switches_dom",
    parse_function=parse_extreme_vsp_switches_dom,
    detect=contains(".1.3.6.1.2.1.1.9.1.3.1", "Extreme Networks Fabric Engine"),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.2.1.2.2.1",
            oids=[OIDEnd(), "7"],  # IF-MIB::ifAdminStatus INTEGER {up(1), down(2), testing(3)}
        ),
        SNMPTree(
            base=".1.3.6.1.2.1.31.1.1.1",
            oids=[OIDEnd(), "1"],  # IF-MIB::ifName
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.2272.1.71.1.1",
            oids=[
                "1", "2", "13", "5",  # Index, DDM mask, DDM support, type
                "17", "18", "19", "20", "21",  # Temperature
                "22", "23", "24", "25", "26",  # Voltage
                "27", "28", "29", "30", "31",  # Bias + shared thresholds
                "32", "33", "34", "35", "36",  # TX + shared thresholds
                "37", "38", "39", "40", "41",  # RX + shared thresholds
                "52", "53", "54", "55", "56",  # Module sensor status
                "59", "60", "61", "62",  # Bias channels 1-4
                "63", "64", "65", "66",  # TX channels 1-4
                "67", "68", "69", "70",  # RX channels 1-4
                "71", "72", "73", "74",  # Bias status channels 1-4
                "75", "76", "77", "78",  # TX status channels 1-4
                "79", "80", "81", "82",  # RX status channels 1-4
            ],
        ),
    ],
)


check_plugin_extreme_vsp_switches_dom = CheckPlugin(
    name = "extreme_vsp_switches_dom",
    service_name = "DOM Port %s",
    discovery_function = discover_extreme_vsp_switches_dom,
    check_function = check_extreme_vsp_switches_dom,
    check_default_parameters= {
        "rx": ("device", None),
        "tx": ("device", None),
        "temp": ("device", None),
        "bias": ("device", None),
        "volt": ("device", None),
    },  
    check_ruleset_name = "extreme_vsp_switches_dom",
)

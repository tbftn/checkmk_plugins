[PACKAGE]: packages/extreme_vsp_switches_dom-0.1.0.mkp "extreme_vsp_mem-0.1.0.mkp"
# Extreme Networks Fabric Engine – Digital Optical Monitoring (DOM)

SNMP-based Digital Optical Monitoring (DOM) for Extreme Networks switches running Fabric Engine / VOSS.

The plugin monitors optical transceiver diagnostics, including temperature, supply voltage, laser bias current, transmit power (TX), and receive power (RX). It supports single-channel SFP/SFP+ optics and four-channel QSFP28 optics, with separate Checkmk services for individual optical channels.

## Check information
The plugin discovers DOM-capable optical modules and creates services according to the transceiver type:

| Transceiver | Discoverd services | Monitoried values |
| :--- | :--- | :--- |
| SFP / SFP+ (single-channel) | `DOM Port 1/17` | Temperature, voltage, bias, TX power, RX power |
| QSFP28 (four-channel) | `DOM Port 1/54` | Shared temperature and voltage |
| QSFP28 channel 1–4 | `DOM Port 1/51 Channel 1` ... `Channel 4` | Bias, TX power and RX power per channel |

![check](img/check.png?raw=true "sample service output")

Only DOM-capable modules on interfaces with `ifAdminStatus = up(1)` are discovered. Administratively disabled interfaces (`down(2)`), interfaces in `testing(3)` state, and ports with unknown administrative status are excluded. Modules without DOM support, such as the tested passive DAC cables, are not discovered.

### Sensor metrics
- RX Power (dBm)
- TX Power (dBm)
- Temperature (°C)
- Bias (A), displayed in mA
- Voltage (V)

### Thresholds configuration
![wato](img/wato.png?raw=true "sample ruleset")

Each sensor type (RX, TX, temperature, bias and voltage) can be configured independently using the Checkmk rule: **Extreme Networks VSP Digital Optical Monitoring (DOM)**

Modes:
- **Use device levels (default)**: Evaluate measurements against the warning and alarm thresholds reported by the transceiver
- **Use the following levels**: Configure custom upper/lower warning and critical limits. Either direction can also be set to No levels.
- **No levels**: Disable threshold evaluation for the chosen direction while continuing to record metrics. This is configured within the custom-levels option.

Custom bias thresholds are entered in mA in the ruleset, while the metric is stored in A for SI scaling.

You can compare optical diagnostics and manufacturer thresholds with the Fabric Engine CLI:
```
show pluggable-optical-modules detail <port>
```

## Download
- [Download the newest mkp file][PACKAGE]

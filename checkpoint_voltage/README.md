[PACKAGE]: packages/checkpoint_voltage-0.1.0.mkp "checkpoint_voltage-0.1.0.mkp"
# Check Point Voltage

This check monitors voltage sensors in Check Point firewalls. It is an **enhanced replacement** for the original Checkmk check *checkpoint_voltage*.

> [!caution]
> This plugin normalizes voltage sensor names during service discovery. As a result, existing services may be renamed (for example, Voltage Voltage 1V2 becomes Voltage 1V2). After upgrading from the original checkpoint_voltage check, a service discovery should be performed on affected hosts to remove obsolete services and create the new ones.

![discovery](img/discovery.png?raw=true "service discovery")

## Improvements over the original check
- Configurable state handling:
    - Out-of-range conditions can be mapped to the desired Checkmk state (default: `CRIT`)
    - Sensor reading errors can be mapped to the desired Checkmk state (default: `UNKNOWN`)
- Optional performance data:
    - Voltage values can be exported as performance data
    - Enables metric collection and graphing in Checkmk
- Improved service naming:
    - Removes redundant occurrences of "Voltage" from sensor names
    - Prevents duplicate service names such as `Voltage Voltage 0V99`

![service](img/service.png?raw=true "sample service output")

## Check information
Creates one service **Voltage** per voltage sensor.

![check](img/check.png?raw=true "sample service output")

**Monitors**
- States (configurable):
    - If a sensor reports an out-of-range condition: `CRIT`
    - If a sensor reading error occurs: `UNKNOWN`

![wato](img/wato.png?raw=true "sample ruleset")

**Metrics**
- Electrical Voltage (V); only if activate in ruleset `Checkpoint Voltage`

![metrics](img/metrics.png?raw=true "sample ruleset")

## Download
- [Download the newest mkp file][PACKAGE]
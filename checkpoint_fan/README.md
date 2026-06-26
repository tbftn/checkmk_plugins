[PACKAGE]: packages/checkpoint_fan-0.1.0.mkp "checkpoint_fan-0.1.0.mkp"
# Check Point Fan

This check monitors fan sensors in Check Point firewalls. It is an **enhanced replacement** for the original Checkmk check *checkpoint_fan*.

> [!note]
> This plugin removes unused fans. After upgrading from the original "checkpoint_fan" check, service discovery should be performed on the affected hosts to remove obsolete services.

![discovery](img/discovery.png?raw=true "service discovery")

## Improvements over the original check
- Configurable state handling:
    - Out-of-range conditions can be mapped to the desired Checkmk state (default: `CRIT`)
    - Sensor reading errors can be mapped to the desired Checkmk state (default: `UNKNOWN`)
- Optional performance data:
    - Speed values can be exported as performance data
    - Enables metric collection and graphing in Checkmk
- Removed unused fans

## Check information
Creates one service **Fan** per fan sensor.

![check](img/check.png?raw=true "sample service output")

**Monitors**
- States (configurable):
    - If a sensor reports an out-of-range condition: `CRIT`
    - If a sensor reading error occurs: `UNKNOWN`

![wato](img/wato.png?raw=true "sample ruleset")

**Metrics**
- Speed (RPM); only if activate in ruleset `Checkpoint Fan`

![metrics](img/metrics.png?raw=true "sample ruleset")

## Download
- [Download the newest mkp file][PACKAGE]
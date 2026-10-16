[PACKAGE]: packages/extreme_vsp_mem-0.1.0.mkp "extreme_vsp_mem-0.1.0.mkp"
# Extreme Networks VOSS Memory Usage

This Checkmk plugin monitors the *memory usage* of Extreme Networks switches running *VOSS* (VSP Operating System / Fabric Engine) via SNMP.

## Check information
Creates one service **Memory** per monitored switch

![check](img/check.png?raw=true "sample service output")

### Monitors
- Used memory: `WARN`/`CRIT` at 80%/90% (configurable)

![wato](img/wato.png?raw=true "sample ruleset")

### Metrics
- Memory usage (%)
- Memory usage (B)

![metrics](img/metrics.png?raw=true "sample ruleset")

## Download
- [Download the newest mkp file][PACKAGE]

[PACKAGE]: packages/netextreme_stp_domain-0.1.0.mkp "netextreme_stp_domain-0.1.0.mkp"
# Extreme Networks Spanning Tree Domain

This check monitors the stability of Spanning Tree Protocol (STP) domains on Extreme Networks switches.

The plugin evaluates topology changes and can detect unstable Layer 2 topologies caused by flapping links, unstable uplinks, loops, or misconfigured edge ports.

> [!note]
> This plugin requires at least Extreme Networks' firmware version 30.x. It has not been tested with earlier versions.

## Check information
Creates one service **STP Domain** per active STP domain. Only enabled domains are discovered.

![check](img/check.png?raw=true "sample service output")

**Monitors**
- Topology change rate: `WARN`/`CRIT` at 1.0/min / 2.0/min (configurable)
- Last topology change: no levels default (lower levels configurable)
- States (configurable):
    - If bride is not the root bridge: `WARN`
    - If RSTP not enabled: `WARN`
    - If Rapid Root Failover not enabled: `WARN`

![wato](img/wato.png?raw=true "sample ruleset")

**Metrics**
- Topology changes
- Topology changes rate (changes/minute)
- Time since last topology change

![metrics](img/metrics.png?raw=true "sample ruleset")

## Download
- [Download the newest mkp file][PACKAGE]

## Tested Devices
This plugin has been tested with the following series:

- ExtremeXOS Switches
  - X440-G2 Series
  - X450-G2 Series
  - X460-G2 Series
  - X465 Series
  - X620 Series
  - X670-G2 Series
  - X690 Series
  - X695 Series
  - X870 Series
- Universal Switches
  - 5520 Series
  - 5420 Series
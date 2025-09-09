[PACKAGE]: packages/netextreme_dom-0.1.0.mkp "netextreme_dom-0.1.0.mkp"
# Extreme Networks Optical Modules (SFP)

This check will monitor the *rx_signal_power* and the *tx_signal_power* of Extreme Networks optical modules (SFP).

> [!note]
> This plugin requires at least Extreme Networks' firmware version 30.x. It has not been tested with earlier versions.

> [!caution]
> There is currently a bug in Extreme Networks' firmware. The "etsysEntitySfpSensorState" returns a value of 6 (highAlarm) instead of 4 (normal). This error only occurs in SNMP queries and not in the CLI. To resolve the issue, you need at least firmware version v31.7.1.4-patch1-77 or v32.3.x.

### Check information

#### Service
- Creates one service **DOM Port** per installed SFP and each Channel with DOM functionality
- DOMs are only recognized if the corresponding interface is not in AdminStatus 2 (disabled)

#### State logic
- `WARN` if the receive/transmit power is outside the warning thresholds (configurable)
- `CRIT` if the receive/transmit power is outside the alert thresholds (configurable)

#### WATO options
- Input Power (RX)/ Output Power (TX)
  - Use devices levels (The state of the DOM is calculated using the thresholds from the device. Use `show port <port> transceiver information detail` to see the thresholds in the cli)
  - Use the following levels (Custom thresholds or no thresholds)

![wato](img/wato.png?raw=true "sample ruleset")

#### Performance data
- RX signal power (dBm)
- TX signal power (dBm)

#### Sample Output

![check](img/check.png?raw=true "sample service output")

### Download

- [Download the newest mkp file][PACKAGE]

### Tested Devices

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
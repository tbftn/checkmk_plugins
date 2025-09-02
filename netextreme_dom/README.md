# Extreme Networks optical modules (SFP)

This check will monitor the *rx_signal_power* and the *tx_signal_power* of Extreme Networks optical modules (SFP).

> [!note]
> This version has not been fully tested. Please use this MKP with caution!

> [!note]
> This plugin requires at least firmware version 30.x. It has not been tested with earlier versions.

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
  - Use devices levels (The state of the DOM is calculated using the thresholds from the device. Use 'show port <port> transceiver information detail' to see the thresholds in the cli)
  - Use the following levels (Custom thresholds or no thresholds)

![wato](img/wato.png?raw=true "sample ruleset")

#### Performance data
- RX signal power (dBm)
- TX signal power (dBm)

#### Sample Output

![check](img/check.png?raw=true "sample service output")

### Tested Devices
This plugin has been tested with the following models:

- Summit Series
  - X440-G2-12p-10G4
  - X440-G2-24p-10G4
  - X440-G2-24t-10G4
  - X440-G2-48p-10G4
  - X450-G2-48p-10G4
  - X460-G2-24p-10G4
  - X460-G2-24t-10G4
  - X460-G2-24t-G4
  - X460-G2-24x-10GE4
  - X460-G2-48p-10G4
  - X460-G2-48t-10G4
  - X460-G2-48x-10G4
  - X465-24XE
  - X465-48P
  - X620-16t
  - X620-16x
  - X670-G2-48x-4q
  - X690-48x-2q-4c
  - X695-48Y-8C
  - X870-32c
- Universal Platform EXOS
  - 5520-48W-EXOS
- Universal Platform Switch Engine
  - 5420M-16MW-32P-4YE-SwitchEngine
  - 5420M-24W-4YE-SwitchEngine
  - 5420M-48T-4YE-SwitchEngine
  - 5420M-48W-4YE-SwitchEngine
  - 5520-12MW-36W-SwitchEngine
  - 5520-24W-SwitchEngine
  - 5520-24X-SwitchEngine
  - 5520-48SE-SwitchEngine
  - 5520-48T-SwitchEngine
  - 5520-48W-SwitchEngine

### Contributing
If you encounter any issues or have ideas for improvements, feel free to contact me at alexander.vogel.2305@gmail.com.

For certain fixes or enhancements, I may need a `snmpwalk` output from the device in question.  
This should include:

- `.1.3.6.1.2.1.1.1` (`sysDescr`)  
- `.1.3.6.1.2.1.1.2` (`sysObjectID`)  
- All SNMP OIDs used by this plugin
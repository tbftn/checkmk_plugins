# Extreme Power Supply Inputs

This check will monitor the *electrical power* and the *state* of Extreme Networks Power Supply Inputs.

It is an **enhanced replacement** for the original Checkmk check *netextreme_psu_in*.

> [!note]
> This plugin requires at least firmware version 30.x. It has not been tested with earlier versions.

> [!note]
> This plugin adds the new "Extreme Power Supply Input" rule. After installation, the old rules named "Parameters for input phases of UPSs and PDUs" will no longer be effective. You must manually migrate them to the new "Extreme Power Supply Input" rule set.

### Improvements over the original check
* More detailed state handling: instead of only ‘OK’ or ‘not detected’, this check distinguishes between Powered On, Powered Off, and Failed.
* Flexible configuration:  
  * "Powered Off" and "Failed" can be mapped to the desired Checkmk states (default: `CRIT`).  
  * Upper power consumption thresholds can be adjusted in WATO.  
* Clearer service information and performance data (electrical power in W).

This way, the check provides more transparency about the actual status of each power supply, while staying fully compatible with Checkmk.

### Check information
#### Service
- Creates one service **Power Supply Input** per installed power supplies

#### State logic
- `WARN` if electrical power > 110 W (default)
- `CRIT` if electrical power > 120 W (default)
- `CRIT` if Power Supply is "Powered Off" or "Failed" (both configurable)

#### WATO options
- Configure threshold values for wattage
- Adjust Checkmk states for "Powered Off" / "Failed"

![wato](img/wato.png?raw=true "sample ruleset")

#### Performance data
- Electrical power (W)

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
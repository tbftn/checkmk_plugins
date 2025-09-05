# Extreme Networks Memory Usage

This check will monitor the *memory usage* of Extreme Networks Switches.

### Check information
#### Service
- Creates one service **Memory**

#### State logic
- `WARN` if memory usage > 80% (default)
- `CRIT` if memory usage > 90% (default)

#### WATO options
- Configure threshold values for memory usage
- Adjust Checkmk states for "Powered Off" / "Failed"

![wato](img/wato.png?raw=true "sample ruleset")

#### Performance data
- total memory usage (percent)
- total memory usage (B)
  - user memory usage (B)
  - system memory usage (B)

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
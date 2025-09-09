[PACKAGE]: ../../raw/master/packages/netextreme_psu_in-1.0.0.mkp "netextreme_psu_in-1.0.0.mkp"
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
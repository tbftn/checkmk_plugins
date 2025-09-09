[PACKAGE]: ../../raw/master/packages/netextreme_mem-1.0.1.mkp "netextreme_mem-1.0.1.mkp"
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

![wato](img/wato.png?raw=true "sample ruleset")

#### Performance data
- total memory usage (percent)
- total memory usage (B)
  - user memory usage (B)
  - system memory usage (B)

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
[PACKAGE]: packages/checkpoint_powersupply-0.1.0.mkp "checkpoint_powersupply-0.1.0.mkp"
# Check Point Power Supply
This check will monitor the *state* of Check Point Power Supplys.

It is an **enhanced replacement** for the original Checkmk check *checkpoint_powersupply*.

### Improvements over the original check
- More states than just "Up" are considered. "Present" and "OK" are also considered positive statuses
- It can be configured when the status is outside the positive states

### Check information

#### Service
- Creates one service **Power Supply ** per installed power supply

#### State logic
- `CRIT` (configurable) if Power Supply is not "OK", "Present" or "Up"

#### WATO options
- The Checkmk state can be selected if the status of the power supply is not "OK", "Present" or "Up"

![wato](img/wato.png?raw=true "sample ruleset")

#### Performance data
- No performance data

#### Sample Output

![check](img/check.png?raw=true "sample service output")

### Download

- [Download the newest mkp file][PACKAGE]

### Tested Devices

This plugin has been tested with the following appliances:

- 1900/2000 Appliances
- 6000 Aplliances
- 15000 Appliances
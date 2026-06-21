[PACKAGE]: packages/checkpoint_powersupply-0.1.1.mkp "checkpoint_powersupply-0.1.1.mkp"
# Check Point Power Supply [DEPRECATED]

> [!caution]
> This MKP is no longer being maintained, as its functionality has been incorporated into Checkmk's built-in check and is being continuously maintained there (e.g., Werks [19680](https://checkmk.com/werk/19680), [19978](https://checkmk.com/werk/19978)).

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
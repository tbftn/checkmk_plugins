# Checkmk Plugins Collection
This repository contains a collection of custom [Checkmk](https://checkmk.com/) plugins.  
Each plugin lives in its own folder and has its own `README.md` with details.  

## Plugin overview

### Check Point
- [**Power Supply**](checkpoint_powersupply/): Monitor the *state* of Power Supplys from Check Point Appliances

### Extreme Networks
- [**Optical Modules (SFP)**](netextreme_dom/): Monitor the *input power* and the *output power* of optical modules (SFPs) from Extreme Network Switches

- [**Memory Usage**](netextreme_mem/): Monitor the *memory usage* of Extreme Networks Switches

- [**Power Supply Input**](netextreme_psu_in/): Monitor the *electrical power* and the *state* of Power Supply Inputs from Extreme Network Switches

- [**ExtremeCloud IQ Controller (Special agent)**](netextreme_xiq_controller/): This special Agent will monitor the *APs*, *Sites* and *WLANs* from the ExtremeCloud IQ Controller

## Installation
You can either copy plugin files manually into your Checkmk site or install an MKP (Checkmk package) via the web interface.
The official Checkmk documentation for MKPs can be found here: **[Checkmk Docs](https://docs.checkmk.com/latest/en/mkps.html)**

## Author
Developed and maintained by: Alexander Vogel (alexander.vogel.2305@gmail.com)

## Contributing
If you encounter any issues or have ideas for improvements, feel free to contact me at alexander.vogel.2305@gmail.com.

For certain fixes or enhancements, I may need a `snmpwalk` output from the device in question.  
This should include:

- `.1.3.6.1.2.1.1.1` (`sysDescr`)  
- `.1.3.6.1.2.1.1.2` (`sysObjectID`)  
- All SNMP OIDs used by the respective plugin
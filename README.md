# Checkmk Plugins Collection
This repository contains a collection of custom [Checkmk](https://checkmk.com/) plugins.  
Each plugin lives in its own folder and has its own `README.md` with details.  

## Plugin overview
| Plugin name | Version | Vendor | Description |
|-------------|---------|--------|-------------|
| [checkpoint_powersupply](checkpoint_powersupply/) | 0.1.0 | Check Point | Monitor the *state* of Power Supplys | 
| [netextreme_dom](netextreme_dom/) | 0.1.0 | Extreme Networks | Monitor the *rx_signal_power* and the *tx_signal_power* of optical modules (SFP) | 
| [netextreme_mem](netextreme_mem/) | 0.1.1 | Extreme Networks | Monitor the *memory usage* of Extreme Networks Switches | 
| [netextreme_psu_in](netextreme_psu_in/) | 0.1.0 | Extreme Networks | Monitor the *electrical power* and the *state* of Power Supply Inputs |

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
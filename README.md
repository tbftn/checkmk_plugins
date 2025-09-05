# Checkmk Plugins Collection
This repository contains a collection of custom [Checkmk](https://checkmk.com/) plugins.  
Each plugin lives in its own folder and has its own `README.md` with details.  

## Plugin overview
| Plugin name | Version | Vendor | Description |
|-------------|---------|--------|-------------|
| [netextreme_dom](netextreme_dom/) | 0.1.0 | Extreme Networks | Monitor the *rx_signal_power* and the *tx_signal_power* of optical modules (SFP) | 
| [netextreme_mem](netextreme_mem/) | 0.1.0 | Extreme Networks | Monitor the *memory usage* of Extreme Networks Switches | 
| [netextreme_psu_in](netextreme_psu_in/) | 0.1.0 | Extreme Networks | Monitor the *electrical power* and the *state* of Power Supply Inputs |

## Installation
You can either copy plugin files into your Checkmk site manually, or build an MKP (Checkmk package).  
See the official Checkmk Docs for MKPs here: **[Checkmk Docs](https://docs.checkmk.com/latest/en/mkps.html)**

## Author
Developed and maintained by: Alexander Vogel (alexander.vogel.2305@gmail.com)
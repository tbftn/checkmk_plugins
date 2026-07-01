# Checkmk Plugins Collection
This repository contains a collection of custom [Checkmk](https://checkmk.com/) plugins.  
Each plugin lives in its own folder and has its own `README.md` with details.  

## Plugin overview

### Check Point
- [**Fan**](checkpoint_fan/): Monitor *fan sensors* on Firewalls and Appliances

- [**Power Supply \[DEPRECATED\]**](checkpoint_powersupply/): Monitor the *state* of Power Supplys on Firewalls and Appliances

- [**Voltage**](checkpoint_voltage/): Monitor *voltage sensors* on Firewalls and Appliances

### Extreme Networks
- [**Optical Modules (SFP)**](netextreme_dom/): Monitor the *input power* and the *output power* of optical modules (SFPs) on Switches

- [**Memory Usage**](netextreme_mem/): Monitor the *memory usage* on Switches

- [**Power Supply Input**](netextreme_psu_in/): Monitor the *electrical power* and the *state* of Power Supply Inputs on Switches

- [**Spanning Tree Domain**](netextreme_stp_domain/): Monitor the stability of Spanning Tree Protocol (STP) domains on Switches

- [**ExtremeCloud IQ Controller (Special Agent)**](netextreme_xiq_controller/): Monitor the *APs*, *Sites* and *WLANs*

### VMware
- [**Avi Load Balancer \[DEPRECATED\]**](vmware_alb/): Monitor the states from *controllers*, *service engines* and *virtual services*
- [**Avi Load Balancer (Special Agent)**](vmware_avi/): Monitor *Alerts*, *Certificates*, *Clouds*, *Cluster*, *Nodes*, *Service Engines* and *Virtual Services*

## Installation
You can either copy plugin files manually into your Checkmk site or install an MKP (Checkmk package) via the web interface.
The official Checkmk documentation for MKPs can be found here: **[Checkmk Docs](https://docs.checkmk.com/latest/en/mkps.html)**

## Author
Developed and maintained by: Alexander Vogel (alexander.vogel.2305@gmail.com)

## Contributing
If you encounter any issues or have ideas for improvements, feel free to contact me at alexander.vogel.2305@gmail.com.
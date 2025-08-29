[PACKAGE]: ../../tree/main/source/packages/netextreme_psu_in-1.0.0.mkp "netextreme_psu_in-1.0.0.mkp"
# Extreme Power Supply Inputs

This check monitors the *electrical power* of Extreme Networks Power Supply Inputs.

It is an **enhanced replacement** for the original Checkmk check *netextreme_psu_in*.


### Improvements over the original check
* More detailed state handling: instead of only reporting "OK" or "not detected", this check differentiates between  
  **Powered On**, **Powered Off**, and **Failed**.
* Flexible configuration:  
  * "Powered Off" and "Failed" can be mapped to the desired Checkmk states (default: `CRIT`).  
  * Upper power consumption thresholds can be adjusted in WATO.  
* Clearer service information and performance data (electrical power in W).

This way, the check provides more transparency about the actual status of each power supply, while staying fully compatible with Checkmk.


### Check information
* *service*: creates the service **Power Supply Input** for each installed PSU  
* *state*: 
  * **warning**:
    * if electrical power exceeds the configured value (default: 110 W)
  * **critical**:
    * if electrical power exceeds the configured value (default: 120 W)
    * if the power supply is in state "Powered Off"
    * if the power supply is in state "Failed"
* *wato*:
  * Configure upper wattage thresholds  
  * Configure how "Powered Off" and "Failed" should be mapped to Checkmk states  
* *perfdata*: 
  * Electrical power in W
    
![sample output](img/sample_output.png?raw=true "sample [SHORT TITLE]")
![sample output](img/wato.png?raw=true "sample [SHORT TITLE]")

### Download
* [Download latest mkp file][PACKAGE]
[PACKAGE]: packages/netextreme_xiq_controller-0.2.0.mkp "netextreme_xiq_controller-0.2.0.mkp"
# ExtremeCloud IQ Controller (Special Agent)

This special agent will monitor the APs, Sites and WLANs from the **ExtremeCloud IQ Controller**

> [!note]
> This Special Agent monitors the on-premises solution, the "[ExtremeCloud IQ Controller](https://www.extremenetworks.com/products/wi-fi-management/extremecloud-iq-controller/extremecloud-iq-controller)". Please do NOT confuse this with "ExtremeCloud IQ", a cloud solution.

This Special Agent can add the following sections:
- Access point
- Site
- WLAN

### Check information netextreme_xiq_controller_ap
To access the ExtremeCloud IQ Controller, you need a user with admin privileges. In the ExtremeCloud IQ Controller rule set, under the Other integrations section, you then need to enter the access data.

![wato](img/wato_special_agent.png?raw=true "sample ruleset")
 
### Check information netextreme_xiq_controller_ap

#### Service
- Creates the service **AP** for each access point that is created in the ExtremeCloud IQ Controller
- Access points are only detected if they are not in the *pending* status

#### WATO options
- Adjust Checkmk states for *In-Service*, *Upgrading*, *In-Service Trouble*, *Critical*
- Configure upper threshold values for number of clients
- Configure upper threshold values for ap power

![wato](img/wato_ap.png?raw=true "sample ruleset")

#### Performance data
- Active Clients
- AP Uptime
- AP Power (W), only for AP-4000 series

#### Sample Output
![check](img/check_ap.png?raw=true "sample service output")

### Check information netextreme_xiq_controller_site

#### Service
- Creates the service **Site** for each Site (Location) that is created in the ExtremeCloud IQ Controller

#### WATO options
- Configure upper threshold values for number of clients

![wato](img/wato_site.png?raw=true "sample ruleset")

#### Performance data
- Active Clients

#### Sample Output
![check](img/check_site.png?raw=true "sample service output")

### Check information netextreme_xiq_controller_wlan

#### Service
- Creates the service **WLAN** for each WLAN (SSID) that is created in the ExtremeCloud IQ Controller
- The service will only be created if the WLAN (SSID) is not disabled

#### WATO options
- Configure upper threshold values for number of clients

![wato](img/wato_wlan.png?raw=true "sample ruleset")

#### Performance data
- Active Clients

#### Sample Output
![check](img/check_wlan.png?raw=true "sample service output")

### Download
- [Download the newest mkp file][PACKAGE]

### Tested Devices
Firmware version 10.15.x is recommended.

AP series:
- AP310i
- AP505i
- AP4000

[PACKAGE]: packages/netextreme_xiq_controller-0.2.0.mkp "netextreme_xiq_controller-0.2.0.mkp"
# ExtremeCloud IQ Controller (Special Agent)

> [!note]
> This Special Agent monitors the on-premises solution, the "[ExtremeCloud IQ Controller](https://www.extremenetworks.com/products/wi-fi-management/extremecloud-iq-controller/extremecloud-iq-controller)". Please do NOT confuse this with "ExtremeCloud IQ", a cloud solution.

This Special Agent can monitor the following sections:
- Access point
- Site
- WLAN

To access the ExtremeCloud IQ Controller, you need a user with admin privileges. In the ExtremeCloud IQ Controller rule set, under the Other integrations section, you then need to enter the access data.

![wato](img/wato_special_agent.png?raw=true "sample ruleset")
 
## Services
**<details><summary>AP</summary>**
Creates the service **AP** for each access point that is created.

![check](img/check_ap.png?raw=true "sample service output")

**Monitors**
- State (configurable)
    - OK if is *In-Service* or *Upgrading*
    - WARN if is *In-Service Trouble*
    - CRIT if is *Upgrade Failed* or *Critical*
- Number of Clients: no levels default (configurable)
- Power: no levels default (configurable)

    ![wato](img/wato_ap.png?raw=true "sample ruleset")

**Metrics**
- Active Clients
- AP Uptime
- AP Power (W), only for AP-4000 series
</details>

**<details><summary>Site</summary>**
Creates the service **Site** for each Site (Location) that is created

![check](img/check_site.png?raw=true "sample service output")

**Monitors**
- Number of Clients: no levels default (configurable)

    ![wato](img/wato_site.png?raw=true "sample ruleset")

**Metrics**
- Active Clients
</details>

**<details><summary>WLAN</summary>**
Creates the service **WLAN** for each WLAN (SSID) that is created. It will only be created if the WLAN (SSID) is not disabled.

![check](img/check_wlan.png?raw=true "sample service output")

**Monitors**
- Number of Clients: no levels default (configurable)

    ![wato](img/wato_wlan.png?raw=true "sample ruleset")

**Metrics**
- Active Clients
</details>

## Download
- [Download the newest mkp file][PACKAGE]

## Tested Devices
Firmware version 10.15.x is recommended.

AP series:
- AP310i
- AP505i
- AP4000

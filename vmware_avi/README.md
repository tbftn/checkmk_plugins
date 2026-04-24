[PACKAGE]: packages/vmware_avi-0.1.0.mkp "vmware_avi-0.1.0.mkp"
# VMware Avi Load Balancer (Special Agent)

> [!note]
> This MKP is an early version (0.1.0) and not final yet. Feedback, suggestions, and improvements are very welcome.

This Special Agent can monitor the following sections:
- Alerts
- Certificates
- Cloud
- Cluster and Nodes
- Service Engines (as hosts with piggyback data)
- Virtual Services

To access the VMware Avi Load Balancer, you need a user with the appropriate permissions. Then, enter the access credentials in the "Other Integrations" section of the VMware Avi Load Balancer rule set.

![wato](img/wato_special_agent.png?raw=true "sample ruleset")

## Services
This special agents creates the following services:

**<details><summary>Alerts</summary>**
Create one service **Avi Alerts**.

![service_alert](img/service_alert.png?raw=true "service alert")

**Monitors**
  - Alerts: CRIT if at least one alarm is present
</details>

**<details><summary>Certificates</summary>**
Creates the service **Avi Cert** for each certificate that is created.

![service_cert](img/service_cert.png?raw=true "service cert")

**Monitors**
- State: CRIT if not "SSL_CERTIFICATE_FINISHED"
- Time until expire: WARN/CRIT if lower as 90 days/30 days (configurable)

**Metrics**
- Time until expire
</details>

**<details><summary>Cloud</summary>**
Creates the service **Avi Cloud** for each cloud that is connected.

![service_cloud](img/service_cloud.png?raw=true "service cloud")

**Monitors**
- State: CRIT if not "CLOUD_STATE_PLACEMENT_READY" (Ready)
</details>

**<details><summary>Cluster and Nodes</summary>**
Creates the service **Avi Cluster** and **Avi Node** for each Node that is created.

![service_cluster](img/service_cluster.png?raw=true "service cluster")

**Monitors (Cluster)**
- State: CRIT if not "CLUSTER_UP_HA_ACTIVE" (Active)
- Services: CRIT if at least one service is not Active (notice only)
- Uptime: no levels default (configurable)

**Metrics (Cluster)**
- Uptime
 
**Monitors (Nodes)**
- State: CRIT if not "CLUSTER_ACTIVE" (Active)
- Uptime: no levels default (configurable)

**Metrics (Nodes)**
- Uptime
</details>

**<details><summary>Virtual Services</summary>**
Creates the service **Avi VS** for each Virtual Service that is created and enabled.

![service_vs](img/service_vs.png?raw=true "service vs")

**Monitors**
- State: CRIT if not "OPER_UP" (Up)
- Health Score: WARN/CRIT if lower as 90%/60% (configurable)
- Service Engines:
  - WARN if assigned SEs are lower then requested SEs (notic only, configurable)
  - CRIT if one or more SEs are not longer connected (notic only, configurable)
- Alerts: CRIT if at least one alarm (low, medium or high) is present

**Metrics**
- Health Score (%)
- Requests per second (/s)
- Connections per second (/s)
- Open Connections
- Throughput (bit/s)
</details>

## Service Engines (Host)
This special agents creates a host for each Service Engine.

![host_se](img/host_se.png?raw=true "host se")

**<details><summary>Alerts</summary>**
Create one service **Avi Alerts**.

**Monitors**
- Alerts: CRIT if at least one alarm (low, medium or high) is present
</details>

**<details><summary>CPU utilization</summary>**
Create one service **Avi CPU utilization**.

**Monitors**
- Total CPU: WARN/CRIT if higher than 80%/90% (configurable)

**Metrics**
- CPU utilization (%)
</details>

**<details><summary>Health</summary>**
Create one service **Avi Health**.

**Monitors**
- Health Score: WARN/CRIT if lower as 90%/60% (configurable)
- Performance Score: WARN/CRIT if lower as 90%/60% (configurable)
- Resource Penalty: WARN/CRIT if higher than 10%/50% (configurable)
- Anomaly Penalty: WARN/CRIT if higher than 10%/50% (configurable)
- Security Penalty: WARN/CRIT if higher than 10%/50% (configurable)

**Metrics**
- Health Score (%)
- Performance Score (%)
- Resource Penalty (%)
- Anomaly Penalty (%)
- Security Penalty (%)
</details>

**<details><summary>Heartbeat</summary>**
Create one service **Avi Heartbeat**.

**Monitors**
- HB misses: CRIT if higher than 1
- HB outstanding: CRIT if higher than 1
- Last request: WARN/CRIT if higher than 30s/60s (configurable)
- Last response: WARN/CRIT if higher than 30s/60s (configurable)

**Metrics**
- HB misses
- HB outstanding
- Last request (s)
- Last response (s)
</details>

**<details><summary>Interface</summary>**
Create one service **Avi Interface**.

**Monitors**
- always OK

**Metrics**
- Throughput (bit/s)
- Input bandwith (bit/s)
- Output bandwith (bit/s)
- Input packets (/s)
- Output packets (/s)
</details>

**<details><summary>Memory</summary>**
Create one service **Avi Memory**.

**Monitors**
- Memory usage: WARN/CRIT if higher than 80%/90% (configurable)
- Connection memory usage: WARN/CRIT if higher than 80%/90% (configurable)
- Dynamic memory usage: WARN/CRIT if higher than 80%/90% (configurable)

**Metrics**
- Memory usage (%)
- Connection memory usage (%)
- Dynamic memory usage (%)
</details>

**<details><summary>Runtime</summary>**
Create one service **Avi Runtime**.

**Monitors**
- State: CRIT if not "OPER_UP"
- Power State: CRIT if not "SE_POWER_ON"
</details>

## Download
- [Download the newest mkp file][PACKAGE]

## Tested Devices
Tested with the following versions:
- 30.2.2

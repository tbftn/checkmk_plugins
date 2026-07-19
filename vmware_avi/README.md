[PACKAGE]: packages/vmware_avi-0.3.0.mkp "vmware_avi-0.3.0.mkp"
# VMware Avi Load Balancer (Special Agent)

> [!NOTE]
> This MKP is an early version (0.3.0) and not final yet. Feedback, suggestions, and improvements are very welcome.

> [!CAUTION]
> **Upgrading from version 0.2.0**
>
> Version 0.3.0 changes the configuration structure of the VMware Avi Special Agent and Virtual Service rules.
>
> Before upgrading:
> 1. Record the current settings of all VMware Avi Special Agent and Virtual Service rules
> 2. Delete these rules before installing version 0.3.0
> 3. Install the new MKP
> 4. Recreate the rules using the new configuration options
>
> Recreating the rules is recommended instead of migrating the existing configuration because it avoids incompatible or incomplete rule parameters.
>
> The Avi API version is now a required Special Agent setting and must be configured when recreating the rule.
>
> Version 0.2.0 also contains a severe parsing error affecting agent sections that may contain one or multiple objects. Version 0.2.0 should therefore no longer be used.


This Special Agent can monitor the following sections:
- Alerts (This feature will be deprecated in a future version) 
- Certificates
- Cloud
- Controller cluster and nodes
- Pools
- Service Engines (provide piggyback monitoring data)
    - CPU
    - Disk
    - Health
    - Heartbeat
    - Interface
    - Memory
    - Runtime
- Virtual Services

To access the VMware Avi Load Balancer, you need a user with the appropriate permissions. Then, enter the access credentials in the "Other Integrations" section of the VMware Avi Load Balancer rule set.

![wato](img/wato_special_agent.png?raw=true "sample ruleset")

## Dashboard
The MKP includes a preconfigured **Avi Load Balancer** dashboard with views and summaries for:

- Controller clusters and nodes
- Service Engines
- Virtual Services
- Pools

![dashboard](img/dashboard.png?raw=true "dashboard")

## Services
This special agent creates the following services:

**<details><summary>Alerts (This feature will be deprecated in a future version)</summary>**
Create one service **Avi Alerts**.

![service_alert](img/service_alert.png?raw=true "service alert")

**Monitors**
  - Alerts: CRIT if at least one alarm is present
</details>

**<details><summary>Certificates</summary>**
Creates the service **Avi Cert** for each certificate that is created.

![service_cert](img/service_cert.png?raw=true "service cert")

**Monitors**
- States: 
    - CRIT when state is not "SSL_CERTIFICATE_FINISHED"
    - WARN if certificate is self-signed (configurable)
-  Remaining certificate validity time: WARN/CRIT if lower than 90 days/30 days (configurable)

**Metrics**
- Remaining certificate validity time

![metrics_cert](img/metrics_cert.png?raw=true "metrics_cert")

</details>

**<details><summary>Cloud</summary>**
Creates the service **Avi Cloud** for each cloud that is connected.

![service_cloud](img/service_cloud.png?raw=true "service cloud")

**Monitors**
- States: 
    - CRIT if state is "CLOUD_STATE_FAILED" (Failed) (configurable)
    - WARN if state is "CLOUD_STATE_IN_PROGRESS" (In progress) (configurable)
</details>

**<details><summary>Cluster and Nodes</summary>**
Creates the service **Avi Cluster** and **Avi Node** for each Node that is created.

![service_cluster](img/service_cluster.png?raw=true "service cluster")

**Monitors (Cluster)**
- State:
    - OK if state is `CLUSTER_UP_HA_ACTIVE`
    - CRIT if state is `CLUSTER_UP_HA_NOT_READY`
    - UNKNOWN for unsupported states
- Services: CRIT if at least one cluster service is not `CLUSTER_ACTIVE`
- Uptime: no levels by default

**Monitors (Nodes)**
- State:
    - OK if state is `CLUSTER_ACTIVE`
    - WARN if state is `CLUSTER_STARTING`
    - UNKNOWN for unsupported states
- Role: OK if role is `CLUSTER_LEADER` or `CLUSTER_FOLLOWER`
- Uptime: no levels by default

**Metrics (Cluster and Nodes)**
- Uptime

![metrics_cluster_node](img/metrics_cluster_node.png?raw=true "metrics_cluster_node")
</details>

**<details><summary>Pools</summary>**
Creates the service **Avi Pool** for each Pool that is created, enabled and not in state OPER_UNUSED (Unused).

![service_vs](img/service_pool.png?raw=true "service vs")

**Monitors**
- State: CRIT if pool is "OPER_DOWN" (Down)
- Health: 
    - Health score: WARN/CRIT if lower than 85/60 (configurable)
    - Performance score: no levels by default (configurable)
    - Resource penalty: no levels by default (configurable)
    - Anomaly penalty: no levels by default (configurable)
    - Security penalty: no levels by default (configurable)
- Alerts: CRIT if at least one alarm (low, medium or high) is present

**Metrics**
- Health Score (Graph)
    - Health score
    - Performance score
    - Resource penalty
    - Anomaly penalty
    - Security penalty
- End to End timing (Graph)
    - Server RTT (s)
    - App response (s)
- New Connections (Graph)
    - New connections rate (/s)
    - Lossy connections rate (/s)
    - Bad connections rate (/s)
- Requests (Graph)
    - Requests rate (/s)
    - 4xx errors rate (/s)
    - 5xx errors rate (/s)
- Request errors (%)
- Servers (Graph)
    - Servers total
    - Servers disabled
    - Servers down
    - Servers up
- Throughput (bit/s)
- Open connections

![metrics_pool](img/metrics_pool.png?raw=true "metrics_pool")
</details>

**<details><summary>Virtual Services</summary>**
Creates the service **Avi VS** for each Virtual Service that is created and enabled.

![service_vs](img/service_vs.png?raw=true "service vs")

**Monitors**
- State: CRIT if VS is "OPER_DOWN" (Down)
- Service Engines:
  - WARN if assigned SEs are lower then requested SEs (notice only, configurable)
  - CRIT if one or more SEs are no longer connected (notice only, configurable)
- Health: 
    - Health score: WARN/CRIT if lower than 85/60 (configurable)
    - Performance score: no levels by default (configurable)
    - Resource penalty: no levels by default (configurable)
    - Anomaly penalty: no levels by default (configurable)
    - Security penalty: no levels by default (configurable)

**Metrics**
- Health Score (Graph)
    - Health score
    - Performance score
    - Resource penalty
    - Anomaly penalty
    - Security penalty
- End to End timing (Graph)
    - Client RTT (s)
    - Server RTT (s)
    - App response (s)
    - Data transfer time (s)
- Connections (Graph)
    - Connections rate (/s)
    - Lossy connections rate (/s)
    - Bad connections rate (/s)
- Requests (Graph)
    - Requests rate (/s)
    - 4xx errors rate (/s)
    - 5xx errors rate (/s)
    - Avi 4xx errors rate (/s)
    - Avi 5xx errors rate (/s)
- Errors (Graph)
    - Connection errors (%)
    - Request errors (%)
- Throughput (bit/s)
- Open connections

![metrics_vs](img/metrics_vs.png?raw=true "metrics_vs")
</details>

## Service Engines (Host)
This special agents creates a host for each Service Engine.

![host_se](img/host_se.png?raw=true "host se")

**<details><summary>Alerts</summary>**
Create one service **Avi Alerts**.

**Monitors**
- Alerts: CRIT if at least one alarm (low, medium or high) is present
</details>

**<details><summary>CPU</summary>**
Create one service **Avi CPU**.

**Monitors**
- Total CPU: WARN/CRIT if higher than 80%/90% (configurable)

**Metrics**
- CPU utilization (%)
</details>

**<details><summary>Disk</summary>**
Create one service **Avi Disk**.

**Monitors**
- Usage: WARN/CRIT if higher than 80%/90% (configurable)

**Metrics**
- Used space (%)
</details>


**<details><summary>Health</summary>**
Create one service **Avi Health**.

**Monitors**
- Health score: WARN/CRIT if lower than 85/60 (configurable)
- Performance score: no levels by default (configurable)
- Resource penalty: no levels by default (configurable)
- Anomaly penalty: no levels by default (configurable)
- Security penalty: no levels by default (configurable)

**Metrics**
- Health Score (Graph)
    - Health score
    - Performance score
    - Resource penalty
    - Anomaly penalty
    - Security penalty
</details>

**<details><summary>Heartbeat</summary>**
Create one service **Avi Heartbeat**.

**Monitors**
- HB misses: WARN/CRIT at 1/10
- HB outstanding: WARN/CRIT at 1/10
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
- Input bandwidth (bit/s)
- Output bandwidth (bit/s)
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
- [Download version 0.3.0][PACKAGE]

## Tested Devices
Tested with the following versions:
- 30.2.x

[PACKAGE]: packages/vmware_avi-0.4.0.mkp "vmware_avi-0.4.0.mkp"
# VMware Avi Load Balancer (Special Agent)

> [!NOTE]
> This MKP is an early version (0.4.0) and not final yet. Feedback, suggestions, and improvements are very welcome.

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

## Download
- [Download version 0.4.0][PACKAGE]

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
    - CRIT when state is "SSL_CERTIFICATE_EXPIRED" (Expired) (configurable)
    - WARN when state is "SSL_CERTIFICATE_EXPIRY_WARNING" (Expire warning) (configurable)
    - WARN if certificate is self-signed (configurable)
-  Remaining certificate validity time: WARN/CRIT if lower than 30 days/7 days (configurable)

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

**Metrics (Cluster)**
- Uptime

![metrics_cluster_node](img/metrics_cluster_node.png?raw=true "metrics_cluster_node")

**Metrics (Nodes)**
- Disk throughput
    - Disk read (byte/s)
    - Disk write (byte/s)
- CPU utilization (%)
- Disk usage (%)
- Memory (%)
- Uptime
</details>

**<details><summary>Pools</summary>**
Creates the service **Avi Pool** for each Pool that is created, enabled and not in states OPER_UNUSED (Unused) and OPER_INACTIVE (Inactive).

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
Creates the service **Avi VS** for each Virtual Service that is created,  enabled and not in state OPER_DISABLED (Disabled).

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

## Compatibility

> [!NOTE]
> The versions listed below are those with which the plugin was tested.
> Other versions may work as well, but have not been tested.

### Checkmk
| Checkmk version | Plugin version |
|-----------------|----------------|
| 2.4.x           | 0.4.0          |
| 2.5.x           | Not yet tested |

The MKP requires at least **Checkmk 2.4.0b1** and is declared usable until **2.6.0b1**.

### VMware Avi Load Balancer

| Avi version | Plugin version |
|-------------|----------------|
| 30.2.x      | 0.4.0          |



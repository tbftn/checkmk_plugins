[PACKAGE]: packages/vmware_alb-0.1.0.mkp "vmware_alb-0.1.0.mkp"
# VMware AVI Load Balancer \[DEPRECATED\]

> [!caution]
> This MKP is no longer maintained and has been replaced by a new special agent for the VMware Avi Load Balancer. The new agent supports significantly more monitoring features than this SNMP-based check. Please use the new agent instead.

This checks will monitor the states from *controllers*, *service engines* and *virtual services* of a VMware AVI Load Balancer.

### Check information vmware_alb_controller

#### Service
- Creates one service **Controller** for each controller

#### State logic
- `OK` if the controller is "Ok"
- `CRIT` if the controller is "Down"

#### Sample Output
![check](img/check_controller.png?raw=true "sample service output")

### Check information vmware_alb_service_engine

#### Service
- Creates one service **Service Engine** for each service engine

#### State logic
- `OK` if the service engine is "Ok"
- `CRIT` if the service engine is "Down"

#### Sample Output
![check](img/check_service_engine.png?raw=true "sample service output")

### Check information vmware_alb_virtual_service

#### Service
- Creates one service **Virtual Service** for each virtual service

#### State logic
- `OK` if the virtual service is "Ok"
- `CRIT` if the virtual service is "Down"

#### Sample Output
![check](img/check_virtual_service.png?raw=true "sample service output")

### Download
- [Download the newest mkp file][PACKAGE]
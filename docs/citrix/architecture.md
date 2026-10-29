# Architecture and Core Components

A **site** is the central administrative boundary for an on-premises CVAD deployment. A production design normally includes redundant infrastructure and avoids a single Delivery Controller, StoreFront server, PVS server, or database path where supported.

## Component categories

### Control plane

| Component | Definition | Purpose |
|---|---|---|
| **Delivery Controller** | Server running Citrix site services, including brokering and configuration services. | Registers VDAs, evaluates launch requests, selects resources, tracks sessions, and coordinates power management. |
| **Site database** | Microsoft SQL database holding site configuration and current operational data. | Persistent source of configuration needed by the controllers. |
| **Monitoring database** | SQL database for historical monitoring information. | Supplies historical session and site data to Director. |
| **Configuration logging database** | SQL database recording administrative changes when configured. | Audit who changed what and when. |
| **Web Studio** | Browser-based administrative console in current releases. | Configure catalogs, delivery groups, applications, policies, hosting connections, and the site. |
| **Director** | Web-based monitoring and support console. | Search users and sessions, inspect failures and performance, and perform help-desk actions. |
| **License Server** | Service that supplies and tracks Citrix product licenses. | Enforce licensed feature and usage rights. |

Older environments may use the MMC-based **Citrix Studio** console. Current Citrix documentation states that beginning with CVAD 2511, Web Studio is the management console and the MMC-based Studio is removed from the installer.

### Resource plane

| Component | Definition | Purpose |
|---|---|---|
| **Virtual Delivery Agent (VDA)** | Software installed on the machine that runs the user workload. | Register with controllers, accept brokered launches, and deliver the session using HDX. |
| **Session host / desktop VM** | The Windows or Linux machine containing the VDA and applications. | Execute the user’s app or desktop session. |
| **Hypervisor or cloud platform** | Compute platform hosting virtual machines. | Run and power the machines; expose management APIs used by MCS and controllers. |
| **Resource location** | In DaaS, a network location containing VDAs and connector components. | Keep workloads near apps/data while connecting them to the cloud control plane. |
| **Cloud Connector** | Citrix component that securely connects a resource location to Citrix Cloud. | Proxy control-plane communication without requiring inbound internet connections to the resource location. |

### Access plane

| Component | Definition | Purpose |
|---|---|---|
| **StoreFront** | On-premises enterprise app store and resource-enumeration service. | Authenticate users, obtain entitlements from controllers, and present apps/desktops. |
| **Citrix Workspace** | Citrix cloud workspace service and user portal. | Provide a cloud-hosted resource feed and access experience. |
| **Citrix Workspace app** | Client software on the user endpoint. | Display resources and establish HDX sessions. |
| **Citrix Gateway / NetScaler Gateway** | Secure remote-access gateway. | Terminate external TLS access and proxy authorized session traffic into the environment. |

### Image, policy, and user-experience services

| Component | Purpose |
|---|---|
| **MCS** | Clone and update VM catalogs from a master image. |
| **PVS** | Stream a shared vDisk image to target devices. |
| **Citrix policies** | Control session behavior and user experience. |
| **Citrix Profile Management** | Preserve and optimize user settings across sessions and machines. |
| **Workspace Environment Management (WEM)** | Optimize logon, resource use, and user environment settings. |

## Important relationships

- A **VDA registers** with one of its configured controllers or cloud connector paths.
- A controller can broker only resources it knows are registered and available.
- StoreFront or Workspace asks the brokering service which resources a user may see.
- The user’s HDX data path is distinct from the administrative and registration paths.
- MCS or PVS can make a machine available, but the VDA and broker are what make it launchable.

## Data-path principle

The controller brokers the connection; it normally does not carry all interactive display traffic for the life of the session. After brokering, HDX traffic flows between the endpoint and VDA, directly or through Gateway depending on the access design.

## Availability questions to ask

1. Are there multiple Delivery Controllers or Cloud Connectors?
2. Are StoreFront and Gateway services load balanced and redundant?
3. Is SQL highly available, backed up, and recoverable?
4. If PVS is used, can target devices reach more than one PVS server and the vDisk storage path?
5. Can DNS, Active Directory, time synchronization, certificate validation, and licensing survive component failure?
6. Are capacity and power-management settings sufficient during host or zone failures?

## Official references

- [CVAD technical overview](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/technical-overview)
- [Citrix DaaS architecture](https://docs.citrix.com/en-us/citrix-daas/overview)

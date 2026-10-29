# Glossary and Study Checklist

## Glossary

| Term | Beginner definition |
|---|---|
| **Application group** | Optional object that groups applications, users, and delivery groups for app-centric assignment. |
| **Broker** | Service that selects a suitable VDA and authorizes a user launch. |
| **Catalog** | Administrative collection describing machines and how they are provisioned. |
| **Citrix DaaS** | Citrix-hosted management and brokering service for customer resource locations. |
| **Citrix policy** | Rule set controlling session behavior and features. |
| **Cloud Connector** | Connector between a customer resource location and Citrix Cloud. |
| **Control plane** | Services that configure, enumerate, broker, license, and monitor resources. |
| **Delivery Controller** | On-premises CVAD server providing central site and brokering services. |
| **Delivery group** | Machines plus user entitlement and the apps/desktops delivered from them. |
| **Director** | Monitoring and help-desk console. |
| **Farm (PVS)** | Highest PVS administrative boundary using a shared PVS database. |
| **Gateway** | Secure edge proxy for remote Citrix access. |
| **HDX** | Citrix technologies and protocol capabilities that deliver the interactive remote experience. |
| **Hosting connection** | Configured link to a hypervisor or cloud used for VM lifecycle operations. |
| **ICA** | Long-standing Citrix protocol/architecture term; HDX describes the broader experience and technologies built around session delivery. |
| **Machine catalog** | See catalog. It answers what the machines are and how they were built. |
| **MCS** | Machine Creation Services; Citrix-integrated VM cloning and image lifecycle. |
| **Multi-session OS** | One OS instance hosting multiple concurrent user sessions. |
| **Nonpersistent** | Machine-level changes are reset or discarded by design. |
| **Persistent** | Machine-level changes remain across restarts. |
| **Provisioning Server** | PVS server that streams vDisk blocks to targets. |
| **Published application** | Remote application presented without a full desktop shell. |
| **Published desktop** | Complete remote desktop made available to users. |
| **PVS** | Citrix Provisioning; streams a centrally managed vDisk to target devices. |
| **Resource location** | Customer-controlled location containing DaaS workloads and connector components. |
| **Session** | A user’s running app or desktop context on a VDA. |
| **Single-session OS** | OS instance normally hosting one interactive user session at a time. |
| **Site (CVAD)** | On-premises CVAD administrative deployment managed by controllers and site databases. |
| **Site (PVS)** | Grouping inside a PVS farm. The meaning is product-specific. |
| **Store (PVS)** | Logical definition of where vDisk files are located. |
| **StoreFront** | On-premises user store that authenticates and enumerates resources. |
| **Target device** | Machine that boots and streams an assigned PVS vDisk. |
| **VDA** | Virtual Delivery Agent installed on the workload machine. |
| **vDisk** | PVS virtual disk image streamed to target devices. |
| **Web Studio** | Current browser-based CVAD management console. |
| **Workspace app** | Endpoint client used to list and launch Citrix resources. |
| **Write cache** | Per-target storage for writes that cannot modify a shared standard-mode vDisk. |

## Knowledge checks

You should be able to answer these without notes:

1. What is the difference between the control plane, access plane, and resource plane?
2. What does a VDA do?
3. Why is a machine catalog not enough to give a user access?
4. What is the difference between a catalog and a delivery group?
5. What is the difference between multi-session and single-session workloads?
6. What is the difference between a published app and a published desktop?
7. How do random and static assignment differ?
8. Why are machine persistence and profile persistence different?
9. How does MCS deliver an image differently from PVS?
10. What are a PVS farm, site, store, vDisk, collection, and target device?
11. Why does standard-mode PVS require a write cache?
12. What are the major phases from authentication to an active HDX session?
13. Why can StoreFront authentication succeed even if the launch fails?
14. What is the difference between disconnect and logoff?
15. Which console would you use for configuration, monitoring, and PVS image administration?

## Hands-on lab path

Use an isolated lab and supported evaluation licensing.

### Lab 1: Trace the objects

- Locate the site or DaaS tenant.
- Find a machine catalog and identify its OS and provisioning categories.
- Find the delivery group consuming its machines.
- Identify entitled users and published resources.
- Locate the VDA machine and confirm registration.

### Lab 2: Follow a launch

- Sign in through Workspace app or StoreFront.
- Enumerate resources and launch one.
- In Director, locate the session, VDA, delivery group, endpoint, and logon duration.
- Disconnect, reconnect, then log off and compare the states.

### Lab 3: Inspect policy and profile behavior

- Identify effective Citrix and Group Policy settings.
- Change one low-risk lab setting with a narrowly scoped policy.
- Verify the effective result in a new session.
- Locate the user profile store and observe what persists on a nonpersistent machine.

### Lab 4: Compare MCS and PVS

- In MCS, identify the hosting connection, master image, catalog, and current image version.
- In PVS, identify the farm, site, store, vDisk, version, collection, target, boot method, and cache mode.
- Draw each boot path and mark every dependency.

### Lab 5: Break and recover safely

In a lab only:

- put one machine in maintenance mode and observe launch behavior;
- stop or isolate one noncritical dependency at a time;
- capture the exact error in Director and relevant logs;
- restore the dependency and verify a real launch;
- write a short root-cause note.

## Recommended next topics

- High availability and zone design
- Gateway and authentication flows
- HDX transport and virtual channels
- Profile containers and logon optimization
- Image automation and change control
- App layering and application compatibility
- Security baselines and least privilege
- Monitoring, alerting, and capacity planning
- Disaster recovery and tested restoration

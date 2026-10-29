# Operations and Troubleshooting

Good Citrix troubleshooting follows the connection path and proves each layer. Avoid rebooting random servers before identifying the failing phase.

## Daily operational view

Check:

- controller, cloud connector, StoreFront, Gateway, licensing, and database health;
- registered versus unregistered VDAs;
- machines in maintenance mode or failed power states;
- failed launches and failure trends in Director;
- concurrent-session capacity and load;
- logon duration and its subphases;
- hypervisor health, storage latency, and free space;
- profile-store health and capacity;
- PVS server, vDisk-store, and write-cache health where used;
- certificate expiration and external monitoring alerts.

## Troubleshooting method

### 1. Define the scope

Ask:

- One user, a user group, one machine, one catalog, one delivery group, one site, or everyone?
- Internal, external, or both?
- One application or all resources?
- New sessions only or existing sessions too?
- What changed immediately before the issue?

### 2. Identify the failed phase

```text
Endpoint
 → DNS/network
 → authentication
 → enumeration
 → brokering
 → machine power
 → VDA registration
 → HDX connection
 → profile/policy/logon
 → application
```

### 3. Compare good and bad

Compare a failing user or machine with a known-good one in the same intended configuration. Differences often reveal entitlement, policy, image version, subnet, profile, or VDA state problems.

### 4. Collect evidence before changing state

Capture timestamps, usernames, machine names, session IDs, correlation IDs where available, Director failure text, event logs, service state, and network tests. A reboot can erase useful evidence.

### 5. Make the smallest reversible change

Prefer a narrow test or canary. Record what changed, the expected result, and the rollback.

## Symptom matrix

| Symptom | Likely categories to inspect |
|---|---|
| Store unavailable | DNS, TLS certificate, load balancer, StoreFront/IIS, Gateway |
| User sees no resources | Authentication identity, delivery-group entitlement, application assignment, broker/store configuration |
| Machine unregistered | VDA services, controller discovery, DNS, firewall, time, machine identity, version compatibility |
| No machines available | Capacity, registration, maintenance mode, power management, assignment, load index |
| Session disconnects | Endpoint network, Gateway, HDX transport, session reliability, VDA health |
| Slow logon | Group Policy, profile, scripts, printers, WEM, overloaded VDA or storage |
| App opens slowly or fails | App dependencies, permissions, image/version, profile, application command line |
| PVS target will not boot | Boot order, DHCP/PXE/BDM, bootstrap, target record, vDisk assignment, streaming path |
| PVS targets freeze or run out of space | Write-cache capacity, disk latency, memory pressure, antivirus, boot storm |

## Maintenance mode

Maintenance mode prevents new brokered connections to the selected scope while allowing controlled administrative work. Understand whether current sessions are allowed to continue; maintenance mode is not the same as logging users off or shutting machines down.

Before maintenance:

1. communicate the user impact;
2. stop new launches at the correct scope;
3. drain, disconnect, or log off sessions according to policy;
4. verify rollback and backups;
5. perform the change;
6. validate registration and real launches;
7. remove maintenance mode;
8. monitor after the change.

## Image-change discipline

For both MCS and PVS:

- use a controlled maintenance image;
- make changes once in the authoritative image;
- test representative applications and peripherals;
- use canary machines or a test delivery group;
- retain a known-good rollback version;
- verify VDA registration after rollout;
- monitor launch failures and logon duration.

## Backup categories

Back up or otherwise protect:

- CVAD site, monitoring, and configuration-logging databases;
- StoreFront configuration;
- Gateway/NetScaler configuration and certificates;
- master images, MCS source snapshots, and image pipeline documentation;
- PVS database, vDisk files, bootstrap configuration, and store definitions;
- profile and user-data stores;
- licensing information and recovery procedures;
- infrastructure-as-code, scripts, and change records.

A backup is not proven until restoration is tested.

## Useful consoles

| Tool | Primary purpose |
|---|---|
| **Web Studio** | Configure the site, catalogs, groups, applications, policies, and hosting. |
| **Director** | Monitor users, sessions, failures, machine state, and performance. |
| **PVS Console** | Manage farms, sites, servers, stores, vDisks, versions, and targets. |
| **Citrix Cloud console** | Manage DaaS services, resource locations, and cloud-hosted control features. |
| **Windows tools** | Event Viewer, services, performance counters, Group Policy results, networking, and storage checks. |
| **Hypervisor/cloud console** | Validate VM power, host health, network, storage, and platform tasks. |

## First-response checklist

- [ ] Record the exact error and time.
- [ ] Determine scope and last known good time.
- [ ] Check service health and recent changes.
- [ ] Locate the failure in the connection flow.
- [ ] Verify entitlement and machine availability.
- [ ] Check VDA registration and maintenance state.
- [ ] Test from a known-good endpoint/user/path.
- [ ] Gather logs before rebooting.
- [ ] Apply a reversible fix and validate with a real launch.
- [ ] Document root cause and prevention.

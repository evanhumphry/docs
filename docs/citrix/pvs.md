# Citrix Provisioning (PVS)

**Citrix Provisioning**, commonly called **PVS** from its former name Provisioning Services, uses software streaming to let many computers boot from a centrally managed virtual disk (**vDisk**) image.

Instead of maintaining a complete OS installation on every target, an administrator maintains the shared image. Target devices request the disk blocks they need across the network. Runtime writes go to a separate write-cache location rather than changing a standard-mode shared image.

## Why PVS exists

PVS is designed for standardized fleets where many machines should run the same image. It can provide:

- centralized image patching and application updates;
- strong consistency among target devices;
- reduced duplicate image storage;
- rapid promotion or rollback between vDisk versions;
- support for virtual or, in supported designs, physical target devices;
- separation of the base image from machine runtime writes.

PVS does **not** replace the VDA, Delivery Controller, delivery group, user profile, or hypervisor. It supplies the machine’s disk image; CVAD brokers the user session.

## PVS hierarchy and component categories

```text
Farm
  ├─ Stores
  ├─ Farm Views (optional)
  └─ Sites
      └─ Site
          ├─ Provisioning Servers
          ├─ Device Collections
          │    └─ Target Devices
          ├─ vDisk Pool
          └─ Site Views (optional)
```

| Component | Definition | Purpose |
|---|---|---|
| **Farm** | Highest PVS administrative boundary sharing a PVS database. | Hold the overall PVS configuration. Do not confuse it with a legacy “XenApp farm.” |
| **Site** | Grouping within a farm containing PVS servers, device collections, a vDisk pool, and related settings. | Organize PVS resources, often by location or administrative boundary. |
| **PVS database** | SQL database containing PVS configuration and object metadata. | Store farm, site, server, store, vDisk, and target definitions. The vDisk payload itself is stored separately. |
| **Provisioning Server** | Server running the PVS streaming service and related services. | Authenticate target requests and stream vDisk blocks. Multiple servers provide capacity and resilience. |
| **Store** | Farm-level logical PVS object pointing to a physical location containing vDisk files. | Tell PVS servers where vDisks are stored. A store can be available to selected sites and servers. |
| **vDisk pool** | Site-level collection of vDisks available to that site. | Make store-backed vDisks available for assignment to target devices in the site. |
| **vDisk** | Virtual hard-disk image containing an OS, applications, and configuration. In a CVAD/DaaS workload it also contains the VDA. | Act as the centrally managed boot disk for one or many targets. |
| **Master target device** | Machine used to build or capture the source image. | Create and maintain the vDisk image. |
| **Target device** | Physical or virtual computer configured to boot from PVS. | Stream and run the assigned vDisk. |
| **Device collection** | Administrative grouping of target-device records. | Apply or manage settings and operations for a related set of targets. |
| **View** | Optional logical grouping of target devices independent of device collections. | Organize and operate on targets across a farm or within a site. |
| **PVS Console** | Administrative interface for PVS. | Configure the farm, vDisks, stores, servers, devices, and versions. |

## Image modes

### Private image mode

One target has direct read/write access to the base vDisk. This is useful for specific single-device image preparation or legacy maintenance workflows, but it is not the normal shared production mode and is not required for the routine versioned update workflow.

### Standard image mode

Multiple targets share the vDisk as read-only. Each target’s writes are redirected to its own write cache. Use this for production fleets requiring a common image.

!!! warning
    Never assume changes made inside one standard-mode target update the shared vDisk. Patch the maintenance image, create or update a version, test it, then promote it.

## vDisk version lifecycle

A common versioned lifecycle keeps production targets on their read-only production version while a designated maintenance target boots a new maintenance version:

1. **Maintenance:** create a new vDisk version and boot a maintenance target.
2. **Update:** install patches, applications, agents, or configuration changes.
3. **Test:** promote to test and boot test targets that are allowed to use it.
4. **Production:** promote the validated version for production targets.
5. **Rollback:** if needed, return targets to a prior known-good production version.
6. **Merge/cleanup:** consolidate or remove old versions according to policy and free-space requirements.

Version naming and promotion discipline are essential. Record the date, change ticket, installed updates, VDA version, and rollback decision.

## Boot and streaming flow

```text
Target powers on
  → obtains network and boot information
  → downloads/loads the PVS bootstrap
  → contacts a PVS server
  → PVS identifies the target and assigned vDisk
  → target streams required OS blocks
  → writes go to the configured write cache
  → OS starts and the VDA registers with CVAD/DaaS
  → broker can offer the machine to users
```

Boot mechanisms vary by environment and release. Traditional designs may use PXE with DHCP and TFTP; alternatives include a boot device manager (BDM) partition, ISO, or platform-supported boot method. PXE, DHCP, TFTP, streaming, and VDA registration are distinct phases.

## Write cache

The write cache holds changes that cannot be written to a shared standard-mode vDisk. Cache location and mode affect performance, resilience, storage use, and what survives a restart.

Common design possibilities include cache on target-device RAM with overflow to a local disk, cache on a target disk, or other modes supported by the deployed PVS release. Do not select a mode from its name alone; validate current support and sizing guidance.

For RAM cache with overflow, plan for both memory and disk consumption. A small or slow overflow disk can cause severe performance or availability problems.

Monitor:

- cache-disk free space and growth;
- memory pressure;
- IOPS and latency;
- antivirus and security-agent behavior;
- pagefile and crash-dump requirements;
- what data must persist after reboot.

## Network and availability design

PVS makes the boot and streaming paths critical. A production design should consider:

- redundant PVS servers per site;
- reliable access from every target network to PVS services;
- DHCP/PXE/TFTP or BDM dependencies;
- PVS server and target network capacity;
- vDisk-store availability and consistent access;
- SQL availability and offline database support behavior;
- load balancing and failover;
- time, DNS, Active Directory, and hypervisor dependencies;
- boot-storm capacity when many targets restart together.

Do not schedule every target to reboot simultaneously unless the PVS, network, storage, hypervisor, and authentication systems are sized for the resulting storm.

## PVS troubleshooting by phase

| Phase | Questions |
|---|---|
| Power/firmware | Did the VM or physical device start, and is network boot ordered correctly? |
| DHCP | Did the target receive the correct IP configuration? |
| Bootstrap | Did it receive or load the expected bootstrap and PVS server information? |
| PVS login | Does the farm contain the target record, and is the correct vDisk assigned? |
| Streaming | Can the target reach a healthy PVS server and vDisk store with acceptable latency? |
| Write cache | Is the cache location available, correctly sized, and writable? |
| Windows/Linux startup | Does the streamed OS complete boot without driver or image problems? |
| VDA registration | Does the VDA register after the OS starts? |
| User launch | Is the registered target allocated and entitled through a delivery group? |

## PVS operational checklist

- [ ] Keep at least one tested previous production vDisk version until the new version is stable.
- [ ] Test image updates with representative targets before production promotion.
- [ ] Confirm PVS servers see the same intended store content and version chain.
- [ ] Monitor write-cache exhaustion and boot storms.
- [ ] Verify target personality data, domain trust, and VDA registration after image changes.
- [ ] Document bootstrap method and DHCP/TFTP dependencies for each target network.
- [ ] Back up the PVS database and vDisk files with application-consistent procedures.
- [ ] Test PVS server, store, database, and network-path failure scenarios.

## Official references

- [Citrix Provisioning architecture](https://docs.citrix.com/en-us/provisioning/current-release/architecture.html)
- [Citrix Provisioning product documentation](https://docs.citrix.com/en-us/provisioning)

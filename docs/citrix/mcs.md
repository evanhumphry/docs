# Machine Creation Services (MCS)

**Machine Creation Services** is Citrix’s integrated VM-provisioning technology. MCS uses a hosting connection and a prepared master image to create and update machines in a catalog.

## Purpose

MCS reduces the need to build and patch every VM separately. The administrator maintains a master image, and Citrix creates or updates catalog machines from it through the hypervisor or cloud API.

## Core concepts

| Term | Definition |
|---|---|
| **Hosting connection** | Stored connection from CVAD or DaaS to a supported hypervisor or cloud platform. |
| **Master image / golden image** | Prepared VM containing the OS, applications, updates, VDA, and configuration used as the source. |
| **Snapshot or image version** | Stable point selected as the catalog’s source. |
| **Identity disk** | Small per-machine disk or identity mechanism used to distinguish cloned machines. |
| **Difference disk** | Per-machine disk that receives writes when a shared base image is used. |
| **Image update** | Operation that points catalog machines to a newer prepared image version, often after restart. |

Exact storage mechanics differ by platform and MCS feature set. Use the documentation for the selected hypervisor or cloud rather than assuming every platform creates identical disk objects.

## Simplified lifecycle

1. Build and patch the master VM.
2. Install applications and the correct VDA.
3. Optimize and validate the image.
4. Shut down the master cleanly when required by the platform.
5. Create a stable snapshot or image version.
6. Create or update the MCS catalog from that version.
7. Test on a small number of machines.
8. Schedule or perform the production restart/rollout.
9. Monitor registrations, launches, logons, and app behavior.
10. Retain a rollback path until the version is proven.

## Persistent and nonpersistent behavior

For pooled nonpersistent machines, changes to the machine’s write layer are typically discarded or replaced according to the catalog lifecycle. Therefore:

- install applications and machine-wide changes in the master image;
- keep user data outside the disposable OS layer;
- use an intentional profile strategy;
- do not expect a manual fix made to one pooled VM to survive or reach its peers.

Dedicated or persistent designs can retain machine changes, but that also increases configuration drift and management burden.

## How MCS differs from PVS

| Area | MCS | PVS |
|---|---|---|
| Delivery method | Clones or platform-native image/disk constructs | Streams requested disk blocks over the network from a vDisk |
| Main dependency at boot/runtime | Hypervisor/cloud storage and APIs | PVS boot path, PVS servers, network, and vDisk storage/cache design |
| Management integration | Built into CVAD/DaaS catalog workflows | Separate Citrix Provisioning infrastructure and console, integrated with CVAD |
| Common strength | Simpler integrated VM lifecycle | Single shared streamed image and rapid version promotion/rollback |
| Common design concern | Storage layout, clone/update operations, cloud costs | Boot services, streaming capacity, cache placement, network and PVS availability |

Neither is universally better. Select based on platform support, scale, operational skill, recovery needs, storage/network design, and application constraints.

## Safe image-update checklist

- [ ] Confirm recent backup or snapshot and a documented rollback point.
- [ ] Patch the image, applications, VDA, and agents in a controlled maintenance state.
- [ ] Verify services, event logs, free disk space, and security tooling.
- [ ] Test registration and a real app/desktop launch.
- [ ] Test profile load, printing, mapped resources, audio/video, and critical peripherals.
- [ ] Roll out to a canary or test delivery group first where possible.
- [ ] Communicate whether a restart will disconnect or replace machines.
- [ ] Monitor failure rate and logon duration after rollout.

## Official reference

- [Machine Creation Services](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/install-configure/machine-catalogs-create.html)

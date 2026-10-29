# Product Categories and Delivery Models

Citrix terms often describe different layers. Do not compare two terms until you know whether they describe a product, a workload, an assignment, or a provisioning method.

## Product and deployment categories

| Category | Definition | Purpose |
|---|---|---|
| **Citrix Virtual Apps and Desktops (CVAD)** | The self-managed, on-premises product. A deployment is organized as a **site**. | Deliver applications and desktops while your organization operates the controllers, databases, StoreFront, and related infrastructure. |
| **Citrix DaaS** | Citrix-hosted management and brokering services with customer-managed resource locations. | Reduce control-plane infrastructure while retaining control of workloads and data locations. |
| **Citrix Workspace app** | Endpoint client for Windows, macOS, Linux, mobile devices, thin clients, and other supported platforms. | Enumerate and launch assigned resources and provide the HDX user experience. |
| **StoreFront / Citrix Workspace** | Resource-enumeration and user-store services. | Authenticate users and show the apps and desktops they are entitled to launch. |
| **Citrix Gateway / NetScaler Gateway** | Secure access gateway, commonly placed at the network edge. | Provide TLS-secured remote access without exposing VDAs directly to the internet. |
| **Citrix Provisioning (PVS)** | Network-streaming image-management product. | Boot many target devices from a centrally managed shared vDisk image. |

## Resource categories: apps and desktops

### Published application

A published application opens only the application window even though it runs in a remote session. Use this when users need a centrally managed application without seeing an entire remote desktop.

### Published desktop

A published desktop gives the user a complete Windows or Linux desktop session. Use this when the workflow needs multiple applications, a controlled workspace, or a full remote desktop experience.

The same multi-session host can commonly publish both applications and a desktop. Entitlement and presentation are controlled through delivery groups and application settings.

## Workload operating-system categories

| Workload | What it means | Common purpose |
|---|---|---|
| **Multi-session OS** | A supported server or multi-session Windows OS hosts multiple concurrent user sessions. | High-density published apps and shared desktops. |
| **Single-session OS** | A supported desktop OS normally hosts one interactive user session at a time. | VDI desktops, stronger per-user isolation, or applications that require a desktop OS. |
| **Linux VDA** | A supported Linux machine has the Citrix Linux VDA. | Linux desktops or applications delivered through Citrix. |
| **Remote PC Access** | A physical office PC is registered as a VDA resource. | Secure remote access to an employee’s existing physical workstation. |

**Multi-session versus single-session describes session density, not provisioning.** Either category may be created and maintained with supported image or lifecycle tools.

## Desktop assignment categories

| Assignment | Definition | Best fit |
|---|---|---|
| **Random / pooled** | An eligible user receives any available machine from a pool. | Standardized, nonpersistent desktops where users do not require the same VM. |
| **Static / assigned** | A particular machine is assigned to a user, automatically or manually. | Users who need the same VM identity on future launches. |
| **Nonpersistent** | Machine changes are discarded or reset according to the image-management design. | Consistency, easier recovery, and large standardized pools. |
| **Persistent** | Machine-level changes remain between restarts. | Specialized use cases requiring machine customization. |

A persistent desktop is not the same as a persistent **user profile**. Nonpersistent machines can preserve user settings and files through profile containers, folder redirection, or other profile technology.

## Provisioning categories

| Method | How machines receive an OS | Why use it |
|---|---|---|
| **Existing / manually provisioned** | Machines already exist and are added to a catalog. | Physical PCs, externally managed VMs, or small/specialized sets. |
| **Machine Creation Services (MCS)** | Citrix creates VMs from a master image through a hypervisor or cloud connection. | Integrated, straightforward lifecycle management for many virtual environments. |
| **Citrix Provisioning (PVS)** | Target devices boot and stream blocks from a shared vDisk through PVS servers. | Centralized single-image management, rapid rollback, and large standardized workloads. |
| **Other management tools** | A third-party or native platform creates and updates the machines. | Existing enterprise deployment pipelines or unsupported MCS/PVS scenarios. |

MCS and PVS solve related image-management problems differently. [Compare them directly](mcs.md#how-mcs-differs-from-pvs).

## Administrative object categories

| Object | Defines |
|---|---|
| **Machine catalog** | What the machines are: OS/session type, provisioning method, and machine population. |
| **Delivery group** | Who can use selected catalog machines and what apps/desktops are delivered. |
| **Application group** | An optional application-centric grouping for controlling application delivery across delivery groups. |
| **Citrix policy** | How sessions behave: graphics, printing, redirection, bandwidth, security, and many other settings. |

A useful memory aid is: **catalog = machines; delivery group = users and resources; policy = behavior.**

## Common beginner mistakes

- Treating “Citrix” as the endpoint client. Workspace app is only one component.
- Assuming a published app runs locally. Its interface is displayed locally, but execution normally occurs on the VDA.
- Calling every desktop “VDI.” Multi-session published desktops and single-session VDI are different delivery models.
- Confusing machine persistence with profile persistence.
- Treating MCS or PVS as the broker. They prepare machines; the Delivery Controller brokers sessions.

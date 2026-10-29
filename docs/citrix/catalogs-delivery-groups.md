# Machine Catalogs, Delivery Groups, and Applications

These objects answer different questions:

```text
Machine catalog:  What machines exist and how were they built?
Delivery group:   Who may use selected machines, and what is delivered?
Application:      What executable is published and how does it appear?
Policy:           How should the session behave?
```

## Machine catalogs

A **machine catalog** is a collection of physical or virtual machines managed as a set. During creation, the administrator identifies the operating-system/session category, provisioning method, and machine population.

Typical catalog decisions include:

- multi-session, single-session, Remote PC Access, or supported Linux resources;
- MCS, PVS, existing machines, or another provisioning tool;
- random/pooled or static assignment where applicable;
- persistent or reset behavior determined by the provisioning design;
- hosting connection, master image, network, storage, and machine count for MCS;
- Active Directory computer-account placement and naming scheme.

A catalog does **not** by itself grant users access.

## Delivery groups

A **delivery group** contains machines selected from one or more compatible catalogs. It defines:

- which users or groups are allowed or blocked;
- how many machines are allocated from catalogs;
- whether desktops, applications, or both are delivered;
- desktop display names and assignment behavior;
- session and power-management behavior;
- which StoreFront or Workspace users can launch the resources.

Citrix’s definition is concise: a delivery group is a collection of machines from catalogs that defines the users who can access those machines and the applications and desktops available to them.

## Published applications

An application object normally includes:

- executable path and command-line arguments;
- working directory;
- display name, description, icon, and folder placement;
- delivery-group or application-group association;
- user visibility and entitlement;
- optional file-type association and limits.

Applications execute on a VDA. Workspace app displays the remote window so it can feel locally integrated.

## Application groups

An **application group** is an optional, application-centered layer that can associate applications, users, and delivery groups. It is useful when application entitlement does not align cleanly with desktop delivery-group boundaries.

Do not add complexity without a reason. For a small deployment, direct delivery-group application assignment may be easier to understand.

## Example design

A company needs a shared office desktop for all staff and a finance application for the finance team.

1. Create a **multi-session catalog** containing standardized Windows session hosts.
2. Create a **Staff Shared Desktop delivery group** and allocate machines from the catalog.
3. Entitle the staff directory group to the published desktop.
4. Publish the finance executable from compatible hosts.
5. Entitle only the finance directory group to the application, directly or through an application group.
6. Use Citrix policies to control printing, drive mapping, graphics, and other session behavior.

## Object hierarchy checklist

When a resource does not appear or launch, check in this order:

1. Is the VDA machine present in the expected catalog?
2. Is the machine allocated to the expected delivery group?
3. Is the machine registered, powered on, and not in maintenance mode?
4. Is the desktop or app published from that delivery group?
5. Is the user included in the allow scope and absent from a block scope?
6. Are application-group restrictions narrowing access?
7. Is StoreFront or Workspace connected to the correct site or resource location?
8. Does policy permit the expected behavior?

## Official references

- [Create machine catalogs](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/install-configure/machine-catalogs-create.html)
- [Create delivery groups](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/install-configure/delivery-groups-create.html)
- [Create and manage applications](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/install-configure/delivery-groups-manage-applications.html)

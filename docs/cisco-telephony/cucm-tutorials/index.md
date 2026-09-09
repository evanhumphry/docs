# CUCM Configuration Tutorials

These tutorials cover common Cisco Unified Communications Manager administration tasks using the web interface. They are written as repeatable lab procedures with prerequisites, configuration steps, verification, rollback, and common mistakes.

!!! warning "Match the tutorial to your CUCM release"
    Menu names, field labels, defaults, and available features vary by CUCM release and installed options. Use the field-level Help link and the administration guide for the deployed release. Perform tutorials in a lab or approved change window before applying them to production.

## Tutorial Lab

Examples use fictional values:

| Item | Example |
|---|---|
| CUCM publisher | `cucm-pub.example.test` |
| CUCM subscriber | `cucm-sub1.example.test` |
| IOS XE gateway | `192.0.2.11` |
| SIP peer | `192.0.2.40` |
| Internal partition | `PT-INTERNAL` |
| PSTN partition | `PT-PSTN-LOCAL` |
| Phone CSS | `CSS-PHONE-LOCAL` |
| Device pool | `DP-HQ` |
| Route group | `RG-HQ-PSTN` |
| Route list | `RL-HQ-PSTN` |
| Test extension | `6985` |

Do not use example passwords, production numbers, or real carrier credentials.

## Standard Change Workflow

Apply this sequence to every CUCM tutorial:

1. **Document the current state:** Export or record the existing object, dependencies, and affected devices.
2. **Define the expected call flow:** State the calling number, called number, CSS, partition, route, gateway or trunk, and media path.
3. **Create dependencies first:** Build objects from the bottom of the dependency chain upward.
4. **Save configuration:** Use **Save**, then apply **Reset**, **Restart**, or **Apply Config** only when the page and change require it.
5. **Test narrowly:** Use a dedicated test device and number.
6. **Verify end to end:** Confirm signaling, route selection, audio, DTMF, caller ID, and clearing.
7. **Check unrelated access:** Make sure the change did not grant or block other number classes.
8. **Record rollback:** Know which object or assignment to restore.

!!! caution "Reset and service impact"
    CUCM pages can offer Reset or Restart operations that interrupt active calls or device registration. Read the confirmation text, identify the affected devices, and schedule disruptive operations appropriately.

## Tutorials

### Endpoints and Calling Privileges

1. [Configure a Phone, Directory Number, and User](phones-lines-users.md)
2. [Configure Partitions and Calling Search Spaces](partitions-css.md)
3. [Configure Device Pools, Regions, and Locations](site-policy.md)

### PSTN and Gateway Routing

4. [Configure a SIP Trunk](sip-trunk.md)
5. [Configure Route Groups, Route Lists, and Route Patterns](pstn-routing.md)
6. [Configure H.323 and MGCP Gateways](gateways.md)
7. [Configure Number Transformations](number-transformations.md)

### Call Distribution and Media

8. [Configure a Line Group and Hunt Pilot](hunt-groups.md)
9. [Configure Media Resource Groups and Lists](media-resources.md)

### Validation

10. [Verify and Troubleshoot CUCM Configuration](verification.md)

## Object Dependency Map

```text
Phone
  +--> Directory Number
  +--> Device Pool
  +--> Calling Search Space
  +--> Media Resource Group List

Dialed PSTN number
  -> Route Pattern
  -> Route List
  -> Route Group
  -> SIP Trunk or Gateway

Hunt Pilot
  -> Hunt List
  -> Line Group
  -> Directory Numbers
```

Build lower-level objects before objects that reference them. Remove them in reverse order after confirming they are no longer used.

## Verification Record

For every tutorial, capture:

| Field | Result |
|---|---|
| Change or lab identifier |  |
| CUCM release |  |
| Node used for administration |  |
| Objects created or changed |  |
| Calling and called numbers |  |
| Expected route |  |
| Actual route |  |
| Audio and DTMF |  |
| Caller ID |  |
| Failover result |  |
| Rollback tested |  |

Use [CUCM Diagnostics and Tracing](../cucm-diagnostics.md) when the GUI configuration appears correct but behavior differs.

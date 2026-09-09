# SRST and Site Survivability

Survivable Remote Site Telephony (SRST) lets supported Cisco gateways provide limited local call control when a branch cannot reach its normal CUCM subscribers. Survivability is an operating mode with reduced features, not a full duplicate of the CUCM cluster.

## Failure Model

```text
Normal operation
Phones -> WAN -> CUCM
   |
   +-> Local gateway -> PSTN

WAN or CUCM outage
Phones -X-> CUCM
   |
   v
Register to local SRST gateway
   |
   v
Local calling and PSTN routes
```

The exact behavior depends on phone protocol, gateway platform, IOS XE release, licenses, certificates, dial plan, and configured SRST mode.

## Decide What Must Survive

Document minimum branch service:

- internal calls within the site;
- inbound and outbound PSTN calls;
- emergency calling;
- reception and published numbers;
- voicemail access or alternate handling;
- analog phones, fax, paging, alarms, and elevators;
- hunt groups or basic call coverage;
- caller ID and callback number;
- DTMF, transfer, hold, and conference expectations;
- management and monitoring during WAN loss.

Features that depend on centralized applications may not work or may behave differently during SRST.

## SCCP and SIP Survivability

Legacy SCCP and modern SIP phone deployments use different SRST configuration models. Verify support for:

- phone models and firmware;
- SCCP, SIP, or mixed registration;
- secure device profiles and certificates;
- directory-number and phone capacity;
- feature support in fallback;
- authentication and trust;
- return to CUCM after recovery.

Do not copy a `call-manager-fallback` or `voice register` template from another release without checking local CLI help and Cisco documentation.

## Address and Certificate Planning

Phones must discover or be told which SRST reference to use. Confirm:

- the SRST address is reachable from every phone VLAN;
- DHCP, TFTP, and CUCM configuration identify the intended reference;
- routing and firewall policy permit registration and media;
- the address remains available during the failure being tested;
- secure phones trust the gateway identity and certificates;
- DNS and time synchronization remain available if required.

A loopback can provide a stable identity, but routing must preserve reachability during WAN and upstream failures.

## Fallback Dial Plan

Build a compact local dial plan that covers only required fallback behavior:

```text
Registered branch phone
    |
    +--> local extension
    +--> local PSTN gateway or trunk
    +--> emergency route
    +--> approved service destinations
```

Define:

- extension and public-number mapping;
- PSTN access code behavior;
- calling-number presentation;
- inbound DID or analog PLAR handling;
- emergency callback and location;
- blocked number classes;
- primary and backup local trunks;
- digit transformations that differ from normal CUCM operation.

Keep SRST patterns explicit to reduce accidental toll access.

## Capacity Planning

Validate:

- maximum registered phones and directory numbers;
- simultaneous calls;
- DSP and PVDM capacity;
- analog or digital port capacity;
- SIP trunk or carrier limits;
- transcoding, conferencing, MTP, and fax needs;
- power and environmental resilience;
- WAN failure plus a local trunk or gateway failure.

Size for the tested platform and release, not a generic family maximum.

## Controlled SRST Test

!!! warning "Treat failure testing as a change"
    Isolating phones from CUCM can interrupt active calls and applications. Use an approved maintenance window, a limited pilot group when possible, and a tested restoration plan.

### Pretest

- [ ] Record normal registration and call behavior.
- [ ] Confirm the exact phones and numbers in scope.
- [ ] Verify gateway capacity, licenses, routes, and trunks.
- [ ] Confirm emergency-test procedures.
- [ ] Define how CUCM reachability will be interrupted and restored.
- [ ] Prepare console or out-of-band access.
- [ ] Notify users and monitoring teams.

### During Failure

- [ ] Phones detect loss of CUCM and register to the expected gateway.
- [ ] Display and feature state clearly indicate fallback where applicable.
- [ ] Local extension calls work.
- [ ] Outbound PSTN calls use the expected local route.
- [ ] Inbound calls reach required branch destinations.
- [ ] Calling number and caller ID are correct.
- [ ] Audio is bidirectional and DTMF works.
- [ ] Required analog services work.
- [ ] Emergency calling is tested only through the approved process.
- [ ] Unauthorized destinations remain blocked.

### Recovery

- [ ] Restore CUCM reachability.
- [ ] Phones return to the expected CUCM node.
- [ ] Active fallback calls behave as designed.
- [ ] Normal route patterns, voicemail, applications, and features return.
- [ ] No phone or port remains registered to the wrong controller.
- [ ] Alarms clear and monitoring reflects recovery.

## Common Failure Scenarios

### Phones Never Enter SRST

Check SRST reference configuration, reachability, DNS, DHCP or TFTP information, protocol mode, certificate trust, firewall policy, and gateway capacity.

### Phones Register but Cannot Call the PSTN

Check fallback dial peers, number format, CSS-like local authorization logic, trunk availability, calling-number translation, and carrier acceptance.

### Inbound Calls Fail During WAN Loss

Confirm where the carrier sends the call, whether the local trunk remains active, how the gateway maps inbound numbers, and whether the destination is registered locally.

### Phones Do Not Return to CUCM

Check restored routing, DNS, CUCM service and node state, certificate trust, phone timers, and whether the gateway still appears preferable or reachable when it should not.

## Operational Evidence

Capture:

- phone registration before, during, and after failure;
- gateway registration counts and call state using release-appropriate commands;
- dial-peer and route selection;
- calling and called numbers;
- trunk and voice-port state;
- CUCM alarms and registration state;
- timestamps for detection, fallback, and recovery.

Continue with [Emergency Calling](emergency-calling.md), [High Availability](high-availability.md), and [Operational Checklists](operational-checklists.md).

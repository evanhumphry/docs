# Cisco Voice Migration Guides

A voice migration must preserve signaling, media, emergency calling, analog behavior, number presentation, and operational support. Treat configuration conversion as one part of the project, not the project itself.

## Universal Migration Workflow

### 1. Discover

- [ ] Record source and target hardware models, modules, PVDMs or DSPs, licenses, and software releases.
- [ ] Export sanitized running and startup configurations.
- [ ] Inventory every analog and digital circuit, port, cable, patch-panel position, and carrier identifier.
- [ ] Map each CUCM gateway, trunk, route group, route list, route pattern, CSS, partition, device pool, location, region, and MRGL dependency.
- [ ] Capture active dial peers, translation rules, profiles, trunk groups, PLAR destinations, codecs, DTMF methods, bindings, and hunt behavior.
- [ ] Record normal calling and called-number formats at each call leg.
- [ ] Verify emergency-service callback number and location behavior using approved procedures.
- [ ] Establish a baseline test matrix and collect successful call evidence.

### 2. Validate the Target Design

- [ ] Confirm the exact target platform and IOS XE release support every required voice feature.
- [ ] Confirm voice NIM, analog or digital interface, PVDM, DSP, and transceiver compatibility.
- [ ] Size DSP capacity for normal load, failover, transcoding, conferencing, and codec use.
- [ ] Confirm protocol support and whether CUBE or another license is required.
- [ ] Validate management, signaling, and RTP routing in both directions.
- [ ] Confirm QoS, firewall, NAT, DNS, NTP, certificates, and trust requirements.
- [ ] Lab-test representative inbound, outbound, transfer, conference, voicemail, IVR, fax, paging, modem, and failure scenarios.

### 3. Prepare Cutover and Rollback

- [ ] Define a maintenance window, owners, escalation contacts, carrier contacts, and decision authority.
- [ ] Create port-by-port cable and configuration maps.
- [ ] Prestage reviewed target configuration without secrets in shared documentation.
- [ ] Back up both devices and CUCM configuration using approved tools.
- [ ] Define measurable success criteria and a rollback deadline.
- [ ] Preserve the old gateway, cables, modules, and configuration until acceptance is complete.
- [ ] Prepare a tested rollback procedure that restores routing and physical connections.

### 4. Cut Over

- [ ] Capture a final pre-change baseline and confirm no unrelated incident is active.
- [ ] Move circuits according to the port map and verify physical state after each group.
- [ ] Activate CUCM, gateway, routing, firewall, and carrier changes in the planned order.
- [ ] Place controlled test calls after each logical stage instead of waiting until the end.
- [ ] Record actual call legs, selected dial peers, ports, codecs, media addresses, DTMF, caller ID, and disconnect behavior.

### 5. Validate and Close

- [ ] Test inbound and outbound calls for every number class and circuit group.
- [ ] Test emergency calling only through the approved process.
- [ ] Test transfer, hold, resume, conference, voicemail, IVR DTMF, fax, paging, and failover as applicable.
- [ ] Confirm bidirectional audio and expected codec.
- [ ] Confirm caller name or number presentation, ANI, DNIS, and digit transformations.
- [ ] Confirm call teardown and analog disconnect supervision.
- [ ] Monitor logs, DSP use, trunk capacity, registration, and call failures through the acceptance period.
- [ ] Update diagrams, port maps, inventory, CUCM records, and operating procedures.

## ISR to Catalyst 8200L

Do not treat an 8200L as a drop-in configuration replacement for an older ISR.

### Prechecks

1. Compare supported voice modules and slot compatibility.
2. Confirm required analog or digital interfaces are available and supported.
3. Confirm PVDM placement and DSP capacity.
4. Compare IOS or IOS XE voice feature support, especially H.323, MGCP, CUBE, SRST, fax, modem, and legacy signaling.
5. Review boot mode, configuration syntax, licensing, Smart Licensing policy, and crypto support.
6. Verify interface names and voice-port numbering on the actual target hardware.
7. Confirm source-address binding, routing, VRFs, QoS, NAT, firewall, and high-availability behavior.
8. Rebuild the intended behavior rather than copying unsupported or obsolete lines.

### Recommended Approach

- Convert the old configuration into a behavior matrix: input, match, transformation, output, media policy, and fallback.
- Build a clean target configuration using commands supported on the chosen release.
- Validate each behavior in a lab.
- Use documentation IP addresses in public examples and inject production addresses only through the controlled implementation record.
- Keep a protocol migration separate from a hardware migration when risk or troubleshooting complexity is high.

## H.323 to SIP

H.323 is important for supporting legacy environments, but SIP is generally the preferred direction for a new interconnection when the design and platform support it.

### Compare Before Converting

| H.323 consideration | SIP equivalent to validate |
|---|---|
| H.225 call setup | SIP request and response routing |
| H.245 capabilities and channels | SDP offer and answer |
| H.323 source-address binding | SIP control and media source binding |
| H.245 DTMF methods | RTP-NTE or agreed SIP method |
| Fast-start or slow-start | Early-offer or delayed-offer behavior |
| H.323 gateway object | SIP trunk and security or profile objects |
| Dial peers and session targets | SIP inbound and outbound dial peers, targets, or server groups |

### Migration Checklist

- [ ] Capture working H.323 call flows, numbers, codecs, DTMF, and supplementary services.
- [ ] Build the CUCM SIP trunk, SIP profile, security profile, route-group membership, and destination settings.
- [ ] Build explicit SIP dial peers and matching rules on IOS XE.
- [ ] Validate SIP source addresses, OPTIONS or status monitoring, DNS, TLS, certificates, and CUBE requirements.
- [ ] Compare number presentation and transformation at every stage.
- [ ] Test SDP addresses, ports, codecs, early-offer behavior, DTMF, transfer, redirect, and media resources.
- [ ] Keep a rollback route to the working H.323 path until SIP acceptance is complete.

## VG224 to VG310

A VG224-to-VG310 migration is primarily an analog endpoint and CUCM control migration. Port density, numbering, registration, SCCP or MGCP behavior, cabling, power, and analog feature requirements must be mapped explicitly.

### Port-by-Port Worksheet

| Old port | New port | Endpoint | Extension | Protocol | Caller ID | PLAR | Fax/modem/paging | Test result |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

### Key Checks

- Verify supported signaling protocol and CUCM compatibility.
- Map physical connectors and patch-panel positions before moving cables.
- Preserve endpoint-specific impedance, gain, fax, modem, paging, and caller-ID requirements.
- Confirm CUCM device, port, DN, partition, CSS, device pool, location, region, and MRGL assignments.
- Test off-hook dial tone, inbound ring, outbound dialing, caller ID, DTMF, transfer, and disconnect for each endpoint class.
- Check power, grounding, environmental, and rack requirements from the hardware installation guide.

## Analog Port Migration

Analog circuits are physical services. Configuration parity does not prove electrical or supervisory parity.

For every port:

- identify whether the router side must be FXS or FXO;
- identify who supplies battery, dial tone, and ringing;
- record signaling type and country-specific settings;
- document caller-ID format and timing;
- record PLAR destination and trunk-group membership;
- test on-hook, off-hook, answer, caller-first disconnect, called-party-first disconnect, and no-answer behavior;
- test fax, modem, paging, alarm, elevator, or other special devices with their owner;
- label both cable ends and update the port map.

## Test Matrix

| Direction or feature | Primary path | Backup path | Numbers verified | Signaling | Audio | DTMF | Caller ID | Disconnect |
|---|---|---|---|---|---|---|---|---|
| Internal to PSTN local |  |  |  |  |  |  |  |  |
| Internal to PSTN long distance |  |  |  |  |  |  |  |  |
| PSTN to published number |  |  |  |  |  |  |  |  |
| CUCM failover |  |  |  |  |  |  |  |  |
| Trunk or port failover |  |  |  |  |  |  |  |  |
| Voicemail or IVR |  |  |  |  |  |  |  |  |
| Fax, modem, or paging |  |  |  |  |  |  |  |  |

Use [Troubleshooting and Commands](troubleshooting.md) to collect comparable evidence before and after the cutover.

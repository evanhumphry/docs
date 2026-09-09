# Cisco Voice Operational Checklists

These checklists are starting points for change plans and runbooks. Adapt them to the exact CUCM release, IOS XE platform, carrier, security policy, and life-safety requirements.

## New Voice Gateway Deployment

### Discovery and Design

- [ ] Exact router PID, modules, PVDMs, licenses, and IOS XE release are documented.
- [ ] Cisco Feature Navigator and platform documentation confirm required features.
- [ ] Management, signaling, and media addresses and VRFs are assigned.
- [ ] Routing, DNS, NTP, QoS, firewall, NAT, and certificate dependencies are documented.
- [ ] CUCM gateway or trunk, device pool, region, location, CSS, and MRGL are designed.
- [ ] Inbound and outbound dial peers and number formats are documented.
- [ ] Analog or digital ports, trunk groups, PLAR, caller ID, and supervision are mapped.
- [ ] DSP capacity covers normal, failure, and growth load.
- [ ] Emergency calling and callback location are approved.
- [ ] Security review covers management access, signaling peers, destinations, TLS, SRTP, and toll fraud.

### Build and Turn-Up

- [ ] Baseline configuration and out-of-band access are available.
- [ ] Interface, routing, DNS, NTP, logging, and monitoring are verified.
- [ ] CUCM or SIP peer sees the intended source identity.
- [ ] Explicit inbound dial peers match only approved sources.
- [ ] Outbound peers allow only approved destinations.
- [ ] Calling and called-number transformations pass test cases.
- [ ] Codecs, DTMF, early media, hold, transfer, fax, and media resources are tested.
- [ ] RTP is bidirectional and marked according to QoS policy.
- [ ] Primary and backup paths are tested through failure and recovery.
- [ ] Configuration is saved and backed up according to policy.

## SIP Trunk or Carrier Turn-Up

- [ ] Carrier demarcation, contacts, maintenance window, and escalation path are confirmed.
- [ ] Signaling addresses, ports, transport, DNS, and authentication are documented.
- [ ] TLS certificates, names, trust chain, and renewal ownership are verified.
- [ ] Inbound and outbound number formats are agreed.
- [ ] Calling identity and privacy requirements are agreed.
- [ ] SDP, codecs, packetization, DTMF, fax, and early-offer behavior are agreed.
- [ ] Concurrent-call limits and rate limits are documented.
- [ ] OPTIONS or peer monitoring is tested.
- [ ] Firewall and NAT policy permits signaling and negotiated media in both directions.
- [ ] Local, national, international, emergency, toll-free, service, and blocked classes are tested as authorized.
- [ ] Redirect, transfer, hold, early media, voicemail, and contact-center calls are tested.
- [ ] Primary and secondary carrier paths present equivalent callback identity and emergency location.

## Analog Port Activation

- [ ] Device owner and business purpose are recorded.
- [ ] FXS or FXO side is correctly identified.
- [ ] Cable and patch-panel positions are labeled.
- [ ] Port number is discovered on the actual gateway.
- [ ] Country, signaling, impedance, and supervision requirements are documented.
- [ ] Extension, DID, caller ID, PLAR, and trunk-group membership are correct.
- [ ] On-hook, off-hook, ring, answer, and both disconnect directions are tested.
- [ ] Calling and called-number presentation is correct.
- [ ] Audio level, echo, noise, and clipping are acceptable.
- [ ] Fax, modem, paging, alarm, or elevator function is tested by the owner.
- [ ] Repeated calls prove that the port releases and returns to service.
- [ ] Monitoring, spares, and rollback are documented.

## Pre-Cutover Checklist

- [ ] Approved change, implementation plan, and rollback plan are attached.
- [ ] Backups of CUCM and gateway configuration are current.
- [ ] Port, cable, number, and circuit maps are complete.
- [ ] Baseline calls and show-command output are captured.
- [ ] Test numbers and authorized testers are scheduled.
- [ ] Carrier, facilities, safety, security, application, and help-desk contacts are available.
- [ ] Required licenses, certificates, modules, optics, cables, and spares are present.
- [ ] Monitoring is adjusted to distinguish planned alarms.
- [ ] Out-of-band access is verified.
- [ ] Go/no-go criteria and rollback deadline are stated.
- [ ] Emergency-call test procedure is approved.

## Post-Cutover Checklist

- [ ] Device, trunk, gateway, and media-resource registration is healthy.
- [ ] Inbound and outbound calls work for every required number class.
- [ ] Calling and called-number transformations are correct.
- [ ] Bidirectional audio, DTMF, hold, transfer, conference, and voicemail work.
- [ ] Fax, paging, modem, alarm, and other special devices pass owner testing.
- [ ] Emergency location, callback, and notification pass approved validation.
- [ ] Primary and backup routes are tested.
- [ ] Voice ports release correctly after calls.
- [ ] DSP, call, interface, and queue utilization are within limits.
- [ ] Logs contain no unexplained errors or repeated call failures.
- [ ] Configuration, diagrams, inventory, port maps, and runbooks are updated.
- [ ] Acceptance owner approves closure before rollback resources are removed.

## Voice Incident Evidence

- [ ] Business impact, start time, scope, and recent changes are recorded.
- [ ] Calling number, called number, direction, timestamp, and timezone are captured.
- [ ] Expected and actual call paths are drawn.
- [ ] CUCM pattern, partition, CSS, route list, route group, gateway, and trunk are identified.
- [ ] IOS inbound and outbound dial peers are identified.
- [ ] Calling and called numbers are recorded at each boundary.
- [ ] SIP response or disconnect cause and its origin are identified.
- [ ] RTP addresses, ports, codec, DTMF, and each media direction are checked.
- [ ] Voice-port, trunk, DSP, registration, and peer state are captured.
- [ ] A narrow trace or packet capture is collected when necessary.
- [ ] All evidence is sanitized before sharing.
- [ ] Temporary debugs are disabled with `undebug all` and verified off.

## Emergency-Call Test

- [ ] Test is approved by the emergency-calling program owner.
- [ ] Carrier, PSAP, security desk, or other parties are notified as required.
- [ ] Endpoint, location, expected callback number, and route are recorded.
- [ ] Approved test number or procedure is used.
- [ ] Reported location is correct.
- [ ] Callback reaches the intended endpoint or response process.
- [ ] On-site notification reaches the correct personnel.
- [ ] Audio is bidirectional.
- [ ] Primary, backup, and SRST paths are tested as authorized.
- [ ] Incorrect results are escalated immediately.
- [ ] Evidence and correction records are retained according to policy.

## Certificate Renewal

- [ ] Certificate owner, expiration date, and renewal lead time are recorded.
- [ ] Subject and Subject Alternative Names match every peer identity used.
- [ ] Root and intermediate trust chains are valid on both sides.
- [ ] NTP and clock health are confirmed.
- [ ] Key and certificate algorithms are supported by every peer.
- [ ] New certificates are staged and validated before expiration.
- [ ] Private keys are protected and never placed in tickets or public notes.
- [ ] Primary and standby nodes receive the required certificate and trust updates.
- [ ] SIP TLS, HTTPS management, and SRTP dependencies are tested.
- [ ] Rollback certificate and procedure are available.
- [ ] Monitoring confirms the new expiration date.

## IOS XE Upgrade Readiness

- [ ] Target release supports the exact router PID, modules, PVDMs, and licenses.
- [ ] Release notes, caveats, field notices, and security advisories are reviewed.
- [ ] H.323, SIP, MGCP, SRST, CUBE, fax, DSP, and analog features are checked.
- [ ] Configuration syntax changes and removed commands are identified.
- [ ] ROMMON, firmware, memory, storage, and boot requirements are satisfied.
- [ ] Current image, configuration, licenses, certificates, and boot variables are backed up.
- [ ] Lab or representative testing covers required call flows.
- [ ] HA upgrade order and reduced-capacity window are planned.
- [ ] Out-of-band access and rollback image are verified.
- [ ] Post-upgrade tests cover registration, routes, media, DTMF, fax, emergency, and failover.
- [ ] Monitoring and logs remain healthy after the observation window.

## Monthly Voice-Gateway Review

- [ ] Configuration backups are current and restorable.
- [ ] No unexpected dial peers, translations, trusted addresses, or management users exist.
- [ ] Certificates and licenses have sufficient remaining life.
- [ ] Voice ports, trunks, SIP peers, and media resources are healthy.
- [ ] DSP, call, interface, and QoS utilization trends are reviewed.
- [ ] Repeated SIP failures, scans, blocked calls, and unusual destinations are investigated.
- [ ] NTP, DNS, logging, monitoring, and alert delivery work.
- [ ] Emergency routes and location records have not drifted after moves and changes.
- [ ] Documentation matches current ports, circuits, addresses, and software.
- [ ] Deferred defects and end-of-support milestones have owners.

Use [Troubleshooting Labs](troubleshooting-labs.md) for practice and [Migration Guides](migrations.md) for larger changes.

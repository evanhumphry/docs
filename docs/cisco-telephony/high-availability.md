# Voice High Availability and Failover

High availability is the ability to continue required service through defined failures. Two configured destinations do not guarantee timely detection, correct rerouting, equivalent media, or safe recovery.

## Define the Failure Domains

List failures the design must tolerate:

- CUCM subscriber loss;
- publisher or database-service loss;
- WAN or site isolation;
- CUBE or gateway loss;
- voice-module or DSP loss;
- SIP carrier peer or circuit loss;
- DNS failure;
- certificate expiration;
- firewall or routing failure;
- analog line busy or failed;
- power or environmental failure;
- maintenance and software upgrade.

For each, define detection time, retained calls, new-call behavior, reduced features, recovery time, and operational owner.

## Layered Call Path

```text
Phone
  |
  +--> CUCM subscriber group
           |
           +--> Route list and route groups
                    |
                    +--> CUBE or gateway pair
                              |
                              +--> SIP carrier peers
                                        |
                                        +--> PSTN
```

Every layer can fail independently. A backup carrier does not help if CUCM cannot reach the backup CUBE, and a backup CUBE does not help if DNS or certificates make its trunk unavailable.

## CUCM Redundancy

Validate:

- CUCM group order in device pools;
- phone and trunk failover behavior;
- TFTP and configuration availability;
- database-dependent feature behavior;
- media-resource registration across nodes;
- CTI and application redundancy;
- recovery and rehome behavior;
- alarm and monitoring ownership.

Do not test only administrative status. Exercise a call before, during, and after node failure.

## Route Lists and Route Groups

CUCM route lists and route groups can provide ordered or distributed path selection.

```text
Route Pattern
    |
    v
Route List
    +--> Primary Route Group
    +--> Secondary Route Group
```

Test:

- member unavailable before the call;
- timeout or failure during setup;
- busy or capacity exhaustion;
- cause codes that do and do not trigger another route;
- calling and called transformations on each route-list detail;
- equivalent emergency and caller-ID behavior;
- route restoration after recovery.

A backup path can create billing, location, or regulatory problems if it presents different numbers.

## IOS XE Dial-Peer Redundancy

Multiple outbound dial peers can use preference and hunt behavior:

```ios
dial-peer voice 2000 voip
 destination-pattern [1-8]...
 session target ipv4:192.0.2.20
 preference 1
!
dial-peer voice 2001 voip
 destination-pattern [1-8]...
 session target ipv4:192.0.2.21
 preference 2
```

Lower preference is favored among equivalent matches. Actual fallback depends on peer state, protocol status, hunt configuration, response or disconnect cause, and release behavior.

Use SIP OPTIONS or supported keepalive mechanisms where appropriate so a failed peer can be removed before user calls reach it. Test both failure and recovery.

## SIP Server Groups

A supported SIP server group can place multiple targets behind one dial peer. This simplifies configuration but still requires decisions about:

- preference or load distribution;
- availability monitoring;
- DNS versus static addresses;
- transport and TLS identity;
- source binding;
- retry timing;
- carrier acceptance of each source;
- in-progress call survival;
- return to the preferred server.

## CUBE Redundancy

CUBE redundancy can range from independent gateways selected by CUCM or DNS to supported box-to-box high-availability designs.

Validate the exact architecture for:

- configuration synchronization;
- signaling and media addresses;
- active and standby state;
- stateful or stateless call behavior;
- interface and routing dependencies;
- licenses and platform scale;
- certificate identity and private-key handling;
- media anchoring and NAT;
- upgrade sequence;
- split-brain prevention;
- monitoring and manual failback.

Do not describe a design as stateful unless an active call is proven to survive the defined failure.

## Analog Trunk Groups

Multiple FXO ports can provide local analog path redundancy:

```text
POTS dial peer -> trunk group
                    +--> FXO line 1
                    +--> FXO line 2
```

Check that each line has equivalent:

- dialing permissions;
- carrier service;
- caller-ID presentation;
- emergency location and callback identity;
- disconnect supervision;
- inbound number handling;
- physical labeling and monitoring.

A trunk group adds line selection, not geographic or carrier diversity unless the circuits actually provide it.

## SRST

SRST covers a different failure domain: phones lose centralized CUCM but can register to a local gateway for reduced service. Combine it with local trunks, fallback dial peers, capacity, and emergency policy.

See [SRST and Site Survivability](srst.md).

## DNS and Certificates

High availability can fail because shared dependencies fail:

- DNS name does not resolve from all nodes;
- DNS returns an unreachable target;
- certificate does not contain the name used by the peer;
- one gateway lacks the trusted intermediate certificate;
- certificate renewal occurs on only one node;
- clock drift makes a valid certificate appear invalid;
- firewall rules permit only the primary address.

Monitor shared dependencies as part of the voice service.

## Failure Test Matrix

| Failure | Detection method | Expected new calls | Expected active calls | Recovery behavior | Result |
|---|---|---|---|---|---|
| CUCM subscriber |  |  |  |  |  |
| Primary gateway |  |  |  |  |  |
| Primary carrier peer |  |  |  |  |  |
| WAN isolation |  |  |  |  |  |
| DSP exhaustion |  |  |  |  |  |
| Analog line busy |  |  |  |  |  |
| DNS failure |  |  |  |  |  |
| Certificate failure |  |  |  |  |  |
| Firewall path failure |  |  |  |  |  |

## Controlled Failure Test

1. Capture a normal call and service baseline.
2. Announce the test and establish out-of-band management.
3. Fail one dependency at a time.
4. Record detection time and alarms.
5. Place approved calls through every required number class.
6. Verify signaling, audio, DTMF, caller ID, emergency policy, and applications.
7. Restore the dependency.
8. Record recovery and failback time.
9. Confirm no stale registrations, dial peers, sessions, or routes remain.
10. Update the design with observed behavior.

## Availability Checklist

- [ ] Required failure domains and service levels are documented.
- [ ] Backup paths are independent enough for the intended failure.
- [ ] Peer-health detection is faster than the accepted call-failure window.
- [ ] Every backup path has equivalent number transformations and security.
- [ ] RTP, QoS, firewall, NAT, and routing work on backup paths.
- [ ] Emergency location and callback remain correct.
- [ ] Capacity is sufficient during failover.
- [ ] Certificates, DNS, NTP, licensing, and monitoring are redundant.
- [ ] Failover and failback are tested, not assumed.
- [ ] Operations has a manual recovery and rollback procedure.

Continue with [SIP and CUBE](sip-cube.md), [SRST](srst.md), and [Operational Checklists](operational-checklists.md).

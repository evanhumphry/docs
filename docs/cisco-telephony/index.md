# Cisco Telephony

A practical operational reference for Cisco Unified Communications Manager (CUCM) and Cisco IOS or IOS XE voice gateways. It is written for administrators who already understand IP networking and Cisco IOS, but need to trace calls, interpret voice configurations, troubleshoot failures, and plan safe migrations.

!!! warning "Verify platform and release support"
    Voice features, commands, interface numbering, and supported signaling protocols vary by router model, installed NIMs or service modules, licenses, DSP resources, and IOS XE release. Check the exact platform and software release before building a design or migration plan. In particular, treat H.323 as legacy technology and do not assume that a Catalyst 8200L release supports every command used on an older ISR.

## Start Here

Learn these four topics first:

1. [Telephony Fundamentals](fundamentals.md): signaling, media, numbers, trunks, stations, and call legs.
2. [Analog Voice Ports](analog-ports.md): FXS, FXO, trunk groups, and PLAR.
3. [Dial Peers and Digit Manipulation](dial-peers.md): inbound and outbound matching, POTS and VoIP call legs, and number transformations.
4. [CUCM Call Routing](cucm-routing.md): route patterns, route lists, route groups, partitions, and calling search spaces.

Once those concepts are familiar, use the protocol, call-flow, troubleshooting, and migration pages as operational references.

## Advanced Operations Path

After the four core topics, build operational depth in this order:

1. [SIP and CUBE Operations](sip-cube.md): SIP messages, SDP, peer health, normalization, TLS, SRTP, and toll-fraud controls.
2. [Voice QoS and Call Quality](qos-quality.md): classification, marking, LLQ, shaping, jitter, loss, and evidence collection.
3. [CUCM Diagnostics and Tracing](cucm-diagnostics.md): Dialed Number Analyzer, RTMT, SDL/SDI traces, CDR, and CMR.
4. [Dial-Plan Design](dial-plan-design.md): E.164 normalization, CSS and partitions, transformations, overlap, and Local Route Groups.
5. [Packet-Capture Walkthroughs](packet-captures.md): SIP, SDP, RTP, H.323, MGCP, DTMF, and one-way-audio analysis.
6. [Troubleshooting Labs](troubleshooting-labs.md): Twelve guided scenarios with concealed reasoning sections.

Then cover [SRST](srst.md), [Emergency Calling](emergency-calling.md), [DSP Capacity](dsp-capacity.md), [Fax and Special Analog Devices](fax-special-devices.md), [High Availability](high-availability.md), [Webex Calling and Local Gateway](webex-local-gateway.md), and [Monitoring and Automation](monitoring-automation.md).

## CUCM Configuration Tutorials

Use the step-by-step [CUCM Configuration Tutorials](cucm-tutorials/index.md) to build and verify:

- phones, directory numbers, and end-user associations;
- partitions and Calling Search Spaces;
- device pools, regions, locations, CUCM groups, SRST references, and MRGL inheritance;
- SIP trunks and security profiles;
- route groups, route lists, and route patterns;
- H.323 and MGCP gateways;
- calling and called-number transformations;
- line groups, hunt lists, and hunt pilots;
- Media Resource Groups and Lists;
- post-change verification, traces, negative testing, and rollback.

Each tutorial includes prerequisites, menu paths, configuration steps, verification, common mistakes, and rollback.

## The Complete Call Path

```text
Cisco Phone
    |
    v
CUCM digit analysis
    |
    v
Route Pattern
    |
    v
Route List
    |
    v
Route Group
    |
    v
Gateway or Trunk
    |
    v
Inbound VoIP Dial Peer
    |
    v
Outbound POTS Dial Peer
    |
    v
FXO Port
    |
    v
PSTN
```

This is a logical model, not a promise that every deployment uses every object. A SIP trunk, H.323 gateway, or MGCP-controlled gateway changes where call-routing decisions are made.

## Reference Map

| Question | Go to |
|---|---|
| What do ANI, DNIS, RTP, DSP, or PLAR mean? | [Vocabulary](glossary.md) |
| Is this port FXS or FXO? | [Analog Voice Ports](analog-ports.md) |
| Why did IOS select this dial peer? | [Dial Peers](dial-peers.md) |
| Why did CUCM choose this gateway? | [CUCM Call Routing](cucm-routing.md) |
| How do I configure common CUCM objects? | [CUCM Configuration Tutorials](cucm-tutorials/index.md) |
| How do SIP, H.323, and MGCP differ? | [Protocols and Media](protocols-media.md) |
| How do I operate and secure a SIP/CUBE edge? | [SIP and CUBE Operations](sip-cube.md) |
| How does Webex Calling connect through a Local Gateway? | [Webex Calling and Local Gateway](webex-local-gateway.md) |
| How should the enterprise dial plan normalize numbers? | [Dial-Plan Design](dial-plan-design.md) |
| How does an inbound or outbound call move end to end? | [Call Flows and Walkthroughs](call-flows.md) |
| How do I collect CUCM evidence? | [CUCM Diagnostics and Tracing](cucm-diagnostics.md) |
| How do I analyze SIP, SDP, and RTP packets? | [Packet-Capture Walkthroughs](packet-captures.md) |
| Why is voice quality poor? | [Voice QoS and Call Quality](qos-quality.md) |
| How do I size or troubleshoot DSP resources? | [DSP and Media Resources](dsp-capacity.md) |
| How should fax, paging, and special analog devices be handled? | [Fax and Special Analog Devices](fax-special-devices.md) |
| How does a site retain calling during an outage? | [SRST](srst.md) and [High Availability](high-availability.md) |
| How should emergency calling be designed and tested? | [Emergency Calling](emergency-calling.md) |
| Which show or debug command should I use? | [Troubleshooting and Commands](troubleshooting.md) |
| Where can I practice real failure scenarios? | [Troubleshooting Labs](troubleshooting-labs.md) |
| Which checklist should I use for a change? | [Operational Checklists](operational-checklists.md) |
| How should voice systems be monitored or inventoried? | [Monitoring and Automation](monitoring-automation.md) |
| How should I migrate an old ISR, analog gateway, or protocol? | [Migration Guides](migrations.md) |

## Core Troubleshooting Model

Every routed gateway call normally has two call legs:

```text
Source system  ->  inbound call leg  ->  Cisco gateway  ->  outbound call leg  ->  destination system
```

For each failed call, identify:

- the calling number and called number;
- the signaling protocol or analog port on the inbound leg;
- the inbound dial peer;
- any number translation;
- the outbound dial peer;
- the selected port, trunk group, gateway, or session target;
- whether signaling completed;
- whether RTP or analog audio was established in both directions.

## Official Verification Resources

Use Cisco documentation for the exact model and software release before implementing a configuration:

- [Cisco Feature Navigator](https://cfnng.cisco.com/): Check feature support by platform, image, and release.
- [Catalyst 8200 Series Edge Platforms support](https://www.cisco.com/c/en/us/support/routers/catalyst-8200-series-edge-platforms/series.html): Hardware, software, release-note, and configuration resources.
- [Cisco Unified Communications Manager support](https://www.cisco.com/c/en/us/support/unified-communications/unified-communications-manager-callmanager/series.html): CUCM configuration and release documentation.
- [Cisco Unified Border Element support](https://www.cisco.com/c/en/us/support/unified-communications/unified-border-element/series.html): CUBE configuration, interoperability, licensing, and troubleshooting resources.
- [Understand Inbound and Outbound Dial Peers Matching](https://www.cisco.com/c/en/us/support/docs/voice/call-routing-dial-plans/14074-in-dial-peer-match.html): Cisco's dial-peer matching overview.

Cisco URLs and document organization can change. Begin from the product support page when a deep link moves, and match documentation to the deployed release.

## Safety and Example Conventions

- Addresses in examples use documentation ranges such as `192.0.2.0/24` and `198.51.100.0/24`.
- Extension numbers are fictional.
- Never copy passwords, SNMP communities, private keys, carrier credentials, or production authentication data into notes or tickets.
- Run broad debug commands only during a controlled window. Prefer filtered debugs where the platform supports them, capture only what is needed, and disable debugging immediately afterward with `undebug all`.

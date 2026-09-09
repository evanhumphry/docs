# DSP and Media-Resource Capacity

Digital Signal Processors (DSPs) perform real-time audio work. Cisco Packet Voice Digital Signal Processor Modules (PVDMs) provide DSP resources on supported gateways. A design can have enough physical ports but insufficient DSP capacity to complete all expected calls and media services.

## What Uses DSP Resources

Depending on platform and design:

- analog and digital voice termination;
- codec encode and decode;
- transcoding between codecs;
- conferencing;
- Media Termination Point functions;
- fax and modem processing;
- secure media processing;
- higher-complexity codecs;
- mixed packetization or media interworking.

Not every call consumes the same amount. Capacity depends on codec complexity, service type, channel count, platform, IOS XE release, and DSP firmware.

## PVDM Planning Questions

1. Which PVDM models are supported in the exact router and module slots?
2. How many DSPs and channels are available?
3. Which codecs and services must be supported?
4. How many simultaneous analog, digital, SIP, and transcoded calls are expected?
5. How much failover and growth margin is required?
6. Are conferencing, MTP, and transcoding colocated with gateway termination?
7. Does SRST increase local DSP demand during a WAN outage?
8. Will secure media, fax, or special codecs change capacity?
9. Can one module or DSP failure reduce capacity below the minimum?
10. What alarms and commands prove exhaustion before users report it?

Use the release-specific Cisco DSP calculator or platform documentation rather than a generic channel number.

## Media Resources

### Transcoder

A transcoder converts one codec or media format into another:

```text
G.729 endpoint -> transcoder/DSP -> G.711-only application
```

CUCM invokes a transcoder only when one is registered, reachable through the effective MRGL, compatible with the required codecs, and has free capacity.

### Conference Bridge

A conference bridge mixes audio from multiple participants. Software and hardware conference bridges have different codec, scale, and feature capabilities.

### Media Termination Point

An MTP can assist with:

- DTMF interworking;
- supplementary services;
- SIP early-offer requirements;
- protocol interworking;
- media anchoring;
- trusted-relay or address-family scenarios, depending on release.

Do not select **MTP Required** as a generic fix. Determine why the call needs an MTP and whether the chosen resource supports the required behavior.

## CUCM Selection Path

```text
Calling device or trunk
        |
        v
Effective Media Resource Group List
        |
        v
Ordered Media Resource Groups
        |
        v
Available MTP, transcoder, or conference bridge
```

Check device-pool and device-level MRGL assignments. A registered resource can still be unavailable to a call because it is not in the caller's effective MRGL.

## IOS or IOS XE Resource Model

DSP farms expose supported DSP functions to CUCM using a supported control protocol and profile. Exact configuration differs by platform, release, and resource type.

Validate:

- DSP farm service is enabled where required;
- SCCP or other resource-control registration uses the expected source address;
- profile type and codec list match CUCM configuration;
- maximum sessions fit validated capacity;
- the CUCM media-resource object name matches the registered resource;
- certificates and secure registration are correct where required;
- shutdown state and registration are monitored.

## Inspection Commands

Availability and output vary by platform:

```ios
show inventory
show platform
show voice dsp
show voice dsp group all
show dspfarm all
show sccp
show call active voice brief
show call history voice brief
```

Use contextual help if a command is absent. Record IOS XE release, PVDM model, DSP state, allocated channels, codec, and current sessions.

## DSP Exhaustion Symptoms

- some calls succeed until concurrency rises;
- analog or digital call setup fails despite an available circuit;
- transcoded calls fail while same-codec calls work;
- conferences fail to add participants;
- CUCM reports unavailable or out-of-resources media devices;
- calls return resource-unavailable causes;
- failover paths work at low load but fail during an outage;
- fax or higher-complexity codec calls fail first.

Confirm actual resource allocation and causes. Similar symptoms can come from licensing, registration, routing, codec, or MRGL errors.

## Capacity Worksheet

| Workload | Normal concurrent | Failure concurrent | Codec/service | DSP cost source | Required capacity |
|---|---:|---:|---|---|---:|
| Analog FXS/FXO calls |  |  |  |  |  |
| Digital trunk calls |  |  |  |  |  |
| Transcoding sessions |  |  |  |  |  |
| Conference sessions |  |  |  |  |  |
| MTP sessions |  |  |  |  |  |
| Fax or modem sessions |  |  |  |  |  |
| SRST load |  |  |  |  |  |
| Growth reserve |  |  |  |  |  |

Use documented resource costs for the exact release and configuration. Do not add unlike session limits as if they consume identical DSP resources.

## Failure-Domain Planning

Consider:

- loss of one PVDM;
- loss of one voice module;
- loss of one gateway;
- CUCM node failover;
- WAN failure that invokes SRST;
- primary carrier failure that redirects calls;
- peak conference or fax demand;
- software upgrade with resources temporarily out of service.

Capacity should satisfy the accepted failure scenario, not only the normal average.

## Turn-Up Tests

- [ ] All DSPs and PVDMs appear healthy in inventory and platform output.
- [ ] Analog and digital channels allocate and release normally.
- [ ] MTPs, transcoders, and conference bridges register to the intended CUCM group.
- [ ] MRGL selection is validated from every relevant device pool and trunk.
- [ ] Each required codec pair is tested.
- [ ] DTMF, hold, transfer, conference, fax, and secure media are tested.
- [ ] Maximum expected concurrency is load-tested in a lab or approved window.
- [ ] Failover load remains within validated capacity.
- [ ] Exhaustion produces an alarm before all user capacity is lost.
- [ ] Monitoring records utilization and registration changes.

Continue with [Protocols and Media](protocols-media.md), [Voice QoS](qos-quality.md), and [High Availability](high-availability.md).

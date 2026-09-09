# Troubleshooting and Command Reference

Use a call trace to identify the first stage that behaves differently from the design. Do not begin with a broad debug and hope the answer appears.

## Ten Questions for Every Failed Call

1. What exact number was dialed?
2. What calling number and device originated the call?
3. Did CUCM match the expected pattern and partition using the caller's effective CSS?
4. Did CUCM select the expected route list, route group, gateway, or trunk?
5. Which inbound dial peer matched on the router?
6. Which outbound dial peer matched?
7. Which voice port, trunk-group member, or session target was selected?
8. Did signaling complete, and what cause or response ended it?
9. Was RTP or analog audio established?
10. Was audio bidirectional, and did DTMF and disconnect supervision work?

Write down the observed answer to each question. A blank answer is the next place to collect evidence.

## Collect Context First

Record:

- timestamp and timezone;
- calling and called numbers;
- originating and destination devices;
- expected and actual route;
- whether the issue is reproducible;
- whether all calls, one direction, one site, one carrier, or one number is affected;
- router model, voice modules, DSPs, IOS XE release, and recent changes;
- CUCM version, gateway or trunk, device pool, CSS, partition, and media-resource context.

Sanitize secrets and private identifiers before sharing output.

## Platform and Inventory

```ios
show version
show inventory
show ip interface brief
show running-config | include ^hostname
```

Use these to verify that you are on the expected gateway, software release, interface address, and hardware inventory.

## Voice Ports

```ios
show voice port summary
show voice port 0/1/5
show running-config | section ^voice-port
```

Look for administrative and operational state, on-hook or off-hook state, signaling type, trunk-group membership, PLAR, caller-ID configuration, and whether the port exists on the installed module.

## Dial Peers and Number Matching

```ios
show dial-peer voice summary
show dialplan number 6985
show voice translation-rule
show voice translation-profile
show running-config | section ^dial-peer voice
```

Use `show dialplan number` to test outbound number matching before placing a call. Then compare that prediction with active or historical call data.

Check:

- exact versus wildcard destination patterns;
- inbound called-number or calling-number criteria;
- most-specific outbound match;
- preference and hunt behavior;
- shutdown or operational state;
- session target reachability;
- port or trunk-group availability;
- translation profiles;
- codec, DTMF, and protocol settings.

## Active and Historical Calls

```ios
show call active voice brief
show call history voice brief
show voip rtp connections
```

Active calls help identify current call legs, peers, endpoints, codecs, and media addresses. History can help after a short test call, but retention and displayed fields vary by release and configuration.

## Controlled CCAPI Debugging

```ios
debug voip ccapi inout
```

CCAPI traces can show call-leg creation, calling and called numbers, dial-peer selection, and disconnect causes.

!!! danger "Debug commands can affect production"
    Debug output can be high volume and CPU intensive. Use it only during a controlled window, preferably with terminal monitoring and supported filtering. Reproduce one test call, collect the needed output, and immediately stop debugging.

```ios
undebug all
show debugging
```

Never leave a broad voice debug enabled. Avoid console logging during high-volume debugging because it can make the device difficult to manage.

## SIP and H.323 Evidence

For SIP, inspect request and response codes, headers, Request-URI, SDP addresses and ports, codecs, and DTMF negotiation. For H.323, inspect call establishment, capability exchange, source addresses, and media channel negotiation.

Protocol-specific debug command names and filtering options vary across IOS XE releases. Consult the command reference for the installed release before enabling them. Prefer packet capture, CUCM traces, CUBE or gateway logging, and narrowly filtered diagnostics over a broad production debug.

## CUCM Routing Checks

Follow this order:

1. Confirm the digits CUCM received.
2. Determine the effective line and device CSS.
3. Confirm the expected pattern's partition appears in that CSS.
4. Compare competing patterns and urgent or variable-length behavior.
5. Identify the selected route list and route group.
6. Confirm member order and availability.
7. Inspect calling and called-party transformations at each layer.
8. Confirm gateway or trunk status and destination address.
9. Check region, location, MRGL, and required media-resource availability.
10. Compare CUCM traces or call records with the expected path.

CUCM's Dialed Number Analyzer can test many digit-analysis scenarios when available on the installed release, but live traces remain important when device state, transformations, or protocol behavior affect the result.

## Symptom-Based Workflow

### Fast Busy or Immediate Reorder

Check CUCM pattern reachability, CSS and partition, route-list or route-group availability, outbound dial-peer matching, trunk-group capacity, and disconnect cause.

### Call Rings but Does Not Connect

Check alerting and connect messages, analog answer supervision, codec negotiation, MTP or transcoder requirements, and whether the far endpoint actually answers.

### One-Way Audio

Check both media directions separately:

```text
Endpoint A source -> route/firewall/NAT -> Endpoint B destination
Endpoint B source -> route/firewall/NAT -> Endpoint A destination
```

Inspect advertised RTP addresses and ports, IP routing, ACLs, firewalls, NAT, asymmetric paths, VRFs, media binding, and inserted media resources.

### No Audio in Either Direction

Confirm that signaling reached a connected state, then check SDP or H.245 media negotiation, codec agreement, DSP availability, MTP or transcoder insertion, and reachability between advertised media endpoints.

### DTMF Does Not Work

Compare the DTMF method on both call legs and any interworking device. Test with the actual IVR or voicemail destination. Check whether an MTP or transcoder is being invoked and whether its MRGL placement and registration are correct.

### Wrong Dial Peer

Compare the received called and calling numbers with inbound criteria. For outbound selection, test the exact called number, compare pattern specificity, then preference and hunt state. Inspect translations before and after selection.

### Wrong FXO Port

Check the selected outbound POTS peer, trunk group, member preference, busy or failed port state, and hunt behavior. Confirm with active call data rather than reading configuration order.

### Analog Call Never Disconnects

Check disconnect supervision, battery reversal or denial, tone detection, timing, country-specific settings, and carrier behavior. Coordinate changes with the carrier and test both caller-first and called-party-first disconnect.

### DSP or Media Resource Failure

Check installed PVDM or DSP inventory, current DSP usage using release-appropriate commands, codec requirements, analog or digital termination demand, transcoder and conference resources, registration, MRGL access, and capacity.

## Before and After a Change

```ios
show clock
show version
show inventory
show voice port summary
show dial-peer voice summary
show call active voice brief
show logging
```

Capture a sanitized baseline before a change. Afterward, repeat the same checks and compare expected differences.

## Quick Command Reference

### Platform

```ios
show version
show inventory
show ip interface brief
show running-config
```

### Voice Ports

```ios
show voice port summary
show voice port 0/1/5
show running-config | section ^voice-port
```

### Dial Peers

```ios
show dial-peer voice summary
show dialplan number 6985
show voice translation-rule
show voice translation-profile
show running-config | section ^dial-peer voice
```

### Calls

```ios
show call active voice brief
show call history voice brief
show voip rtp connections
```

### Controlled Debugging

```ios
debug voip ccapi inout
undebug all
show debugging
```

### Configuration Preservation

```ios
show running-config
show startup-config
copy running-config startup-config
```

Saving configuration is not a substitute for validating calls. Complete the [Call Flows](call-flows.md) worksheet and the [Migration Guides](migrations.md) validation checklist.

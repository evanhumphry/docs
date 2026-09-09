# Verify and Troubleshoot CUCM Configuration

## Goal

Prove that a CUCM change is saved, applied to the intended devices, selected by digit analysis, operational at runtime, and reversible.

## Five Verification Layers

```text
1. Configuration exists
2. Dependencies and assignments are correct
3. Device or service received the change
4. Call routing selects the expected objects
5. Signaling and media work end to end
```

A green Save message proves only the first layer.

## Step 1: Confirm the Saved Object

1. Return to the configuration page.
2. Search for the object by exact name or pattern.
3. Reopen it.
4. Confirm every field saved as intended.
5. Record the **Last Modified** information if the release displays it.
6. Capture a sanitized screenshot or export for the change record.

Check for accidental whitespace, wrong partition, wrong device pool, similar object names, and defaults inherited from a copied object.

## Step 2: Review Dependency Records

Use **Related Links > Dependency Records** where available.

Confirm:

- which devices or objects use the configuration;
- whether a supposedly dedicated profile is shared;
- whether the new object is unused because assignment was missed;
- whether deletion or rollback would affect another service.

Dependency records may need to be enabled or generated according to the CUCM release and service settings. Treat them as important evidence, not the only inventory source.

## Step 3: Determine Whether Apply Config or Reset Is Required

CUCM pages may offer:

- **Save:** Store the configuration.
- **Apply Config:** Push an applicable change to selected devices.
- **Reset:** Reset device registration or configuration state.
- **Restart:** Restart the device or service behavior exposed by that page.

Read the page guidance and confirmation dialog. Determine:

- affected devices;
- active-call impact;
- whether the operation applies to one node or cluster-wide service;
- whether a maintenance window is required;
- how to verify recovery.

Do not use Reset as a generic troubleshooting step before collecting state.

## Step 4: Confirm Device Registration and Runtime State

For a phone:

- registration status;
- current IP address;
- active CUCM node;
- firmware;
- directory numbers;
- device pool;
- security state.

For a SIP trunk:

- destination and transport;
- OPTIONS or monitoring status;
- active call-processing nodes;
- SIP profile and security profile;
- certificate state for TLS.

For a gateway:

- registration for MGCP;
- address and source identity for H.323;
- endpoint or port state;
- route-group membership;
- IOS dial-peer and voice-port state.

For media resources:

- registration;
- controlling node;
- MRG and MRGL reachability;
- codec and service capabilities;
- current and maximum sessions.

## Step 5: Verify Digit Analysis

Use Dialed Number Analyzer when available:

1. Select the exact calling device, line, trunk, or context.
2. Enter digits exactly as the source presents them.
3. Confirm effective CSS.
4. Confirm visible partitions.
5. Confirm translation pattern or route pattern.
6. Confirm called and calling transformations.
7. Confirm route list, route group, and selected gateway or trunk.
8. Repeat with an unauthorized calling context.

DNA predicts routing. It does not prove peer availability, codec agreement, media, or carrier acceptance.

## Step 6: Place a Controlled Test Call

Record:

| Observation | Result |
|---|---|
| Calling number and device |  |
| Called number as dialed |  |
| Timestamp and timezone |  |
| CUCM node |  |
| Pattern and partition |  |
| Route list and route group |  |
| Gateway or trunk |  |
| IOS inbound and outbound peers |  |
| Number presented to peer |  |
| SIP response or cause |  |
| Codec and DTMF |  |
| RTP addresses and audio |  |
| Disconnect origin |  |

Verify ringback, answer, bidirectional audio, DTMF, hold, transfer, conference, caller ID, and clearing as applicable.

## Step 7: Use RTMT and Traces

Use Real-Time Monitoring Tool to check:

- node and service alarms;
- registration;
- trunk and gateway state;
- performance counters;
- media-resource status;
- trace collection.

For detailed call processing:

1. Configure only the necessary SDL, SDI, SIP, or protocol trace detail.
2. Record cluster time and test-call time.
3. Reproduce one call.
4. Collect a narrow time window.
5. Return trace settings to the approved baseline.
6. Search by calling number, called number, Call-ID, device name, or call identifier.

Protect traces because they can contain subscriber data and authentication details.

## Step 8: Correlate the Gateway

On IOS or IOS XE, use commands supported by the release:

```ios
show dial-peer voice summary
show dialplan number 6985
show call active voice brief
show call history voice brief
show voice port summary
show voip rtp connections
```

For a controlled trace, `debug voip ccapi inout` can show call-leg creation and dial-peer selection. Use an approved window, stop with `undebug all`, and sanitize the output.

Align CUCM and gateway timezones before correlating timestamps.

## Step 9: Verify Negative Cases

A configuration is incomplete until unintended behavior is tested.

Test:

- a phone without the new CSS;
- a number outside the new pattern;
- a blocked destination class;
- an unapproved inbound source;
- a failed primary trunk or gateway;
- an unavailable media resource;
- wrong or missing caller identity;
- a forwarded or transferred call;
- a device in another site or device pool.

Confirm the change is no broader than intended.

## Step 10: Exercise Rollback

1. State the exact rollback trigger.
2. Restore the recorded previous assignment or object.
3. Apply or reset only what is required.
4. Confirm device registration and service recovery.
5. Place the baseline test call.
6. Confirm blocked and allowed classes return to the former state.
7. Remove abandoned test objects in reverse dependency order.
8. Record rollback duration and any unexpected behavior.

A rollback plan that has never been exercised is an assumption.

## Symptom Map

| Symptom | First place to inspect |
|---|---|
| Object not found | Name, partition, save result, publisher/node used for administration |
| Phone did not change | Apply/reset requirement, device pool, line versus device assignment |
| Pattern exists but call fails | CSS, partition, competing pattern, translation, route-list destination |
| Trunk shows down | OPTIONS, transport, address, port, TLS, certificate, firewall, peer state |
| MGCP gateway unregistered | Domain name, call agent, routing, source address, service state |
| Correct route but wrong digits | Transformation order across CUCM, gateway, and carrier |
| Call connects without audio | SDP/H.245 address, RTP routing, firewall, NAT, codec, media resource |
| DTMF fails | Relay method, SIP profile, dial peer, MTP/transcoder interworking |
| Works until load increases | location CAC, trunk capacity, DSP, MTP, transcoder, conference capacity |
| Backup route fails | member state, cause handling, transformations, certificates, firewall, capacity |

## Change Completion Checklist

- [ ] Saved object was reopened and verified.
- [ ] Dependency records match intended use.
- [ ] Apply, reset, and restart impact were evaluated.
- [ ] Device or service runtime state is healthy.
- [ ] DNA selects the expected route from authorized and unauthorized contexts.
- [ ] Controlled calls prove signaling, audio, DTMF, identity, and clearing.
- [ ] RTMT, traces, gateway history, and packet evidence agree.
- [ ] Negative cases show no unintended access.
- [ ] Primary and backup behavior are tested.
- [ ] Rollback was exercised or validated in the lab.
- [ ] Screenshots, traces, and exports are sanitized.
- [ ] Documentation and monitoring are updated.

Return to the [CUCM Configuration Tutorials](index.md) or use [CUCM Diagnostics and Tracing](../cucm-diagnostics.md) for deeper analysis.

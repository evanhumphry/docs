# CUCM Diagnostics and Tracing

Use CUCM diagnostic tools to prove how digit analysis, device state, signaling, media-resource selection, and call clearing behaved. Start with a narrow call record, then enable only the traces needed to answer a specific question.

## Minimum Call Record

Collect before opening tools:

- date, time, and timezone;
- calling and called numbers exactly as dialed and displayed;
- originating device name, line, site, and user impact;
- destination device, gateway, trunk, or carrier;
- call direction;
- expected and actual behavior;
- whether the call rang, connected, had audio, accepted DTMF, transferred, and cleared;
- CUCM nodes and gateway involved;
- whether the problem is reproducible.

One precise test call is more useful than a large trace containing hundreds of unrelated calls.

## Diagnostic Tool Map

| Tool | Best use |
|---|---|
| **Device and trunk status pages** | Registration, IP address, active node, reset/restart state, and basic configuration |
| **Dialed Number Analyzer** | Predicting digit analysis for a calling context and dialed string |
| **Route Plan Report** | Finding patterns, DNs, partitions, and overlapping dial-plan entries |
| **RTMT** | Alerts, performance counters, traces, service status, and real-time monitoring |
| **Cisco CallManager SDL/SDI traces** | Detailed call processing, digit analysis, signaling, and device control |
| **SIP traces** | SIP requests, responses, headers, SDP, and dialog correlation |
| **CDR** | Call-detail records such as parties, timestamps, duration, and route information |
| **CMR** | Call-management records with media-quality measurements where generated |
| **Gateway call history** | IOS or IOS XE call legs, dial peers, causes, codecs, and media endpoints |
| **Packet capture** | On-the-wire signaling and RTP evidence at a chosen point |

Availability, names, and menu locations vary by CUCM release and enabled services.

## Dialed Number Analyzer

Dialed Number Analyzer can model many CUCM digit-analysis decisions. Supply the correct calling device or line context, CSS, time, and dialed digits.

Use it to answer:

- Which pattern matches?
- Which partition contains it?
- Which CSS made it reachable?
- Are digits discarded, prefixed, or transformed?
- Which route list, route group, gateway, or trunk is selected?
- Does a blocking pattern or call-classification rule apply?

DNA is predictive. It may not reflect transient registration, trunk availability, bandwidth, media resources, or every runtime feature. Confirm important findings with live traces or call records.

## Route Plan Report

Use the Route Plan Report to search for:

- directory numbers;
- route patterns;
- translation patterns;
- call-park and feature patterns;
- partitions;
- unassigned or duplicate patterns;
- overlapping exact and wildcard matches.

Export and protect reports according to policy because they can reveal internal numbering and routing architecture.

## RTMT Workflow

Real-Time Monitoring Tool can help with:

- service and node status;
- registered device counts;
- trunk and gateway alerts;
- resource usage and performance counters;
- trace collection;
- syslog and event monitoring;
- call-processing alarms;
- media-resource registration and exhaustion.

Recommended workflow:

1. Confirm cluster time synchronization.
2. Select the affected call-processing node.
3. Record current service and alarm state.
4. Configure only the needed trace level and components.
5. Reproduce one call and record its exact time.
6. Collect a narrow time window.
7. Return trace settings to their approved baseline.
8. Sanitize numbers, names, addresses, and credentials before sharing.

## SDL and SDI Traces

Cisco CallManager traces can reveal:

- digit collection and analysis;
- calling and called-number transformations;
- selected route pattern, list, group, gateway, or trunk;
- SIP, H.323, SCCP, or MGCP message handling;
- device state and call-control events;
- media-resource requests and allocation;
- disconnect causes and error conditions.

Trace detail can be large. Do not enable all components at detailed level across a busy cluster without a reason, a window, and storage monitoring.

## SIP Trace Reading Order

For one SIP call:

1. Locate the initial INVITE using timestamp, calling number, called number, or Call-ID.
2. Identify the receiving CUCM node and inbound trunk or device.
3. Record the Request-URI, From, To, asserted identity, and diversion history.
4. Inspect the SDP offer.
5. Find CUCM digit-analysis and route-selection events.
6. Locate the outbound INVITE and compare numbers and SDP.
7. Follow provisional and final responses.
8. Confirm ACK and connected state.
9. Identify re-INVITEs or UPDATEs for hold, transfer, or media change.
10. Follow the BYE and final response, noting which side cleared the call.

Use Call-ID and CUCM call identifiers to correlate events, but remember that a border element can terminate one dialog and create another with a different Call-ID.

## CDR and CMR

**Call Detail Records (CDR)** provide historical call metadata. Depending on configuration and release, useful fields can include:

- origination and destination numbers;
- device names;
- start, connect, and end times;
- duration;
- redirect information;
- destination gateway or trunk;
- disconnect causes.

**Call Management Records (CMR)** can provide media-quality measurements such as packet loss, jitter, latency, and codec information when endpoints report them.

CDR and CMR are excellent for scope and trend analysis, but they may not contain every signaling transformation or packet-level detail. Use them to find the affected calls and then select the correct detailed evidence.

## Cause Codes and Clearing

A disconnect cause shows how a component categorized the failure. It may be generated locally or mapped from a downstream protocol response.

For a failed call, record:

- the SIP response or H.323/Q.850 cause;
- which device generated it;
- the calling and called numbers at that point;
- whether another route was attempted;
- whether the cause was transformed by CUBE or another gateway.

Do not treat a generic cause such as unallocated number or temporary failure as proof until you find the component that originated it.

## CUCM-to-Gateway Correlation

```text
CUCM trace or CDR
    | timestamp, parties, trunk/gateway, call identifier
    v
IOS XE call history or CCAPI
    | inbound peer, outbound peer, transformed digits, cause
    v
SIP/H.323 messages and RTP capture
```

Normalize timezones before comparing logs. NTP drift can make a correct call path look unrelated.

## Registration and Reachability Checks

Confirm:

- the device, trunk, gateway, or media resource is registered or in service;
- CUCM is using the expected active or backup node;
- IP routing and DNS are correct;
- certificates are valid for secure trunks or devices;
- OPTIONS, registration, or protocol status reflects the intended state;
- a reset or configuration change has actually taken effect;
- the selected route-group member is available.

A configured object is not necessarily registered, reachable, or selected.

## Escalation Bundle

Provide a small, reproducible evidence set:

- problem statement and business impact;
- topology and call-flow diagram;
- exact test-call record;
- expected route and number formats;
- relevant CUCM object screenshots or exports;
- narrow SDL/SDI or SIP trace window;
- matching CDR/CMR record when available;
- gateway call history and selected dial peers;
- sanitized packet capture if media or protocol details matter;
- recent changes and attempted fixes;
- platform and software versions.

Never include passwords, private keys, unredacted authentication headers, or unrelated subscriber data.

Continue with [Dial-Plan Design](dial-plan-design.md), [Packet Captures](packet-captures.md), and [Troubleshooting](troubleshooting.md).

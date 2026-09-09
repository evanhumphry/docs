# Voice Monitoring and Automation

Monitoring should detect registration loss, capacity pressure, certificate risk, call failures, and media degradation before users report them. Automation should collect and validate state safely, not push unreviewed voice changes at scale.

## Monitoring Layers

```text
Business service
  -> call success and emergency readiness
  -> CUCM/Webex routing and registration
  -> CUBE/gateway peers, dial peers, ports, DSPs
  -> SIP/H.323/MGCP signaling and RTP media
  -> IP routing, DNS, NTP, QoS, firewall, power
```

Monitor every layer because a healthy router CPU does not prove calling works.

## Signals to Collect

### CUCM and Call Control

- node and service status;
- registered and unregistered devices;
- trunk and gateway status;
- media-resource registration and utilization;
- database or replication health where applicable;
- call-processing alarms;
- CDR and CMR records;
- certificate expiration;
- application and CTI integration status.

### IOS or IOS XE Gateways

- platform, module, and environmental health;
- interface, routing, DNS, and NTP state;
- SIP peer or registration state;
- dial-peer operational state;
- voice-port state and stuck seizures;
- active and failed call counts;
- disconnect causes;
- DSP and PVDM utilization;
- CUBE license and session capacity;
- QoS queue drops and interface errors;
- certificate expiration;
- configuration changes.

### Call Quality

- call completion rate;
- post-dial delay;
- packet loss, jitter, and latency by direction;
- codec and transcoder usage;
- one-way or zero-packet streams;
- abnormal short-duration calls;
- repeated SIP response families;
- carrier and site comparisons;
- peak concurrent calls and blocked calls.

## Data Sources

| Source | Useful for |
|---|---|
| **SNMP or streaming telemetry** | Platform, interface, environment, queue, and supported voice counters |
| **Syslog** | State changes, registration, security, errors, and configuration events |
| **CUCM RTMT and serviceability APIs** | Cluster services, devices, counters, traces, and alarms |
| **CDR and CMR** | Historical call outcomes and media-quality trends |
| **IOS XE NETCONF or RESTCONF** | Structured configuration and operational data where supported |
| **CUCM AXL** | Configuration inventory and controlled configuration workflows |
| **CUCM RISPort** | Real-time device registration and status queries |
| **Webex APIs and Control Hub** | Cloud calling inventory, status, and analytics according to licensed capabilities |
| **Synthetic calls** | End-to-end validation of dialing, answer, media, DTMF, and clearing |

API versions, schemas, authentication, and support vary. Use the published API documentation for the installed product release.

## CDR and CMR Analytics

Use CDR to trend:

- attempted and completed calls;
- route, gateway, or trunk use;
- failure causes;
- call duration;
- calling and called number classes;
- site and carrier differences;
- changes after a migration.

Use CMR where available to trend:

- packet loss;
- jitter;
- latency;
- codec;
- endpoint or stream quality.

Protect call records as sensitive data. Apply retention, access, and redaction requirements.

## Synthetic Call Testing

A synthetic test places or simulates a controlled call and validates the full service:

1. Originate from a known test endpoint.
2. Dial a dedicated test destination.
3. Confirm alerting and answer.
4. Exchange audio in both directions.
5. Send a known DTMF sequence.
6. Confirm caller ID and called number.
7. Clear the call and verify release.
8. Record route, codec, quality, and duration.

Use dedicated numbers and approved automation. Never generate emergency calls, premium calls, or uncontrolled traffic.

Useful synthetic scenarios:

- CUCM to local PSTN;
- PSTN to a test DN;
- primary and backup carrier paths;
- SRST fallback;
- Webex Calling through Local Gateway;
- voicemail or IVR DTMF;
- fax test service where authorized.

## Alert Design

Alert on actionable conditions:

- trunk or gateway unavailable beyond the accepted interval;
- abnormal call-failure rate;
- DSP or session utilization near validated capacity;
- repeated `4xx`, `5xx`, or timeout responses above baseline;
- voice port seized beyond normal duration;
- certificate or license approaching expiration;
- NTP drift or DNS failure;
- QoS priority drops;
- registration count deviation;
- missing CDR/CMR ingestion;
- synthetic-call failure.

Include service, site, affected path, start time, evidence link, and owner. Avoid one alert per failed call during a provider outage.

## Configuration Inventory

Automate read-only collection first:

- hostname, serial number, PID, IOS XE release, and uptime;
- modules, PVDMs, DSPs, and voice ports;
- interfaces, addresses, VRFs, routes, and bindings;
- dial peers, translation rules, trunk groups, and codec classes;
- SIP/CUBE service state and peer targets;
- certificates and expiration dates without private keys;
- CUCM trunks, gateways, route groups, device pools, and media resources;
- Webex trunks, route groups, and locations where API access permits.

Store secrets separately from collected configuration and redact credentials before version control.

## Drift Detection

Compare intended and observed state:

- unexpected dial peer or destination pattern;
- broad inbound match added without source restriction;
- changed session target or trunk group;
- modified translation rule;
- missing QoS service policy;
- certificate replacement not applied to a standby node;
- CUCM CSS or partition change;
- voice port shutdown or moved;
- software release outside the approved baseline.

A diff should trigger review, not automatic rollback, unless the remediation has been explicitly designed and tested.

## Safe Automation Rules

1. Start with read-only queries.
2. Use least-privilege service accounts.
3. Store credentials in an approved secret manager.
4. Validate schemas and device capabilities before sending changes.
5. Generate a human-readable proposed diff.
6. Require approval for routing, emergency, security, or carrier changes.
7. Limit changes to a small canary scope.
8. Verify call behavior after configuration state.
9. Stop and roll back on unexpected results.
10. Keep audit logs and correlation IDs.

## CUCM AXL

AXL provides configuration access to CUCM objects. Good uses include:

- inventory and documentation;
- duplicate or unused-object reporting;
- route-plan review;
- controlled bulk provisioning;
- validating CSS, partition, device-pool, and trunk standards.

Risks include broad administrative access and large-scale impact. Match the AXL schema to the CUCM release, use transactions carefully, and test on a nonproduction publisher or lab where possible.

## RISPort and Serviceability

RISPort can report real-time device registration and status. Serviceability interfaces can expose performance and operational information.

Use them to answer:

- Which node owns this device?
- Is the trunk or phone registered?
- What address and protocol is it using?
- Did registration counts change after a failure?

Do not use a real-time status query as proof that calling, media, or emergency location works.

## IOS XE NETCONF and RESTCONF

Structured interfaces can avoid fragile screen scraping when the required YANG model covers the data. Confirm:

- model support on the exact IOS XE release;
- candidate or running datastore behavior;
- authentication and authorization;
- transaction and rollback behavior;
- whether voice-specific configuration is modeled;
- operational data freshness;
- rate and session limits.

If a voice command is not modeled, do not silently mix unsupported CLI injection into a structured automation workflow.

## Monitoring Dashboard

A useful site dashboard should show:

- required call paths and current health;
- CUCM and Webex control-plane status;
- gateway, CUBE, and carrier peer status;
- current and peak concurrent calls;
- call success and top failure causes;
- packet loss, jitter, and latency trends;
- DSP, MTP, transcoder, and conference utilization;
- voice-port and trunk-group state;
- QoS priority drops;
- certificate and license deadlines;
- last successful synthetic call by path.

Avoid a green aggregate that hides a failed emergency or backup path.

## Monthly Automation Review

- [ ] Inventory collection completes for every managed system.
- [ ] Failed collectors and stale devices are investigated.
- [ ] Drift reports are reviewed by a voice engineer.
- [ ] Certificates and licenses have assigned renewal owners.
- [ ] CDR/CMR ingestion and retention are healthy.
- [ ] Synthetic calls cover primary and backup paths.
- [ ] Alerts are actionable and routed to current owners.
- [ ] Service accounts remain least privilege.
- [ ] Secrets and tokens are rotated according to policy.
- [ ] API and schema compatibility is checked before upgrades.

Continue with [CUCM Diagnostics](cucm-diagnostics.md), [Voice QoS](qos-quality.md), and [Operational Checklists](operational-checklists.md).

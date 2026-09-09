# Webex Calling and Local Gateway

A Webex Calling Local Gateway connects Webex cloud call control with an on-premises PSTN, PBX, CUCM environment, or other voice service. Cisco Unified Border Element commonly provides the Local Gateway function on a supported and licensed platform.

!!! warning "Use the current Webex and CUBE deployment guide"
    Supported trunk models, onboarding workflows, certificates, scale, licensing, regions, and commands change over time. Build from the current Webex Control Hub workflow and the CUBE guide for the exact IOS XE release.

## Basic Call Paths

### Webex User to Local PSTN

```text
Webex Calling user
    |
    v
Webex cloud dial plan
    |
    v
Webex trunk and route group
    |
    v
CUBE Local Gateway
    |
    v
Enterprise or carrier SIP trunk
    |
    v
PSTN
```

### PSTN to Webex User

```text
PSTN
  |
  v
Carrier or enterprise trunk
  |
  v
CUBE Local Gateway
  |
  v
Webex Calling trunk
  |
  v
Webex cloud routing
  |
  v
User or service
```

Treat CUBE as two call legs. Number format, codec, DTMF, signaling security, and media policy may differ between the Webex and PSTN sides.

## Control Hub Objects

Depending on the current service model, expect concepts such as:

- **Location:** Webex Calling site or service location.
- **Trunk:** Signaling relationship between Webex and a Local Gateway.
- **Route group:** One or more trunks used for route selection or resilience.
- **Dial plan:** Patterns that route selected enterprise destinations through a route group.
- **PSTN connection:** Cloud-connected or premises-based PSTN choice for a location.
- **Calling permissions:** Policy controlling destination classes.

Names and capabilities vary by release and subscription. Document the Control Hub object and the matching CUBE call leg together.

## Trunk Models

Webex Calling can support different Local Gateway onboarding models depending on region, design, and current product capabilities. These can include certificate-based or registration-based approaches.

Validate:

- public or private reachability requirements;
- FQDN and DNS behavior;
- TLS certificate identity and trust;
- registration credentials where applicable;
- signaling and media addresses;
- transport ports;
- NAT and firewall policy;
- redundancy and scale;
- CUBE platform and license.

Never publish registration credentials, private keys, or Control Hub onboarding data.

## Number Normalization

Define a consistent boundary:

| Stage | Recommended documentation |
|---|---|
| Webex user dialing | What users enter and which calling permissions apply |
| Webex route selection | Pattern, location, dial plan, route group, and trunk |
| CUBE inbound leg | Number and identity received from Webex |
| CUBE outbound leg | Number and identity sent to carrier, CUCM, or PBX |
| Inbound PSTN | Carrier-delivered called and calling formats |
| Webex destination | Final normalized user or service number |

Use [Dial-Plan Design](dial-plan-design.md) principles. Avoid building unrelated transformations on both Control Hub and CUBE without a number trace.

## Coexistence with CUCM

A migration or hybrid design may include both CUCM and Webex Calling:

```text
Webex Calling <-> Local Gateway/CUBE <-> CUCM <-> legacy phones/apps
                                      |
                                      +-> PSTN
```

Document:

- which system owns each number range;
- where calls between platforms route;
- calling identity and diversion headers;
- voicemail and auto-attendant ownership;
- contact-center and recording dependencies;
- emergency-location ownership;
- codec, DTMF, transfer, and media-resource behavior;
- migration sequence and rollback.

Avoid routing loops between overlapping Webex, CUCM, and PSTN patterns.

## Security

- Restrict inbound signaling to documented Webex and enterprise peers using the current Cisco guidance.
- Use TLS and certificate validation where required.
- Protect private keys and enrollment data.
- Permit only required outbound number classes.
- Monitor failed authentication, unexpected sources, and unusual destinations.
- Separate management access from voice signaling.
- Review CUBE trusted-address and toll-fraud behavior for the installed release.
- Keep certificates, DNS, NTP, and licensing monitored.

## Media and Firewall

Confirm current Webex network requirements for:

- signaling destinations and ports;
- RTP or SRTP destinations and ports;
- DNS resolution;
- NTP;
- proxy or firewall behavior;
- NAT and public-address mapping;
- QoS marking and preservation;
- regional media and data-residency requirements.

Do not create permanent broad internet rules based on an old static list. Use Cisco's current network-requirements source and a controlled change process.

## High Availability

Validate:

- multiple Local Gateways or CUBE nodes where required;
- Control Hub route-group selection;
- trunk health detection;
- DNS and certificate independence;
- carrier-side redundancy;
- active-call and new-call behavior;
- failback after recovery;
- capacity when one node is unavailable;
- emergency calling through every path.

## Turn-Up Checklist

- [ ] Webex subscription, location, trunk model, CUBE support, and licenses are validated.
- [ ] Current Cisco deployment and network-requirements guides are attached to the change.
- [ ] FQDN, DNS, NTP, TLS identity, and trust are correct.
- [ ] Signaling and media paths work in both directions.
- [ ] Control Hub dial plans, route groups, trunks, and calling permissions are documented.
- [ ] CUBE inbound and outbound dial peers match only intended peers and destinations.
- [ ] Webex, CUCM, PBX, and carrier number formats are traced end to end.
- [ ] Codec, DTMF, fax, hold, transfer, redirect, and early media are tested.
- [ ] Caller ID, privacy, and forwarded-call identity are correct.
- [ ] Emergency location, callback, and notification pass approved testing.
- [ ] Failure and recovery of each gateway and trunk are tested.
- [ ] Monitoring and certificate-renewal ownership are active.

## Troubleshooting Order

1. Confirm user, location, and service status in Control Hub.
2. Confirm Webex route pattern, route group, and trunk selection.
3. Confirm trunk status and Local Gateway identity.
4. Identify CUBE inbound and outbound dial peers.
5. Compare calling and called numbers on both legs.
6. Follow SIP responses and SDP.
7. Confirm RTP or SRTP in both directions.
8. Check TLS, DNS, NTP, firewall, and NAT.
9. Test carrier or CUCM routing independently when possible.
10. Collect a sanitized evidence bundle with timestamps and call identifiers.

Continue with [SIP and CUBE Operations](sip-cube.md), [High Availability](high-availability.md), and [Monitoring and Automation](monitoring-automation.md).

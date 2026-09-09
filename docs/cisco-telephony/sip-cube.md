# SIP and CUBE Operations

Session Initiation Protocol (SIP) establishes, modifies, and clears calls. Cisco Unified Border Element (CUBE) provides session-border-controller functions on supported and licensed IOS XE platforms. CUBE can enforce a signaling boundary, normalize SIP, interwork protocols, control media, and separate an enterprise from a carrier or another call-control domain.

!!! warning "Validate support and licensing"
    CUBE capabilities, scale, licensing, crypto support, and command syntax vary by platform and IOS XE release. Confirm the exact Catalyst 8200L PID, image, license, and feature set in Cisco Feature Navigator and the release documentation.

## SIP Call Establishment

```text
CUCM or PBX                         CUBE                         Carrier
    |--- INVITE + SDP -------------->|--- INVITE + SDP ---------->|
    |<-- 100 Trying -----------------|<-- 100 Trying -------------|
    |<-- 180 Ringing or 183 ---------|<-- 180 Ringing or 183 -----|
    |<-- 200 OK + SDP ---------------|<-- 200 OK + SDP -----------|
    |--- ACK ------------------------>|--- ACK -------------------->|
    |<========================= RTP media =========================>|
    |--- BYE ------------------------>|--- BYE -------------------->|
    |<-- 200 OK ---------------------|<-- 200 OK -----------------|
```

CUBE terminates one SIP dialog and creates another. Treat the inbound and outbound SIP legs separately, just as you would any other pair of dial peers.

## Messages and Responses

| Message or response | Operational meaning |
|---|---|
| `INVITE` | Requests a new session and often carries an SDP offer. |
| `100 Trying` | The request was received and is being processed. |
| `180 Ringing` | The far endpoint is being alerted. |
| `183 Session Progress` | Progress information, often with early media in SDP. |
| `200 OK` | The request succeeded; for an INVITE it normally carries the accepted session details. |
| `ACK` | Confirms the final response to an INVITE. |
| `BYE` | Ends an established dialog. |
| `CANCEL` | Stops a pending INVITE before it is answered. |
| `OPTIONS` | Tests capabilities or reachability without placing a call. |
| `REFER` | Requests a transfer or related action. |

Common failure families:

| Code | Meaning | First checks |
|---|---|---|
| `400` | Malformed or unacceptable request | Header syntax, normalization, URI format |
| `401` / `407` | Authentication challenge | Credentials, realm, method, security policy |
| `403` | Forbidden | Carrier authorization, source identity, calling number, policy |
| `404` | Destination not found | Request-URI, called-number normalization, carrier routing |
| `408` | Request timeout | Reachability, firewall, DNS, transport, peer health |
| `480` | Temporarily unavailable | Registration, endpoint state, forwarding, carrier status |
| `486` | Busy here | Called endpoint or downstream resource is busy |
| `488` | Session description unacceptable | Codec, DTMF, encryption, fax, or SDP mismatch |
| `500` / `503` | Server or service unavailable | Peer health, capacity, maintenance, retry path |

A response code identifies where to investigate; it does not always identify the root cause.

## Headers to Recognize

- **Request-URI:** The destination being requested from the next SIP hop.
- **From:** Logical calling identity for the dialog.
- **To:** Logical called identity.
- **Contact:** Address where the endpoint can receive subsequent requests.
- **Call-ID:** Identifier used to correlate messages in one SIP dialog.
- **CSeq:** Method sequence within the dialog.
- **Via:** Return path and transaction information.
- **P-Asserted-Identity:** Trusted-network calling identity used in many carrier designs.
- **Diversion or History-Info:** Redirection and forwarding history, depending on deployment.
- **Supported and Require:** SIP extensions understood or required by the peer.

Do not assume that `From`, P-Asserted-Identity, and the public caller ID are always the same. Trace which field the carrier and CUCM use for presentation and authorization.

## SDP Offer and Answer

Session Description Protocol describes the proposed media:

```text
v=0
c=IN IP4 192.0.2.30
m=audio 18462 RTP/AVP 0 101
a=rtpmap:0 PCMU/8000
a=rtpmap:101 telephone-event/8000
```

Key items:

- `c=` advertises the media address.
- `m=audio` advertises the UDP port and payload types.
- `a=rtpmap` maps payload numbers to codecs or telephone events.
- Direction attributes such as `sendrecv`, `sendonly`, or `inactive` affect media direction.
- Crypto attributes or DTLS information may appear when encrypted media is used.

For one-way audio, compare the advertised address and port on both legs with the packets actually transmitted.

## Early Offer and Delayed Offer

- **Early offer:** The initial INVITE contains an SDP offer.
- **Delayed offer:** SDP is exchanged later in the dialog.

Carriers often impose a specific requirement. CUCM SIP profiles, MTP insertion, CUBE configuration, and dial-peer media policy can affect offer behavior. Validate hold, transfer, early media, and failover in addition to a basic call.

## CUBE Call-Leg Model

```text
CUCM
  |
  | inbound SIP dial peer
  v
CUBE policy, normalization, and media handling
  |
  | outbound SIP dial peer
  v
Carrier
```

For each leg, document:

- match criteria;
- source and destination signaling address;
- transport, port, and encryption;
- calling and called-number format;
- codec list;
- DTMF method;
- SDP and media binding;
- OPTIONS or other availability monitoring;
- translation and SIP-profile behavior.

## Basic Dial-Peer Pattern

```ios
dial-peer voice 3100 voip
 description OUT to SIP peer
 destination-pattern 9T
 session protocol sipv2
 session target ipv4:192.0.2.40
 voice-class codec 1
 dtmf-relay rtp-nte
 no vad
```

This is a learning example, not a secure CUBE configuration. A production design also needs explicit inbound classification, source restrictions, destination restrictions, transport and certificate policy, media design, redundancy, monitoring, and licensing validation.

## Server Groups and Redundancy

Supported IOS XE releases can group SIP destinations and assign preferences. The conceptual model is:

```text
Outbound dial peer
    |
    v
SIP server group
    +--> Primary peer
    +--> Secondary peer
```

Server groups reduce duplicate dial peers, but they do not replace a failover design. Define how peer state is detected, which failures trigger another target, how long recovery takes, and whether in-progress calls survive.

Use contextual help and the release command reference before implementing `voice class server-group` or SIP OPTIONS keepalive profiles, because syntax and available timers differ.

## SIP OPTIONS Monitoring

OPTIONS can help mark a peer available or unavailable before a user call reaches it. Validate:

- source address and transport;
- response code treated as healthy;
- interval and retry timing;
- dial-peer busy-out behavior;
- firewall and carrier allowance;
- recovery after the peer returns;
- interaction with DNS or server groups.

A successful OPTIONS response proves SIP reachability, not that every destination, codec, or media path works.

## SIP Normalization

Normalization can change headers, URIs, parameters, SDP, or response handling. Use it only when a documented interworking requirement cannot be solved with ordinary number translation or standard profiles.

For every normalization rule:

1. Save a sanitized before-message.
2. State the exact defect or requirement.
3. Define the expected after-message.
4. Test calls in both directions.
5. Test transfer, redirect, hold, early media, DTMF, and failover.
6. Keep a rollback copy.

Avoid a broad rule that silently changes every SIP message when only one peer or method needs adjustment.

## Toll-Fraud Controls

!!! danger "A reachable SIP listener is not automatically safe"
    A broad inbound dial peer combined with permissive outbound routes can allow unauthorized calls. Treat signaling reachability and dial-plan authorization as separate controls.

Use defense in depth:

- permit signaling only from approved peers at routing, firewall, and platform layers;
- configure explicit inbound dial-peer matching;
- restrict outbound destination patterns to required number classes;
- block premium, international, or other classes unless authorized;
- validate calling identity rather than trusting an arbitrary header;
- use authentication and TLS where required;
- rate-limit or alarm on unusual attempts;
- protect management access separately from SIP;
- review logs for scanning, repeated failures, and unexpected destinations;
- verify the release-specific CUBE trusted-address behavior before relying on it.

## TLS, Certificates, and SRTP

TLS protects SIP signaling between authenticated peers. SRTP protects media. They solve different problems.

Certificate operations should cover:

- trusted root and intermediate certificates;
- subject name or Subject Alternative Name matching;
- clock synchronization;
- key strength and supported cipher suites;
- expiration monitoring and renewal ownership;
- trustpoint and private-key backup policy;
- staged renewal and rollback;
- mutual authentication requirements.

Never publish private keys, shared secrets, carrier credentials, or unredacted authentication headers.

## Operational Commands

Availability varies by release:

```ios
show dial-peer voice summary
show sip-ua status
show sip-ua connections tcp brief
show call active voice brief
show call history voice brief
show voip rtp connections
show running-config | section ^voice service voip
show running-config | section ^dial-peer voice
```

During an approved window, `debug ccsip messages` can expose full SIP messages. It can also produce high volume and reveal telephone numbers, identities, network details, and authentication material. Filter where supported, reproduce one call, stop with `undebug all`, and sanitize the capture.

## Turn-Up Checklist

- [ ] Exact CUBE platform, release, feature, scale, and license are validated.
- [ ] Signaling and media source addresses are documented.
- [ ] Inbound dial peers match only intended peers.
- [ ] Outbound dial peers allow only intended destinations.
- [ ] Calling and called-number formats are correct on both legs.
- [ ] Early-offer, codec, DTMF, fax, and encryption behavior are agreed.
- [ ] OPTIONS or peer monitoring is tested through failure and recovery.
- [ ] RTP routing, firewall, NAT, and QoS are bidirectional.
- [ ] Certificates and expiration monitoring are assigned to an owner.
- [ ] Transfer, redirect, hold, early media, voicemail, and failover are tested.
- [ ] Emergency calling follows an approved test process.
- [ ] Debug output and packet captures are sanitized before sharing.

Continue with [Voice QoS and Call Quality](qos-quality.md), [Packet-Capture Walkthroughs](packet-captures.md), and [High Availability](high-availability.md).

# Packet-Capture Walkthroughs

Packet captures show what signaling and media actually crossed an interface. Use them to confirm, not replace, the call-flow model.

!!! warning "Protect capture data"
    Voice captures can contain telephone numbers, names, internal addressing, SIP identities, authentication exchanges, and recoverable audio when RTP is unencrypted. Collect the smallest necessary window, store it securely, and sanitize it before sharing.

## Choose the Capture Point

The same call can look different at each point:

```text
Phone -- CUCM -- CUBE inside -- CUBE outside -- Carrier
  A        B          C              D             E
```

Choose based on the question:

- **A:** What did the phone send or receive?
- **B:** What did CUCM signal, and where did it expect media?
- **C and D:** What did CUBE change between call legs?
- **E:** What did the carrier actually receive?

A capture from only one side of CUBE cannot prove what CUBE transmitted on the other side.

## Build a Capture Record

Record:

- exact start and stop time with timezone;
- calling and called numbers;
- expected protocol and peer addresses;
- capture interface and direction;
- test-call result;
- whether signaling or media encryption is enabled;
- who authorized collection and where the file is stored.

## Useful Wireshark Display Filters

```text
sip
rtp
rtcp
h225
h245
mgcp
ip.addr == 192.0.2.20
udp.port == 5060
tcp.port == 5060
sip.Call-ID == "example-call-id"
```

Port `5060` is common for unencrypted SIP but is not universal. TLS commonly uses another configured port, and SIP can use UDP, TCP, or TLS. Filter by observed addresses and protocol rather than assuming one port.

Wireshark may need to be told to decode a nonstandard port as SIP or RTP. Encrypted signaling or media limits what can be inspected without approved keys and decryption procedures.

## Successful SIP Call

Follow one dialog:

1. Find the initial INVITE.
2. Record source, destination, transport, Request-URI, From, To, asserted identity, and Call-ID.
3. Inspect the SDP offer.
4. Follow `100`, `180` or `183`, and `200` responses.
5. Inspect the SDP answer.
6. Confirm the ACK.
7. Identify both RTP address and port pairs.
8. Confirm RTP flows in both directions.
9. Inspect re-INVITEs or UPDATEs during hold, transfer, or codec change.
10. Identify which endpoint sent BYE and whether it received `200 OK`.

```text
INVITE -> 100 -> 180/183 -> 200 -> ACK -> RTP -> BYE -> 200
```

## SIP 488: Media Negotiation Failure

A `488 Not Acceptable Here` commonly points to SDP or media-policy disagreement.

Compare:

- offered and accepted codecs;
- packetization;
- DTMF payload and method;
- SRTP requirement;
- fax or T.38 offer;
- media direction attributes;
- address family and reachable media address;
- CUCM region and required transcoder or MTP.

Find the device that generated the 488. A CUBE-forwarded response may have originated from the carrier or from local policy.

## Wrong SDP Address and One-Way Audio

Example failure:

```text
SIP signaling reaches peer successfully
SDP advertises media address 198.51.100.25
peer sends RTP to that address
routing or firewall cannot return traffic
```

Check each SDP `c=` and `m=` line, then locate matching UDP packets. If only one direction appears, determine whether packets were never sent, sent to the wrong address, dropped between points, or received but not played.

NAT, VRFs, source binding, media anchoring, and asymmetric routing are common causes.

## RTP Analysis

Wireshark can decode RTP streams and report sequence, jitter, loss, timing, and payload information.

Inspect each direction separately:

| Field | What it tells you |
|---|---|
| Source and destination | Actual media endpoints and direction |
| UDP ports | Negotiated media sockets |
| Payload type | Codec or telephone-event mapping from SDP |
| Sequence number | Gaps and reordering |
| Timestamp | Media clock progression and packetization |
| Delta time | Arrival spacing and jitter symptoms |
| DSCP | Observed QoS marking at the capture point |
| Packet count | Whether media was sent and received |

A sequence gap at one capture point does not prove where loss occurred. Compare captures before and after the suspected link or queue.

## DTMF with RTP-NTE

When SDP advertises `telephone-event`, keypad presses may appear as RTP named events rather than audible tones.

Validate:

- both sides advertise compatible telephone-event payloads;
- the payload number in RTP matches the SDP mapping;
- event duration and end packets are present;
- CUBE, MTP, or transcoder interworking preserves the event;
- the receiving IVR interprets the same method.

Do not publish captured digits because they may contain account numbers, meeting PINs, or authentication data.

## Early Media

`183 Session Progress` can include SDP that establishes media before final answer. Use this for carrier announcements or ringback.

If users hear silence before answer:

- check for `183` and SDP;
- verify RTP from the early-media endpoint;
- check CUCM and CUBE early-offer policy;
- inspect whether a firewall opens media before `200 OK`;
- check whether local ringback was expected instead.

## Hold and Resume

SIP can signal hold using direction attributes such as `sendonly`, `recvonly`, or `inactive`, sometimes with address changes.

Follow re-INVITEs and SDP through:

1. initial connection;
2. hold request and response;
3. expected music-on-hold media source;
4. resume request and response;
5. restored bidirectional RTP.

A call that fails only after hold or transfer often involves media-resource, SDP, firewall, or normalization behavior not exercised during basic setup.

## H.323 Capture

For a legacy H.323 call, correlate:

- H.225 call setup and clearing;
- H.245 capability exchange;
- fast-start or separate channel behavior;
- negotiated codec and media channels;
- RTP addresses and ports;
- DTMF capability;
- disconnect cause.

A CUBE or gateway may tunnel H.245 or use fast-start, so the exact sequence varies.

## MGCP Capture

For MGCP, identify:

- CUCM call-agent address;
- gateway endpoint identifier;
- commands and responses controlling the endpoint;
- requested events and notifications;
- connection parameters and media descriptors;
- retransmissions, timeouts, or endpoint mismatch.

Correlate the packet capture with CUCM gateway registration and the physical port state.

## Capture Comparison Worksheet

| Observation | Inside leg | Outside leg |
|---|---|---|
| Call-ID |  |  |
| Calling identity |  |  |
| Called destination |  |  |
| SIP transport |  |  |
| Response code |  |  |
| SDP address and port |  |  |
| Codec |  |  |
| DTMF method |  |  |
| Encryption |  |  |
| RTP packets each direction |  |  |
| DSCP |  |  |
| Disconnect origin and cause |  |  |

## Safe Collection Checklist

- [ ] Capture point answers a specific question.
- [ ] Time window contains one controlled test call.
- [ ] Capture filters do not exclude the expected media range.
- [ ] Clock and timezone are recorded.
- [ ] Collection is authorized.
- [ ] File permissions and retention are appropriate.
- [ ] Numbers, identities, IP addresses, DTMF, and authentication data are sanitized before sharing.
- [ ] RTP audio is treated as sensitive communication content.
- [ ] Temporary capture configuration is removed afterward.

Continue with [SIP and CUBE](sip-cube.md), [Voice QoS](qos-quality.md), and [CUCM Diagnostics](cucm-diagnostics.md).

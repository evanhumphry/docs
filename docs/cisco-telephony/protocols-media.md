# Voice Protocols and Media

Voice calls use signaling to establish and control sessions, then media to carry audio. Cisco environments commonly contain a mix of SIP, H.323, MGCP, SCCP, and RTP.

## Protocol Comparison

| Protocol | Model | Where routing logic usually lives | Operational position |
|---|---|---|---|
| **SIP** | Peer-to-peer signaling using requests and responses | CUCM, CUBE, gateway dial peers, and adjacent systems | Current, widely used |
| **H.323** | ITU protocol family for multimedia calls | CUCM and IOS gateway dial peers | Legacy but still encountered |
| **MGCP** | Controller and controlled gateway | CUCM controls gateway endpoints; router retains limited fallback/local behavior | Common in some CUCM gateway designs |
| **SCCP** | Cisco call-control protocol | CUCM controls registered endpoints and some media resources | Commonly associated with Cisco phones and registered media resources |
| **RTP** | Media transport | Negotiated by signaling; audio usually flows between media endpoints | Carries voice, not call setup |

!!! warning "Support varies"
    Confirm the exact router, voice module, DSP, license, CUCM release, and IOS XE feature support. Do not assume that a legacy ISR H.323 configuration can be moved unchanged to a Catalyst 8200L.

## H.323

H.323 is a legacy multimedia signaling family used in older CUCM and gateway deployments.

- **H.225** handles call signaling and establishment.
- **H.245** negotiates capabilities and logical media channels, including codecs and some DTMF capabilities.
- **RTP** normally carries the audio after signaling establishes the call.

```text
CUCM                         H.323 Gateway
  |------ H.225 setup ------------>|
  |<----- H.225 progress/connect --|
  |<==== H.245 capabilities ======>|
  |<========= RTP audio ==========>|
```

Exact sequencing changes when fast-start, tunneling, media resources, or interworking features are involved.

### CUCM and H.323 Gateway Identity

A CUCM H.323 gateway is generally configured with an address that CUCM uses as the signaling peer. This is not the same controller registration model used by MGCP. A separate H.323 gatekeeper design can involve registration, but a direct CUCM-to-gateway deployment does not require the IOS gateway to register to CUCM as an MGCP endpoint would.

### Source-Address Binding

CUCM may expect H.323 signaling from the address configured on its gateway object. Binding helps make the gateway use a stable source address:

```ios
interface Loopback0
 ip address 192.0.2.11 255.255.255.255
 h323-gateway voip interface
 h323-gateway voip bind srcaddr 192.0.2.11
```

The command context and support can vary. Verify the source address with packet capture or call signaling, and confirm two-way routing between CUCM and the bound interface.

### H.323 Operational Checks

```ios
show dial-peer voice summary
show call active voice brief
show call history voice brief
show running-config | section ^dial-peer voice
```

When migrating, check codec, DTMF, number presentation, fast-start or slow-start expectations, source binding, firewall policy, and supplementary services. Prefer SIP for a new design unless a validated requirement dictates otherwise.

## SIP and SDP

Session Initiation Protocol (SIP) establishes, modifies, and clears sessions. Session Description Protocol (SDP), carried within SIP messages, advertises media addresses, ports, codecs, and related capabilities.

```text
CUCM or CUBE                         SIP Gateway
     |----------- INVITE + SDP ---------->|
     |<---------- 18x response -----------|
     |<---------- 200 OK + SDP -----------|
     |-------------- ACK ---------------->|
     |<============ RTP =================>|
     |-------------- BYE ---------------->|
     |<----------- 200 OK ----------------|
```

A basic SIP dial peer can make the protocol explicit:

```ios
dial-peer voice 3000 voip
 description Four-digit destinations to CUCM
 destination-pattern [1-8]...
 session protocol sipv2
 session target ipv4:192.0.2.20
 dtmf-relay rtp-nte
 voice-class codec 1
 no vad
```

Real SIP designs may also require SIP server groups, OPTIONS keepalives, tenant or trunk profiles, TLS, certificate trust, authentication, URI matching, early-offer policy, normalization, and CUBE licensing. Use release-specific configuration guides.

### SIP Troubleshooting Questions

- Did the INVITE reach the intended peer?
- Which calling and called numbers appear in the Request-URI and headers?
- Did the peer return a provisional response and final response?
- Does SDP offer an address and port reachable from the other media endpoint?
- Is there a common codec?
- Do both sides agree on DTMF transport?
- Did a firewall, NAT device, or SIP inspection feature rewrite signaling or media information?

## MGCP

Media Gateway Control Protocol (MGCP) uses a controller model. CUCM acts as the call agent and controls gateway endpoints. Analog ports and digital spans are represented more directly in CUCM than they are with an autonomous H.323 or SIP gateway.

```text
CUCM call agent
    |
    | MGCP control
    v
Cisco gateway endpoint
    |
    v
FXS, FXO, or digital circuit
```

With MGCP, more call-control logic resides in CUCM. With H.323 or SIP, the router uses dial peers for more local routing and call-leg treatment.

Common checks include gateway registration state in CUCM, endpoint identity, name and domain consistency, IP reachability, interface binding, clocking for digital circuits, and fallback configuration where Survivable Remote Site Telephony or MGCP fallback is designed.

## SCCP

Skinny Client Control Protocol (SCCP) is a Cisco call-control protocol. It is commonly associated with Cisco phones and with some DSP-based resources, such as transcoders or conference bridges, that register to CUCM.

SCCP differs from SIP or H.323 gateway trunks. When troubleshooting a media resource, verify both its IOS configuration and its registration and availability in CUCM.

## RTP and Media

RTP carries real-time audio. Real-time Transport Control Protocol (RTCP) can report quality and session statistics. Signaling may pass through CUCM while RTP flows directly between endpoints, or a media resource may anchor the media.

### One-Way or No Audio

Check:

1. IP routing in both directions between the advertised media addresses.
2. Access lists, stateful firewalls, and security policy for the negotiated UDP ports.
3. NAT and whether SDP or H.245 advertises reachable addresses.
4. Codec agreement and packetization.
5. DSP availability on analog or transcoded call legs.
6. MTP, transcoder, conference bridge, or CUBE media anchoring.
7. Asymmetric routing and interface or VRF selection.
8. Whether packets leave and return on the expected interfaces.

A successful ring and answer proves signaling, not audio reachability.

## Codecs and Voice-Class Codec

Common codecs include:

- **G.711 µ-law or A-law:** Higher bit rate and little compression.
- **G.729:** Lower bit rate and more compression; check licensing, DSP, and endpoint support.

A reusable preference list can be applied to supported VoIP dial peers:

```ios
voice class codec 1
 codec preference 1 g711ulaw
 codec preference 2 g729r8
```

CUCM regions influence the codec or bandwidth relationship between devices. CUCM locations provide call-admission bandwidth policy. A codec mismatch may require a transcoder if one is configured, registered, available, and allowed by the Media Resource Group List.

## DTMF Relay

DTMF relay determines how keypad tones cross an IP call leg. Common methods include:

- RTP named telephone events, often `rtp-nte`;
- H.245 alphanumeric or signal methods in H.323;
- SIP signaling methods where supported;
- in-band audio when codec and network conditions preserve the tones.

Test DTMF against the actual destination, such as voicemail or an IVR. Audio working does not prove DTMF interworking works.

## VAD

Voice Activity Detection suppresses packet transmission during silence. Many Cisco voice dial peers disable it:

```ios
no vad
```

Do not treat this as a universal template. Confirm bandwidth policy, platform behavior, and the adjacent system requirements.

## DSP, PVDM, MTP, and Transcoding

- **DSP:** Real-time processor for voice termination, codec work, transcoding, and conferencing.
- **PVDM:** Cisco module that supplies DSP resources on supported platforms.
- **Transcoder:** Converts one codec to another, such as G.729 to G.711.
- **MTP:** Media Termination Point that can assist with DTMF, supplementary-service, protocol, or media interworking.

```text
G.729 endpoint -> Transcoder/DSP -> G.711-only service
```

Resource selection depends on CUCM media-resource configuration, Media Resource Groups, Media Resource Group Lists, device pools, codec policy, protocol details, and current capacity. DSP exhaustion can allow signaling to begin but prevent a call from establishing media or completing through an analog or digital interface.

Continue with [CUCM Call Routing](cucm-routing.md), [Call Flows](call-flows.md), and [Troubleshooting](troubleshooting.md).

# Telephony Fundamentals

## Stations and Trunks

A **station** is an endpoint used by a person or device. Examples include an analog telephone, fax machine, modem, paging adapter, or IP phone.

A **trunk** carries calls between telephony systems. Examples include an analog PSTN line, a T1 or E1 circuit, a SIP trunk, or an intercluster trunk.

The distinction matters because a station-facing interface and a network-facing trunk provide and expect different electrical or signaling behavior.

## Calling and Called Numbers

| Term | Meaning | Practical use |
|---|---|---|
| **Calling number** | The number associated with the originator | Caller ID, policy, billing, and return calls |
| **Called number** | The destination that was dialed | Route selection and destination lookup |
| **ANI** | Automatic Number Identification, commonly used to mean the calling number | Identifies the calling party to a carrier or receiving system |
| **DNIS** | Dialed Number Identification Service, commonly used to mean the called number | Identifies which published number the caller reached |

Do not assume that the displayed caller ID is the unmodified ANI. CUCM, the gateway, or a carrier may transform calling and called numbers at several points in the call.

## Signaling and Media

**Signaling** establishes, modifies, and clears a call. SIP and H.323 are signaling protocol families. MGCP lets CUCM control gateway endpoints using a controller model.

**Media** carries the actual audio. In IP voice deployments, Real-time Transport Protocol (RTP) usually carries that audio after signaling establishes the session.

```text
Signaling:  CUCM  <-------------------->  Gateway
              negotiates and controls

Media:     Phone <======= RTP ========>  Gateway
                       audio
```

A call can signal successfully while media fails. This commonly appears as one-way audio or no audio after the called party answers.

## Call Legs

A **call leg** is one side of a call from the perspective of a gateway. A routed call normally has an inbound leg and an outbound leg.

```text
CUCM
  |
  | VoIP call leg
  v
Cisco Gateway
  |
  | POTS call leg
  v
FXO
  |
  v
PSTN
```

The inbound dial peer describes and controls how the call entered the router. The outbound dial peer controls where the router sends it next. Codecs, DTMF relay, number manipulation, and other treatment can differ between the two legs.

## Analog and Digital Voice

**Analog voice** represents audio as a continuously varying electrical signal. FXS and FXO ports are common analog interfaces.

**Digital voice** samples and encodes audio as data. T1 and E1 voice circuits, IP telephony, and RTP transport are digital even when an analog endpoint exists at one edge.

A gateway converts between these domains when necessary:

```text
Analog phone -> FXS -> DSP/codec processing -> RTP/IP -> CUCM
```

## On-Hook, Off-Hook, Ringing, and Supervision

- **On-hook:** The analog endpoint is idle.
- **Off-hook:** The endpoint has seized the line, such as when a handset is lifted.
- **Ringing:** The station-facing side applies ringing voltage to alert an endpoint.
- **Supervision:** Electrical state changes indicate seizure, answer, and disconnect. Exact behavior depends on signaling type and carrier or PBX implementation.

Correct supervision is essential. A mismatched port signaling configuration can cause calls that do not answer, do not disconnect, or show unreliable caller ID.

## DTMF

Dual-tone multifrequency (DTMF) is the keypad signaling used to enter digits after a call is established. IVRs, voicemail, conferencing systems, and automated attendants depend on it.

On an IP call, DTMF may be carried:

- in the audio stream;
- as RTP named telephone events, commonly configured as `rtp-nte`;
- through signaling methods such as H.245 alphanumeric or SIP NOTIFY, depending on the protocol and endpoint support.

A call can have normal two-way audio while DTMF fails because the two call legs do not agree on a relay method.

## Codecs, DSPs, and Bandwidth

A **codec** encodes and decodes audio. Common Cisco voice environments use G.711 and G.729.

- **G.711:** Higher bandwidth, minimal compression, and commonly used on LANs.
- **G.729:** Lower bit rate and greater compression; licensing and platform support must be checked.

A **DSP** performs real-time voice processing such as codec termination, transcoding, and conferencing. A **PVDM** is Cisco hardware that supplies DSP resources on supported platforms.

Codec selection affects bandwidth, audio quality, packetization, and DSP consumption. Signaling can complete while media setup fails because required codec or DSP resources are unavailable.

## PSTN and Hairpin Calls

The **Public Switched Telephone Network (PSTN)** is the traditional public telephone network.

A **hairpin call** enters a gateway and leaves the same gateway on another call leg. For example, a call can arrive from CUCM on a VoIP leg and leave through an FXO port on a POTS leg. Troubleshoot each leg separately.

## Next Steps

- Learn the electrical sides in [Analog Voice Ports](analog-ports.md).
- Learn call-leg selection in [Dial Peers](dial-peers.md).
- Compare signaling families in [Protocols and Media](protocols-media.md).
- Trace complete examples in [Call Flows](call-flows.md).

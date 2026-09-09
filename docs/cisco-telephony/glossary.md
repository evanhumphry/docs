# Cisco Telephony Vocabulary Reference

Use this glossary while reading CUCM and IOS or IOS XE configurations. Follow the links for operational detail and examples.

| Term | Plain-English definition | Practical Cisco meaning |
|---|---|---|
| **ANI** | Automatic Number Identification | Usually the calling number delivered with a call; it may be transformed before reaching the destination. |
| **Answer address** | An inbound dial-peer matching criterion | Generally compares the calling number against `answer-address`. See [Dial Peers](dial-peers.md). |
| **Called number** | The destination number | Drives CUCM digit analysis and outbound dial-peer matching. |
| **Calling number** | The originating number | Used for caller ID, policy, transformations, and some inbound matches. |
| **Call leg** | One side of a call | A gateway call normally has an inbound and outbound leg, each with its own dial peer and treatment. |
| **Codec** | A method for encoding and decoding audio | Determines media format, bandwidth, quality, and possible DSP or transcoder requirements. |
| **CUBE** | Cisco Unified Border Element | IOS XE session border controller functions used for SIP interconnection, demarcation, security, normalization, and media services when licensed and supported. |
| **CUCM** | Cisco Unified Communications Manager | Cisco call-control platform that performs digit analysis, device control, routing, and media-resource selection. |
| **CSS** | Calling Search Space | Ordered set of partitions a device, line, or routing object can search. Controls reachability. |
| **Destination pattern** | A called-number pattern on a dial peer | Makes an outbound dial peer a candidate; for example, `[1-8]...` matches four digits beginning with 1 through 8. |
| **Dial peer** | A voice call-leg routing and treatment rule | Defines matching, destination, protocol, codec, DTMF, translation, and other behavior on IOS or IOS XE. |
| **Dial-peer hunt** | Selection among eligible outbound dial peers | Uses match specificity, preference, peer state, failure conditions, and configured hunt behavior. |
| **Directory number** | A line or destination number in CUCM | Belongs to a partition and is reachable through an appropriate CSS. |
| **DNIS** | Dialed Number Identification Service | Usually the called number that identifies which destination or published service was reached. |
| **DSP** | Digital Signal Processor | Hardware that performs real-time codec, voice termination, transcoding, and conferencing work. |
| **DTMF** | Dual-tone multifrequency keypad signaling | Must cross IP legs through a compatible in-band or relay method for IVRs and voicemail to work. |
| **DTMF relay** | A method for carrying keypad events over an IP call | Examples include RTP-NTE and H.245 methods; both call legs must interwork correctly. |
| **FXO** | Foreign Exchange Office | Analog port that connects toward a carrier or PBX line and receives battery and dial tone. |
| **FXS** | Foreign Exchange Station | Analog port that serves a station and supplies battery, dial tone, and ringing. |
| **Forward digits** | Controls digits sent on a POTS call leg | `forward-digits all` sends all digits; a number sends the specified rightmost digit count. |
| **Gateway bind source address** | Stable source address for voice signaling or media | Helps the adjacent system recognize and route to the intended gateway address. Syntax and support vary by protocol and release. |
| **H.225** | H.323 call-signaling component | Handles call establishment and clearing. |
| **H.245** | H.323 capability and media-channel control | Negotiates codecs, logical channels, and related capabilities. |
| **H.323** | Legacy multimedia signaling family | Used by older CUCM gateway deployments; the router commonly performs local dial-peer routing. |
| **Hairpin call** | A call that enters and leaves the same gateway | Still consists of separate inbound and outbound call legs that must be traced independently. |
| **Inbound dial peer** | Dial peer associated with the arriving call leg | Can affect codec, DTMF, translation, media, and other call treatment. |
| **Incoming called number** | Inbound match against the called number | `incoming called-number` helps classify calls as they arrive. |
| **Location** | CUCM call-admission bandwidth policy object | Can restrict call bandwidth between sites or logical locations. |
| **MGCP** | Media Gateway Control Protocol | Lets CUCM act as call agent and control gateway endpoints directly. |
| **MRGL** | Media Resource Group List | Ordered access to groups containing MTPs, transcoders, conference bridges, and other media resources. |
| **MTP** | Media Termination Point | Media/signaling interworking resource used in some DTMF, supplementary-service, and protocol scenarios. |
| **Outbound dial peer** | Dial peer selected for the departing call leg | Determines where IOS sends the call, such as a port, trunk group, or IP session target. |
| **Partition** | CUCM logical grouping for dial-plan entries | A pattern is reachable only when the relevant CSS can search its partition. |
| **PLAR** | Private Line Automatic Ringdown | Automatically originates a call to a configured destination when a voice port becomes active. |
| **PLAR destination** | Number automatically called by PLAR | In `connection plar 6985`, the destination is `6985`. |
| **POTS** | Plain Old Telephone Service | Traditional analog or circuit voice domain represented by a POTS dial peer. |
| **POTS dial peer** | Traditional telephony call-leg rule | Routes toward analog ports, trunk groups, or digital voice circuits. |
| **Preference** | Tie-breaking priority among equivalent dial-peer matches | Lower values are preferred after match specificity is considered. |
| **Prefix** | Digits added before a POTS call is sent | `prefix 1` adds a leading `1` to the forwarded digits. |
| **PSTN** | Public Switched Telephone Network | Traditional public telephone network reached through carrier trunks or lines. |
| **PVDM** | Packet Voice Digital Signal Processor Module | Cisco hardware that supplies DSP capacity on supported platforms. |
| **Region** | CUCM codec relationship object | Influences codec or audio-bandwidth choices between devices. |
| **Route group** | CUCM collection of gateways or trunks | Provides ordered or distributed member selection for a route list. |
| **Route list** | CUCM ordered collection of route groups | Provides a sequence of routing paths and failover choices. |
| **Route pattern** | CUCM dialed-number routing rule | Matches digits and sends calls toward a route list, gateway, or trunk. |
| **RTP** | Real-time Transport Protocol | Usually carries audio after SIP, H.323, or another signaling method establishes a call. |
| **SCCP** | Skinny Client Control Protocol | Cisco call-control protocol used by phones and some registered media resources. |
| **SDP** | Session Description Protocol | Describes media addresses, ports, codecs, and capabilities inside SIP messages. |
| **Session target** | IP destination for a VoIP dial peer | For example, `session target ipv4:192.0.2.20`. |
| **SIP** | Session Initiation Protocol | Widely used signaling protocol for CUCM trunks, gateways, CUBE, carriers, PBXs, and phones. |
| **Transcoding** | Converting media from one codec to another | Uses DSP resources and may be selected through CUCM media-resource policy. |
| **Translation profile** | Container that applies number-translation rules | Can apply calling or called-number transformations to a dial peer or call leg. |
| **Translation rule** | Pattern-based telephone-number rewrite | Normalizes, adds, removes, or replaces digits for routing or carrier requirements. |
| **Trunk** | Connection between telephony systems | Can be analog, digital, SIP, H.323, intercluster, or another supported type. |
| **Trunk group** | Logical collection of physical voice ports | Lets a POTS dial peer select an available port from the group. |
| **Trunk-group preference** | Member selection order inside a trunk group | Lower member preference values are generally tried first. |
| **VAD** | Voice Activity Detection | Can suppress transmission during silence; `no vad` disables it on supported dial peers. |
| **Voice-class codec** | Reusable codec preference list | Applied to supported VoIP dial peers to control codec offer or preference. |
| **Voice port** | Physical telephony interface | Represents an analog or digital port such as FXS or FXO on a router or voice gateway. |
| **VoIP dial peer** | IP voice call-leg rule | Routes calls toward CUCM, CUBE, another gateway, carrier, or IP endpoint. |

## Memory Aids

- **FXS serves the station.**
- **FXO points toward the office or carrier side.**
- **CSS searches partitions.**
- **Signaling establishes the call; RTP carries the media.**
- **Every routed gateway call has an inbound and outbound call leg.**

Start with [Telephony Fundamentals](fundamentals.md), [Analog Voice Ports](analog-ports.md), and [Dial Peers](dial-peers.md).

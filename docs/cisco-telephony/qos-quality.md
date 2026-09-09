# Voice QoS and Call Quality

Voice quality depends on predictable packet delivery. A call may establish correctly and still sound poor because RTP encounters congestion, delay, jitter, loss, reordering, or an incorrect QoS policy.

## Four Measurements

| Measurement | Meaning | User experience when excessive |
|---|---|---|
| **Latency** | Time for audio to travel from speaker to listener | Talk-over, awkward pauses, delayed conversation |
| **Jitter** | Variation in packet arrival time | Choppy or uneven audio when buffers cannot compensate |
| **Packet loss** | RTP packets that never arrive in time | Gaps, clicks, robotic audio, or silence |
| **Reordering** | Packets arriving out of sequence | Loss-like artifacts and jitter-buffer stress |

Also inspect codec, packetization interval, echo, gain, clipping, and analog supervision. Not every voice-quality problem is an IP QoS problem.

## Signaling Versus Media

```text
SIP or H.323 signaling: establishes and controls the call
RTP media: carries the actual audio
```

Signaling and RTP can use different addresses, ports, and paths. Prioritize both appropriately, but reserve strict priority treatment for bounded real-time traffic rather than placing all voice-related traffic in one unlimited priority class.

## Classification and Marking

A common enterprise design marks RTP bearer traffic with DSCP EF and voice signaling with a separate signaling class such as CS3 or another value defined by organizational policy. Do not copy markings without confirming the end-to-end design.

The trust boundary answers: **Where does the network begin believing packet markings?**

Possible trust boundaries include:

- the IP phone;
- the access switch port;
- the CUCM, CUBE, or gateway interface;
- an enterprise WAN edge;
- a carrier handoff.

At an untrusted boundary, classify by controlled attributes and remark traffic. Do not trust arbitrary DSCP from user devices or an untrusted network.

## End-to-End QoS Path

```text
Phone -> access switch -> campus -> WAN edge -> provider -> WAN edge -> gateway
 mark       trust/queue      preserve     shape/LLQ       SLA      LLQ/shape
```

A single correctly configured router does not provide end-to-end QoS. Verify marking, queueing, shaping, and capacity at every congestion point.

## Low-Latency Queuing

Low-Latency Queuing (LLQ) gives a bounded real-time class priority access during congestion. The priority class must be sized for the expected simultaneous calls, codec, packetization, Layer 2 overhead, and growth.

Too little bandwidth causes drops during normal load. Too much unbounded priority traffic can starve other applications. Police or bound the class according to the design.

## Shaping Before Queueing

When the physical interface speed exceeds the contracted WAN rate, shape to the actual service rate so congestion occurs in the router's managed queues instead of an uncontrolled provider policer.

```text
Fast physical interface
        |
        v
Parent shaper at provider rate
        |
        v
Child policy with voice priority and other classes
```

Hierarchical QoS syntax and support vary by platform and interface type. Validate the policy against the installed IOS XE release.

## Bandwidth Planning

Codec bit rate is only part of the bandwidth consumed by a call. Include:

- IP, UDP, and RTP headers;
- Layer 2 encapsulation;
- packetization interval;
- encryption overhead;
- tunnel overhead;
- call signaling;
- expected concurrency;
- failover and growth margin.

Use a validated calculator or lab capture for the actual codec and encapsulation instead of relying on the codec name alone.

## Codec and Packetization Effects

Shorter packetization intervals create more packets per second and more header overhead, but reduce the audio represented by one lost packet. Longer intervals reduce overhead but increase delay and the audible effect of loss.

Transcoding can add processing and delay. Confirm whether CUCM inserted a transcoder, MTP, conference bridge, or recording resource into the media path.

## Jitter Buffers

A jitter buffer temporarily holds packets to smooth arrival variation. If it is too small, late packets are discarded. If it grows too large, conversational delay increases.

Treat repeated jitter-buffer underruns as evidence to inspect the network path, queueing, clocking, and packet arrival pattern, not just a reason to increase the buffer.

## Voice Quality Troubleshooting

### 1. Define the Scope

- One user or many?
- One direction or both?
- Internal, PSTN, voicemail, or conference calls?
- Constant or only during busy periods?
- One site, WAN circuit, carrier, codec, or gateway?

### 2. Separate Signaling from Media

Identify the actual RTP endpoints from SDP, H.245, active-call output, or packet capture. CUCM may not be in the media path.

### 3. Inspect Both Directions

A good inbound stream does not prove the outbound stream is good. Collect loss, jitter, latency, codec, and packet counts separately for each direction.

### 4. Check Interfaces and Queues

```ios
show interfaces
show policy-map interface
show class-map
show policy-map
```

Look for physical errors, drops, queue depth, priority-class drops, policing, shaping, and whether packets match the intended class.

### 5. Check the Active Call

```ios
show call active voice brief
show voip rtp connections
```

Field availability varies by release. Confirm codec, media addresses, ports, packet counts, and the selected call legs.

### 6. Compare with a Packet Capture

Look for:

- expected DSCP markings;
- RTP sequence gaps;
- reordering;
- arrival-time variation;
- asymmetric media paths;
- ICMP errors or fragmentation;
- unexpected codec or packetization;
- silence caused by no packets versus packets carrying silence.

## Symptom Map

| Symptom | Likely areas to investigate |
|---|---|
| Choppy audio during busy periods | Queue drops, undersized LLQ, missing shaping, provider policing |
| One-way audio | Routing, ACL, firewall, NAT, wrong SDP/H.245 address, VRF or binding |
| Delay and talk-over | Long network path, congestion, large jitter buffer, transcoding, satellite path |
| Echo | Analog hybrid, impedance, gain, delay, echo canceller behavior |
| Clipping at the start of speech | VAD, jitter buffer, media cut-through, early-media handling |
| Robotic sound | Loss, jitter, codec impairment, DSP or packetization issues |
| Good internal calls, poor PSTN calls | Gateway, carrier, analog circuit, codec conversion, WAN edge |
| Poor conference calls only | Conference bridge, transcoding, MRGL, resource load, mixed codecs |

## QoS Validation Checklist

- [ ] RTP and signaling classes are defined by policy.
- [ ] The trust boundary is documented for each access path.
- [ ] Markings are verified before and after every routed or switched domain.
- [ ] WAN shaping matches the actual provider service rate.
- [ ] LLQ capacity includes headers, encapsulation, concurrency, and margin.
- [ ] Priority traffic is bounded so it cannot starve other classes.
- [ ] Provider QoS treatment and remarking are documented.
- [ ] Failover paths provide equivalent capacity and policy.
- [ ] Monitoring alerts on interface errors, drops, queue drops, and abnormal utilization.
- [ ] A controlled load test proves policy behavior under congestion.

## Evidence Worksheet

| Item | Direction A to B | Direction B to A |
|---|---|---|
| Source and destination IP |  |  |
| UDP ports |  |  |
| Codec and packetization |  |  |
| DSCP observed |  |  |
| Packets sent/received |  |  |
| Loss |  |  |
| Jitter |  |  |
| Interface and queue |  |  |
| Media resource inserted |  |  |

Continue with [Packet-Capture Walkthroughs](packet-captures.md), [DSP and Media Resources](dsp-capacity.md), and [Troubleshooting](troubleshooting.md).

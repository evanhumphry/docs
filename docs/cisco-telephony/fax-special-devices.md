# Fax, Modem, Paging, and Special Analog Devices

A normal voice call does not validate a fax machine, modem, paging adapter, alarm panel, elevator phone, or door system. These devices can depend on tones, timing, supervision, gain, codec behavior, and carrier features that ordinary speech does not exercise.

## Inventory First

For every analog endpoint or line, record:

- device owner and business purpose;
- exact device type, model, and firmware;
- FXS or FXO handoff;
- cable and patch-panel location;
- voice gateway and port;
- extension, DID, and calling number;
- partition, CSS, device pool, and route dependencies;
- fax, modem, paging, or alarm protocol;
- power and battery-backup requirements;
- test procedure and acceptance owner;
- replacement or retirement plan.

Unknown analog lines are a migration risk. Trace and label them before moving hardware.

## Fax Transport Modes

### T.38 Fax Relay

T.38 demodulates fax tones at one gateway and transports fax information across the IP network as a fax relay protocol. The far gateway reconstructs the fax signal.

```text
Fax -> FXS gateway -> T.38 over IP -> gateway/carrier -> fax
```

Both call legs and intermediate systems must agree on T.38 negotiation and transport. SIP re-INVITEs commonly signal the transition from audio to fax, but exact behavior varies.

### Fax Pass-Through

Pass-through keeps the fax tones in an audio codec, commonly using G.711 with settings intended to preserve modem-like signals.

```text
Fax tones -> G.711 audio/RTP -> far endpoint
```

Pass-through is sensitive to loss, jitter, VAD, codec changes, and echo-processing behavior. It may work for a voice call while failing on multi-page fax transmission.

### Know the Carrier Requirement

A carrier may support T.38, pass-through, both, or neither for a specific trunk. Document:

- protocol and version;
- redundancy settings;
- codec fallback;
- error correction expectations;
- maximum fax rate;
- re-INVITE or offer requirements;
- NAT and firewall handling;
- tested page count and content.

## Modems

Modems, telemetry, alarm panels, point-of-sale devices, and other data-over-voice equipment are sensitive to compression, packet loss, jitter, clocking, echo cancellation, and gain.

Validate:

- whether the device is supported over the intended IP voice path;
- codec and pass-through requirements;
- VAD state;
- modem relay or named signaling support, if any;
- negotiated speed and stability;
- long-duration session behavior;
- carrier and application-owner acceptance.

A short handshake is not a complete test. Exercise the actual application transaction.

## Paging Adapters

Paging can use:

- an analog FXS port connected to a paging interface;
- an FXO-style interface that seizes a paging controller line;
- multicast IP paging;
- SIP paging endpoints or application servers.

For analog paging, test:

- seizure and answer supervision;
- DTMF zone selection;
- one-way audio direction;
- gain and clipping;
- disconnect and port release;
- timeout and busy behavior;
- access restrictions.

Paging interfaces can require dry contacts, relays, impedance matching, or specialized adapters not provided by a standard voice port.

## Elevator and Emergency Phones

Coordinate with facilities, life-safety, vendor, and regulatory owners. Verify:

- expected line type and battery behavior;
- automatic dialing or PLAR destination;
- location and callback identity;
- hands-free answer and disconnect;
- power-failure operation;
- monitoring and test interval;
- carrier migration approval;
- physical labeling and access.

Do not change or disconnect a life-safety circuit solely because it appears unused.

## Alarm and Security Panels

Some panels use modem-like signaling over analog lines. IP conversion, compression, or carrier changes can make them unreliable.

Before migration:

1. Identify the monitoring company and account owner.
2. Confirm supported line type and transport.
3. Place the system in an approved test state.
4. Trigger actual supervised events.
5. Confirm event receipt and restoration.
6. Document rollback and alternate communication path.

## Caller ID and Timing

Analog caller ID can be delivered between ringing cycles or according to country-specific signaling. Validate:

- carrier service is enabled;
- the voice module supports the required standard;
- port country and signaling settings are correct;
- calling-number translation preserves the number;
- receiving device supports the format;
- ring timing and answer behavior do not suppress delivery.

## Disconnect Supervision

Special devices can hold a line indefinitely if the gateway misses disconnect signaling. Possible mechanisms include battery denial, battery reversal, supervisory tones, or timing behavior supplied by the carrier or PBX.

Test:

- far party hangs up first;
- local device hangs up first;
- no-answer timeout;
- busy and reorder tones;
- carrier failure;
- repeated calls after release.

Do not tune detection by guesswork. Determine what the connected system actually supplies.

## Gain, Echo, and Impedance

Poor analog matching can produce low volume, clipping, echo, noise, or unstable modem and fax behavior.

Capture a baseline before changing:

- input and output level;
- endpoint type;
- cable length and condition;
- impedance and regional settings;
- echo-canceller behavior;
- codec and packetization;
- observed symptom in each direction.

Change one parameter at a time and keep rollback values.

## Troubleshooting Evidence

```ios
show voice port summary
show voice port 0/1/5
show call active voice brief
show call history voice brief
show voip rtp connections
show dial-peer voice summary
```

Release-specific DSP, fax, modem, SIP, and analog signaling commands may provide more detail. Use contextual help and the installed release command reference before enabling debugs.

## Acceptance Test Matrix

| Device class | Inbound | Outbound | DTMF | Caller ID | Long test | Disconnect | Power fail | Owner signoff |
|---|---|---|---|---|---|---|---|---|
| Fax |  |  | N/A |  |  |  |  |  |
| Modem/data device |  |  |  |  |  |  |  |  |
| Paging adapter |  |  |  |  |  |  |  |  |
| Elevator phone |  |  |  |  |  |  |  |  |
| Alarm panel |  |  |  |  |  |  |  |  |
| Door/intercom |  |  |  |  |  |  |  |  |

## Migration Checklist

- [ ] Every port has an owner and documented purpose.
- [ ] Exact FXS/FXO behavior is known.
- [ ] Fax or modem mode is agreed by both ends.
- [ ] Codec, VAD, echo, gain, and packetization requirements are documented.
- [ ] DTMF and caller ID are tested where required.
- [ ] Actual application transactions succeed repeatedly.
- [ ] Disconnect works in both directions.
- [ ] Battery backup and power-failure behavior are tested.
- [ ] Life-safety and monitoring owners approve the change.
- [ ] The old path remains available until acceptance is complete.

Continue with [Analog Voice Ports](analog-ports.md), [DSP and Media Resources](dsp-capacity.md), and [Migration Guides](migrations.md).

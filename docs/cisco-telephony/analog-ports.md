# Analog Voice Ports

A **voice port** is a physical telephony interface on a Cisco router or analog gateway.

```ios
voice-port 0/1/5
 description Example incoming analog line
```

Port numbering is platform and module dependent. Confirm the actual inventory and interface names on the target device instead of assuming that numbering will match an older gateway.

## FXS and FXO

### FXS: Foreign Exchange Station

An FXS port connects to an analog station such as:

- an analog telephone;
- a fax machine;
- a modem;
- an overhead paging adapter.

The FXS side normally provides battery voltage, dial tone, and ringing voltage to the endpoint.

**Memory aid:** FXS serves the station.

```text
Cisco FXS port  ->  analog telephone
provides power, dial tone, and ringing
```

### FXO: Foreign Exchange Office

An FXO port connects toward something that behaves like a telephone-company line, such as:

- a PSTN analog line;
- an analog PBX trunk;
- a line-side connection presented by another telephony system.

The FXO side receives battery and dial tone from the far side.

**Memory aid:** FXO connects toward the office or carrier side.

```text
Carrier or PBX line  ->  Cisco FXO port
provides battery and dial tone to the FXO interface
```

### The Pairing Rule

FXS connects to FXO. A telephone contains an FXO-type interface and expects service from an FXS port. A router FXO port expects service from a carrier or PBX FXS-style line interface.

## Voice-Port Configuration

```ios
voice-port 0/1/5
 description Example incoming line
 caller-id enable
 connection plar 6985
 no shutdown
```

- `description` documents the circuit or purpose.
- `caller-id enable` enables caller-ID handling where supported by the hardware, signaling type, and IOS XE release.
- `connection plar 6985` automatically originates a call toward destination `6985` when this voice port is seized.
- `no shutdown` administratively enables the port.

!!! note "Configuration varies"
    Country-specific tones, impedance, gain, supervisory signaling, caller-ID format, and disconnect behavior may require additional settings. Validate them against the carrier handoff and the exact interface documentation.

## Inspect Voice Ports

```ios
show voice port summary
show voice port 0/1/5
show running-config | section ^voice-port
show inventory
```

Use the output to answer:

- Is the port administratively enabled?
- Is it on-hook, off-hook, ringing, or seized?
- Which signaling type is configured?
- Does the hardware detect battery or supervisory state as expected?
- Is caller ID enabled where required?
- Does the port have PLAR or trunk-group configuration?
- Does the physical port and module actually exist on this platform?

## Trunk Groups

A **trunk group** is a logical group of physical voice ports. A POTS dial peer can reference the group instead of a single FXO port, allowing IOS to choose a member.

```ios
trunk group PSTN-FXO
!
voice-port 0/1/2
 description Primary outbound PSTN FXO
 trunk-group PSTN-FXO 1
!
voice-port 0/1/3
 description Backup outbound PSTN FXO
 trunk-group PSTN-FXO 2
```

Notice the three command forms:

- `trunk group` defines the group in global configuration where required by the release.
- `trunk-group` adds a physical voice port to the group.
- `trunkgroup` points a POTS dial peer at the group.

The final number under each voice port is the member preference. Lower values are generally selected first, subject to port availability and the configured hunt behavior.

A POTS dial peer can then reference the group:

```ios
dial-peer voice 911 pots
 destination-pattern 911
 trunkgroup PSTN-FXO
 forward-digits all
```

Trace the selection with [Dial Peers and Digit Manipulation](dial-peers.md) and the commands on the [Troubleshooting](troubleshooting.md) page.

## PLAR

PLAR means **Private Line Automatic Ringdown**. A PLAR-configured port automatically originates a call toward a predefined destination when the port becomes active.

```ios
voice-port 0/1/5
 description Example incoming analog line
 connection plar 6985
```

A common inbound FXO flow is:

```text
PSTN rings analog line
    |
    v
FXO 0/1/5 detects the incoming call
    |
    v
connection plar supplies called number 6985
    |
    v
IOS selects an outbound VoIP dial peer for 6985
    |
    v
Gateway signals CUCM
    |
    v
CUCM routes 6985 to the destination directory number
```

PLAR supplies a destination. It does not eliminate dial-peer matching, CUCM digit analysis, codec negotiation, or media setup.

Some platforms and releases also support `connection plar opx`. Off-premises extension (OPX) behavior can delay answer supervision toward an FXO line until the remote VoIP destination answers, instead of answering the analog leg as soon as routing begins. Confirm command availability and supervision behavior on the exact interface and test it with the actual carrier or PBX line.

## Common Problems

### The port never seizes

Check cabling, administrative state, signaling type, battery detection, and whether the installed NIM or service module is recognized.

### Inbound calls ring but never reach CUCM

Check the PLAR destination, inbound POTS call leg, outbound VoIP dial-peer match, session target, source-address expectations, and CUCM routing for the destination.

### Calls do not disconnect

Check supervisory signaling and disconnect detection. Carrier behavior and country-specific analog settings can affect this symptom.

### The wrong FXO line is selected

Inspect the outbound POTS dial peer, referenced trunk group, port preferences, port state, and global or dial-peer hunt behavior.

### Caller ID is missing

Confirm service from the carrier, the supported caller-ID standard and timing, port configuration, and whether calling-number translation removes or replaces the number later in the call.

# Call Flows and Configuration Walkthroughs

Call-flow diagrams connect CUCM routing, gateway dial peers, physical ports, signaling, and media into one troubleshooting model.

## Outbound PSTN Call

```text
Cisco Phone
    |
    | user dials 911
    v
CUCM digit analysis
    |
    v
Route Pattern 911
    |
    v
Route List -> Route Group
    |
    v
H.323 or SIP gateway
    |
    | inbound VoIP dial peer
    v
Cisco IOS XE call routing
    |
    | outbound POTS dial peer 911
    v
Trunk Group 1 -> FXO 0/1/2
    |
    v
PSTN
```

Trace it step by step:

1. The phone sends dialed digits to CUCM.
2. The caller's effective CSS determines which partitions CUCM can search.
3. CUCM matches the route pattern and selects a route-list and route-group path.
4. CUCM sends H.323 or SIP signaling to the gateway.
5. IOS selects an inbound VoIP dial peer for the arriving call leg.
6. IOS applies any inbound translation or call treatment.
7. IOS selects the best outbound POTS dial peer for the called number.
8. The POTS peer selects trunk group 1.
9. IOS chooses an available FXO member according to trunk-group and hunt behavior.
10. The FXO port seizes the analog line and sends the configured digits.

## Inbound Analog Call with PLAR

```text
PSTN
  |
  | analog ring
  v
FXO 0/1/5
  |
  | connection plar 6985
  v
IOS called number becomes 6985
  |
  | outbound VoIP dial peer
  v
CUCM
  |
  | CSS/partition and digit analysis
  v
Directory Number 6985
```

Possible failure points include ringing or supervision, port state, PLAR configuration, outbound dial-peer matching, session target, source-address binding, protocol negotiation, CUCM gateway or trunk state, CSS and partition reachability, DN state, and RTP routing.

## Annotated Gateway Example

This configuration is illustrative. Validate commands, hardware support, signaling, licenses, and release behavior before adapting it.

```ios
voice class codec 1
 codec preference 1 g711ulaw
!
trunk group 1
!
trunk group 5
!
voice-port 0/1/2
 description Primary outbound PSTN FXO
 trunk-group 1 1
 no shutdown
!
voice-port 0/1/3
 description Backup outbound PSTN FXO
 trunk-group 1 2
 no shutdown
!
voice-port 0/1/5
 description Example incoming analog line
 trunk-group 5 3
 caller-id enable
 connection plar 6985
 no shutdown
!
dial-peer voice 15 pots
 description Inbound call leg from FXO 0/1/5
 port 0/1/5
!
dial-peer voice 1000 voip
 description Inbound IP call legs from call-control system
 incoming called-number .
 voice-class codec 1
 no vad
!
dial-peer voice 911 pots
 description Emergency calls through analog trunk group
 destination-pattern 911
 trunkgroup 1
 forward-digits all
!
dial-peer voice 2000 voip
 description Four-digit destinations to primary CUCM server
 destination-pattern [1-8]...
 session target ipv4:192.0.2.20
 preference 1
 voice-class codec 1
 no vad
!
dial-peer voice 2001 voip
 description Four-digit destinations to secondary CUCM server
 destination-pattern [1-8]...
 session target ipv4:192.0.2.21
 preference 2
 voice-class codec 1
 no vad
```

### Line-by-Line Meaning

| Configuration | Meaning |
|---|---|
| `voice class codec 1` | Creates reusable codec preference list 1. |
| `codec preference 1 g711ulaw` | Makes G.711 µ-law the first codec in that list. |
| `trunk group 1` / `trunk group 5` | Defines logical voice-port groups used by POTS routing. |
| `voice-port 0/1/x` | Enters configuration for the specified physical analog voice port. |
| `description ...` | Documents the purpose of the port or dial peer without changing call behavior. |
| `trunk-group 1 1` | Adds the port to group 1 with member preference 1. Lower member preferences are normally tried first. |
| `caller-id enable` | Enables caller-ID handling where supported by the port, signaling, and release. |
| `connection plar 6985` | Supplies called number 6985 automatically when the port becomes active. |
| `no shutdown` | Administratively enables the voice port. |
| `dial-peer voice 15 pots` | Creates POTS dial peer tag 15 for the incoming analog call leg. |
| `port 0/1/5` | Associates that POTS peer with the physical port and can identify its inbound leg. |
| `dial-peer voice 1000 voip` | Creates an explicit inbound VoIP call-leg peer. |
| `incoming called-number .` | Broadly matches an inbound called number containing at least one digit. |
| `dial-peer voice 911 pots` | Creates outbound POTS dial peer tag 911. |
| `destination-pattern 911` | Makes the peer an outbound candidate for called number 911. |
| `trunkgroup 1` | Sends the POTS call to an available member of trunk group 1. |
| `forward-digits all` | Sends all called digits on the POTS leg. |
| `dial-peer voice 2000 voip` | Creates VoIP dial peer tag 2000. |
| `destination-pattern [1-8]...` | Matches four-digit destinations beginning with 1 through 8. |
| `session target ipv4:192.0.2.20` | Sends matching signaling toward the documented example address. |
| `preference 1` | Prefers this peer over an equivalent match with a higher value. |
| `voice-class codec 1` | Applies codec list 1 to the VoIP call leg. |
| `no vad` | Disables Voice Activity Detection on the VoIP call leg. |

The two VoIP dial peers use syntax commonly associated with an H.323-style gateway. A SIP design should explicitly configure and validate SIP protocol, DTMF, source binding, CUCM trunk settings, and any required CUBE features.

## Walkthrough: Incoming FXO Call to Extension 6985

1. The carrier applies ringing to the analog circuit connected to `0/1/5`.
2. The FXO port detects the call and goes active.
3. `connection plar 6985` supplies `6985` as the destination.
4. IOS evaluates outbound dial peers for `6985`.
5. Both VoIP peers `2000` and `2001` match `[1-8]...`.
6. Peer `2000` is preferred because it has preference `1`.
7. If the first peer is unavailable or a hunt-eligible failure occurs, IOS may try peer `2001`, subject to hunt and protocol behavior.
8. The gateway signals the selected CUCM server.
9. CUCM applies digit analysis using the trunk or gateway's effective CSS and the destination partition.
10. CUCM alerts directory number `6985`.
11. RTP is negotiated between media endpoints or through an inserted media resource.

## Walkthrough: Extension to Emergency Service

1. A phone dials `911`.
2. CUCM must match an emergency route with the correct CSS, transformations, notifications, and location policy.
3. CUCM sends the call to this gateway through the selected route path.
4. IOS receives the call on an inbound VoIP dial peer.
5. Outbound POTS peer `911` matches the called number.
6. `trunkgroup 1` selects an available FXO member, normally `0/1/2` before `0/1/3` based on the example preferences.
7. `forward-digits all` sends `911` to the analog line.
8. Signaling and two-way audio must be verified using an approved test procedure.

!!! danger "Emergency calling"
    Emergency calling is life-safety functionality. Use approved test numbers and procedures, coordinate with the carrier and public-safety requirements, confirm callback number and location delivery, and never place an unannounced live emergency call as a routine test.

## Number Trace Worksheet

Use this table for an actual call:

| Stage | Calling number | Called number | Selected object |
|---|---|---|---|
| Originating endpoint |  |  | Device and line CSS |
| CUCM digit analysis |  |  | Pattern and partition |
| Route selection |  |  | Route list and route group |
| Gateway inbound leg |  |  | Inbound dial peer |
| Gateway outbound leg |  |  | Outbound dial peer |
| Final interface |  |  | Port, trunk group, or session target |

Record observed values from CUCM traces, IOS call records, signaling, or packet capture. Do not fill the worksheet from memory.

## Validation Commands

```ios
show voice port summary
show dial-peer voice summary
show dialplan number 6985
show dialplan number 911
show call active voice brief
show call history voice brief
show running-config | section ^voice-port
show running-config | section ^dial-peer voice
```

Use [Troubleshooting and Commands](troubleshooting.md) for a controlled diagnostic workflow.

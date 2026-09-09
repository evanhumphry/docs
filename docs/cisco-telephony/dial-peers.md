# Dial Peers and Digit Manipulation

A **dial peer** is a Cisco IOS or IOS XE voice-routing rule. Dial peers classify call legs and define how calls enter or leave a gateway.

A routed call normally matches:

- one **inbound dial peer**, which describes how the call entered the router;
- one **outbound dial peer**, which determines where the router sends the call next.

```text
Source -> inbound call leg -> Cisco gateway -> outbound call leg -> destination
              dial peer                         dial peer
```

This call-leg model is the foundation of gateway troubleshooting.

## POTS and VoIP Dial Peers

### POTS Dial Peer

A POTS dial peer represents a traditional telephony call leg. POTS means Plain Old Telephone Service.

POTS dial peers commonly route calls toward:

- FXO or FXS ports;
- trunk groups;
- T1 or E1 circuits.

```ios
dial-peer voice 911 pots
 description Emergency calls to analog trunk group
destination-pattern 911
 trunkgroup 1
 forward-digits all
```

- `dial-peer voice 911 pots` creates POTS dial peer tag `911`. The tag identifies configuration and does not have to equal the dialed number.
- `destination-pattern 911` makes the peer an outbound candidate when the called number matches `911`.
- `trunkgroup 1` sends the call to an available voice port in trunk group 1.
- `forward-digits all` sends all called digits on the POTS leg.

### VoIP Dial Peer

A VoIP dial peer represents an IP-based call leg. It can send calls toward CUCM, another gateway, a CUBE, a SIP provider, or another supported endpoint.

Legacy H.323-style example:

```ios
dial-peer voice 2000 voip
 description Four-digit extensions to call-control server
 destination-pattern [1-8]...
 session target ipv4:192.0.2.20
 preference 1
 no vad
```

- `[1-8]...` matches a four-digit number whose first digit is 1 through 8.
- `session target` identifies the remote signaling destination.
- `preference 1` helps order otherwise valid matching peers.
- `no vad` disables Voice Activity Detection on this call leg.

For a SIP call leg, make the protocol explicit where the platform and release support it:

```ios
dial-peer voice 3000 voip
 description Four-digit extensions to CUCM subscriber
 destination-pattern [1-8]...
 session protocol sipv2
 session target ipv4:192.0.2.21
 dtmf-relay rtp-nte
 voice-class codec 1
 no vad
```

!!! warning "Do not paste legacy dial peers blindly"
    Default protocols, supported commands, codec syntax, media binding, and voice feature availability vary by platform and IOS XE release. Validate the full configuration on the intended Catalyst 8200L hardware and software release.

!!! warning "Prevent unintended call routing"
    Broad inbound matches and permissive outbound patterns can create toll-fraud exposure when signaling is reachable from an untrusted source. Restrict signaling with routing and firewall policy, use explicit inbound classification supported by the release, and permit only required destinations.

## Inbound Dial-Peer Matching

The inbound dial peer is selected as the call arrives. Depending on call type and available signaling information, IOS can use criteria including:

- `incoming called-number`, which matches the called number;
- `answer-address`, which generally matches the calling number;
- `destination-pattern`, which can participate in inbound matching against calling information;
- the associated voice port for POTS calls;
- URI or voice-class matching features on supported SIP configurations.

Example broad called-number match:

```ios
dial-peer voice 1000 voip
 description Inbound calls from call-control system
 incoming called-number .
```

The dot matches one wildcard digit. This pattern broadly matches called numbers containing at least one digit, but it is not the same as matching an empty or unavailable called number.

An inbound dial peer can control:

- codec selection and negotiation;
- DTMF relay;
- number translation;
- media and signaling behavior;
- call admission and treatment.

If no configured peer matches, IOS may use default dial peer 0. That often produces unexpected codec, DTMF, or media behavior, so identify the actual inbound match instead of assuming one.

## Outbound Dial-Peer Matching

For an outbound call leg, IOS compares the called number and other configured criteria against available peers. Number matching favors the most specific match. Preference helps order peers with equivalent destination-pattern matches.

```ios
dial-peer voice 2000 voip
 destination-pattern [1-8]...
 session target ipv4:192.0.2.20
 preference 1
!
dial-peer voice 2001 voip
 destination-pattern [1-8]...
 session target ipv4:192.0.2.21
 preference 2
```

The first peer is preferred when both are eligible. The second can provide an alternate path, subject to protocol state, hunt configuration, call-disconnect behavior, and release-specific logic.

Lower preference values are preferred. Preference does not make a less-specific number pattern beat a more-specific pattern.

## Destination Patterns

A `destination-pattern` describes called numbers that can select an outbound dial peer.

| Pattern | Meaning |
|---|---|
| `911` | Exactly `911` |
| `[1-8]...` | Four digits; first digit 1 through 8 |
| `9T` | `9` followed by a variable-length number, collected until timeout or termination |
| `....` | Any four digits |

The dot is a single-digit wildcard. Brackets define a set or range. `T` is a variable-length interdigit timeout match and can introduce post-dial delay if the dial plan is not designed carefully.

Inspect the result rather than reasoning from the configuration alone:

```ios
show dialplan number 6985
show dial-peer voice summary
```

## Incoming Called Number and Answer Address

`incoming called-number` primarily matches the called number on an inbound call leg:

```ios
dial-peer voice 1100 voip
 incoming called-number 6...
```

`answer-address` is an inbound matching method that generally compares the calling number:

```ios
dial-peer voice 1200 voip
 answer-address 5...
```

Calling or called information may be unavailable, transformed, or presented differently by the adjacent system. Confirm what IOS actually receives with call records or a controlled trace.

## Session Target

A session target identifies the remote destination for a VoIP dial peer:

```ios
session target ipv4:192.0.2.20
```

For SIP, deployments may use IP addresses, DNS names, SIP server groups, or other supported target mechanisms. Account for DNS, routing, source-address binding, TLS, and failover requirements where applicable.

## Digit Manipulation

Digit manipulation changes calling or called numbers by adding, removing, replacing, or normalizing digits. Always record the number before and after each stage.

### Simple POTS Manipulation

`forward-digits` controls which called digits leave a POTS call leg, while `prefix` adds digits before they are sent:

```ios
dial-peer voice 90 pots
 description Example ten-digit PSTN route
 destination-pattern 9[2-9].........
 port 0/1/2
 forward-digits 10
 prefix 1
```

For a matching dial string, this example forwards the rightmost ten digits and adds a leading `1`. Validate the actual result with the exact dialed number and release behavior.

### Voice Translation Rule and Profile

A translation rule rewrites a telephone number. A translation profile groups calling or called-number rules and applies them to a call leg.

```ios
voice translation-rule 10
 rule 1 /^9\(.*\)/ /\1/
!
voice translation-profile STRIP-ACCESS-CODE
 translate called 10
!
dial-peer voice 3000 voip
 translation-profile incoming STRIP-ACCESS-CODE
 incoming called-number 9T
```

This illustrative rule removes a leading `9` from the called number. IOS voice translation rules use their own pattern syntax, which is not identical to shell or PCRE syntax.

Test a rule before applying it:

```ios
test voice translation-rule 10 95551212
```

Translation can be applied inbound or outbound and to calling or called numbers. CUCM may also transform the same number, so document every transformation point to avoid double stripping or double prefixing.

## Dial-Peer Hunting

Dial-peer hunting controls how IOS selects among multiple matching outbound peers and what alternatives it tries after a failure. Hunt behavior is affected by:

- destination-pattern specificity;
- `preference` values;
- dial-peer operational state;
- cause codes or failure conditions;
- global or feature-specific hunt settings;
- protocol and release behavior.

Do not infer the chosen peer only from tag numbers or configuration order. Verify the match with `show dialplan number`, active calls, call history, and a controlled CCAPI trace when necessary.

## Forward Digits and Prefixes

POTS call legs commonly manipulate digits as the number is sent toward an analog or digital circuit.

```ios
forward-digits all
```

Sends all called digits.

```ios
forward-digits 10
```

Sends the rightmost ten digits.

```ios
prefix 1
```

Adds a leading `1` to the digits that the POTS call leg sends.

POTS dial peers can strip digits matched explicitly by the destination pattern. `forward-digits`, `prefix`, and other digit-manipulation features determine the final digits sent. Always verify the resulting number with a test or dial-plan inspection.

## Translation Rules and Profiles

A voice translation rule rewrites calling or called numbers. A translation profile groups rules and applies them to a call leg.

Example: remove an access code `9` from the called number.

```ios
voice translation-rule 10
 rule 1 /^9\(.*\)/ /\1/
!
voice translation-profile STRIP-ACCESS-CODE
 translate called 10
!
dial-peer voice 150 pots
 translation-profile outgoing STRIP-ACCESS-CODE
 destination-pattern 9T
 trunkgroup 1
 forward-digits all
```

Translation processing is powerful and easy to misread. Test rules before applying them:

```ios
test voice translation-rule 10 95551212
show voice translation-rule
show voice translation-profile
```

Call-number transformations can also occur in CUCM. Document which system owns normalization so the same digits are not changed twice.

## Codec and DTMF Reuse

A voice-class codec provides a reusable ordered codec list:

```ios
voice class codec 1
 codec preference 1 g711ulaw
 codec preference 2 g729r8
```

Apply it to supported VoIP dial peers:

```ios
voice-class codec 1
dtmf-relay rtp-nte
no vad
```

Both ends must support a compatible codec and DTMF method. Transcoding or an MTP may be inserted when CUCM policy and available media resources allow it.

## Practical Matching Workflow

For a failed or misrouted call:

1. Record the exact calling and called numbers.
2. Identify how the call entered the gateway.
3. Determine the inbound dial peer that matched.
4. Check inbound translation and call-leg settings.
5. Determine the outbound dial peer selected for the resulting called number.
6. Identify its port, trunk group, or session target.
7. Check outbound translation, codec, DTMF, and protocol settings.
8. Confirm signaling completion and bidirectional media.

Continue with [Call Flows](call-flows.md) and [Troubleshooting](troubleshooting.md).

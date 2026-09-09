# CUCM Call Routing

Cisco Unified Communications Manager (CUCM) uses digit analysis, routing objects, and calling privileges to decide where a call should go.

## Core Routing Chain

```text
Dialed Number
    |
    v
Digit Analysis
    |
    v
Route Pattern
    |
    v
Route List
    |
    v
Route Group
    |
    v
Gateway or Trunk
```

Partitions and Calling Search Spaces determine which directory numbers, route patterns, and other patterns the caller is allowed to reach.

## Directory Number

A **directory number (DN)** identifies a line or reachable destination in CUCM. A DN normally belongs to a partition. The combination of pattern and partition is significant because the same number can exist in different partitions for different routing contexts.

## Partition

A **partition** is a logical grouping of route patterns, directory numbers, translation patterns, and other dial-plan entries. It is part of CUCM's class-of-service model.

A partition does not grant access by itself. It makes a pattern available to Calling Search Spaces that include that partition.

## Calling Search Space

A **Calling Search Space (CSS)** is an ordered list of partitions that a device, line, or call-routing object can search. It controls which destinations and routes a caller can reach.

```text
Caller line/device CSS
    |
    v
Ordered list of partitions
    |
    v
Reachable DNs, translation patterns, and route patterns
```

Both line-level and device-level CSS settings can participate in effective calling privileges. Translation and forwarding operations can introduce additional CSS decisions. When a pattern appears correct but CUCM does not select it, inspect the effective CSS and the pattern's partition.

## Route Pattern

A **route pattern** matches dialed numbers and directs matching calls toward a route list, gateway, or trunk, depending on the design.

Common uses include:

- emergency calls;
- local PSTN calls;
- long-distance calls;
- international calls;
- on-net or intercluster routes.

A route pattern can also apply digit-discard instructions, prefixes, calling or called-party transformations, route filters, and call-classification settings.

## Route List

A **route list** gives CUCM an ordered list of route groups to try. It provides a layer for path selection and failover.

```text
Route Pattern 9.@
    |
    v
Route List PSTN-RL
    | first choice
    +--> Route Group HQ-GW
    |
    | second choice
    +--> Route Group DR-GW
```

Route-list and route-group details can influence number transformations and selection behavior. Document transformations at every layer.

## Route Group

A **route group** contains gateways or trunks and defines an order or distribution algorithm for selecting them. Members might include:

- SIP trunks;
- H.323 gateways;
- MGCP gateways or endpoints;
- intercluster trunks.

If CUCM sends a call to the wrong gateway, check the selected route pattern, route list, route-group member order, device state, and whether an earlier member was unavailable.

## Gateway or Trunk

The final CUCM routing object delivers signaling to another system.

- An **H.323 gateway** gives the IOS router more local dial-peer logic and is treated as a legacy option.
- A **SIP trunk** exchanges SIP signaling with a gateway, CUBE, cluster, provider, or PBX.
- An **MGCP gateway** exposes controlled endpoints to CUCM, placing more control in CUCM.

## Device Pool

A **device pool** groups operational settings for devices. Depending on deployment and CUCM release, it can influence items such as region, location, date/time group, call-processing redundancy, media resources, and local route group behavior.

A device pool is not itself a dial-plan permission object, but settings associated with it can affect codec selection, bandwidth policy, redundancy, and route localization.

## Regions and Locations

- **Regions** define codec or audio-bandwidth relationships between devices.
- **Locations** provide call-admission bandwidth policy between sites or logical locations.

A call can match the correct route and still fail because the requested codec or bandwidth cannot be supported.

## Media Resource Group List

A **Media Resource Group List (MRGL)** gives a device access to ordered Media Resource Groups. Those groups can contain MTPs, transcoders, conference bridges, annunciators, and other media resources.

When CUCM needs an MTP or transcoder, check:

1. whether the resource is registered and available;
2. whether it supports the required protocol and codec;
3. whether the device's effective MRGL can select it;
4. whether capacity is exhausted.

## Protocol-Specific Control Boundaries

### CUCM to MGCP Gateway

```text
CUCM owns call control and endpoint selection
            |
            v
MGCP controls gateway ports
            |
            v
Router supplies physical interfaces and media resources
```

Start troubleshooting in CUCM registration, endpoint, and route configuration, then verify physical port, circuit, clocking, and media state on the gateway.

### CUCM to H.323 Gateway

```text
CUCM route pattern/list/group
            |
            v
H.323 signaling to router
            |
            v
IOS inbound and outbound dial peers
            |
            v
POTS port, trunk group, or another VoIP peer
```

Both CUCM digit analysis and IOS dial-peer matching matter. Source-address binding and legacy H.323 negotiation are common inspection points.

### CUCM to SIP Gateway or CUBE

```text
CUCM route pattern/list/group
            |
            v
SIP trunk
            |
            v
IOS XE inbound SIP dial peer
            |
            v
IOS XE outbound dial peer or carrier trunk
```

Inspect SIP messages and SDP, dial-peer selection, calling and called transformations, codec and DTMF agreement, trunk security, and RTP reachability.

## Where Number Manipulation Can Occur

CUCM can transform numbers at several layers, including:

- translation patterns;
- route patterns;
- route-list or route-group details;
- calling and called-party transformation patterns and CSSs;
- device, trunk, or gateway configuration;
- service parameters and normalization scripts where supported.

The gateway can then manipulate numbers using destination patterns, prefixes, forward digits, translation rules, translation profiles, and protocol-specific features.

Create a before-and-after number table when troubleshooting:

| Stage | Calling number | Called number |
|---|---|---|
| Phone dials | `6985` | `95551212` |
| CUCM route pattern | `6985` | `5551212` |
| Gateway inbound leg | `6985` | `5551212` |
| Gateway outbound POTS leg | `5556985` | `5551212` |

Use the numbers observed in signaling or call records, not assumptions.

## Why Did CUCM Choose This Gateway?

Ask these questions in order:

1. What digits did CUCM receive?
2. What was the caller's effective CSS?
3. Which matching patterns were visible in that CSS?
4. Which pattern won digit analysis?
5. Which transformations occurred?
6. Which route list did the pattern reference?
7. Which route group was selected?
8. Which member was available and selected?
9. What signaling address and protocol did CUCM use?
10. What did the gateway do with the call after receiving it?

Use CUCM's Dialed Number Analyzer when it is available and appropriate for the installed release. Confirm the result with traces or call records when actual behavior differs from the expected analysis.

Continue with [Dial Peers](dial-peers.md), [Protocols and Media](protocols-media.md), and [Call Flows](call-flows.md).

# Dial-Plan Design and Number Normalization

A good dial plan makes numbers predictable at each boundary. It separates what users dial from the normalized identity used for routing, policy, carrier presentation, and intersite calling.

## Start with a Numbering Policy

Document:

- internal extension lengths and site ranges;
- full public numbers assigned to users and services;
- emergency and service numbers;
- local, national, and international dialing formats;
- PSTN access codes, if retained;
- carrier-required called-number format;
- carrier-required calling-number format;
- inbound DID format delivered by each carrier;
- voicemail, contact center, paging, fax, and analog ranges;
- reserved and blocked number classes.

Do not build patterns before deciding what a number should look like at each stage.

## Globalized and Localized Dialing

A **globalized** dial plan normalizes numbers into a consistent full format, often based on E.164, before core routing decisions. A **localized** presentation lets users dial familiar local formats and converts them at a controlled boundary.

```text
User dials local format
        |
        v
Translation or normalization
        |
        v
Consistent global form
        |
        v
Route selection
        |
        v
Carrier-specific localization
```

Benefits include simpler intersite routing, fewer overlapping patterns, clearer calling identity, and easier migrations between carriers.

## E.164

E.164 represents a public telephone number with a country code and national number, commonly written with a leading plus sign in documentation and call-control systems.

Example documentation number:

```text
+12065550100
```

Not every trunk or endpoint accepts the plus sign. Normalize internally when useful, then transform to the format required by the adjacent system.

## CUCM Pattern Types

| Object | Purpose |
|---|---|
| **Directory number** | Identifies a line or destination. |
| **Translation pattern** | Rewrites or reroutes a number before another digit-analysis pass. |
| **Route pattern** | Selects a route list, gateway, or trunk for off-cluster destinations. |
| **Calling-party transformation pattern** | Changes calling identity at an assigned transformation boundary. |
| **Called-party transformation pattern** | Changes the destination at an assigned transformation boundary. |
| **SIP route pattern** | Routes SIP URI destinations in designs that use them. |

Partitions and Calling Search Spaces control which patterns are visible to a caller or transformation operation.

## Partitions and Calling Search Spaces

Build class of service with intentional layers, for example:

```text
PT-INTERNAL
PT-LOCAL-PSTN
PT-LONG-DISTANCE
PT-INTERNATIONAL
PT-PREMIUM-BLOCK
PT-EMERGENCY
```

A CSS contains the partitions a caller may search, in order. Names should describe the privilege or routing scope rather than a specific person.

Test:

- line CSS and device CSS interaction;
- forwarded-call CSS;
- extension mobility or device-profile behavior;
- trunk and gateway inbound CSS;
- voicemail and application CSS;
- transformation CSS;
- emergency access from every endpoint class.

## Access Codes

An access code such as `9` can distinguish PSTN dialing, but it also introduces overlap and interdigit-delay risks.

If users dial `9` plus a public number:

1. Collect the access code and destination.
2. Strip the access code at one documented boundary.
3. Normalize the remaining number.
4. Route by normalized number class.
5. Present the carrier-required final format.

Do not strip the same digit in CUCM and again on a POTS dial peer.

## Overlapping Patterns

Patterns can overlap by length or wildcard. Problems include:

- a short internal extension that overlaps a service code;
- `9T` competing with fixed-length PSTN patterns;
- an urgent pattern routing before users finish dialing;
- a broad translation pattern hiding a more specific route;
- identical patterns in partitions visible through different CSS orders.

Use fixed-length, specific patterns when possible. Document why any variable-length or urgent pattern is required.

## Interdigit Timeout and Urgent Priority

Variable-length patterns may wait for more digits until a timer expires. Urgent priority tells CUCM to route immediately when a pattern matches, even if longer matches may exist.

Both can solve one problem and create another. Test every overlapping number class, including slow dialing, en bloc dialing, redial, forwarded calls, and emergency numbers.

## Local Route Groups

Local Route Groups allow a common route list to select a gateway based on the originating device's location or device-pool context. They can reduce duplicate route patterns across sites.

```text
Common Route Pattern
        |
        v
Standard Local Route Group
        |
        v
Originating site's gateway
```

Validate device-pool assignments, route-list details, failover, calling-number presentation, and emergency behavior. A phone assigned to the wrong device pool can select the wrong local gateway.

## Transformations by Layer

Number changes can occur in many places:

```text
Endpoint
  -> CUCM translation pattern
  -> route pattern
  -> route-list or route-group details
  -> trunk or gateway transformation CSS
  -> IOS inbound translation profile
  -> IOS outbound translation profile
  -> POTS digit stripping, prefix, or forward-digits
  -> carrier normalization
```

Prefer one clear owner for each transformation. When troubleshooting, build a table:

| Boundary | Calling before | Calling after | Called before | Called after |
|---|---|---|---|---|
| Endpoint to CUCM |  |  |  |  |
| CUCM route selection |  |  |  |  |
| CUCM to gateway |  |  |  |  |
| Gateway inbound leg |  |  |  |  |
| Gateway outbound leg |  |  |  |  |
| Carrier handoff |  |  |  |  |

## Calling-Number Presentation

Calling identity can affect:

- caller ID;
- carrier authorization;
- callback routing;
- emergency location;
- privacy and blocking;
- billing and fraud controls;
- diversion and forwarded-call handling.

Distinguish the user-facing display number from ANI, P-Asserted-Identity, From, Diversion, and other protocol fields. Define which field each adjacent system trusts.

## Inbound DID Normalization

Carriers may send:

- the full national number;
- the final seven or ten digits;
- only the extension digits;
- a plus-prefixed E.164 number;
- different formats on primary and backup trunks.

Normalize all accepted carrier formats to one internal form before routing to users or applications. Keep carrier-specific rules at the edge.

## Blocking and Authorization

Do not rely on a carrier to block unauthorized destinations. Define explicit classes for:

- local and national calls;
- international calls;
- premium-rate destinations;
- operator or service calls;
- emergency calls;
- feature codes;
- internal and application routes.

Use positive allow lists where practical and test from each endpoint class. Include forwarded and transferred calls because their calling context can differ.

## Dial-Plan Review Checklist

- [ ] Every number class has an owner and documented format.
- [ ] Internal extensions do not create unresolved overlap with service or PSTN patterns.
- [ ] Normalization occurs at named boundaries.
- [ ] Calling and called transformations are documented separately.
- [ ] CSS and partition names communicate purpose.
- [ ] Line, device, forwarding, trunk, gateway, and transformation CSSs are tested.
- [ ] Local Route Group behavior is validated for every site.
- [ ] Emergency routes work without unnecessary access codes.
- [ ] Carrier formats are documented in both directions.
- [ ] Primary and backup paths present equivalent numbers.
- [ ] Blocked classes are tested, logged, and monitored.
- [ ] Dialed Number Analyzer results are confirmed with controlled calls.

Continue with [CUCM Call Routing](cucm-routing.md), [CUCM Diagnostics](cucm-diagnostics.md), and [Emergency Calling](emergency-calling.md).

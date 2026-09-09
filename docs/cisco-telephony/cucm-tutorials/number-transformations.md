# Configure Number Transformations

## Goal

Normalize user-dialed and carrier-delivered numbers at clear CUCM boundaries without applying the same transformation twice on CUCM and the gateway.

## Transformation Tools

| Tool | Use |
|---|---|
| **Translation Pattern** | Match, transform, and reroute a number through another digit-analysis pass |
| **Route Pattern discard/prefix** | Change digits as an off-cluster route is selected |
| **Calling-Party Transformation Pattern** | Normalize or present the calling identity |
| **Called-Party Transformation Pattern** | Normalize the called destination at a transformation boundary |
| **Transformation CSS** | Controls which transformation patterns a device or trunk can search |
| **External Phone Number Mask** | Builds a public calling identity from a line where the design uses it |
| **Route-list detail transformations** | Applies path-specific changes before a selected gateway or trunk |
| **SIP normalization** | Changes SIP message structure for interworking, not a first choice for ordinary digit changes |

## Example Requirements

- Internal extension: `6985`
- Public number: `+12065556985`
- Users dial access code `9` before PSTN numbers
- Carrier expects national format without the plus sign
- Inbound carrier sends ten digits

Create a trace before configuring:

```text
Outbound:
9 2065550100 -> normalize -> +12065550100 -> carrier format 12065550100

Inbound:
2065556985 -> normalize -> +12065556985 -> map to extension 6985
```

## Tutorial 1: Strip a PSTN Access Code with a Translation Pattern

1. Open **Call Routing > Translation Pattern**.
2. Select **Add New**.
3. Enter a lab pattern matching the approved test format.
4. Select a partition visible only to the test phone's CSS.
5. Enter a description such as `Normalize lab PSTN access code`.
6. Select a CSS that can reach the normalized route patterns after translation.
7. Configure called-party transformation to discard or replace the access code according to the design.
8. Select **Save**.
9. Use Dialed Number Analyzer with the test phone and exact digits.
10. Confirm the transformed digits undergo the expected second digit-analysis pass.

!!! caution "Translation patterns reroute calls"
    The CSS assigned to a translation pattern controls the next search. A broad CSS can unintentionally grant destinations the original caller could not reach.

## Tutorial 2: Map an Inbound DID to Extension 6985

Use a translation pattern when the carrier sends a public-format number but the internal DN is shorter.

1. Confirm the exact called number CUCM receives from the trunk.
2. Open **Call Routing > Translation Pattern**.
3. Add an exact lab pattern for the test DID.
4. Place it in a partition visible to the inbound trunk CSS.
5. Configure the called-party transformation to produce `6985`.
6. Select a CSS that can search `PT-INTERNAL`.
7. Save.
8. Test with Dialed Number Analyzer using the trunk calling context when supported.
9. Place a controlled inbound call.
10. Confirm the resulting DN, caller ID, alerting name, audio, and disconnect.

Start with one exact DID. Expand to a range only after confirming that the range maps correctly and does not overlap other services.

## Tutorial 3: Configure Calling-Party Transformation

Use a calling-party transformation pattern when phones present internal extensions but an external trunk requires a public callback number.

1. Open **Call Routing > Transformation Pattern > Calling Party Transformation Pattern**, or the equivalent menu in the release.
2. Select **Add New**.
3. Enter a pattern matching the internal calling-number range.
4. Select a dedicated transformation partition.
5. Configure discard, prefix, or mask settings to create the public number.
6. Save.
7. Open **Call Routing > Class of Control > Calling Search Space**.
8. Create a transformation CSS containing the transformation partition.
9. Assign that CSS at the chosen trunk, gateway, device pool, or route-list boundary.
10. Place controlled calls from several extensions and inspect the identity sent to the peer.

Document whether the carrier uses From, P-Asserted-Identity, ANI, or another field for authorization and presentation.

## Tutorial 4: Configure Called-Party Transformation

Use a called-party transformation when CUCM routes with a normalized number but an adjacent system expects another format.

1. Open the called-party transformation pattern page.
2. Add a pattern matching the normalized destination range.
3. Place it in a dedicated transformation partition.
4. Configure the carrier- or gateway-required final format.
5. Create or reuse an approved transformation CSS.
6. Assign it at the intended trunk, gateway, device pool, or route-list detail.
7. Save and apply configuration where required.
8. Inspect the outbound SIP Request-URI or gateway called number.

Apply the rule at one boundary. Avoid simultaneously transforming the same digits on the route pattern, route list, trunk, and IOS translation profile.

## Tutorial 5: External Phone Number Mask

1. Open the directory number or line appearance.
2. Enter an external phone-number mask following the organizational standard, using `X` placeholders only as supported by the release.
3. Save.
4. On the route pattern or calling-party transformation, select mask use only where the dial plan requires it.
5. Place a test call and verify the actual outbound identity.

An external mask does nothing unless another routing object is configured to use it.

## Transformation Order Worksheet

| Stage | Calling before | Calling after | Called before | Called after |
|---|---|---|---|---|
| Endpoint |  |  |  |  |
| Translation pattern |  |  |  |  |
| Route pattern |  |  |  |  |
| Route-list detail |  |  |  |  |
| Trunk or gateway transformation |  |  |  |  |
| IOS inbound peer |  |  |  |  |
| IOS outbound peer |  |  |  |  |
| Carrier handoff |  |  |  |  |

Fill this from traces or signaling, not from assumptions.

## Test Matrix

- exact test DID;
- adjacent DID inside the intended range;
- number outside the range;
- internal caller without public mask;
- internal caller with public mask;
- forwarded call;
- transferred call;
- voicemail redirect;
- primary and backup trunks;
- privacy-restricted call;
- emergency call through the approved process.

## Common Mistakes

### Access Code Is Removed Twice

CUCM discards it, then an IOS translation rule or POTS dial peer strips another digit.

### Translation Grants Extra Calling Privileges

The translation pattern uses a CSS broader than the caller's intended class.

### Caller ID Is Correct on One Trunk Only

Path-specific route-list details or trunk transformation CSSs differ.

### Forwarded Call Shows the Wrong Identity

Forwarding introduces diversion headers, original called number, redirecting number, and carrier policy. Trace all relevant fields.

### Pattern Does Not Match

Check the number format before the transformation, partition visibility, pattern syntax, and whether another pattern wins first.

## Rollback

1. Restore the former transformation CSS assignment.
2. Disable or move the new pattern to an unreachable lab partition.
3. Confirm calls use the previous number format.
4. Delete the test pattern only after dependency records show no use.
5. Remove the transformation CSS and partition in reverse dependency order.

## Completion Checklist

- [ ] Before-and-after number format is documented at every boundary.
- [ ] Translation pattern uses a deliberately limited CSS.
- [ ] Calling and called transformations are separate and testable.
- [ ] Exact, adjacent, unauthorized, forwarded, and backup-path calls are tested.
- [ ] CUCM and IOS do not transform the same digits twice.
- [ ] Carrier-authorized identity and emergency callback remain correct.
- [ ] Rollback restores the previous format.

Next: [Verify and Troubleshoot CUCM Configuration](verification.md).

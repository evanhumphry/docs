# Configure Route Groups, Route Lists, and Route Patterns

## Goal

Route a documentation test number through an HQ SIP trunk using this chain:

```text
Route Pattern
    -> Route List
        -> Route Group
            -> SIP Trunk or Gateway
```

## Prerequisites

- A working SIP trunk or gateway exists.
- The calling phone has a CSS that can reach the route-pattern partition.
- Number format and access-code policy are documented.
- Calling-party presentation is defined.
- Backup-route behavior is defined.
- Emergency calling uses a separate approved design.

This tutorial uses fictional called number `+12065550100`. Do not place real emergency or premium calls during testing.

## Step 1: Create the Route Group

1. Open **Call Routing > Route/Hunt > Route Group**.
2. Select **Add New**.
3. Enter `RG-HQ-PSTN`.
4. Enter a description naming the site and service.
5. Choose the distribution algorithm required by the design.
6. Find `TRK-CUBE-HQ` or the lab gateway in available devices.
7. Move it into selected devices.
8. Add a backup trunk or gateway only when its number presentation, permissions, and emergency behavior are equivalent.
9. Order members according to the design.
10. Save.

The route-group algorithm and member order affect selection. Record the intended behavior rather than assuming the first displayed member always handles every call.

## Step 2: Create the Route List

1. Open **Call Routing > Route/Hunt > Route List**.
2. Select **Add New**.
3. Enter `RL-HQ-PSTN`.
4. Enter a description.
5. Select the appropriate CUCM group when the release requires it.
6. Save the route list.
7. Select **Add Route Group**.
8. Choose `RG-HQ-PSTN`.
9. Review route-list-detail digit manipulation and calling-party settings.
10. Save.
11. Add a secondary route group only when the failover design requires it.
12. Confirm route-group order.

Transformations configured on route-list details can differ for each path. Document them explicitly.

## Step 3: Create a Dedicated Test Partition

1. Open **Call Routing > Class of Control > Partition**.
2. Create or select a lab partition such as `PT-PSTN-TEST`.
3. Add it only to a lab CSS such as `CSS-PHONE-PSTN-TEST`.
4. Assign that CSS to the test calling context.

Using a dedicated test partition reduces the risk of exposing a new route to production phones.

## Step 4: Create an Exact Test Route Pattern

1. Open **Call Routing > Route/Hunt > Route Pattern**.
2. Select **Add New**.
3. Enter an exact lab pattern matching the approved test destination.
4. Select `PT-PSTN-TEST`.
5. Enter a description.
6. Select `RL-HQ-PSTN` as the gateway or route-list destination.
7. Review route option, call classification, urgent priority, and block settings.
8. Configure discard digits, prefix, or transformations only when required by the documented number format.
9. Review calling-party transformation and external phone-number mask behavior.
10. Save.

Start with an exact pattern. Expand to a number class only after the exact route works and authorization is reviewed.

## Access-Code Example

If users dial `9` before a public number, CUCM route patterns commonly use the dot as a discard delimiter in patterns designed for PreDot digit discard.

Conceptual example:

```text
User dials:             9 12065550100
CUCM access boundary:   strip 9
Normalized destination: +12065550100 or carrier-required form
```

The exact route-pattern syntax and discard options must match the deployed dial plan. Do not confuse CUCM route-pattern notation with IOS dial-peer wildcards.

## Step 5: Expand to a Number Class

After the exact route is validated:

1. Define local, national, international, toll-free, service, and blocked classes.
2. Create specific patterns in purpose-based partitions.
3. Add only approved partitions to each CSS.
4. Avoid a broad variable-length pattern when fixed-length patterns cover the requirement.
5. Review overlap, urgent priority, and interdigit timeout.
6. Test representative allowed and blocked destinations.

Use [Dial-Plan Design](../dial-plan-design.md) for normalization and class-of-service architecture.

## Step 6: Verify with Dialed Number Analyzer

When available:

1. Select the lab phone or calling context.
2. Enter the exact dialed digits.
3. Confirm the visible route-pattern partition.
4. Confirm the selected route pattern.
5. Confirm route list and route group.
6. Review digit transformations.
7. Repeat with an unauthorized phone.
8. Confirm the route is not visible or is blocked.

DNA does not prove that the trunk is up or media works.

## Step 7: Place the Test Call

Record:

| Stage | Calling number | Called number | Selected object |
|---|---|---|---|
| Phone |  |  | Device and line CSS |
| CUCM route pattern |  |  | Pattern and partition |
| Route list |  |  | Route-list detail |
| Route group |  |  | Selected member |
| Gateway or trunk |  |  | Inbound and outbound peer |
| Carrier |  |  | Accepted identity and destination |

Confirm ringback, answer, bidirectional audio, DTMF, caller ID, and disconnect.

## Step 8: Test Failover

In a lab or approved window:

1. Capture the normal selected member.
2. Make the primary member unavailable using an approved method.
3. Confirm CUCM detects the state or responds to the call failure as designed.
4. Place the test call.
5. Confirm the backup member, number format, codec, and media.
6. Restore the primary.
7. Confirm recovery and expected future selection.

Do not assume all SIP response codes or gateway failures trigger another route.

## Common Mistakes

### Route Pattern Exists but Phone Cannot Use It

The route-pattern partition is missing from the phone's effective CSS.

### Wrong Gateway Is Selected

Check route-list order, route-group algorithm, member status, Local Route Group substitution, and device-pool assignment.

### Carrier Receives Wrong Digits

Check translation pattern, route pattern, route-list detail, trunk transformation, IOS translation profile, and POTS digit handling.

### Backup Route Fails

The backup may use different transformations, firewall paths, certificates, codec policy, capacity, or carrier authorization.

### Every Phone Can Use the New Route

The pattern was placed in a broadly visible partition or an existing CSS was expanded without dependency review.

## Rollback

1. Restore the former route-pattern destination and transformations.
2. Remove the test partition from the calling CSS.
3. Confirm calls use the previous path.
4. Delete the route pattern.
5. Remove the route list only after no patterns reference it.
6. Remove the route group only after no route lists reference it.
7. Leave shared trunks and gateways intact unless separately approved for removal.

## Completion Checklist

- [ ] Route group contains intended members in the intended order.
- [ ] Route list references the correct route group and transformations.
- [ ] Route pattern is in the correct partition.
- [ ] CSS grants only intended callers access.
- [ ] Number format is recorded at every stage.
- [ ] DNA and live call select the expected path.
- [ ] Backup path, media, caller ID, and recovery are tested.
- [ ] Rollback dependency order is documented.

Next: [Configure Number Transformations](number-transformations.md).

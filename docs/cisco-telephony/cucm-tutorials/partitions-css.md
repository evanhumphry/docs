# Configure Partitions and Calling Search Spaces

## Goal

Create a simple class-of-service design in which phones can reach internal extensions and approved local PSTN routes without gaining international access.

## Example Design

| Object | Purpose |
|---|---|
| `PT-INTERNAL` | Internal directory numbers |
| `PT-PSTN-LOCAL` | Local PSTN route patterns |
| `PT-PSTN-LD` | Long-distance route patterns |
| `PT-PSTN-INTL` | International route patterns |
| `CSS-PHONE-INTERNAL` | Internal destinations only |
| `CSS-PHONE-LOCAL` | Internal plus local PSTN |
| `CSS-PHONE-LD` | Internal, local, and long distance |

A CSS searches partitions. A partition does not grant access by itself.

## Step 1: Inventory the Current Dial Plan

Before creating objects:

1. Open **Call Routing > Route Plan Report**.
2. Search existing partitions, CSSs, directory numbers, translation patterns, and route patterns.
3. Identify naming standards.
4. Check whether equivalent objects already exist.
5. Document devices, trunks, gateways, forwards, applications, and transformations that use related CSSs.

Avoid near-duplicate objects such as `CSS-Local`, `CSS_LOCAL`, and `Local-CSS` that provide the same access.

## Step 2: Create the Partitions

1. Open **Call Routing > Class of Control > Partition**.
2. Select **Add New**.
3. Enter partition names, one per line if the release supports bulk entry on the page:

```text
PT-INTERNAL
PT-PSTN-LOCAL
PT-PSTN-LD
PT-PSTN-INTL
```

4. Enter descriptions that state the permitted destination class.
5. Select **Save**.

Partition names participate in the dial plan. Renaming or deleting a partition can have broad impact because many patterns may reference it.

## Step 3: Create an Internal-Only CSS

1. Open **Call Routing > Class of Control > Calling Search Space**.
2. Select **Add New**.
3. Enter `CSS-PHONE-INTERNAL`.
4. Enter a description.
5. Move `PT-INTERNAL` into the selected partitions list.
6. Confirm the intended order.
7. Select **Save**.

## Step 4: Create a Local-PSTN CSS

1. Add `CSS-PHONE-LOCAL`.
2. Select these partitions in the intended order:

```text
PT-INTERNAL
PT-PSTN-LOCAL
```

3. Save.

Do not add long-distance or international partitions merely because they exist. A CSS should include only the number classes the caller requires.

## Step 5: Create a Long-Distance CSS

1. Add `CSS-PHONE-LD`.
2. Select:

```text
PT-INTERNAL
PT-PSTN-LOCAL
PT-PSTN-LD
```

3. Save.

The order can matter when equivalent patterns exist in multiple partitions. Design to avoid ambiguous duplicates rather than relying on partition order to explain every call.

## Step 6: Assign Partitions to Patterns

Assign objects to their intended partitions:

- internal directory numbers to `PT-INTERNAL`;
- local route patterns to `PT-PSTN-LOCAL`;
- long-distance route patterns to `PT-PSTN-LD`;
- international patterns to `PT-PSTN-INTL`.

Changing a pattern's partition changes who can reach it. Record the original value before editing.

## Step 7: Assign the CSS

A phone can have CSS settings at multiple layers, including device and line. Forwarding fields, trunks, gateways, translation patterns, and applications can also have CSSs.

For a test phone:

1. Open **Device > Phone**.
2. Record the current device CSS.
3. Open the line appearance and record the line CSS and forwarding CSSs.
4. Assign the CSS at the layer required by the design.
5. Save and apply configuration only if required.

Use a consistent policy. Randomly splitting privileges between line and device CSS makes troubleshooting difficult.

## Step 8: Test with Dialed Number Analyzer

When available:

1. Open **Cisco Unified Serviceability > Tools > Dialed Number Analyzer** or the release-specific DNA interface.
2. Select the test device or calling context.
3. Enter an internal extension.
4. Confirm the internal pattern and partition.
5. Test a local PSTN number.
6. Test long distance.
7. Test international.
8. Confirm the selected pattern, partition, and route match the intended class.

DNA predicts digit analysis but does not prove trunk availability, media, or runtime state.

## Step 9: Place Controlled Calls

From each CSS class, test:

| Destination | Internal CSS | Local CSS | Long-distance CSS |
|---|---|---|---|
| Internal extension | Allow | Allow | Allow |
| Local PSTN | Block | Allow | Allow |
| Long distance | Block | Block | Allow |
| International | Block | Block | Block unless explicitly authorized |

Use approved test numbers and avoid premium or emergency destinations.

## Common Mistakes

### Pattern Is Correct but Unreachable

The route pattern or DN is in a partition absent from the caller's effective CSS.

### Forwarded Calls Behave Differently

Call-forward CSS fields can differ from the normal calling CSS. Test forward-all, no-answer, busy, and voicemail paths.

### Trunk Calls Cannot Reach Internal DNs

The inbound trunk or gateway CSS may not include `PT-INTERNAL`, or a transformation changes the called number before digit analysis.

### Unexpected Route Wins

Look for overlapping patterns in multiple visible partitions, translation patterns, urgent priority, variable length, and partition order.

### Privilege Is Too Broad

A reused CSS may contain a partition added later for another purpose. Review all selected partitions, not only the one you expect.

## Rollback

1. Restore the original line, device, trunk, or forward CSS.
2. Restore changed patterns to their former partitions.
3. Retest the previous calling matrix.
4. Remove new CSSs only after dependency records show no object uses them.
5. Remove new partitions only after moving or deleting every contained pattern.

## Completion Checklist

- [ ] Existing objects and dependencies were reviewed first.
- [ ] Partitions represent clear destination classes.
- [ ] CSSs grant only required classes.
- [ ] Assignment layer is documented.
- [ ] Internal, local, long-distance, international, forwarding, and trunk-originated calls are tested.
- [ ] Blocked calls remain blocked.
- [ ] Rollback restores the previous access matrix.

Next: [Configure Route Groups, Route Lists, and Route Patterns](pstn-routing.md).

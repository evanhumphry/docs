# Configure a Line Group and Hunt Pilot

## Goal

Create a hunt pilot `7000` that distributes calls to extensions `6985`, `6986`, and `6987`.

## Object Chain

```text
Caller dials 7000
    |
    v
Hunt Pilot 7000
    |
    v
Hunt List HL-SERVICE-DESK
    |
    v
Line Group LG-SERVICE-DESK
    |
    +--> 6985
    +--> 6986
    +--> 6987
```

## Prerequisites

- Member DNs exist and are in the intended partitions.
- Phones are registered.
- Members and business owner approve the hunt order.
- Voicemail or final-destination behavior is defined.
- Busy, no-answer, logged-out, and unregistered behavior is defined.
- Call Pickup, shared lines, mobility, and contact-center overlap are reviewed.

A hunt group is not a replacement for a contact center when reporting, queuing, agent state, recording, or service-level features are required.

## Step 1: Create the Line Group

1. Open **Call Routing > Route/Hunt > Line Group**.
2. Select **Add New**.
3. Enter `LG-SERVICE-DESK`.
4. Enter a description.
5. Select a distribution algorithm:
   - **Top Down:** Start at the top of the member list.
   - **Circular:** Continue through members in sequence.
   - **Longest Idle:** Prefer the member idle longest, subject to release behavior.
   - **Broadcast:** Alert multiple available members.
6. Configure the RNA reversion timeout according to business requirements.
7. Define no-answer, busy, and unavailable member handling exposed by the release.
8. Find DNs `6985`, `6986`, and `6987` in their partitions.
9. Add them to selected members.
10. Order members when the algorithm uses order.
11. Save.

Verify that each selected line appearance, not merely the device, is correct.

## Step 2: Create the Hunt List

1. Open **Call Routing > Route/Hunt > Hunt List**.
2. Select **Add New**.
3. Enter `HL-SERVICE-DESK`.
4. Enter a description.
5. Select the appropriate CUCM group.
6. Save.
7. Select **Add Line Group**.
8. Choose `LG-SERVICE-DESK`.
9. Save.
10. Add additional line groups only when a tiered escalation design requires them.
11. Confirm the hunt list is enabled or active according to the release interface.

## Step 3: Create the Hunt Pilot

1. Open **Call Routing > Route/Hunt > Hunt Pilot**.
2. Select **Add New**.
3. Enter `7000`.
4. Select the intended partition, such as `PT-INTERNAL`.
5. Enter a description and alerting name.
6. Select `HL-SERVICE-DESK` as the hunt list.
7. Configure calling and called-party transformations only when required.
8. Configure final forwarding for hunt-busy and hunt-no-answer conditions.
9. Select the correct CSS for final forwarding destinations.
10. Choose voicemail behavior when the design sends unanswered calls to voicemail.
11. Save.

Confirm `7000` does not overlap an existing DN, route pattern, translation pattern, or feature code visible through the same CSS.

## Step 4: Test Distribution

Place repeated calls and record:

| Test | Expected member | Actual member | Result |
|---|---|---|---|
| All members idle |  |  |  |
| First member busy |  |  |  |
| First member no answer |  |  |  |
| One member unregistered |  |  |  |
| All members busy |  |  |  |
| All members no answer |  |  |  |
| Final destination |  |  |  |

Validate caller ID, alerting name, ring duration, answered call, transfer, hold, and disconnect.

## Step 5: Test Login and Logout Behavior

If hunt login/logout is enabled:

1. Confirm which users or phones can change status.
2. Log one member out.
3. Place a call and confirm the member is skipped.
4. Log the member back in.
5. Confirm the member returns to distribution.
6. Verify status survives phone reset or failover according to design.

Do not assume unregistered, logged-out, busy, and do-not-disturb states are handled identically.

## Step 6: Test Final Forwarding

1. Make every member unavailable using an approved lab method.
2. Call `7000`.
3. Confirm the hunt-busy or hunt-no-answer destination.
4. Confirm the forwarding CSS can reach that destination.
5. If voicemail is used, confirm the correct mailbox greeting rather than a member's personal mailbox.
6. Restore members and confirm normal hunting.

## Common Mistakes

### Hunt Pilot Rings No One

Check hunt-list activation, selected line group, registered member line appearances, member state, CSS and partition, and distribution settings.

### Calls Always Ring the Same Person

Top-down distribution may be working as configured. Select circular or longest-idle only if it matches business requirements.

### Final Forward Fails

The hunt-pilot forward CSS cannot reach the destination, or the voicemail routing does not identify the intended mailbox.

### Member Receives Direct Calls but Not Hunt Calls

Check line-group membership, hunt login state, maximum calls, busy trigger, do-not-disturb behavior, and line registration.

### Contact Center Features Are Missing

Native hunting does not provide full agent state, queue announcements, reporting, or contact-center routing.

## Rollback

1. Restore the former hunt pilot or forwarding destination.
2. Remove the hunt-pilot partition from test CSSs if required.
3. Confirm direct calls to members still work.
4. Delete the hunt pilot.
5. Delete the hunt list after removing its line groups.
6. Delete the line group after preserving member documentation.

## Completion Checklist

- [ ] Line group contains the correct line appearances and order.
- [ ] Distribution algorithm matches business behavior.
- [ ] Hunt list is active and uses the intended CUCM group.
- [ ] Hunt pilot is in the correct partition.
- [ ] Caller CSS can reach the pilot.
- [ ] Busy, no-answer, unregistered, login/logout, and final-forward behavior are tested.
- [ ] Voicemail reaches the correct mailbox.
- [ ] Rollback preserves direct member calling.

Next: [Configure Media Resource Groups and Lists](media-resources.md).

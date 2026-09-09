# Configure a Phone, Directory Number, and User

## Goal

Register a Cisco phone, assign extension `6985`, apply the correct site and calling policy, and associate the phone with an end user.

## Prerequisites

Collect:

- phone model and supported firmware;
- MAC address or device name;
- device pool;
- location and region policy;
- phone button template;
- device security profile;
- SIP profile or SCCP protocol requirement;
- device and line Calling Search Spaces;
- directory-number partition;
- Media Resource Group List;
- end-user ID;
- switch port, voice VLAN, DHCP, DNS, TFTP, and power readiness.

!!! note "Auto-registration"
    Auto-registration can simplify labs but can create uncontrolled device records in production. Use approved policy and disable or restrict it when it is not intentionally required.

## Step 1: Add the Phone

1. In **Cisco Unified CM Administration**, open **Device > Phone**.
2. Select **Add New**.
3. Choose the exact phone type.
4. Choose the supported device protocol, such as SIP or SCCP, when the model offers a choice.
5. Select **Next**.
6. Enter the device name. For many hardware phones, this is `SEP` followed by the MAC address without separators.
7. Enter a useful description containing site, room, or owner according to naming policy.
8. Select the correct **Device Pool**.
9. Select the approved **Phone Button Template**.
10. Select the device-level **Calling Search Space** if the design uses one.
11. Select the correct **Location** and **Media Resource Group List** if they are not inherited as intended.
12. Select the supported **Device Security Profile** and **SIP Profile** where applicable.
13. Set **Owner User ID** if required by the feature and licensing design.
14. Select **Save**.

Do not guess a security profile or copy one from an unrelated device. Secure registration, certificates, and mixed-mode clusters require release-specific planning.

## Step 2: Add Directory Number 6985

1. On the phone page, select **Line [1] - Add a new DN**.
2. Enter `6985` in **Directory Number**.
3. Select the intended partition, such as `PT-INTERNAL`.
4. Enter an **Alerting Name**, **ASCII Alerting Name**, and description according to policy.
5. Set the line-level CSS only if the class-of-service design requires it.
6. Review call-forward destinations and their CSS fields.
7. Select the voicemail profile when voicemail is assigned.
8. Configure display, ring, busy trigger, and maximum calls according to the endpoint standard.
9. Select **Save**.
10. Select **Apply Config** or reset the device only when required and approved.

Directory number plus partition must be unique for the intended dial-plan context.

## Step 3: Associate the User

1. Open **User Management > End User**.
2. Find the user and open the record.
3. Verify user ID, status, directory URI, and service-profile assignments according to policy.
4. Under **Device Information**, select **Device Association**.
5. Find and select the new phone.
6. Save the association.
7. Return to the user page and select `6985` as the primary extension when required.
8. Review controlled devices, mobility, presence, and self-service settings before saving.

Device association alone does not automatically grant every service. Licensing, service profile, home cluster, and application permissions can also matter.

## Step 4: Confirm Network Registration

At the phone:

1. Confirm power and switch-port link.
2. Confirm the expected voice VLAN.
3. Confirm DHCP address, default gateway, DNS, and TFTP information.
4. Confirm correct date and time.
5. Confirm the phone downloads configuration and registers.
6. Confirm extension `6985` appears on the intended line button.

In CUCM:

1. Return to **Device > Phone** and open the phone.
2. Confirm the device shows the expected registration state, address, active server, and firmware.
3. Confirm the line association and configured CSS, partition, device pool, location, and MRGL.

## Step 5: Test Calls

Test according to the assigned class of service:

- another internal extension;
- voicemail;
- an allowed local PSTN number;
- a number class that should be blocked;
- inbound calling to the DN or associated DID;
- hold, resume, transfer, and conference;
- DTMF to voicemail or an IVR;
- caller ID and called-name display;
- failover to another CUCM node when part of the approved lab.

Use approved emergency-call procedures only.

## Troubleshooting

### Phone Does Not Register

Check:

- MAC address and device type;
- DHCP and TFTP options;
- DNS and routing;
- phone firmware and load;
- device security profile and certificates;
- CUCM service and node status;
- duplicate device name;
- switch port, VLAN, power, and access control.

### Phone Registers but Cannot Call

Check line and device CSS, destination partition, translation patterns, route patterns, device pool, region, location, and whether the destination is registered.

### Wrong Caller ID

Check directory-number external phone-number mask, calling-party transformation, route-list details, trunk or gateway transformation, and carrier policy.

## Rollback

1. Restore the former line, CSS, device pool, or user association if this was a change.
2. Reset only the affected phone if necessary.
3. Confirm the previous device registration and calling behavior.
4. Remove the test DN only after dependencies such as voicemail, forwarding, hunt groups, and user association are cleared.
5. Delete the phone record only after preserving any required ownership and inventory data.

## Completion Checklist

- [ ] Phone registers to the expected CUCM node.
- [ ] Correct firmware, device pool, location, region, CSS, and MRGL apply.
- [ ] DN `6985` appears in the intended partition.
- [ ] End-user association and primary extension are correct.
- [ ] Allowed calls succeed and blocked calls remain blocked.
- [ ] Inbound route, caller ID, audio, DTMF, and call clearing work.
- [ ] Reset impact and rollback are documented.

Next: [Configure Partitions and Calling Search Spaces](partitions-css.md).

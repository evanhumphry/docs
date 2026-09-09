# Configure Device Pools, Regions, and Locations

## Goal

Create a site policy for an HQ phone group using a device pool, codec region, call-admission location, CUCM group, date/time group, SRST reference, and media-resource policy.

## Understand the Objects

| Object | Main purpose |
|---|---|
| **CUCM Group** | Ordered call-processing nodes used by devices |
| **Date/Time Group** | Timezone and display format |
| **Region** | Codec and audio-bandwidth relationships |
| **Location** | Call-admission bandwidth policy |
| **SRST Reference** | Local survivability gateway information |
| **MRGL** | Ordered access to MTPs, transcoders, and conference resources |
| **Device Pool** | Assigns a reusable bundle of site policy to devices |

Menu names and inheritance vary by CUCM release.

## Step 1: Create or Verify the CUCM Group

1. Open **System > Cisco Unified CM Group**.
2. Search for an existing group matching the site's redundancy design.
3. If required, select **Add New**.
4. Enter a descriptive name such as `CMG-HQ`.
5. Add call-processing nodes in the intended registration order.
6. Enable automatic registration fallback or related options only according to the cluster design.
7. Save.

Do not change node order in a shared CUCM group without reviewing every device pool that references it.

## Step 2: Create the Date/Time Group

1. Open **System > Date/Time Group**.
2. Select **Add New**.
3. Enter `DTG-HQ`.
4. Select the correct timezone.
5. Select date and time display formats.
6. Save.

Confirm the operating system, NTP, and cluster time are healthy. A display timezone does not correct clock drift.

## Step 3: Create or Review the Region

1. Open **System > Region Information > Region**.
2. Select **Add New** or copy an approved regional standard.
3. Enter `REG-HQ`.
4. Define relationships to other regions according to codec and bandwidth policy.
5. Review audio codec, video, immersive video, and loss-handling fields available in the release.
6. Save.

The region relationship is directional in some configurations and may require reviewing both sides. Test the actual selected codec.

## Step 4: Create or Review the Location

1. Open **System > Location Info > Location**, or the equivalent menu for the release.
2. Select **Add New**.
3. Enter `LOC-HQ`.
4. Configure audio, video, and immersive bandwidth policy according to the WAN design.
5. Review links or enhanced-location call-admission relationships if the deployment uses them.
6. Save.

Locations control call-admission bandwidth, not packet queueing. Configure network QoS separately.

## Step 5: Create or Verify the SRST Reference

1. Open **System > SRST**.
2. Select **Add New**.
3. Enter the supported SRST gateway address and port information for the phone protocol.
4. Enter a descriptive name such as `SRST-HQ`.
5. Save.

Validate gateway platform, license, capacity, dial plan, certificates, and failover behavior using the [SRST tutorial](../srst.md).

## Step 6: Verify the MRGL

1. Open **Media Resources > Media Resource Group List**.
2. Find the site MRGL or create it using the [Media Resources tutorial](media-resources.md).
3. Confirm resource-group order for local and shared MTP, transcoder, and conference resources.
4. Record the intended MRGL name, such as `MRGL-HQ`.

## Step 7: Create the Device Pool

1. Open **System > Device Pool**.
2. Select **Add New**.
3. Enter `DP-HQ`.
4. Select `CMG-HQ` as the CUCM group.
5. Select `DTG-HQ` as the date/time group.
6. Select `REG-HQ` as the region.
7. Select `LOC-HQ` as the location if the release exposes it in the device pool.
8. Select `SRST-HQ` as the SRST reference.
9. Select `MRGL-HQ` when site media resources should be inherited.
10. Review local route group, network locale, user locale, media-resource, and mobility settings.
11. Save.

A device pool can affect many devices. Do not edit an existing shared pool when a new site requires different behavior unless every dependency has been reviewed.

## Step 8: Assign a Test Phone

1. Open **Device > Phone**.
2. Select a lab phone.
3. Record the current device pool and inherited settings.
4. Assign `DP-HQ`.
5. Save.
6. Apply configuration or reset the phone only in the approved window.
7. Confirm the phone re-registers to the expected CUCM node.

## Step 9: Verify Behavior

Check:

- phone timezone and display;
- active CUCM subscriber;
- selected codec for same-region and cross-region calls;
- call-admission behavior under controlled capacity testing;
- local media-resource selection;
- Local Route Group path if used;
- SRST registration during an approved failure test;
- return to CUCM after recovery.

Use call details, CMR, packet capture, and RTMT rather than assuming inheritance worked.

## Common Mistakes

### Wrong CUCM Node

The device pool references the wrong CUCM group or unexpected node order.

### Unexpected Codec

Region relationships, SIP trunk codec policy, endpoint capabilities, or a transcoder change the result.

### Calls Fail Despite Available Network Bandwidth

Location call-admission policy can deny the call even when the network is uncongested.

### Wrong PSTN Gateway

The device pool can influence Local Route Group selection. A phone assigned to another site's pool may use that site's gateway.

### Media Resource Not Selected

The inherited MRGL may differ from a device-level override, or the resource may be unregistered, incompatible, or exhausted.

## Rollback

1. Restore the phone's original device pool.
2. Reset only the affected test device when required.
3. Confirm original registration, codec, route, media, and timezone behavior.
4. Remove the new device pool only after no devices reference it.
5. Remove dependent objects in reverse order only when they are unused.

## Completion Checklist

- [ ] CUCM group order matches the redundancy design.
- [ ] Timezone and date display are correct.
- [ ] Region codec relationships are documented and tested.
- [ ] Location call-admission policy is tested.
- [ ] SRST reference and capacity are validated.
- [ ] MRGL inheritance selects intended resources.
- [ ] Local Route Group behavior is correct.
- [ ] Phone returns to expected operation after reset and rollback.

Next: [Configure Media Resource Groups and Lists](media-resources.md).

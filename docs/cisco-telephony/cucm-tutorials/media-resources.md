# Configure Media Resource Groups and Lists

## Goal

Create a site-specific Media Resource Group List (MRGL) that prefers local media resources and falls back to shared resources.

## Object Chain

```text
Phone, trunk, gateway, or device pool
        |
        v
MRGL-HQ
    |
    +--> MRG-HQ-LOCAL
    |       +--> local MTP
    |       +--> local transcoder
    |
    +--> MRG-SHARED
            +--> shared conference bridge
            +--> shared MTP
```

## Media Resources to Recognize

- **Media Termination Point:** Assists with selected signaling, DTMF, early-offer, or media interworking requirements.
- **Transcoder:** Converts between codecs or media formats.
- **Conference Bridge:** Mixes participant audio or video according to resource capability.
- **Music on Hold:** Supplies audio during hold.
- **Annunciator:** Supplies tones or announcements for supported features.

Software and hardware resources differ in codec support, capacity, registration, and features.

## Prerequisites

- Resources are configured and registered.
- IOS DSP farm profiles are active where hardware resources are used.
- CUCM media-resource names match registered resources.
- Region and location policies are documented.
- Required codecs, DTMF, early-offer, and conferencing behaviors are known.
- DSP capacity covers normal and failover load.
- Device-pool and device-level inheritance is understood.

## Step 1: Verify Resource Registration

1. Open the applicable **Media Resources** administration page for MTPs, transcoders, conference bridges, music-on-hold servers, or annunciators.
2. Find each resource.
3. Confirm registration status, controlling CUCM node, device pool, location, and supported capabilities.
4. Use RTMT to inspect alarms and performance where available.
5. On IOS resources, confirm DSP farm, SCCP or other control registration, profile state, codec list, and sessions using release-supported commands.

Do not add an unregistered resource to an MRG and expect selection to fix registration.

## Step 2: Create the Local MRG

1. Open **Media Resources > Media Resource Group**.
2. Select **Add New**.
3. Enter `MRG-HQ-LOCAL`.
4. Enter a description.
5. Decide whether multicast is required for music on hold; leave it disabled unless the design supports it end to end.
6. Move the HQ MTP, transcoder, conference bridge, or other intended resources into selected resources.
7. Save.

A resource can belong to only the combinations allowed by CUCM. Review dependency records before moving a shared resource.

## Step 3: Create or Review the Shared MRG

1. Find an approved shared resource group such as `MRG-SHARED`.
2. Confirm resources, codec capabilities, registration, and capacity.
3. Create a dedicated shared MRG only when the existing design does not provide one.
4. Save.

## Step 4: Create the MRGL

1. Open **Media Resources > Media Resource Group List**.
2. Select **Add New**.
3. Enter `MRGL-HQ`.
4. Enter a description.
5. Move `MRG-HQ-LOCAL` into selected groups first.
6. Move `MRG-SHARED` after it.
7. Confirm order.
8. Save.

MRG order expresses preference. It does not guarantee a specific resource when it is unavailable, incompatible, or exhausted.

## Step 5: Assign the MRGL

Preferred assignment is often through a device pool:

1. Open **System > Device Pool**.
2. Open `DP-HQ`.
3. Record the current MRGL.
4. Assign `MRGL-HQ`.
5. Save.
6. Reset affected devices only when required and approved.

A device-level MRGL can override device-pool inheritance. Check the actual phone, trunk, gateway, or resource-consuming object before concluding which list applies.

## Step 6: Test an MTP Requirement

Use a controlled call known to require an MTP according to the design:

1. Capture the baseline call without changing MTP settings.
2. Confirm whether CUCM requests an MTP.
3. Confirm the selected MRG and resource.
4. Confirm codec, DTMF, hold, transfer, and media path.
5. Make the preferred resource unavailable only in a lab.
6. Confirm selection of a compatible shared resource or the documented failure.
7. Restore and confirm recovery.

Do not enable **MTP Required** simply to make one call work without determining the actual interworking requirement.

## Step 7: Test Transcoding

1. Create a lab call between regions or endpoints with no direct common codec but an approved transcoding design.
2. Confirm CUCM selects a transcoder from `MRGL-HQ`.
3. Confirm input and output codecs.
4. Confirm audio and DTMF.
5. Verify DSP session use and release.
6. Test behavior when transcoder capacity is unavailable.

## Step 8: Test Conferencing

1. Start a conference from an HQ test phone.
2. Add the expected number of participants and codec types.
3. Confirm selected bridge and registration.
4. Confirm audio in every direction.
5. Verify resource release after the conference ends.
6. Test failover only within approved capacity and windows.

## Common Mistakes

### Resource Is Registered but Never Selected

The consuming device's effective MRGL cannot reach it, an earlier group wins, or the resource is incompatible with the requested codec or feature.

### Calls Fail Only Under Load

DSP or session capacity is exhausted. Size for failure and peak conditions, not average use.

### Wrong Site Resource Is Used

The device has the wrong device pool, an unexpected device-level MRGL override, or MRG order prefers a remote resource.

### DTMF Works Only When MTP Required Is Enabled

There is an underlying DTMF or signaling interworking issue. Document why the MTP is required and confirm capacity and failover.

### Conference Bridge Registers but Mixed-Codec Calls Fail

The bridge or required transcoder does not support the codec combination, or the MRGL cannot select both resources.

## Rollback

1. Restore the former device-pool or device-level MRGL.
2. Reset only affected devices if required.
3. Confirm previous media-resource selection.
4. Remove MRGs from the new MRGL.
5. Delete the MRGL only when unused.
6. Remove resources from an MRG before deleting it.
7. Do not delete or reset shared media resources without separate approval.

## Completion Checklist

- [ ] All selected resources are registered and healthy.
- [ ] MRG membership matches site and shared design.
- [ ] MRGL order prefers local then approved fallback resources.
- [ ] Device-pool inheritance and device overrides are documented.
- [ ] MTP, transcoding, conferencing, codec, and DTMF behavior are tested.
- [ ] Capacity and failure behavior are validated.
- [ ] Rollback restores previous resource selection.

Next: [Verify and Troubleshoot CUCM Configuration](verification.md).

# Configure a SIP Trunk

## Goal

Create a CUCM SIP trunk to an IOS XE gateway or CUBE at documentation address `192.0.2.11`, then make it available for route-group selection.

## Prerequisites

Document:

- remote peer address or FQDN;
- signaling source addresses on both sides;
- UDP, TCP, or TLS transport;
- destination and source ports;
- certificate names and trust chain for TLS;
- device pool, location, region, and MRGL;
- inbound Calling Search Space;
- calling and called-number formats;
- codec and early-offer policy;
- DTMF method;
- OPTIONS or other monitoring;
- redundancy and secondary destinations;
- CUBE license and IOS XE support.

Confirm IP routing, DNS, NTP, firewall, and media reachability before troubleshooting CUCM routing.

## Step 1: Create or Review the SIP Trunk Security Profile

1. Open **System > Security > SIP Trunk Security Profile**.
2. Search for an approved existing profile matching the required transport and authentication.
3. If required, select **Add New**.
4. Enter a descriptive name such as `STSP-CUBE-TCP` or the organization's naming standard.
5. Select the incoming and outgoing transport type.
6. Configure the incoming port and authentication fields according to the peer design.
7. Enable digest authentication, TLS, or related security options only when required and fully configured on both sides.
8. Save.

!!! danger "Do not weaken a shared profile"
    A security profile can be used by multiple trunks. Create a dedicated profile rather than weakening authentication or transport requirements for unrelated peers.

## Step 2: Create or Review the SIP Profile

1. Open **Device > Device Settings > SIP Profile**.
2. Copy an approved profile or select **Add New**.
3. Enter a descriptive name such as `SIP-PROFILE-CUBE`.
4. Review:
   - early-offer behavior;
   - OPTIONS ping or trunk-status behavior;
   - timers;
   - DTMF and media options exposed by the release;
   - SIP normalization script assignment, if justified;
   - SDP and presentation options;
   - retry and failover behavior.
5. Save.

Avoid changing the system Standard SIP Profile for one trunk requirement.

## Step 3: Create the SIP Trunk

1. Open **Device > Trunk**.
2. Select **Add New**.
3. Choose **SIP Trunk**.
4. Select the appropriate device protocol and trunk service type for the deployment.
5. Select **Next**.
6. Enter a device name such as `TRK-CUBE-HQ`.
7. Enter a description and device-pool assignment.
8. Select the correct **Location** and **Media Resource Group List** when not inherited as designed.
9. Set the inbound **Calling Search Space** so calls from this trunk can reach only intended partitions.
10. Review calling-party selection, presentation, rerouting CSS, out-of-dialog REFER CSS, and related call-routing fields.
11. In the SIP information section, enter destination address `192.0.2.11` or the validated FQDN.
12. Add secondary destinations only when the peer and failover design require them.
13. Enter the destination port matching the security profile and remote listener.
14. Select the configured **SIP Trunk Security Profile**.
15. Select the configured **SIP Profile**.
16. Assign a SIP normalization script only when a documented interworking issue requires it.
17. Save.
18. Select **Reset** or **Apply Config** during the approved window if required.

A trunk destination is not a route. CUCM needs a route pattern or other routing object that ultimately selects this trunk.

## Step 4: Configure TLS When Required

For a secure trunk:

1. Confirm CUCM cluster security mode and feature prerequisites.
2. Import the trusted root and intermediate certificate chain into the appropriate CUCM trust store.
3. Confirm the peer certificate Subject Alternative Name matches the FQDN or identity CUCM uses.
4. Confirm the remote peer trusts the CUCM certificate chain.
5. Use a TLS-enabled SIP trunk security profile.
6. Configure the supported TLS versions and cipher policy on both sides.
7. Verify NTP and certificate validity dates.
8. Reset the trunk only when required.

Never export or publish private keys. Plan renewal for all CUCM and CUBE nodes before certificate expiration.

## Step 5: Add the Trunk to Routing

Use [Configure Route Groups, Route Lists, and Route Patterns](pstn-routing.md):

1. Add `TRK-CUBE-HQ` to a route group.
2. Add the route group to a route list.
3. Create a route pattern that points to the route list.
4. Apply calling and called transformations at the documented boundary.

## Step 6: Verify Trunk Status

In CUCM:

1. Open the trunk and inspect status links available in the release.
2. Use RTMT to inspect SIP trunk and call-processing alarms.
3. Confirm OPTIONS or monitoring state if configured.
4. Confirm the trunk is on the expected CUCM nodes.

On the gateway or CUBE, use release-supported commands such as:

```ios
show sip-ua status
show sip-ua connections tcp brief
show dial-peer voice summary
show call active voice brief
show call history voice brief
```

A healthy OPTIONS response does not prove that destination routing, codecs, or RTP work.

## Step 7: Test Calls

Test:

- CUCM to gateway;
- gateway to CUCM;
- calling and called-number presentation;
- allowed and blocked number classes;
- early media and ringback;
- answer and bidirectional audio;
- DTMF to an IVR;
- hold, resume, transfer, redirect, and conference;
- codec negotiation and media-resource insertion;
- primary and secondary destination behavior;
- TLS recovery after service or peer restart in an approved lab.

## Troubleshooting

### Trunk Shows Down

Check OPTIONS configuration, destination address, transport, port, firewall, source address, TLS identity, certificates, DNS, NTP, and remote listener.

### SIP 403

Check source authorization, calling identity, authentication, destination permissions, and carrier policy.

### SIP 404

Check Request-URI and called-number normalization on the selected call leg.

### SIP 488

Compare SDP codecs, DTMF, encryption, fax, media direction, region policy, and MTP or transcoder requirements.

### Call Connects with One-Way Audio

Trace SDP addresses and RTP in both directions. Check routing, firewall, NAT, media binding, VRF, and inserted media resources.

## Rollback

1. Restore the previous route pattern, route list, or route-group member.
2. Reset only the affected trunk if required.
3. Confirm calls use the previous path.
4. Remove the new trunk from route groups.
5. Delete the trunk only after dependency records show it is unused.
6. Delete dedicated SIP and security profiles only after confirming no other trunk references them.

## Completion Checklist

- [ ] Security profile matches transport and authentication design.
- [ ] SIP profile matches early-offer, OPTIONS, timer, and normalization requirements.
- [ ] Inbound CSS grants only intended reachability.
- [ ] Destination, port, source identity, DNS, NTP, and TLS are verified.
- [ ] Route group, route list, and pattern select the trunk.
- [ ] Numbers, codec, DTMF, media, transfer, and failover are tested.
- [ ] Toll-fraud controls and rollback are documented.

Next: [Configure PSTN Routing](pstn-routing.md).

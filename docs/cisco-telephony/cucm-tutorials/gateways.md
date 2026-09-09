# Configure H.323 and MGCP Gateways

## Goal

Understand the CUCM configuration workflow for two legacy gateway models:

- an autonomous H.323 gateway where IOS performs substantial dial-peer routing;
- an MGCP gateway whose endpoints are controlled by CUCM.

For new designs, evaluate SIP first. Use H.323 or MGCP when supported requirements, existing architecture, or migration constraints justify them.

!!! warning "Verify exact support"
    H.323, MGCP, analog modules, endpoint types, and configuration commands vary by CUCM, IOS XE, router, NIM, and DSP release. Do not assume an older ISR gateway configuration is supported unchanged on a Catalyst 8200L.

## H.323 Gateway Tutorial

### H.323 Control Boundary

```text
CUCM route pattern/list/group
        |
        v
H.323 gateway object and signaling
        |
        v
IOS inbound and outbound dial peers
        |
        v
POTS or VoIP destination
```

CUCM selects the gateway. IOS then selects call legs using dial peers.

### Prerequisites

- stable router signaling address;
- bidirectional routing and firewall policy;
- IOS H.323 feature support;
- source-address binding plan;
- CUCM device pool, location, region, MRGL, and inbound CSS;
- codec, DTMF, fast-start or slow-start, and media policy;
- IOS inbound and outbound dial peers;
- route group, route list, and route pattern.

### Step 1: Prepare the Router

On the router:

1. Configure and verify the stable signaling interface or loopback.
2. Verify H.323 commands exist in the installed release.
3. Configure supported H.323 gateway identity and source-address binding.
4. Create explicit inbound dial peers for calls from CUCM.
5. Create outbound POTS or VoIP dial peers for required destinations.
6. Configure codec, DTMF, translations, and media behavior.
7. Verify routes between the bound address, CUCM nodes, and media endpoints.

A common legacy binding pattern uses `h323-gateway voip interface` and `h323-gateway voip bind srcaddr` under the intended interface, but confirm command context locally.

### Step 2: Add the H.323 Gateway in CUCM

1. Open **Device > Gateway**.
2. Select **Add New**.
3. Choose **H.323 Gateway**.
4. Select **Next**.
5. Enter the gateway device name or address exactly as required by the release and source-binding design.
6. Enter a description.
7. Select the correct device pool, location, and MRGL.
8. Select the inbound CSS for calls arriving from the gateway.
9. Review significant digits, calling-party selection, presentation, and transformation fields.
10. Review H.323 protocol settings such as fast-start behavior only when the design requires a change.
11. Save.
12. Reset or apply configuration only when required.

### Step 3: Add It to Routing

1. Open or create a route group.
2. Add the H.323 gateway.
3. Add the route group to a route list.
4. Point a test route pattern at the route list.
5. Confirm CSS and partition access.

### Step 4: Verify

- Confirm CUCM sends H.225 signaling to the bound gateway address.
- Confirm the router selects the intended inbound H.323 dial peer.
- Confirm the called number selects the intended outbound peer.
- Confirm H.245 or fast-start capability negotiation.
- Confirm RTP addresses, codec, DTMF, caller ID, and clearing.
- Test primary and backup CUCM or gateway behavior.

H.323 gateways do not use the same CUCM-controlled endpoint registration model as MGCP. A separate H.323 gatekeeper architecture can introduce registration, but direct CUCM gateway operation is peer based.

## MGCP Gateway Tutorial

### MGCP Control Boundary

```text
CUCM call agent
    |
    | MGCP endpoint control
    v
IOS gateway
    |
    v
FXS, FXO, or digital endpoint
```

CUCM owns more port and call-routing logic. The router provides physical interfaces, media resources, and supported fallback behavior.

### Prerequisites

- router hostname and domain naming standard;
- CUCM call-agent addresses;
- stable source interface;
- supported gateway model, modules, and endpoint types;
- CUCM group and device pool;
- MGCP fallback or SRST plan;
- interface signaling, clocking, and country settings;
- route group, route list, patterns, CSS, and partitions;
- DSP capacity.

The MGCP domain name configured on IOS must match the gateway identity expected by CUCM.

### Step 1: Prepare the Router

Using release-specific Cisco documentation:

1. Configure hostname, domain, routing, DNS, and NTP.
2. Configure the MGCP call agent and redundant CUCM hosts.
3. Configure the source interface or address.
4. Enable supported CUCM configuration download when used by the design.
5. Configure physical controller or voice-module prerequisites.
6. Configure MGCP fallback and local dial peers if survivability requires them.
7. Save the baseline and verify reachability to all CUCM nodes.

Do not paste legacy `mgcp`, `ccm-manager`, or controller commands without matching the current platform and release.

### Step 2: Add the MGCP Gateway in CUCM

1. Open **Device > Gateway**.
2. Select **Add New**.
3. Choose the supported Cisco IOS MGCP gateway type.
4. Choose **MGCP** as the protocol.
5. Select **Next**.
6. Enter the domain name that exactly matches IOS.
7. Enter a description.
8. Select the correct device pool, CUCM group, location, and MRGL.
9. Configure the supported module or slot layout to match physical hardware.
10. Save.

### Step 3: Add Endpoints

For each installed subunit or port:

1. Select the module or endpoint link on the gateway page.
2. Choose the correct endpoint type.
3. Assign port direction and signaling options.
4. For FXS, add a directory number and partition where required.
5. For FXO or digital endpoints, configure route and caller-ID behavior according to the circuit.
6. Apply country, companding, or supervision settings only from validated carrier requirements.
7. Save and reset the affected endpoint or gateway only in the approved window.

### Step 4: Add MGCP Endpoints to Routing

1. Create or open a route group.
2. Add the appropriate MGCP gateway endpoint.
3. Add the route group to a route list.
4. Point a lab route pattern at the route list.
5. Confirm CSS and partition access.

MGCP ports are represented more directly in CUCM than autonomous H.323 dial peers.

### Step 5: Verify Registration and Calls

In CUCM and RTMT:

- confirm gateway registration;
- confirm each endpoint state;
- confirm the active call-processing node;
- inspect alarms and configuration-download status.

On IOS, use release-appropriate commands to inspect MGCP and `ccm-manager` state, voice ports, controllers, DSPs, and active calls.

Test:

- CUCM to PSTN;
- PSTN to CUCM;
- calling and called-number presentation;
- codec and RTP;
- DTMF;
- analog answer and disconnect supervision;
- CUCM failover;
- MGCP fallback and restoration where configured.

## H.323 and MGCP Comparison

| Question | H.323 | MGCP |
|---|---|---|
| Who owns gateway routing logic? | More logic on IOS dial peers | More control in CUCM |
| How are ports represented? | IOS POTS dial peers and ports | CUCM-controlled endpoints |
| Does the gateway register to CUCM? | Not in the MGCP endpoint sense | Yes, as an MGCP gateway/endpoints |
| Where are number translations? | CUCM and IOS | Primarily CUCM, with supported gateway fallback logic |
| Survivability | Local dial peers and design-specific fallback | MGCP fallback and SRST design |
| Modern direction | Legacy | Existing controlled-gateway deployments; evaluate requirements |

## Common Mistakes

### H.323 Calls Arrive from the Wrong Source Address

CUCM expects the configured gateway address, but IOS sources signaling from another interface. Verify binding and routing.

### H.323 Uses Dial Peer 0

The expected inbound dial peer does not match actual calling or called information.

### MGCP Gateway Will Not Register

Check exact domain name, call-agent addresses, source interface, CUCM group, reachability, firewall, NTP, certificates where applicable, and IOS/CUCM compatibility.

### MGCP Port Exists in CUCM but Not Hardware

The configured slot or subunit does not match installed modules. Compare CUCM gateway layout with `show inventory` and platform output.

### Calls Work Normally but Fail During WAN Loss

Fallback dial peers, SRST capacity, local PSTN routes, or number transformations are incomplete.

## Rollback

1. Restore the previous route group or route pattern.
2. Confirm calls use the former gateway.
3. Restore prior IOS configuration and source binding.
4. Reset only affected CUCM devices or endpoints when required.
5. Remove endpoints before removing an MGCP gateway.
6. Remove the gateway only after route-group and dependency records are clear.

## Completion Checklist

- [ ] Exact gateway platform, modules, protocol, and release are supported.
- [ ] Source identity, routing, DNS, NTP, and firewall are verified.
- [ ] CUCM device pool, CSS, location, region, and MRGL are correct.
- [ ] Route group, route list, and pattern select the intended gateway.
- [ ] IOS dial peers are explicit for H.323.
- [ ] MGCP domain and endpoint layout match IOS hardware.
- [ ] Signaling, RTP, codec, DTMF, caller ID, supervision, failover, and recovery are tested.

Next: [Verify and Troubleshoot CUCM Configuration](verification.md).

# Emergency Calling

Emergency calling is life-safety functionality. It must deliver the call, present a valid callback identity, associate the caller with an accurate location, notify required personnel, and continue through expected failure scenarios.

!!! danger "Do not use this page as legal or production design approval"
    Requirements vary by jurisdiction, carrier, building, organization, and deployment model. Coordinate with legal, safety, facilities, carrier, and emergency-services stakeholders. Use only approved test procedures and numbers. Never place an unannounced live emergency call as a routine test.

## Core Terms

- **Dispatchable location:** Information sufficient to locate the caller within a site or facility according to applicable requirements.
- **Emergency Response Location (ERL):** Logical location grouping used by emergency-calling systems such as Cisco Emergency Responder.
- **Emergency Location Identification Number (ELIN):** Callback or routing number associated with an emergency location in designs that use it.
- **PSAP:** Public Safety Answering Point that receives emergency calls.
- **Callback:** Ability for emergency services to call back and reach an appropriate endpoint or response process.
- **On-site notification:** Alert delivered to designated personnel when an emergency call is placed, according to policy and applicable requirements.

## End-to-End Flow

```text
Caller
  |
  v
CUCM digit analysis and emergency policy
  |
  v
Cisco Emergency Responder or routing logic, when used
  |
  v
Selected local gateway, CUBE, or carrier trunk
  |
  v
Carrier emergency network
  |
  v
PSAP

Location + callback identity + on-site notification follow the call
```

A call reaching the PSAP is not the only success criterion. Validate location, callback, notification, and failure handling.

## Dial-Plan Requirements

Emergency dialing should:

- work from every endpoint class in scope;
- avoid an unnecessary access code where required by policy or law;
- account for common user dialing behavior;
- take precedence over overlapping variable-length patterns;
- remain available from restricted phones and common areas as required;
- preserve or deliberately transform calling identity;
- route through an appropriate local or approved emergency path;
- work during CUCM failover, WAN failure, and SRST where designed.

Test phones, soft clients, remote workers, analog endpoints, contact-center phones, common-area devices, conference rooms, and application-originated calls according to the approved inventory.

## Location Sources

Emergency location can depend on:

- switch port and access-switch discovery;
- subnet or IP range;
- wireless access point;
- device pool, location, or site assignment;
- user-entered location for nomadic clients;
- analog gateway and port mapping;
- carrier-managed location records;
- administrative databases and building records.

A device move can invalidate location even when ordinary calling still works. Include moves, adds, and changes in the emergency-location process.

## Analog Lines and Gateways

Analog FXO lines can provide a resilient local route, but verify:

- the line remains active and correctly labeled;
- the carrier associates the correct service address with it;
- outbound digits and access codes are correct;
- ANI or callback number is correct;
- the selected trunk-group member has the intended location identity;
- port preference does not send the call through a line associated with another site;
- PLAR and hotline devices reach the intended emergency or assistance destination;
- disconnect and callback behavior work.

Do not assume every line in a trunk group is equivalent for emergency location.

## CUCM and Route Design

Document:

- emergency route patterns and partitions;
- CSS access from every device class;
- route lists and route groups;
- local route group behavior;
- calling-party transformation;
- CER integration where used;
- primary and backup gateway paths;
- alternate routing during SRST;
- on-site notification systems;
- monitoring and alarm ownership.

Prevent ordinary number normalization from stripping or delaying emergency digits incorrectly.

## Approved Test Plan

Before testing:

- obtain approval and identify the authorized test destination;
- notify the carrier, PSAP, security desk, or other parties as required;
- choose a maintenance window and test endpoints;
- record the expected location and callback identity;
- prepare immediate escalation if information is wrong;
- avoid testing during an actual emergency or unrelated outage.

For each endpoint:

| Item | Expected | Observed |
|---|---|---|
| Dialed digits |  |  |
| Route pattern |  |  |
| Gateway or trunk |  |  |
| Calling/callback number |  |  |
| Reported location |  |  |
| On-site notification |  |  |
| Bidirectional audio |  |  |
| Callback result |  |  |
| Test timestamp |  |  |

## Failure Scenarios to Validate

- one CUCM subscriber unavailable;
- primary SIP trunk or carrier peer unavailable;
- primary gateway unavailable;
- local WAN disconnected and phones in SRST;
- one analog trunk-group member busy or failed;
- remote or nomadic user at a different location;
- phone moved to another switch port or subnet;
- incorrect or missing location record;
- callback after the original call clears;
- notification service unavailable.

Test only scenarios approved by the emergency-calling program owner.

## Change-Control Checklist

- [ ] New sites, floors, rooms, and subnets are entered into the location system.
- [ ] Phone moves trigger location review.
- [ ] Analog ports and circuits have physical labels and database mappings.
- [ ] Carrier location and callback records match the design.
- [ ] Route, CSS, partition, and transformation changes include emergency regression testing.
- [ ] CUCM, CER, CUBE, gateway, and SRST upgrades include an emergency-call test plan.
- [ ] Certificates, licenses, trunks, and notifications are monitored.
- [ ] Test evidence is retained according to policy.
- [ ] Failures have an escalation owner and correction deadline.

## Incident Response

If a test presents the wrong location or callback identity:

1. Stop additional unsupervised testing.
2. Notify the emergency-calling program owner.
3. Identify all devices sharing the affected mapping.
4. Determine whether the fault is endpoint assignment, CUCM routing, CER policy, gateway transformation, or carrier data.
5. Apply an approved mitigation or block unsafe use according to the response plan.
6. Retest through the approved process.
7. Document root cause and update change procedures.

Continue with [Dial-Plan Design](dial-plan-design.md), [SRST](srst.md), and [High Availability](high-availability.md).

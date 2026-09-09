# Cisco Voice Troubleshooting Labs

These labs turn the reference pages into hands-on practice. Use disposable lab systems or an approved maintenance environment. Each scenario requires you to identify the call legs, collect evidence, explain the first failure, apply the smallest safe correction, and verify the complete call.

## Lab Method

For every lab:

1. Record calling number, called number, direction, timestamp, and expected path.
2. Draw the inbound and outbound call legs.
3. Predict the matching CUCM object and IOS dial peers.
4. Collect read-only evidence.
5. Identify the first stage that differs from the design.
6. Make one controlled correction.
7. Retest signaling, audio, DTMF, caller ID, and disconnect where applicable.
8. Prove that configuration and behavior survive the intended failure or reboot.

!!! caution "Use debugs carefully"
    `debug voip ccapi inout` and protocol debugs can be high volume. Use a controlled window, narrow the test where supported, stop with `undebug all`, and sanitize output.

## Lab 1: Why Did the Call Use FXO 0/1/2?

**Scenario:** An outbound `911` lab call matches a POTS dial peer pointing to trunk group `1`. Ports `0/1/2` and `0/1/3` are available, with member preferences `1` and `2`.

**Collect:**

```ios
show dialplan number 911
show dial-peer voice summary
show voice port summary
show running-config | section ^trunk group|^voice-port|^dial-peer voice
show call history voice brief
```

**Questions:** Which outbound peer matched? Which trunk group did it reference? Were both ports available? What member preference applied?

??? success "Expected reasoning"
    The called number selects the POTS dial peer. That peer references the trunk group. If both ports are healthy and hunt behavior is otherwise equal, the lower member preference makes `0/1/2` the normal first choice. Prove selection with call history or a controlled CCAPI trace rather than configuration order alone.

**Verification:** Busy or administratively remove the primary only in an approved lab, place another call, and confirm the documented backup behavior and recovery.

## Lab 2: Trace FXO 0/1/5 to Extension 6985

**Scenario:** An analog line rings on `0/1/5`. The port has `connection plar 6985`, but the CUCM phone does not ring.

**Collect:**

```text
PSTN -> FXO 0/1/5 -> inbound POTS leg -> PLAR 6985
     -> outbound VoIP peer -> CUCM -> CSS/partition -> DN 6985
```

**Collect:** Voice-port state, POTS inbound peer, PLAR configuration, `show dialplan number 6985`, call history, session-target reachability, CUCM gateway or trunk status, and digit analysis.

??? success "Expected reasoning"
    PLAR supplies the destination but does not bypass outbound dial-peer matching or CUCM digit analysis. Find the first missing transition: analog seizure, PLAR number, outbound VoIP peer, signaling to CUCM, or CUCM reachability to the DN.

**Verification:** Confirm ring, answer, bidirectional audio, caller ID, and both disconnect directions.

## Lab 3: Eliminate Dial Peer 0

**Scenario:** Calls complete, but DTMF and codec behavior differ from the configured inbound VoIP dial peer.

**Collect:** Calling and called numbers as received, inbound matching criteria, active call legs, codec, DTMF, and CCAPI evidence.

??? success "Expected reasoning"
    The intended inbound peer may not match the number or source information that actually arrives. IOS then uses default dial peer 0. Create or correct an explicit inbound match supported by the release, then confirm the active call uses it.

**Verification:** Confirm inbound peer tag, codec, DTMF with an IVR, and no new overly broad toll route.

## Lab 4: Wrong Outbound Dial Peer

**Scenario:** A four-digit extension call uses a broad `T` pattern instead of the intended internal route.

**Collect:** Exact called number after translation, all matching destination patterns, pattern specificity, peer state, preference, and `show dialplan number` output.

??? success "Expected reasoning"
    Outbound selection is based on the called number and most-specific eligible match before preference resolves equivalent matches. Check whether translation changed the number or whether the intended peer is down or shut.

**Verification:** Test the target number, an adjacent internal number, a PSTN number, and an unauthorized number.

## Lab 5: One-Way RTP Audio

**Scenario:** Signaling connects normally. The branch user hears the PSTN caller, but the PSTN caller hears silence.

**Collect:** SDP or H.245 media addresses, RTP endpoints and ports, `show voip rtp connections`, routing, ACL/firewall policy, NAT, VRF, source binding, and packet captures on both sides of the suspected boundary.

??? success "Expected reasoning"
    Signaling success does not prove both RTP directions. Trace the silent direction from source to destination. Determine whether packets were never generated, sent to the wrong address, dropped in transit, or received but not decoded.

**Verification:** Confirm increasing packet counters and audible speech in both directions across primary and backup paths.

## Lab 6: DTMF Fails in Voicemail

**Scenario:** Two-way audio works, but voicemail does not recognize keypad presses.

**Collect:** SDP telephone-event advertisement, dial-peer `dtmf-relay`, CUCM trunk settings, MTP insertion, codec, and RTP event packets.

??? success "Expected reasoning"
    The two call legs may disagree on in-band tones, RTP-NTE, H.245, or another relay method. An MTP or transcoder can also change interworking. Align supported methods and test against the real application.

**Verification:** Enter a known test sequence, confirm each digit once, and ensure audio and transfer still work.

## Lab 7: Codec Mismatch and Transcoder Selection

**Scenario:** G.711 calls work, but calls from a G.729 region to a G.711-only application fail.

**Collect:** CUCM regions, SDP or H.245 offers, dial-peer codec lists, transcoder registration, MRGL reachability, and DSP capacity.

??? success "Expected reasoning"
    If the endpoints have no common codec, CUCM may require a compatible transcoder. A registered transcoder is not enough if the device cannot reach it through its effective MRGL or the DSP sessions are exhausted.

**Verification:** Confirm selected codec on each leg, transcoder use, audio, DTMF, and behavior when transcoder capacity is intentionally unavailable in the lab.

## Lab 8: CSS and Partition Block the Route

**Scenario:** Extension `6985` can call a PSTN destination, but extension `6986` receives reorder.

**Collect:** Line and device CSS for both phones, route-pattern partition, translation patterns, forwarding CSS, device pool, and Dialed Number Analyzer results.

??? success "Expected reasoning"
    Compare the effective calling context rather than only the dialed digits. The failing phone may not be allowed to search the route pattern's partition, or a different visible translation pattern may win.

**Verification:** Test permitted and blocked number classes from both phones and confirm the change grants no unintended access.

## Lab 9: Trunk-Group Member Is Never Used

**Scenario:** FXO `0/1/3` is intended as backup but calls fail when `0/1/2` is busy.

**Collect:** Port administrative and operational state, group membership, member preference, signaling, circuit battery, POTS peer, hunt behavior, and call clearing cause.

??? success "Expected reasoning"
    A configured backup may be unavailable because of shutdown state, failed circuit, incorrect group name, signaling mismatch, or hunt behavior that does not retry after the observed cause.

**Verification:** Place an approved call on the primary, generate another call, confirm use of the backup, then confirm normal preference after release.

## Lab 10: SIP OPTIONS Shows the Peer Down

**Scenario:** IP reachability works, but the SIP dial peer remains unavailable.

**Collect:** OPTIONS source and destination, transport, port, response code, TLS identity, firewall policy, keepalive profile, peer status, and packet capture.

??? success "Expected reasoning"
    Ping proves IP reachability, not SIP health. The peer may reject the source, require a different transport, fail TLS validation, or return a response not treated as healthy by the configured profile.

**Verification:** Confirm healthy monitoring, successful call setup, failure detection, alternate target selection, and recovery.

## Lab 11: Incorrect POTS Digit Stripping

**Scenario:** The user dials `9` plus a ten-digit number, but the carrier receives too few digits.

**Collect:** Number after CUCM transformation, gateway inbound number, outbound pattern, translation profile, `prefix`, `forward-digits`, and translation-rule test output.

??? success "Expected reasoning"
    POTS destination-pattern stripping, a translation profile, and `forward-digits` can all alter the final number. The access code may be removed twice. Assign one clear transformation boundary and verify the exact final digits.

**Verification:** Test local, long-distance, emergency, and blocked patterns without placing unauthorized calls.

## Lab 12: Analog Port Remains Seized

**Scenario:** The far party disconnects, but the FXO port remains off-hook and cannot accept another call.

**Collect:** Carrier or PBX supervision method, voice-port state, disconnect tones, battery behavior, regional settings, timers, and event timeline.

??? success "Expected reasoning"
    The gateway is not detecting the disconnect supervision delivered by the far side. Determine whether the circuit provides battery denial, reversal, supervisory tone, or another method. Do not tune timers or tones by guesswork.

**Verification:** Test caller-first disconnect, called-party-first disconnect, no answer, busy, repeated calls, and carrier failure.

## Lab Completion Record

| Lab | Date | Platform/release | Root cause explained | Fix verified | Rollback tested |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |
| 6 |  |  |  |  |  |
| 7 |  |  |  |  |  |
| 8 |  |  |  |  |  |
| 9 |  |  |  |  |  |
| 10 |  |  |  |  |  |
| 11 |  |  |  |  |  |
| 12 |  |  |  |  |  |

Use [Operational Checklists](operational-checklists.md) for real changes and [Troubleshooting](troubleshooting.md) for command selection.

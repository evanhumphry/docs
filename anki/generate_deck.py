#!/usr/bin/env python3
"""Generate an Anki .apkg deck from the documentation site content.

Run: python3 anki/generate_deck.py
Output: anki/evans-docs-study.apkg

Cards are grouped into subdecks under "Evan's Docs Study" so they can be
studied per-topic or all together. Re-running updates existing notes (stable
GUIDs) rather than creating duplicates on re-import.
"""

import hashlib
import genanki

OUTPUT = "anki/evans-docs-study.apkg"
TOP = "Evan's Docs Study"


def stable_id(name: str) -> int:
    """Deterministic id in genanki's recommended [2^30, 2^31) range."""
    h = int(hashlib.sha1(name.encode()).hexdigest()[:8], 16)
    return (1 << 30) | (h & ((1 << 30) - 1))


MODEL = genanki.Model(
    stable_id("evans-docs-basic-model"),
    "Evan's Docs Basic",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<div class="front">{{Front}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="back">{{Back}}</div>',
        }
    ],
    css="""
.card {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 19px;
  text-align: left;
  color: #1b1b1b;
  background: #ffffff;
  padding: 16px;
}
.front { font-weight: 600; }
.back { margin-top: 6px; }
hr#answer { border: none; border-top: 2px solid #ddd; margin: 12px 0; }
code { background: #f2f2f2; padding: 1px 5px; border-radius: 4px;
       font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 0.92em; }
pre { background: #f5f5f5; padding: 10px 12px; border-radius: 6px;
      overflow-x: auto; font-family: "SF Mono", Menlo, Consolas, monospace;
      font-size: 0.85em; line-height: 1.35; white-space: pre; }
table { border-collapse: collapse; margin-top: 4px; }
td, th { border: 1px solid #ccc; padding: 3px 8px; }
.nightMode .card { color: #e6e6e6; background: #2b2b2b; }
.nightMode code, .nightMode pre { background: #3a3a3a; }
.nightMode hr#answer { border-top-color: #555; }
.nightMode td, .nightMode th { border-color: #555; }
""",
)


def fmt(s: str) -> str:
    s = s.strip("\n")
    if "<pre" in s or "<table" in s:
        return s
    return s.replace("\n", "<br>")


def pre(code_text: str) -> str:
    esc = (code_text.strip("\n")
           .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f"<pre>{esc}</pre>"


# (subdeck, front, back) — back may contain HTML; pre() for code blocks.
CARDS = []


def add(deck, front, back):
    CARDS.append((deck, front, back))


# ───────────────────────── Network Fundamentals ─────────────────────────
ND = "CCNA::Network Fundamentals"
add(ND, "OSI Layer 7 — name and role?",
    "<b>Application</b> — user-facing protocols.\nExamples: HTTP, DNS, SMTP, FTP, SSH")
add(ND, "OSI Layer 6 — name and role?",
    "<b>Presentation</b> — data format, encryption, compression.\nExamples: SSL/TLS, JPEG, ASCII")
add(ND, "OSI Layer 5 — name and role?",
    "<b>Session</b> — session management.\nExamples: NetBIOS, PPTP")
add(ND, "OSI Layer 4 — name and role?",
    "<b>Transport</b> — end-to-end delivery, segmentation.\nExamples: TCP, UDP")
add(ND, "OSI Layer 3 — name and role?",
    "<b>Network</b> — logical addressing, routing.\nExamples: IP, ICMP, OSPF, EIGRP")
add(ND, "OSI Layer 2 — name and role?",
    "<b>Data Link</b> — MAC addressing, framing, error detection.\nExamples: Ethernet, 802.11, ARP")
add(ND, "OSI Layer 1 — name and role?",
    "<b>Physical</b> — bits over wire/wireless.\nExamples: cables, hubs, connectors")
add(ND, "Which OSI layer does a router primarily operate at?",
    "Layer 3 (Network) — it uses logical (IP) addressing to route packets.")
add(ND, "Which OSI layer does a switch primarily operate at?",
    "Layer 2 (Data Link) — it forwards frames using MAC addresses.")
add(ND, "OSI PDU names by layer (top to bottom)?",
    "Layers 7–5: <b>Data</b>\nLayer 4: <b>Segment</b>\nLayer 3: <b>Packet</b>\nLayer 2: <b>Frame</b>\nLayer 1: <b>Bits</b>")
add(ND, "What are the 4 layers of the TCP/IP model?",
    "<b>Application</b> (OSI 5–7), <b>Transport</b> (OSI 4), <b>Internet</b> (OSI 3), <b>Network Access</b> (OSI 1–2)")
add(ND, "Which TCP/IP layer maps to OSI Layer 3, and what runs there?",
    "<b>Internet</b> layer — IP, ICMP, ARP")
add(ND, "TCP vs UDP: connection model?",
    "TCP = connection-oriented (3-way handshake).\nUDP = connectionless (best-effort).")
add(ND, "TCP vs UDP: reliability and ordering?",
    "TCP = guaranteed, in-order delivery, flow control (windowing).\nUDP = best-effort, no ordering, no flow control.")
add(ND, "TCP vs UDP: header size?",
    "TCP = 20 bytes.\nUDP = 8 bytes.")
add(ND, "Typical TCP use cases?",
    "HTTP, SSH, FTP, SMTP — anything needing reliable delivery.")
add(ND, "Typical UDP use cases?",
    "DNS, DHCP, VoIP, TFTP — speed-sensitive / tolerant of loss.")
add(ND, "Steps of the TCP three-way handshake?",
    "1. <b>SYN</b> — client → server\n2. <b>SYN-ACK</b> — server → client\n3. <b>ACK</b> — client → server (established)")
add(ND, "Steps of TCP connection teardown?",
    "1. <b>FIN</b> (initiator)\n2. <b>ACK</b> (receiver)\n3. <b>FIN</b> (receiver)\n4. <b>ACK</b> (initiator) — closed")
add(ND, "Straight-through vs crossover cable — when to use each?",
    "<b>Straight-through</b>: unlike devices (PC↔switch, router↔switch).\n<b>Crossover</b>: like devices (switch↔switch, PC↔PC).\nModern gear uses Auto-MDIX to detect automatically.")
add(ND, "Half duplex vs full duplex?",
    "<b>Half</b>: send OR receive, not both (hubs).\n<b>Full</b>: send AND receive simultaneously (switches).\nMismatch → collisions and poor performance.")
add(ND, "Max distance and speed of Cat 6a?",
    "10GBASE-T, 100 m, 10 Gbps")
add(ND, "Single-mode fiber (1000BASE-LX) max distance?",
    "5 km at 1 Gbps")

# Ports — forward
PORTS = [
    ("20", "TCP", "FTP Data"), ("21", "TCP", "FTP Control"), ("22", "TCP", "SSH"),
    ("23", "TCP", "Telnet"), ("25", "TCP", "SMTP"), ("53", "TCP/UDP", "DNS"),
    ("67", "UDP", "DHCP Server"), ("68", "UDP", "DHCP Client"), ("69", "UDP", "TFTP"),
    ("80", "TCP", "HTTP"), ("110", "TCP", "POP3"), ("143", "TCP", "IMAP"),
    ("161", "UDP", "SNMP"), ("443", "TCP", "HTTPS"), ("514", "UDP", "Syslog"),
    ("3389", "TCP", "RDP"),
]
for num, proto, svc in PORTS:
    add(ND, f"Port {num} — which service?", f"<b>{svc}</b> ({proto})")
# Ports — reverse (key ones)
for svc, ans in [
    ("SSH", "TCP 22"), ("Telnet", "TCP 23"), ("HTTP", "TCP 80"), ("HTTPS", "TCP 443"),
    ("DNS", "TCP/UDP 53"), ("SMTP", "TCP 25"), ("FTP (control / data)", "TCP 21 / TCP 20"),
    ("TFTP", "UDP 69"), ("SNMP", "UDP 161"), ("Syslog", "UDP 514"), ("RDP", "TCP 3389"),
    ("DHCP (server / client)", "UDP 67 / UDP 68"),
]:
    add(ND, f"Which port number(s) does {svc} use?", ans)

# ───────────────────────── IP Addressing & Subnetting ─────────────────────────
IP = "CCNA::IP Addressing"
add(IP, "IPv4 Class A range and default mask?",
    "1.0.0.0 – 126.255.255.255, /8 (255.0.0.0). Large networks.")
add(IP, "IPv4 Class B range and default mask?",
    "128.0.0.0 – 191.255.255.255, /16 (255.255.0.0). Medium networks.")
add(IP, "IPv4 Class C range and default mask?",
    "192.0.0.0 – 223.255.255.255, /24 (255.255.255.0). Small networks.")
add(IP, "What are Class D and Class E used for?",
    "Class D (224.0.0.0–239.255.255.255) = multicast.\nClass E (240.0.0.0–255.255.255.255) = experimental.")
add(IP, "What is 127.0.0.0/8 reserved for?",
    "Loopback (localhost).")
add(IP, "The three RFC 1918 private IP ranges?",
    "10.0.0.0/8 (A)\n172.16.0.0/12 (B)\n192.168.0.0/16 (C)")
add(IP, "Powers of 2 from 2^0 to 2^7?",
    "1, 2, 4, 8, 16, 32, 64, 128")
add(IP, "Three key subnetting formulas?",
    "Usable hosts = 2^(host bits) − 2\nNumber of subnets = 2^(borrowed bits)\nBlock size = 256 − mask octet value")
add(IP, "Subnet mask, block size, usable hosts for /26?",
    "255.255.255.192, block 64, 62 usable hosts")
add(IP, "Subnet mask, block size, usable hosts for /27?",
    "255.255.255.224, block 32, 30 usable hosts")
add(IP, "Subnet mask, block size, usable hosts for /28?",
    "255.255.255.240, block 16, 14 usable hosts")
add(IP, "Subnet mask, block size, usable hosts for /29?",
    "255.255.255.248, block 8, 6 usable hosts")
add(IP, "Subnet mask and usable hosts for /30? Typical use?",
    "255.255.255.252, 2 usable. Used for point-to-point links.")
add(IP, "What is a /31 used for?",
    "Point-to-point links (RFC 3021) — 2 addresses, both usable, no broadcast.")
add(IP, "How do you calculate a wildcard mask from a subnet mask?",
    "Wildcard = 255.255.255.255 − subnet mask.\ne.g. 255.255.255.192 → 0.0.0.63")
add(IP, "Wildcard mask for a /24 and a /26?",
    "/24 → 0.0.0.255\n/26 → 0.0.0.63")
add(IP, "Given 192.168.1.0/26: block size, subnets, hosts/subnet?",
    "Mask 255.255.255.192, block 64.\nSubnets: .0, .64, .128, .192\nHosts/subnet: 2^6 − 2 = 62")
add(IP, "How many bits is an IPv6 address, and how is it written?",
    "128 bits, eight groups of four hex digits.\ne.g. 2001:0db8:0000:0000:0000:0000:0000:0001")
add(IP, "IPv6 shortening rules?",
    "Drop leading zeros in each group; replace one run of all-zero groups with ::  (only once).\n2001:0db8:0000:...:0001 → 2001:db8::1")
add(IP, "IPv6 Global Unicast prefix?", "2000::/3 — routable on the internet")
add(IP, "IPv6 Link-Local prefix and scope?",
    "FE80::/10 — local link only, auto-configured")
add(IP, "IPv6 Unique Local prefix?",
    "FC00::/7 — private addresses (like RFC 1918)")
add(IP, "IPv6 Multicast prefix and loopback address?",
    "Multicast FF00::/8; Loopback ::1/128")
add(IP, "EUI-64 process to build an interface ID from a MAC?",
    "1. Split MAC in half\n2. Insert FFFE in the middle\n3. Flip the 7th bit of the first byte")
add(IP, "What problem does VLSM solve?",
    "It lets subnets use different prefix lengths so each is sized to fit, instead of one fixed mask wasting addresses (e.g. a /30 P2P link vs a /24 LAN).")
add(IP, "VLSM design process (4 steps)?",
    "1. List subnets, largest host count first\n2. Pick smallest prefix that fits each\n3. Assign sequentially (next starts after prev broadcast)\n4. Verify no overlap")
add(IP, "Prefix for a subnet needing 100 hosts? 50 hosts? 25 hosts?",
    "100 → /25 (126 usable)\n50 → /26 (62 usable)\n25 → /27 (30 usable)")
add(IP, "Common VLSM mistakes?",
    "Not sorting largest-first (fragments space); forgetting the −2; overlapping subnets (next must start after prev broadcast).")
add(IP, "What is the standard IPv6 subnet size for host segments, and why?",
    "/64 — required for SLAAC (Stateless Address Autoconfiguration) to work.")
add(IP, "How is a /48 IPv6 allocation structured?",
    "48-bit global prefix (from ISP) | 16-bit subnet ID (you assign, 65,536 subnets) | 64-bit interface ID")
add(IP, "IPv6 point-to-point link prefix options?",
    "/64 (simplest), /127 (RFC 6164, conserves and avoids ping-pong), /126 (mimics IPv4 /30).")
add(IP, "IPv4 VLSM vs IPv6 VLSM — main difference in goal?",
    "IPv4: conserve addresses (host count drives prefix, sort largest-first).\nIPv6: organize cleanly — LAN is always /64, host count irrelevant.")

# ───────────────────────── Switching ─────────────────────────
SW = "CCNA::Switching"
add(SW, "What does a VLAN create, and what's needed for inter-VLAN traffic?",
    "VLANs logically segment a switch into separate broadcast domains. Traffic between VLANs needs a Layer 3 device (router or L3 switch).")
add(SW, "Access port vs trunk port?",
    "<b>Access</b>: belongs to a single VLAN, connects end devices.\n<b>Trunk</b>: carries multiple VLANs between switches using 802.1Q tagging.")
add(SW, "What is the native VLAN?",
    "The untagged VLAN on a trunk (default VLAN 1). Must match on both ends of the trunk.")
add(SW, "Best practice regarding VLAN 1?",
    "It's the default VLAN (all ports start there). Don't use it for user traffic.")
add(SW, "What is router-on-a-stick?",
    "Inter-VLAN routing using one router interface split into sub-interfaces (one per VLAN), with the switch port set as a trunk.")
add(SW, "Key sub-interface config line that's required per VLAN?",
    "<code>encapsulation dot1Q &lt;vlan-id&gt;</code> on each sub-interface. The physical interface gets no IP.")
add(SW, "What is an SVI?",
    "Switched Virtual Interface — a VLAN interface on a Layer 3 switch (<code>interface vlan 10</code>) used for inter-VLAN routing instead of a router. Requires <code>ip routing</code>.")
add(SW, "What does STP prevent, and how?",
    "Prevents Layer 2 loops by blocking redundant paths so only one active path exists between any two switches.")
add(SW, "How is the STP root bridge elected?",
    "Lowest Bridge ID (priority + MAC) becomes root.")
add(SW, "STP port roles in selecting paths?",
    "Root port (best port toward root on each non-root switch); Designated port (one per segment, lowest cost); other redundant ports are Blocked.")
add(SW, "STP port states and their durations?",
    "Blocking (20s, BPDUs only), Listening (15s), Learning (15s, learns MACs), Forwarding, Disabled.\nConvergence ~50s.")
add(SW, "STP 802.1D path costs: 10M / 100M / 1G / 10G?",
    "10 Mbps = 100\n100 Mbps = 19\n1 Gbps = 4\n10 Gbps = 2")
add(SW, "RSTP (802.1w) port roles?",
    "Root, Designated, Alternate (backup to root port), Backup. Converges in seconds.")
add(SW, "RSTP port states?",
    "Discarding, Learning, Forwarding")
add(SW, "What do PortFast and BPDU Guard do?",
    "PortFast: skips STP listening/learning on access ports (end devices only).\nBPDU Guard: err-disables a port if it receives a BPDU.")
add(SW, "STP priority must be a multiple of what value?",
    "4096")
add(SW, "What is EtherChannel?",
    "Bundles multiple physical links into one logical link for more bandwidth + redundancy. STP treats it as a single link.")
add(SW, "EtherChannel negotiation protocols and modes?",
    "<b>LACP</b> (open, 802.3ad): Active / Passive.\n<b>PAgP</b> (Cisco): Desirable / Auto.\nAt least one side must be Active (LACP) or Desirable (PAgP). <code>mode on</code> = forced, no negotiation.")
add(SW, "EtherChannel member port requirements?",
    "All ports must match: speed/duplex, VLAN config, switchport mode (access/trunk), and STP settings.")

# ───────────────────────── Routing ─────────────────────────
RT = "CCNA::Routing"
add(RT, "Three ways routes are learned?",
    "Directly connected, static (manual), and dynamic routing protocols (OSPF, EIGRP, BGP).")
add(RT, "What does Administrative Distance decide?",
    "When multiple sources offer a route to the same destination, the lowest AD is preferred (it ranks trustworthiness of the source).")
add(RT, "AD: Directly connected / Static / eBGP?",
    "Connected = 0, Static = 1, eBGP = 20")
add(RT, "AD: EIGRP internal / OSPF / RIP / EIGRP external / iBGP?",
    "EIGRP internal = 90, OSPF = 110, RIP = 120, EIGRP external = 170, iBGP = 200")
add(RT, "Syntax of a default route?",
    pre("ip route 0.0.0.0 0.0.0.0 192.168.1.1"))
add(RT, "What is a floating static route?",
    "A backup static route with a higher AD than the primary (dynamic) route, so it's only used when the primary fails.\n" + pre("ip route 10.0.0.0 255.255.255.0 192.168.2.1 210"))
add(RT, "Main drawback of router-on-a-stick?",
    "All inter-VLAN traffic shares one physical link → bandwidth bottleneck. Use a Layer 3 switch with SVIs for higher performance.")
add(RT, "OSPF: type, algorithm, AD, metric?",
    "Link-state, Dijkstra (SPF), AD 110, metric = cost (reference BW / interface BW).")
add(RT, "What IP protocol number and multicast addresses does OSPF use?",
    "IP protocol 89. Multicast 224.0.0.5 (all routers), 224.0.0.6 (DR/BDR).")
add(RT, "OSPF default hello and dead timers?",
    "Hello 10s (broadcast) / 30s (non-broadcast). Dead timer = 4× hello.")
add(RT, "What is OSPF Area 0?",
    "The backbone area — every other area must connect to it.")
add(RT, "OSPF ABR vs ASBR?",
    "ABR (Area Border Router) connects two or more areas.\nASBR (AS Boundary Router) connects OSPF to another routing domain.")
add(RT, "OSPF neighbor states in order?",
    "Down → Init → 2-Way → ExStart → Exchange → Loading → Full")
add(RT, "What must match for two routers to form an OSPF adjacency?",
    "Area ID, hello/dead timers, subnet + mask, authentication, stub flag, and MTU (for Full).")
add(RT, "OSPF DR/BDR election rules?",
    "Highest priority wins (default 1, 0–255); priority 0 never becomes DR/BDR; tie → highest Router ID. Non-preemptive.")
add(RT, "EIGRP: type, AD, protocol number, multicast?",
    "Advanced distance-vector (hybrid), Cisco. AD 90 internal / 170 external. IP protocol 88. Multicast 224.0.0.10.")
add(RT, "EIGRP metric components (default)?",
    "Composite of bandwidth + delay (also reliability, load available). Uses the DUAL algorithm.")
add(RT, "EIGRP: successor vs feasible successor?",
    "Successor = best route (in routing table).\nFeasible successor = backup route meeting the feasibility condition.")
add(RT, "EIGRP feasibility condition?",
    "A route is a feasible successor if its Reported Distance (RD) < the Feasible Distance (FD) of the current successor. Guarantees a loop-free path.")
add(RT, "What is route summarization, and where is it done in OSPF?",
    "Combining multiple routes into one summary route to shrink the table. In OSPF it's done on the ABR with <code>area &lt;n&gt; range</code>.")

# ───────────────────────── OSPF (deep) ─────────────────────────
OS = "CCNA::OSPF"
add(OS, "OSPF transport — does it run over TCP or UDP?",
    "Neither — OSPF runs directly over IP as protocol 89.")
add(OS, "OSPF cost formula and default reference bandwidth?",
    "Cost = Reference BW / Interface BW. Default reference = 100 Mbps (10^8).")
add(OS, "Why set auto-cost reference-bandwidth, and what's the catch?",
    "By default FastEthernet and GigabitEthernet both cost 1. Raise the reference (e.g. 10000 = 10 Gbps) so faster links get lower cost. Set the SAME value on every router.")
add(OS, "OSPF default cost for Gig vs Fast at reference 10G?",
    "FastEthernet = 100, GigabitEthernet = 10, 10GbE = 1")
add(OS, "How is the OSPF Router ID chosen?",
    "Manual config > highest loopback IP > highest physical interface IP.")
add(OS, "Is the OSPF process ID significant between routers?",
    "No — <code>router ospf 1</code>'s process ID is locally significant; it need not match neighbors.")
add(OS, "What does passive-interface do in OSPF?",
    "Stops sending hellos on that interface (no neighbors formed) but still advertises the network.")
add(OS, "Preferred way to enable OSPF on an interface (vs network statements)?",
    pre("interface GigabitEthernet0/0\n ip address 192.168.1.1 255.255.255.0\n ip ospf 1 area 0") + "Cleaner; avoids wildcard mask mistakes.")
add(OS, "OSPF stuck in ExStart/Exchange — most likely cause?",
    "MTU mismatch. Fix MTU on both sides (<code>ip mtu 1500</code>).")
add(OS, "OSPF stuck in 2-Way — is it a problem?",
    "Normal for DROther↔DROther on multi-access segments — only DR and BDR form full adjacencies with everyone.")
add(OS, "How do you inject a default route into OSPF?",
    pre("ip route 0.0.0.0 0.0.0.0 203.0.113.1\nrouter ospf 1\n default-information originate") + "Add <code>always</code> to advertise even without a static default in the table.")
add(OS, "OSPF MD5 authentication interface config?",
    pre("interface Gi0/1\n ip ospf authentication message-digest\n ip ospf message-digest-key 1 md5 SecurePass") + "Same key ID and password on both sides.")
add(OS, "Is there DR/BDR election on point-to-point links?",
    "No — DR/BDR is only elected on multi-access networks (Ethernet).")
add(OS, "Order to troubleshoot OSPF neighbors not forming?",
    "L1/2 link up → same subnet → interface in right area → timers match → area match → auth match → MTU → ACL blocking protocol 89 / 224.0.0.5-6.")

# ───────────────────────── ACLs ─────────────────────────
AC = "CCNA::ACLs"
add(AC, "How are ACLs processed, and what's at the end of every ACL?",
    "Top-down — first match wins, processing stops. There's an implicit <code>deny any</code> at the end.")
add(AC, "ACL number ranges: standard vs extended?",
    "Standard: 1–99, 1300–1999.\nExtended: 100–199, 2000–2699.")
add(AC, "What does a standard ACL match on? An extended ACL?",
    "Standard: source IP only.\nExtended: source/dest IP, protocol, and port.")
add(AC, "ACL placement rule: standard vs extended?",
    "Standard → near the <b>destination</b> (only matches source, so placing near source blocks too much).\nExtended → near the <b>source</b> (specific enough to filter early).")
add(AC, "ACL wildcard mask: meaning of a 0 bit vs 1 bit?",
    "0 = must match; 1 = don't care. It's the inverse of a subnet mask.")
add(AC, "Shorthand: 'host 10.0.0.1' and 'any' expand to what wildcards?",
    "<code>host 10.0.0.1</code> = 10.0.0.1 0.0.0.0\n<code>any</code> = 0.0.0.0 255.255.255.255")
add(AC, "Which command applies an ACL to VTY lines, and why not ip access-group?",
    "Use <code>access-class &lt;acl&gt; in</code> on the VTY lines. <code>ip access-group</code> is for interfaces (traffic through the router), not the VTY lines (traffic to the router).")
add(AC, "ACL direction: in vs out (from whose perspective)?",
    "From the router's perspective on that interface.\n<code>in</code> = packets arriving on the interface; <code>out</code> = packets leaving it.")
add(AC, "How many ACLs can be applied per interface?",
    "One per interface, per direction, per protocol.")
add(AC, "Extended ACL to allow only HTTP/HTTPS from a subnet?",
    pre("ip access-list extended ALLOW_WEB\n permit tcp 192.168.1.0 0.0.0.255 any eq 80\n permit tcp 192.168.1.0 0.0.0.255 any eq 443\n deny ip any any"))
add(AC, "Do ACL changes need to be reapplied to take effect?",
    "No — changes take effect immediately. Named ACLs can also be edited by sequence number.")

# ───────────────────────── Network Services ─────────────────────────
NS = "CCNA::Network Services"
add(NS, "DHCP DORA steps?",
    "1. <b>Discover</b> (client→broadcast)\n2. <b>Offer</b> (server→client)\n3. <b>Request</b> (client→broadcast)\n4. <b>Ack</b> (server→client, lease confirmed)")
add(NS, "How does DHCP work across subnets (relay)?",
    "Configure <code>ip helper-address &lt;server&gt;</code> on the router interface facing the clients; it forwards the broadcast to the remote DHCP server.")
add(NS, "DNS record: A vs AAAA?",
    "A = hostname → IPv4. AAAA = hostname → IPv6.")
add(NS, "DNS record: CNAME / MX / NS?",
    "CNAME = alias to another hostname. MX = mail server. NS = authoritative name server.")
add(NS, "DNS record: PTR / SOA / TXT?",
    "PTR = reverse lookup (IP→hostname). SOA = Start of Authority (zone metadata). TXT = arbitrary text (SPF, DKIM).")
add(NS, "NAT terms: Inside Local vs Inside Global?",
    "Inside Local = private IP on the internal network.\nInside Global = public IP representing that internal host.")
add(NS, "NAT terms: Outside Local vs Outside Global?",
    "Outside Local = external host's IP as seen internally.\nOutside Global = the external host's actual public IP.")
add(NS, "Static vs Dynamic NAT vs PAT?",
    "Static = fixed 1:1 mapping (servers).\nDynamic = pool of public IPs assigned on demand (ACL picks hosts).\nPAT (overload) = many hosts share one public IP, tracked by port. Most common.")
add(NS, "Key NAT interface config?",
    pre("interface Gi0/0\n ip nat inside\ninterface Gi0/1\n ip nat outside"))
add(NS, "Command to view active NAT translations and to clear them?",
    "<code>show ip nat translations</code> to view; <code>clear ip nat translation *</code> to clear (needed when changing NAT config).")
add(NS, "What does NTP do and why does it matter?",
    "Synchronizes clocks across devices. Accurate time is critical for logging and troubleshooting.")
add(NS, "Syslog severity levels 0–7?",
    "0 Emergency, 1 Alert, 2 Critical, 3 Error, 4 Warning, 5 Notification, 6 Informational, 7 Debugging.")
add(NS, "Mnemonic for Syslog severity levels?",
    "<b>E</b>very <b>A</b>wesome <b>C</b>isco <b>E</b>ngineer <b>W</b>ill <b>N</b>eed <b>I</b>ce cream <b>D</b>aily.")
add(NS, "SNMP versions and their security?",
    "v1 & v2c: community string, no encryption.\nv3: username/password, optional encryption.")

# ───────────────────────── Security ─────────────────────────
SE = "CCNA::Security"
add(SE, "Port security violation modes and their actions?",
    "<b>Protect</b>: drop silently (no log, no shut).\n<b>Restrict</b>: drop + log + increment counter.\n<b>Shutdown</b> (default): err-disable the port + log.")
add(SE, "What does 'sticky' do in port security?",
    "<code>switchport port-security mac-address sticky</code> dynamically learns MACs and saves them to the running-config.")
add(SE, "How do you recover an err-disabled port?",
    "Manually: <code>shutdown</code> then <code>no shutdown</code>.\nAuto: <code>errdisable recovery cause psecure-violation</code> + <code>errdisable recovery interval 300</code>.")
add(SE, "What does DHCP snooping prevent, and how?",
    "Prevents rogue DHCP servers. Ports are trusted (DHCP servers/uplinks) or untrusted (default — only DHCP requests allowed).")
add(SE, "What does Dynamic ARP Inspection (DAI) do?",
    "Validates ARP packets against the DHCP snooping binding table to stop ARP spoofing.")
add(SE, "What do the three A's in AAA stand for?",
    "Authentication (who are you?), Authorization (what can you do?), Accounting (what did you do?).")
add(SE, "RADIUS vs TACACS+ (transport, scope)?",
    "RADIUS: UDP 1812/1813, encrypts only the password.\nTACACS+: TCP 49, Cisco proprietary, encrypts the entire payload.")
add(SE, "Commands to enable SSH on a Cisco device?",
    pre("ip domain-name example.com\ncrypto key generate rsa modulus 2048\nip ssh version 2") + "Then on VTY: <code>transport input ssh</code> + <code>login local</code>.")
add(SE, "enable secret vs enable password — which to use?",
    "Use <code>enable secret</code> — it's hashed. <code>enable password</code> is weakly stored / deprecated.")

# ───────────────────────── WAN ─────────────────────────
WN = "CCNA::WAN"
add(WN, "WAN terms: CPE, DCE, DTE, Demarcation?",
    "CPE = Customer Premises Equipment (router/modem).\nDCE = Data Comms Equipment (provides clocking).\nDTE = Data Terminal Equipment (connects to DCE).\nDemarc = where ISP responsibility ends.")
add(WN, "Common WAN connection types?",
    "Leased line (T1/T3), Metro Ethernet, MPLS, Broadband (DSL/cable), Cellular (4G/5G), Satellite.")
add(WN, "Three VPN types?",
    "Site-to-Site (router↔router), Remote Access (users→corp), DMVPN (dynamic hub-and-spoke + spoke-to-spoke).")
add(WN, "IPsec protocols: IKE, ESP, AH?",
    "IKE = key exchange / SA negotiation (UDP 500).\nESP = encryption + authentication (IP protocol 50).\nAH = authentication only, no encryption (IP protocol 51).")
add(WN, "What is GRE, and is it encrypted?",
    "Generic Routing Encapsulation — tunnels packets inside IP. Not encrypted on its own; often paired with IPsec.")
add(WN, "HDLC vs PPP?",
    "HDLC: default Cisco serial encapsulation, Cisco version proprietary, no auth.\nPPP: open standard, multi-vendor, supports authentication and multilink.")
add(WN, "PPP authentication: PAP vs CHAP?",
    "PAP = plain text. CHAP = challenge-based, more secure.")
add(WN, "QoS traffic priority order (highest to lowest)?",
    "Voice > Video > Critical Data > Best Effort > Scavenger.")
add(WN, "Four QoS mechanisms?",
    "Classification & Marking (DSCP/CoS), Queuing (LLQ/CBWFQ), Policing (drop over rate), Shaping (buffer over rate).")
add(WN, "Policing vs shaping?",
    "Policing drops traffic exceeding the rate; shaping buffers it (smoother).")

# ───────────────────────── Wireless ─────────────────────────
WL = "CCNA::Wireless"
add(WL, "802.11n — frequency, max speed, Wi-Fi name?",
    "2.4/5 GHz, 600 Mbps, Wi-Fi 4")
add(WL, "802.11ac — frequency, max speed, Wi-Fi name?",
    "5 GHz, 6.9 Gbps, Wi-Fi 5")
add(WL, "802.11ax — frequency, max speed, Wi-Fi name?",
    "2.4/5/6 GHz, 9.6 Gbps, Wi-Fi 6/6E")
add(WL, "2.4 GHz vs 5 GHz tradeoffs?",
    "2.4 GHz: longer range, slower, only 3 non-overlapping channels (1,6,11), more interference.\n5 GHz: shorter range, faster, 24 non-overlapping channels, less interference.")
add(WL, "Autonomous vs controller-based (WLC) APs?",
    "Autonomous: each AP configured/managed independently (small deployments).\nController-based: WLC centrally manages lightweight APs via CAPWAP (enterprise scale).")
add(WL, "CAPWAP tunnel ports?",
    "Control tunnel = UDP 5246 (management/config).\nData tunnel = UDP 5247 (client data).")
add(WL, "AP modes: Local, FlexConnect, Monitor, Sniffer, Bridge?",
    "Local: default, serves clients + monitors.\nFlexConnect: local switching at branches.\nMonitor: passive (IDS, rogue detection).\nSniffer: captures frames for analysis.\nBridge: point-to-point/multipoint.")
add(WL, "WLC physical port: Service port — purpose?",
    "Out-of-band management dedicated to recovery/maintenance. Always Layer 2, untagged, single IP; carries NO AP or client data.")
add(WL, "WLC physical port: Console port — purpose?",
    "CLI access over serial (RJ-45 or mini-USB) for initial setup, recovery, and troubleshooting.")
add(WL, "WLC physical port: Distribution system (data) port — purpose?",
    "In-band ports connecting the WLC to the wired network, usually an 802.1Q trunk. Carry CAPWAP, client, and management traffic; can be bundled with LAG.")
add(WL, "WLC physical port: Redundancy port (RP) — purpose?",
    "Links two WLCs for High Availability (SSO), synchronizing state between active and standby controllers.")
add(WL, "WLC logical interface: Management — purpose?",
    "In-band management (GUI, SSH, Telnet, SNMP) and CAPWAP AP discovery/join.")
add(WL, "WLC logical interface: Virtual interface — purpose?",
    "Uses a non-routable address (e.g. 192.0.2.1) for client web authentication, DHCP relay, and mobility.")
add(WL, "WLC logical interface: Dynamic interface — purpose?",
    "Mapped to client VLANs like an SVI — each WLAN is tied to a dynamic interface.")
add(WL, "WLC logical interface: AP-manager — purpose?",
    "Layer 3 source for CAPWAP traffic to APs (older AireOS); often merged into the management interface.")
add(WL, "Wireless security: WEP vs WPA vs WPA2 vs WPA3?",
    "WEP: RC4, deprecated/cracked.\nWPA: TKIP, interim.\nWPA2: AES-CCMP, current standard.\nWPA3: AES-GCMP + SAE, strongest, forward secrecy.")
add(WL, "Wireless auth: PSK vs 802.1X?",
    "PSK (pre-shared key): shared password, home/small office.\n802.1X (Enterprise): RADIUS server + EAP for per-user authentication.")
add(WL, "EAP types: EAP-TLS, PEAP, EAP-FAST?",
    "EAP-TLS: certs on client AND server (most secure).\nPEAP: server cert + username/password.\nEAP-FAST: Cisco, uses PAC for fast reconnect.")
add(WL, "RF concepts: RSSI and SNR?",
    "RSSI = Received Signal Strength Indicator (signal power in dBm).\nSNR = Signal-to-Noise Ratio (higher is better, aim for >25 dB).")
add(WL, "Co-channel vs adjacent channel interference?",
    "Co-channel: neighboring APs on the same channel.\nAdjacent channel: overlapping channels (e.g. 1 and 3 on 2.4 GHz).")

# ───────────────────────── IOS Commands ─────────────────────────
IO = "CCNA::IOS Commands"
add(IO, "show running-config vs show startup-config?",
    "running-config = active config in RAM.\nstartup-config = saved config in NVRAM (loads on reboot).")
add(IO, "Command for a quick summary of all interfaces (IP + status)?",
    "<code>show ip interface brief</code>")
add(IO, "Command to view the full routing table?",
    "<code>show ip route</code>")
add(IO, "Command to view the MAC address table on a switch?",
    "<code>show mac address-table</code>")
add(IO, "Command to list VLANs and their ports?",
    "<code>show vlan brief</code>")
add(IO, "Command to view STP topology and port roles/states?",
    "<code>show spanning-tree</code>")
add(IO, "Command to view EtherChannel status?",
    "<code>show etherchannel summary</code>")
add(IO, "CDP vs LLDP neighbor discovery commands?",
    "<code>show cdp neighbors</code> (Cisco proprietary) vs <code>show lldp neighbors</code> (open standard). Add <code>detail</code> for IPs/versions.")
add(IO, "How do you disable all active debugs?",
    "<code>no debug all</code> (or <code>undebug all</code>).")
add(IO, "Command to save the running-config to startup-config?",
    "<code>write memory</code> (or <code>copy running-config startup-config</code>).")
add(IO, "Three steps to factory-reset a switch?",
    "<code>write erase</code> (clear startup-config), <code>delete flash:vlan.dat</code> (clear VLAN DB), <code>reload</code>.")
add(IO, "What does 'do' let you do in config mode?",
    "Run a show/EXEC command without leaving config mode, e.g. <code>do show ip int brief</code>.")
add(IO, "DHCP client release/renew commands on an interface?",
    "<code>release dhcp Gi0/1</code> and <code>renew dhcp Gi0/1</code>")

# ───────────────────────── Linux: Commands ─────────────────────────
LX = "Linux::Commands"
add(LX, "How do you add a permanent alias in bash?",
    "Add to <code>~/.bashrc</code>: <code>alias name='command'</code>, then <code>source ~/.bashrc</code>.")
add(LX, "Vim: enter insert mode before / after cursor / new line below?",
    "<code>i</code> = before cursor, <code>a</code> = after cursor, <code>o</code> = open new line below.")
add(LX, "Vim: go to first line / last line?",
    "<code>gg</code> = first line, <code>G</code> = last line.")
add(LX, "Vim: start vs end of line?",
    "<code>^</code> = start of line, <code>$</code> = end of line.")
add(LX, "Vim: delete line / yank line / paste?",
    "<code>dd</code> = delete (cut), <code>yy</code> = yank (copy), <code>p</code> = paste.")
add(LX, "Vim: undo and redo?",
    "<code>u</code> = undo, <code>Ctrl+r</code> = redo.")
add(LX, "Vim: save and quit / quit without saving?",
    "<code>:wq</code> = save and quit, <code>:q!</code> = quit without saving.")
add(LX, "Vim: replace all occurrences of 'old' with 'new'?",
    "<code>:%s/old/new/g</code>")
add(LX, "Vim: search forward vs backward?",
    "<code>/text</code> = forward, <code>?text</code> = backward.")
add(LX, "Tmux: list sessions and attach to last session?",
    "<code>tmux ls</code> to list, <code>tmux a</code> to attach to the last one (<code>tmux a -t name</code> for a named one).")
add(LX, "Tmux default prefix key?",
    "<code>Ctrl+b</code>")
add(LX, "Tmux: split pane vertically vs horizontally (after prefix)?",
    "<code>%</code> = vertical split, <code>\"</code> = horizontal split.")
add(LX, "Tmux: detach from a session (after prefix)?",
    "<code>d</code>")
add(LX, "Generate an SSH key (ed25519)?",
    "<code>ssh-keygen -t ed25519</code> — public key saved to <code>~/.ssh/id_ed25519.pub</code>.")
add(LX, "Copy your SSH public key to a remote server?",
    "<code>ssh-copy-id user@remoteserver</code> — adds it to <code>~/.ssh/authorized_keys</code> there.")
add(LX, "SCP: copy a local file to a remote host?",
    pre("scp /path/to/file user@host:/destination/path/"))
add(LX, "SCP: copy a whole directory?",
    "<code>scp -r /path/to/dir user@host:/destination/path/</code>")

# ───────────────────────── Linux: Web Server ─────────────────────────
WS = "Linux::Web Server"
add(WS, "Check nginx status, enable on boot, and test config?",
    pre("sudo systemctl status nginx\nsudo systemctl enable nginx\nsudo nginx -t"))
add(WS, "Verify nginx is listening on port 443?",
    "<code>sudo ss -tulpn | grep :443</code>")
add(WS, "Two SSL files nginx needs and what they are?",
    "<code>fullchain.pem</code> = domain + intermediate certs.\n<code>privkey.pem</code> = private key.")
add(WS, "Minimal nginx SSL server block?",
    pre("server {\n    listen 443 ssl;\n    server_name yourdomain.com;\n    ssl_certificate /path/to/fullchain.pem;\n    ssl_certificate_key /path/to/privkey.pem;\n}"))
add(WS, "Open HTTPS in firewalld vs UFW?",
    "firewalld: <code>sudo firewall-cmd --permanent --add-service=https</code> then <code>--reload</code>.\nUFW: <code>sudo ufw allow https</code>.")
add(WS, "Test SSL handshake and port reachability from CLI?",
    "<code>openssl s_client -connect yourdomain.com:443 -servername yourdomain.com</code> and <code>nc -zv yourdomain.com 443</code>.")
add(WS, "Restart nginx?",
    "<code>sudo systemctl restart nginx</code>")


# ───────────────────────── Build ─────────────────────────
decks = {}
for sub, front, back in CARDS:
    name = f"{TOP}::{sub}"
    deck = decks.get(name)
    if deck is None:
        deck = genanki.Deck(stable_id(name), name)
        decks[name] = deck
    note = genanki.Note(
        model=MODEL,
        fields=[fmt(front), fmt(back)],
        guid=genanki.guid_for("evansdocs", sub, front),
    )
    deck.add_note(note)

genanki.Package(list(decks.values())).write_to_file(OUTPUT)
print(f"Wrote {OUTPUT}")
print(f"Decks: {len(decks)}  Cards: {len(CARDS)}")
for name in sorted(decks):
    print(f"  {len(decks[name].notes):3d}  {name}")

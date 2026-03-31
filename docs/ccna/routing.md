# Routing

---

## Routing Basics

A router selects the best path for a packet using the routing table. Routes are learned via:

- **Directly connected** — networks on the router's own interfaces
- **Static routes** — manually configured
- **Dynamic routing protocols** — OSPF, EIGRP, BGP, etc.

### Administrative Distance (AD)

When multiple sources provide a route to the same destination, the route with the lowest AD is preferred.

| Route Source        | AD  |
|---------------------|-----|
| Directly connected  | 0   |
| Static route        | 1   |
| EIGRP summary       | 5   |
| eBGP                | 20  |
| EIGRP (internal)    | 90  |
| OSPF                | 110 |
| IS-IS               | 115 |
| RIP                 | 120 |
| EIGRP (external)    | 170 |
| iBGP                | 200 |

---

## Static Routes

Manually configured routes. Good for small or stub networks.

```
! Standard static route
ip route 10.0.0.0 255.255.255.0 192.168.1.1

! Static route via exit interface
ip route 10.0.0.0 255.255.255.0 GigabitEthernet0/1

! Default route (gateway of last resort)
ip route 0.0.0.0 0.0.0.0 192.168.1.1

! Floating static route (backup — higher AD than dynamic route)
ip route 10.0.0.0 255.255.255.0 192.168.2.1 210
```

---

## OSPF (Open Shortest Path First)

Link-state protocol that uses Dijkstra's SPF algorithm to find the shortest path. It is an open standard (not vendor-specific).

### Key Characteristics

- **AD:** 110
- **Metric:** Cost (based on bandwidth: 10^8 / bandwidth in bps)
- **Protocol:** IP protocol 89
- **Multicast addresses:** 224.0.0.5 (all OSPF routers), 224.0.0.6 (DR/BDR)
- **Hello timer:** 10 sec (broadcast), 30 sec (non-broadcast)
- **Dead timer:** 4× hello timer

### OSPF Areas

- **Area 0 (backbone)** — all areas must connect to area 0
- **Single-area OSPF** — all routers in area 0
- **Multi-area OSPF** — reduces LSA flooding, smaller routing tables
- **ABR (Area Border Router)** — connects two or more areas
- **ASBR (Autonomous System Boundary Router)** — connects OSPF to another routing domain

### OSPF Neighbor States

1. **Down** — no hellos received
2. **Init** — hello received, but own router ID not in neighbor's hello
3. **2-Way** — bidirectional communication established (DR/BDR election happens here)
4. **ExStart** — master/slave negotiation for DBD exchange
5. **Exchange** — DBD packets exchanged
6. **Loading** — LSR/LSU/LSAck exchange
7. **Full** — fully adjacent, databases synchronized

### OSPF Neighbor Requirements

For two routers to become OSPF neighbors, they must match:

- Area ID
- Hello and dead timers
- Subnet and mask
- Authentication (if configured)
- Stub area flag
- MTU (for adjacency to reach Full)

### DR/BDR Election

On multi-access networks (Ethernet), OSPF elects a **Designated Router (DR)** and **Backup DR (BDR)** to reduce flooding.

- Highest OSPF priority wins (default 1, range 0-255)
- Priority 0 = never become DR/BDR
- If priority ties, highest Router ID wins
- Election is **non-preemptive** — a new router with higher priority won't replace an existing DR

### OSPF Configuration

```
! Single-area OSPF
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0

! Set interface cost
interface GigabitEthernet0/1
 ip ospf cost 10

! Set reference bandwidth (use same value on all routers)
router ospf 1
 auto-cost reference-bandwidth 10000

! Verify
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
```

---

## EIGRP (Enhanced Interior Gateway Routing Protocol)

Cisco-developed advanced distance-vector (hybrid) protocol. Uses DUAL algorithm.

### Key Characteristics

- **AD:** 90 (internal), 170 (external)
- **Metric:** Composite of bandwidth, delay, reliability, load (default: bandwidth + delay)
- **Protocol:** IP protocol 88
- **Multicast address:** 224.0.0.10
- **Hello timer:** 5 sec (fast links), 60 sec (slow links)
- **Hold timer:** 3× hello timer
- Supports **unequal-cost load balancing** (via `variance` command)

### EIGRP Terminology

| Term                  | Definition                                           |
|-----------------------|------------------------------------------------------|
| Successor             | Best route to a destination (in routing table)       |
| Feasible Successor    | Backup route that meets the feasibility condition    |
| Feasible Distance (FD)| Metric from local router to destination              |
| Reported Distance (RD)| Metric reported by neighbor to destination           |

**Feasibility condition:** A route is a feasible successor if its RD < the FD of the current successor. This guarantees a loop-free path.

### EIGRP Configuration

```
router eigrp 100
 network 192.168.1.0 0.0.0.255
 network 10.0.0.0 0.0.0.3
 passive-interface GigabitEthernet0/0
 no auto-summary

! Verify
show ip eigrp neighbors
show ip eigrp topology
show ip route eigrp
```

---

## Route Summarization

Combine multiple specific routes into a single summary route to reduce routing table size.

```
! OSPF summary (on ABR)
router ospf 1
 area 1 range 10.0.0.0 255.255.252.0

! EIGRP summary
interface GigabitEthernet0/0
 ip summary-address eigrp 100 10.0.0.0 255.255.252.0
```

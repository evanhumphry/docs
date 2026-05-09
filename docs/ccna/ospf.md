# OSPF (Open Shortest Path First)

OSPF is a **link-state** routing protocol that uses Dijkstra's SPF algorithm. It is an **open standard** (RFC 2328), uses **IP protocol 89**, and has an **administrative distance of 110**.

---

## At a Glance

| Property               | Value                               |
|------------------------|-------------------------------------|
| Type                   | Link-state (IGP)                    |
| Algorithm              | Dijkstra (SPF)                      |
| AD                     | 110                                 |
| Metric                 | Cost (reference BW / interface BW)  |
| Transport              | IP protocol 89 (not TCP or UDP)     |
| Multicast (all routers)| 224.0.0.5                           |
| Multicast (DR/BDR)     | 224.0.0.6                           |
| Hello (broadcast)      | 10 seconds                          |
| Hello (non-broadcast)  | 30 seconds                          |
| Dead timer             | 4× hello                           |

---

## OSPF Areas

OSPF uses a hierarchical area structure to limit LSA flooding and reduce routing table size.

- **Area 0 (backbone)** — every other area must connect to area 0
- **Single-area OSPF** — all routers are in area 0
- **Multi-area OSPF** — breaks the domain into areas for scalability

### Router Roles

| Role | Description                                           |
|------|-------------------------------------------------------|
| Internal Router | All interfaces in a single area                |
| ABR (Area Border Router) | Connects two or more areas, one must be area 0 |
| ASBR (AS Boundary Router) | Connects OSPF to a different routing domain (e.g., EIGRP, BGP) |
| Backbone Router | Has at least one interface in area 0          |

---

## Neighbor Requirements

Two routers must match **all** of the following to become OSPF neighbors:

- Area ID
- Hello and dead timers
- Subnet and mask
- Authentication type and key (if configured)
- Stub area flag
- MTU (must match for adjacency to reach Full state)

---

## Neighbor States

| State    | What Happens                                              |
|----------|-----------------------------------------------------------|
| Down     | No hellos received                                        |
| Init     | Hello received, but own RID not seen in neighbor's hello  |
| 2-Way    | Bidirectional — RID seen in neighbor's hello. DR/BDR election occurs here |
| ExStart  | Master/slave negotiation for database exchange            |
| Exchange | DBD (Database Description) packets exchanged              |
| Loading  | LSR/LSU/LSAck — requesting and receiving missing LSAs     |
| Full     | Databases fully synchronized — adjacency complete         |

**Stuck in 2-Way?** That's normal for DROther-to-DROther relationships on multi-access segments. They don't form full adjacencies with each other.

---

## DR/BDR Election

On **multi-access networks** (Ethernet), OSPF elects a Designated Router (DR) and Backup DR (BDR) to reduce the number of adjacencies.

**Election rules:**

1. Highest OSPF **priority** wins (default 1, range 0–255)
2. Priority `0` = **never** become DR/BDR
3. If priority ties → highest **Router ID** wins
4. Election is **non-preemptive** — a new router with higher priority won't replace the current DR

On point-to-point links there is **no DR/BDR election**.

---

## OSPF Cost

```
Cost = Reference Bandwidth / Interface Bandwidth
```

Default reference bandwidth is **100 Mbps** (10^8). That means FastEthernet and GigabitEthernet both default to cost 1 — set a higher reference bandwidth so GigE gets a lower cost.

| Interface         | Default BW    | Default Cost (ref 100M) | Cost (ref 10G) |
|-------------------|---------------|-------------------------|-----------------|
| FastEthernet      | 100 Mbps      | 1                       | 100             |
| GigabitEthernet   | 1 Gbps        | 1                       | 10              |
| 10 GigabitEthernet| 10 Gbps       | 1                       | 1               |

---

## Configuration

### Single-Area OSPF

All interfaces advertised into area 0.

```
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0
```

- `router ospf 1` — the `1` is the **process ID** (locally significant, does not need to match between routers)
- `router-id` — manually set; otherwise OSPF uses the highest loopback IP, then highest physical IP
- `passive-interface` — stops sending hellos on that interface (use on LAN-facing ports that don't need neighbors)

### Using the `ip ospf` Interface Command (Preferred Method)

Instead of `network` statements, you can enable OSPF directly on the interface:

```
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip ospf 1 area 0

interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.252
 ip ospf 1 area 0
```

This is cleaner and avoids wildcard mask mistakes.

### Setting Reference Bandwidth

Do this on **every** router in the OSPF domain so cost calculations are consistent.

```
router ospf 1
 auto-cost reference-bandwidth 10000
```

Sets reference to 10 Gbps (10000 Mbps).

### Setting Interface Cost Manually

```
interface GigabitEthernet0/1
 ip ospf cost 50
```

### Adjusting Timers

Must match on both sides of a link.

```
interface GigabitEthernet0/1
 ip ospf hello-interval 5
 ip ospf dead-interval 20
```

### DR/BDR Priority

```
interface GigabitEthernet0/0
 ip ospf priority 200
```

Set to `0` to prevent a router from becoming DR/BDR.

---

## Multi-Area OSPF

### Example Topology

```
[Area 1] --- R1(ABR) --- [Area 0] --- R2(ABR) --- [Area 2]
```

**R1 (ABR between Area 0 and Area 1):**

```
router ospf 1
 router-id 1.1.1.1

interface GigabitEthernet0/0
 ip address 10.0.0.1 255.255.255.0
 ip ospf 1 area 1

interface GigabitEthernet0/1
 ip address 172.16.0.1 255.255.255.252
 ip ospf 1 area 0
```

**R2 (ABR between Area 0 and Area 2):**

```
router ospf 1
 router-id 2.2.2.2

interface GigabitEthernet0/0
 ip address 172.16.0.2 255.255.255.252
 ip ospf 1 area 0

interface GigabitEthernet0/1
 ip address 192.168.10.1 255.255.255.0
 ip ospf 1 area 2
```

### Route Summarization (ABR)

Summarize routes at area boundaries to reduce the routing table in other areas.

```
router ospf 1
 area 1 range 10.0.0.0 255.255.252.0
```

---

## Default Route Injection

Advertise a default route into OSPF from the router that has the internet/default gateway:

```
ip route 0.0.0.0 0.0.0.0 203.0.113.1

router ospf 1
 default-information originate
```

Use `default-information originate always` if you want the default route advertised even when the static default doesn't exist in the routing table.

---

## Authentication

### Plain-Text (interface level)

```
interface GigabitEthernet0/1
 ip ospf authentication
 ip ospf authentication-key MyPassword
```

### MD5 (interface level)

```
interface GigabitEthernet0/1
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 SecurePass
```

Both sides must use the same key ID and password.

---

## Troubleshooting Scenarios

### Neighbors Not Forming

Check these in order:

1. **Layer 1/2** — Is the link up? (`show ip interface brief`)
2. **IP addressing** — Are they on the same subnet?
3. **OSPF enabled?** — Is the interface in the right area? (`show ip ospf interface`)
4. **Timers** — Do hello/dead timers match? (`show ip ospf interface`)
5. **Area mismatch** — Both ends must be in the same area
6. **Authentication** — Type and key must match
7. **MTU mismatch** — Causes stuck in ExStart/Exchange (`debug ip ospf adj`)
8. **ACL blocking** — Is protocol 89 or multicast 224.0.0.5/6 being filtered?

### Stuck in ExStart/Exchange

Almost always an **MTU mismatch**. Fix the MTU on both sides:

```
interface GigabitEthernet0/1
 ip mtu 1500
```

### Stuck in 2-Way

Normal for **DROther ↔ DROther** on multi-access segments. Only DR and BDR form full adjacencies with all other routers.

---

## Verification Commands

```
! View neighbors and their state
show ip ospf neighbor

! View OSPF-enabled interfaces with area, cost, timers, DR/BDR
show ip ospf interface brief
show ip ospf interface GigabitEthernet0/0

! View OSPF routes in the routing table
show ip route ospf

! View the OSPF database (LSAs)
show ip ospf database

! View OSPF process details (RID, areas, SPF runs)
show ip ospf

! Debug adjacency issues
debug ip ospf adj
```

---

## Key Things to Remember

- All areas must connect to **area 0** (backbone)
- Process ID is **locally significant** — doesn't need to match between routers
- Router ID is chosen: manual config > highest loopback > highest physical IP
- `passive-interface` stops hellos but still advertises the network
- DR/BDR election is **non-preemptive** — changing priority won't take effect until the DR/BDR goes down
- Set `auto-cost reference-bandwidth` on **all routers** to the same value
- The `ip ospf` interface command is generally preferred over `network` statements
- OSPF only forms adjacencies over links in the **same area and subnet**

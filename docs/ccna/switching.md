# Switching

---

## VLANs (Virtual LANs)

VLANs logically segment a switch into separate broadcast domains. Traffic between VLANs requires a Layer 3 device (router or L3 switch).

### Key Concepts

- **Access port** — belongs to a single VLAN, connects to end devices
- **Trunk port** — carries traffic for multiple VLANs between switches, uses 802.1Q tagging
- **Native VLAN** — untagged VLAN on a trunk (default is VLAN 1). Should match on both sides of a trunk.
- **VLAN 1** — default VLAN, all ports are in VLAN 1 by default. Best practice: don't use it for user traffic.

### VLAN Configuration

```
! Create VLANs
vlan 10
 name SALES
vlan 20
 name ENGINEERING

! Assign access port to VLAN
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10

! Configure trunk port
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 switchport trunk native vlan 99
```

### Inter-VLAN Routing (Router-on-a-Stick)

Uses subinterfaces on a router connected to a trunk port:

```
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0

interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
```

### SVI (Switched Virtual Interface)

On a Layer 3 switch, create SVIs instead of using a router:

```
ip routing

interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown

interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
```

---

## Spanning Tree Protocol (STP)

STP prevents Layer 2 loops by blocking redundant paths. Only one active path exists between any two switches.

### How STP Works

1. **Root bridge election** — switch with the lowest Bridge ID (priority + MAC) becomes root
2. **Root ports** — each non-root switch selects its best port toward the root bridge
3. **Designated ports** — one designated port per segment (lowest cost to root)
4. **Blocked ports** — all other redundant ports are blocked

### STP Port States

| State       | Duration    | Sends/Receives | Learns MACs |
|-------------|-------------|----------------|-------------|
| Blocking    | 20 sec      | No / Yes (BPDUs only) | No    |
| Listening   | 15 sec      | Yes / Yes      | No          |
| Learning    | 15 sec      | Yes / Yes      | Yes         |
| Forwarding  | —           | Yes / Yes      | Yes         |
| Disabled    | —           | No / No        | No          |

**Convergence time:** ~50 seconds (Blocking → Forwarding)

### STP Path Cost

| Speed    | Cost (802.1D) |
|----------|---------------|
| 10 Mbps  | 100           |
| 100 Mbps | 19            |
| 1 Gbps   | 4             |
| 10 Gbps  | 2             |

### Rapid Spanning Tree (RSTP / 802.1w)

- Converges in seconds instead of ~50 seconds
- Port roles: **Root**, **Designated**, **Alternate** (backup to root port), **Backup**
- Port states: **Discarding**, **Learning**, **Forwarding**

### STP Configuration

```
! Set root bridge (lower priority wins)
spanning-tree vlan 10 root primary
spanning-tree vlan 20 root secondary

! Or set priority manually (must be multiple of 4096)
spanning-tree vlan 10 priority 4096

! PortFast (skip STP on access ports — use only on end-device ports)
interface GigabitEthernet0/1
 spanning-tree portfast

! BPDU Guard (shuts port if it receives a BPDU)
interface GigabitEthernet0/1
 spanning-tree bpduguard enable
```

---

## EtherChannel

EtherChannel bundles multiple physical links into one logical link, increasing bandwidth and providing redundancy. STP sees the bundle as a single link.

### Negotiation Protocols

| Protocol | Type           | Modes              |
|----------|----------------|---------------------|
| LACP     | Open standard (802.3ad) | Active / Passive |
| PAgP     | Cisco proprietary       | Desirable / Auto |

- **Active/Desirable** — initiates negotiation
- **Passive/Auto** — responds but doesn't initiate
- At least one side must be Active (LACP) or Desirable (PAgP)
- You can also use `mode on` (force, no negotiation) — both sides must be `on`

### EtherChannel Configuration

```
! LACP EtherChannel
interface range GigabitEthernet0/1-2
 channel-group 1 mode active
 channel-protocol lacp

! Configure the logical interface
interface port-channel 1
 switchport mode trunk
 switchport trunk allowed vlan 10,20

! Verify
show etherchannel summary
show etherchannel port-channel
```

### EtherChannel Requirements

All member ports must match:

- Speed and duplex
- VLAN configuration (access VLAN or trunk allowed VLANs)
- Switchport mode (access or trunk)
- STP settings

# Cisco IOS Commands

Handy Cisco IOS commands for troubleshooting and configuration.

---

## Show Commands (Read-Only)

### System Info

```
show version
```
Displays IOS version, uptime, hardware model, and memory.

```
show running-config
```
Shows the active configuration in RAM.

```
show startup-config
```
Shows the saved configuration in NVRAM (what loads on reboot).

```
show processes cpu
```
Shows CPU utilization — useful for identifying high-load issues.

```
show log
```
Displays system log messages.

---

### Interface Status

```
show ip interface brief
```
Quick summary of all interfaces — IP address, status (up/down), and protocol state.

```
show interfaces
```
Detailed stats for all interfaces: errors, packet counts, duplex, speed.

```
show interfaces GigabitEthernet0/1
```
Detailed stats for a specific interface.

```
show interfaces status
```
(Switches) Shows port status, VLAN assignment, duplex, and speed.

---

### Routing & Layer 3

```
show ip route
```
Displays the full routing table.

```
show ip route 10.0.0.1
```
Shows the best route to a specific destination.

```
show arp
```
Displays the ARP cache (IP-to-MAC mappings).

```
show ip protocols
```
Shows active routing protocols and their parameters.

---

### Switching & Layer 2

```
show mac address-table
```
Displays the MAC address table on a switch.

```
show vlan brief
```
Lists all VLANs and their assigned ports.

```
show spanning-tree
```
Displays STP topology and port roles/states.

```
show spanning-tree vlan 10
```
STP info for a specific VLAN.

```
show etherchannel summary
```
Shows EtherChannel (port-channel) status.

---

### Neighbors & Topology

```
show cdp neighbors
```
Lists directly connected Cisco devices via CDP.

```
show cdp neighbors detail
```
Extended CDP neighbor info — IP addresses, IOS version, etc.

```
show lldp neighbors
```
Same as CDP but using the open LLDP standard.

---

## Connectivity Tests

```
ping 192.168.1.1
```
Basic ICMP ping to test Layer 3 reachability.

```
ping 192.168.1.1 source GigabitEthernet0/1
```
Ping from a specific source interface.

```
traceroute 8.8.8.8
```
Traces the path packets take to a destination.

---

## Debug Commands

> **Warning:** Debug commands can be CPU-intensive on production equipment. Use with care and always disable when done.

```
debug ip icmp
```
Debugs ICMP packets (ping traffic).

```
debug ip routing
```
Shows routing table changes in real time.

```
no debug all
```
Disables all active debug outputs. Run this when done debugging.

```
undebug all
```
Alias for `no debug all`.

---

## Static Routes

```
! Route to a remote network via next-hop IP
ip route 10.10.10.0 255.255.255.0 192.168.1.1

! Route via exit interface
ip route 10.10.10.0 255.255.255.0 GigabitEthernet0/1

! Default route (gateway of last resort)
ip route 0.0.0.0 0.0.0.0 192.168.1.1

! Floating static (backup route with higher AD)
ip route 10.10.10.0 255.255.255.0 192.168.2.1 210
```

### Verify

```
show ip route static
show ip route 10.10.10.0
```

---

## OSPF Configuration

### Single-Area OSPF

```
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0
```

### Enable OSPF Directly on an Interface

```
interface GigabitEthernet0/0
 ip ospf 1 area 0
```

### Set Reference Bandwidth

```
router ospf 1
 auto-cost reference-bandwidth 10000
```

### Advertise a Default Route into OSPF

```
ip route 0.0.0.0 0.0.0.0 203.0.113.1
router ospf 1
 default-information originate
```

### Verify

```
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
show ip ospf database
```

---

## ACLs

### Standard ACL (Numbered)

```
access-list 10 deny host 192.168.1.100
access-list 10 permit any
```

### Standard ACL (Named)

```
ip access-list standard BLOCK_GUEST
 deny 10.10.10.0 0.0.0.255
 permit any
```

### Extended ACL — Allow Only Web Traffic

```
ip access-list extended ALLOW_WEB
 permit tcp 192.168.1.0 0.0.0.255 any eq 80
 permit tcp 192.168.1.0 0.0.0.255 any eq 443
 deny ip any any
```

### Extended ACL — Block a Host from a Server

```
ip access-list extended BLOCK_TO_SERVER
 deny ip host 192.168.1.50 host 10.0.0.100
 permit ip any any
```

### Extended ACL — Allow SSH from Management Subnet Only

```
ip access-list extended SSH_MGMT
 permit tcp 172.16.0.0 0.0.0.255 any eq 22
 deny tcp any any eq 22
 permit ip any any
```

### Editing ACLs by Sequence Number

```
! View current ACL with sequence numbers
show access-lists

! Enter the ACL and insert/remove lines
ip access-list extended ALLOW_WEB
 15 permit tcp any any eq 8080
 no 30
```

### Applying ACLs to an Interface

```
! Apply inbound on an interface
interface GigabitEthernet0/0
 ip access-group ALLOW_WEB in

! Apply outbound on an interface
interface GigabitEthernet0/1
 ip access-group BLOCK_GUEST out
```

### Applying an ACL to VTY Lines (SSH/Telnet Access)

```
ip access-list standard VTY_ACCESS
 permit 192.168.1.0 0.0.0.255

line vty 0 15
 access-class VTY_ACCESS in
```

### Removing an ACL from an Interface

```
interface GigabitEthernet0/0
 no ip access-group ALLOW_WEB in
```

### Verify

```
show access-lists
show ip access-lists
show ip interface GigabitEthernet0/0
```

---

## Switch — Upgrading IOS

```
show flash:
```
List files stored in flash memory.

```
copy tftp: flash:
```
Copy a new IOS image from a TFTP server to flash.

```
boot system flash:new-ios-image.bin
```
Set the new image as the boot file (add to running-config, then save).

```
write memory
```
Save the running-config to startup-config.

---

## Switch — Factory Reset

```
write erase
```
Erases the startup-config (NVRAM).

```
delete flash:vlan.dat
```
Deletes the VLAN database.

```
reload
```
Reboots the switch. It will come up with factory defaults.

---

## Useful Shortcuts

| Command          | Description                          |
|------------------|--------------------------------------|
| `?`              | Context-sensitive help               |
| `Tab`            | Auto-complete a command              |
| `Ctrl+C`         | Abort a command or running process   |
| `Ctrl+Z`         | Exit to privileged EXEC mode         |
| `do show ...`    | Run a show command from config mode  |
| `no <command>`   | Negate / remove a configuration line |

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

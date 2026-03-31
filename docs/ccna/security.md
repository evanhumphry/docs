# Security

---

## Access Control Lists (ACLs)

ACLs filter traffic based on source/destination IP, protocol, and port. They are processed top-down — first match wins. An implicit `deny any` exists at the end of every ACL.

### ACL Types

| Type              | Number Range | Matches On                           |
|-------------------|--------------|--------------------------------------|
| Standard          | 1-99, 1300-1999 | Source IP only                    |
| Extended          | 100-199, 2000-2699 | Source/dest IP, protocol, port |
| Named             | —            | Either standard or extended          |

### ACL Placement

- **Standard ACLs** — place close to the **destination** (they only match source IP, so placing them near the source could block unintended traffic)
- **Extended ACLs** — place close to the **source** (they're specific enough to filter precisely)

### Standard ACL Configuration

```
! Named standard ACL
ip access-list standard BLOCK_HOST
 deny host 192.168.1.100
 permit any

! Apply to interface
interface GigabitEthernet0/0
 ip access-group BLOCK_HOST in
```

### Extended ACL Configuration

```
! Named extended ACL
ip access-list extended WEB_ONLY
 permit tcp 192.168.1.0 0.0.0.255 any eq 80
 permit tcp 192.168.1.0 0.0.0.255 any eq 443
 deny ip any any

! Apply to interface
interface GigabitEthernet0/0
 ip access-group WEB_ONLY in
```

### ACL Verification

```
show access-lists
show ip interface GigabitEthernet0/0
```

---

## Port Security

Limits the number of MAC addresses allowed on a switchport and defines the action when violated.

### Violation Modes

| Mode       | Action                          | Drops Traffic | Sends Log | Shuts Port |
|------------|---------------------------------|---------------|-----------|------------|
| Protect    | Drops offending frames silently | Yes           | No        | No         |
| Restrict   | Drops frames, increments counter | Yes          | Yes       | No         |
| Shutdown   | Err-disables the port (default) | Yes           | Yes       | Yes        |

### Port Security Configuration

```
interface GigabitEthernet0/1
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security mac-address sticky

! Verify
show port-security interface GigabitEthernet0/1
show port-security address
```

### Recovering from Err-Disabled

```
! Re-enable manually
interface GigabitEthernet0/1
 shutdown
 no shutdown

! Auto-recovery
errdisable recovery cause psecure-violation
errdisable recovery interval 300
```

---

## DHCP Snooping

Prevents rogue DHCP servers by filtering DHCP messages.

- **Trusted ports** — connect to legitimate DHCP servers or uplinks
- **Untrusted ports** — all other ports (default); only DHCP requests allowed

```
ip dhcp snooping
ip dhcp snooping vlan 10

interface GigabitEthernet0/24
 ip dhcp snooping trust

! Verify
show ip dhcp snooping
show ip dhcp snooping binding
```

---

## Dynamic ARP Inspection (DAI)

Validates ARP packets against the DHCP snooping binding table to prevent ARP spoofing.

```
ip arp inspection vlan 10

interface GigabitEthernet0/24
 ip arp inspection trust
```

---

## AAA Overview

**Authentication, Authorization, Accounting** — centralized security framework.

| Component      | Purpose                                    |
|----------------|--------------------------------------------|
| Authentication | Verifies identity (who are you?)           |
| Authorization  | Determines permissions (what can you do?)  |
| Accounting     | Logs activity (what did you do?)           |

Common AAA servers: **RADIUS** (UDP 1812/1813) and **TACACS+** (TCP 49, Cisco proprietary, encrypts entire payload).

---

## Device Hardening Basics

```
! Set hostname
hostname SW1

! Secure console
line console 0
 password cisco
 login
 exec-timeout 5 0

! Secure VTY (SSH)
line vty 0 15
 transport input ssh
 login local

! Create local user
username admin privilege 15 secret StrongPass123

! Disable unused ports
interface range GigabitEthernet0/10-24
 shutdown

! Enable SSH
ip domain-name example.com
crypto key generate rsa modulus 2048
ip ssh version 2

! Set enable secret
enable secret StrongEnablePass

! Disable HTTP server
no ip http server
no ip http secure-server

! Banner
banner motd # Authorized access only. #
```

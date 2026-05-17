# Network Services

---

## DHCP (Dynamic Host Configuration Protocol)

DHCP automatically assigns IP addresses and network configuration to clients.

### DORA Process

| Step      | Message   | Direction          | Description                       |
|-----------|-----------|--------------------|-----------------------------------|
| 1         | Discover  | Client → Broadcast | Client looks for a DHCP server    |
| 2         | Offer     | Server → Client    | Server offers an IP address       |
| 3         | Request   | Client → Broadcast | Client requests the offered IP    |
| 4         | Ack       | Server → Client    | Server confirms the lease         |

### DHCP Server Configuration (IOS)

```
ip dhcp excluded-address 192.168.1.1 192.168.1.10

ip dhcp pool LAN_POOL
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8 8.8.4.4
 lease 7

! Verify
show ip dhcp binding
show ip dhcp pool
```

### DHCP Relay

When the DHCP server is on a different subnet, the router must relay requests:

```
interface GigabitEthernet0/0
 ip helper-address 10.0.0.100
```

---

## DNS (Domain Name System)

DNS resolves hostnames to IP addresses.

### Common Record Types

| Record | Purpose                                      |
|--------|----------------------------------------------|
| A      | Maps hostname to IPv4 address                |
| AAAA   | Maps hostname to IPv6 address                |
| CNAME  | Alias for another hostname                   |
| MX     | Mail server for a domain                     |
| NS     | Authoritative name server for a domain       |
| PTR    | Reverse lookup (IP to hostname)              |
| SOA    | Start of Authority — zone metadata           |
| TXT    | Arbitrary text (used for SPF, DKIM, etc.)    |

### DNS on IOS

```
! Enable DNS lookup
ip domain-lookup
ip name-server 8.8.8.8

! Static hostname mapping
ip host SERVER1 192.168.1.100

! Verify
show hosts
```

---

## NAT / PAT (Network Address Translation)

NAT translates private IPs to public IPs for internet access.

### NAT Terminology

| Term           | Meaning                              |
|----------------|--------------------------------------|
| Inside Local   | Private IP on the internal network   |
| Inside Global  | Public IP representing the internal host |
| Outside Local  | IP of external host as seen internally |
| Outside Global | Actual public IP of the external host |

### Interface Roles

Every NAT configuration requires marking interfaces as **inside** or **outside**. This tells the router which direction to translate.

```
interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside
```

---

### Static NAT

One-to-one mapping — a single private IP always maps to a single public IP. Used for servers that need to be reachable from the outside.

```
ip nat inside source static 192.168.1.100 203.0.113.10

interface GigabitEthernet0/0
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
```

---

### Dynamic NAT

A pool of public IPs is assigned to internal hosts on demand. An ACL defines **which internal hosts** are allowed to be translated.

```
! Step 1: ACL defines which source IPs can be translated
access-list 1 permit 192.168.1.0 0.0.0.255

! Step 2: Define the public IP pool
ip nat pool PUBLIC_POOL 203.0.113.10 203.0.113.20 netmask 255.255.255.0

! Step 3: Bind the ACL to the pool
ip nat inside source list 1 pool PUBLIC_POOL

! Step 4: Mark interfaces
interface GigabitEthernet0/0
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
```

If the pool runs out of addresses, new connections are dropped until an existing translation times out.

---

### PAT (NAT Overload)

Many internal hosts share **one public IP** — the router tracks connections by port number. This is the most common type of NAT.

#### PAT Using the Outside Interface IP

```
access-list 1 permit 192.168.1.0 0.0.0.255

ip nat inside source list 1 interface GigabitEthernet0/1 overload

interface GigabitEthernet0/0
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
```

#### PAT Using a Pool (Overloaded)

```
access-list 1 permit 192.168.1.0 0.0.0.255

ip nat pool PAT_POOL 203.0.113.10 203.0.113.10 netmask 255.255.255.0
ip nat inside source list 1 pool PAT_POOL overload

interface GigabitEthernet0/0
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
```

---

### Using Named ACLs with NAT

You can use named ACLs instead of numbered ones. Reference them by name in the NAT statement.

```
ip access-list standard NAT_HOSTS
 permit 192.168.10.0 0.0.0.255
 permit 192.168.20.0 0.0.0.255

ip nat inside source list NAT_HOSTS interface GigabitEthernet0/1 overload
```

---

### Using Extended ACLs with NAT

Extended ACLs give you more control — you can NAT based on **source and destination**, not just source. This is useful when you only want to translate traffic going to specific destinations.

#### Example: Only NAT Traffic Going to the Internet

Internal hosts should be translated when going to the internet, but **not** when talking to other internal subnets:

```
ip access-list extended NAT_INTERNET_ONLY
 deny ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255
 permit ip 192.168.1.0 0.0.0.255 any

ip nat inside source list NAT_INTERNET_ONLY interface GigabitEthernet0/1 overload
```

#### Example: Only NAT Traffic to a Specific Server

```
ip access-list extended NAT_TO_SERVER
 permit ip 192.168.1.0 0.0.0.255 host 203.0.113.50

ip nat inside source list NAT_TO_SERVER interface GigabitEthernet0/1 overload
```

---

### NAT with Route Maps (Advanced)

Route maps let you combine ACLs with interface matching for even more granular NAT control — for example, only translate traffic leaving a specific interface.

```
ip access-list extended INTERNAL_TRAFFIC
 permit ip 192.168.1.0 0.0.0.255 any

route-map NAT_MAP permit 10
 match ip address INTERNAL_TRAFFIC
 match interface GigabitEthernet0/1

ip nat inside source route-map NAT_MAP interface GigabitEthernet0/1 overload
```

---

### Clearing and Verifying NAT

```
! View active translations
show ip nat translations

! View NAT stats (hits, misses, active translations)
show ip nat statistics

! Clear the translation table (useful when changing NAT config)
clear ip nat translation *
```

**Note:** If you change a NAT configuration, clear the translation table for the new rules to take effect on existing sessions.

---

### NAT Quick Reference

| Type        | ACL Purpose                     | NAT Command Key Part              |
|-------------|---------------------------------|-----------------------------------|
| Static      | Not needed                      | `source static <private> <public>` |
| Dynamic     | Defines which hosts get translated | `source list <acl> pool <name>`  |
| PAT (interface) | Defines which hosts get translated | `source list <acl> interface <if> overload` |
| PAT (pool)  | Defines which hosts get translated | `source list <acl> pool <name> overload` |

---

## NTP (Network Time Protocol)

Synchronizes clocks across network devices. Accurate time is critical for logging and troubleshooting.

```
! Set NTP server
ntp server 216.239.35.0

! Set timezone
clock timezone EST -5

! Verify
show ntp status
show ntp associations
show clock
```

---

## Syslog

Centralized logging for network events.

### Severity Levels

| Level | Name          | Description                 |
|-------|---------------|-----------------------------|
| 0     | Emergency     | System is unusable           |
| 1     | Alert         | Immediate action needed      |
| 2     | Critical      | Critical conditions          |
| 3     | Error         | Error conditions             |
| 4     | Warning       | Warning conditions           |
| 5     | Notification  | Normal but significant       |
| 6     | Informational | Informational messages       |
| 7     | Debugging     | Debug-level messages         |

**Mnemonic:** **E**very **A**wesome **C**isco **E**ngineer **W**ill **N**eed **I**ce cream **D**aily

```
! Send logs to syslog server
logging host 10.0.0.200
logging trap informational
logging source-interface Loopback0
```

---

## SNMP (Simple Network Management Protocol)

Used for monitoring and managing network devices.

| Version | Authentication     | Encryption |
|---------|--------------------|------------|
| v1      | Community string   | None       |
| v2c     | Community string   | None       |
| v3      | Username/password  | Yes (optional) |

```
! SNMPv2c
snmp-server community PUBLIC ro
snmp-server community PRIVATE rw
snmp-server host 10.0.0.200 version 2c PUBLIC
```

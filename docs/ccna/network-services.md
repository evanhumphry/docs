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

### NAT Types

| Type        | Description                                           |
|-------------|-------------------------------------------------------|
| Static NAT  | 1:1 mapping — one private IP to one public IP         |
| Dynamic NAT | Pool of public IPs assigned on demand                 |
| PAT (NAT Overload) | Many private IPs share one public IP using port numbers |

### NAT Terminology

| Term           | Meaning                              |
|----------------|--------------------------------------|
| Inside Local   | Private IP on the internal network   |
| Inside Global  | Public IP representing the internal host |
| Outside Local  | IP of external host as seen internally |
| Outside Global | Actual public IP of the external host |

### Static NAT Configuration

```
ip nat inside source static 192.168.1.100 203.0.113.10

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside
```

### PAT (Overload) Configuration

```
access-list 1 permit 192.168.1.0 0.0.0.255

ip nat inside source list 1 interface GigabitEthernet0/1 overload

interface GigabitEthernet0/0
 ip nat inside

interface GigabitEthernet0/1
 ip nat outside

! Verify
show ip nat translations
show ip nat statistics
```

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

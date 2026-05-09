# Access Control Lists (ACLs)

ACLs filter traffic on router interfaces. They are processed **top-down** — the first matching rule is applied and processing stops. Every ACL has an implicit `deny any` at the end.

---

## ACL Types

| Type     | Number Range       | Matches On                         |
|----------|--------------------|-------------------------------------|
| Standard | 1–99, 1300–1999    | Source IP only                      |
| Extended | 100–199, 2000–2699 | Source/dest IP, protocol, port      |
| Named    | —                  | Either standard or extended by name |

---

## Placement Rules

- **Standard ACLs** → place close to the **destination** (they only match source, so placing near the source blocks too much)
- **Extended ACLs** → place close to the **source** (specific enough to filter precisely early)

---

## Wildcard Masks

Wildcard masks are the **inverse** of subnet masks. A `0` bit means "must match," a `1` bit means "don't care."

| Goal                        | Wildcard Mask     | Meaning                       |
|-----------------------------|-------------------|-------------------------------|
| Match a single host         | `0.0.0.0`         | All bits must match           |
| Match a /24 subnet          | `0.0.0.255`       | Last octet is any             |
| Match a /26 subnet          | `0.0.0.63`        | Last 6 bits are any           |
| Match a /16 subnet          | `0.0.255.255`     | Last two octets are any       |
| Match any address            | `255.255.255.255` | Nothing needs to match        |

**Quick formula:** `255.255.255.255 − subnet mask = wildcard mask`

---

## Standard ACLs

Match on **source IP only**. Best for simple permit/deny decisions.

### Numbered Standard ACL

```
! Block a single host from all traffic
access-list 10 deny host 192.168.1.100
access-list 10 permit any

! Apply inbound on the interface closest to the destination
interface GigabitEthernet0/0
 ip access-group 10 in
```

### Named Standard ACL

```
ip access-list standard BLOCK_GUEST
 deny 10.10.10.0 0.0.0.255
 permit any

interface GigabitEthernet0/1
 ip access-group BLOCK_GUEST in
```

---

## Extended ACLs

Match on **source IP, destination IP, protocol, and port**. Much more granular.

### Syntax

```
access-list <number> <permit|deny> <protocol> <source> <wildcard> <dest> <wildcard> [eq <port>]
```

### Example: Allow Only Web Traffic

```
ip access-list extended ALLOW_WEB
 permit tcp 192.168.1.0 0.0.0.255 any eq 80
 permit tcp 192.168.1.0 0.0.0.255 any eq 443
 deny ip any any

interface GigabitEthernet0/0
 ip access-group ALLOW_WEB in
```

### Example: Block a Host from Reaching a Server

```
ip access-list extended BLOCK_TO_SERVER
 deny ip host 192.168.1.50 host 10.0.0.100
 permit ip any any

interface GigabitEthernet0/0
 ip access-group BLOCK_TO_SERVER in
```

### Example: Allow Ping But Block Telnet

```
ip access-list extended PING_NO_TELNET
 deny tcp any any eq 23
 permit icmp any any
 permit ip any any

interface GigabitEthernet0/0
 ip access-group PING_NO_TELNET in
```

### Example: Restrict SSH Access to Management Subnet

```
ip access-list extended SSH_MGMT_ONLY
 permit tcp 172.16.0.0 0.0.0.255 any eq 22
 deny tcp any any eq 22
 permit ip any any

interface GigabitEthernet0/0
 ip access-group SSH_MGMT_ONLY in
```

---

## ACLs on VTY Lines

Control who can SSH/Telnet into the router itself (not passing through it).

```
ip access-list standard VTY_ACCESS
 permit 192.168.1.0 0.0.0.255

line vty 0 15
 access-class VTY_ACCESS in
 transport input ssh
```

**Note:** Use `access-class` (not `ip access-group`) on VTY lines.

---

## ACL Direction: `in` vs `out`

| Direction | Meaning                                                  |
|-----------|----------------------------------------------------------|
| `in`      | Filter packets **arriving** on the interface              |
| `out`     | Filter packets **leaving** the interface                  |

Think of it from the **router's perspective** on that specific interface.

---

## Editing ACLs

Named ACLs support inserting and removing individual lines by sequence number:

```
ip access-list extended ALLOW_WEB
 15 permit tcp any any eq 8080
 no 30
```

To view sequence numbers:

```
show access-lists
```

---

## Common Scenarios

### Scenario 1: Two departments, block inter-department traffic

LAN A (`192.168.10.0/24`) should not reach LAN B (`192.168.20.0/24`), but both should reach the internet.

```
ip access-list extended BLOCK_A_TO_B
 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
 permit ip any any

! Apply inbound on the interface facing LAN A
interface GigabitEthernet0/0
 ip access-group BLOCK_A_TO_B in
```

### Scenario 2: Allow DNS and HTTPS only from a VLAN

VLAN 30 (`10.30.0.0/24`) should only be able to use DNS and HTTPS.

```
ip access-list extended VLAN30_RESTRICTED
 permit udp 10.30.0.0 0.0.0.255 any eq 53
 permit tcp 10.30.0.0 0.0.0.255 any eq 53
 permit tcp 10.30.0.0 0.0.0.255 any eq 443
 deny ip any any

interface GigabitEthernet0/2
 ip access-group VLAN30_RESTRICTED in
```

---

## Verification Commands

```
show access-lists
show ip access-lists
show ip interface GigabitEthernet0/0
show running-config | section access-list
```

---

## Key Things to Remember

- Implicit `deny any` at the end — always add a `permit any` if you want to allow unmatched traffic
- **One ACL per interface, per direction, per protocol**
- Standard ACLs near the destination, extended near the source
- `host 10.0.0.1` is shorthand for `10.0.0.1 0.0.0.0`
- `any` is shorthand for `0.0.0.0 255.255.255.255`
- ACL changes take effect immediately — no need to reapply
- Use `remark` lines to document what each rule does

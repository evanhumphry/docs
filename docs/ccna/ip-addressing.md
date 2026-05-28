# IP Addressing & Subnetting

---

## IPv4 Address Classes

| Class | Range                       | Default Mask           | Purpose           |
|-------|-----------------------------|------------------------|-------------------|
| A     | 1.0.0.0 – 126.255.255.255   | /8 (255.0.0.0)        | Large networks    |
| B     | 128.0.0.0 – 191.255.255.255 | /16 (255.255.0.0)     | Medium networks   |
| C     | 192.0.0.0 – 223.255.255.255 | /24 (255.255.255.0)   | Small networks    |
| D     | 224.0.0.0 – 239.255.255.255 | N/A                    | Multicast         |
| E     | 240.0.0.0 – 255.255.255.255 | N/A                    | Experimental      |

**Note:** 127.0.0.0/8 is reserved for loopback (localhost).

---

## Private IP Ranges (RFC 1918)

| Range                          | CIDR Notation    | Class |
|--------------------------------|------------------|-------|
| 10.0.0.0 – 10.255.255.255     | 10.0.0.0/8       | A     |
| 172.16.0.0 – 172.31.255.255   | 172.16.0.0/12    | B     |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16   | C     |

---

## Quick Binary Reference

### Powers of 2

| 2^7 | 2^6 | 2^5 | 2^4 | 2^3 | 2^2 | 2^1 | 2^0 |
|-----|-----|-----|-----|-----|-----|-----|-----|
| 128 | 64  | 32  | 16  | 8   | 4   | 2   | 1   |

To convert **binary → decimal**, add up the bit positions that are `1`:

- `11010000` = 128 + 64 + 16 = **208**
- `10110100` = 128 + 32 + 16 + 4 = **180**

To convert **decimal → binary**, subtract the largest power of 2 that fits and mark each bit:

- **200** → 128 fits (1), remainder 72 → 64 fits (1), remainder 8 → 8 fits (1) → `11001000`
- **150** → 128 fits (1), remainder 22 → 16 fits (1), remainder 6 → 4 fits (1), remainder 2 → 2 fits (1) → `10010110`

### Subnetting Cheat Sheet

| **Group Size** | 128  | 64   | 32   | 16   | 8    | 4    | 2    | 1    |
|----------------|------|------|------|------|------|------|------|------|
| **Subnet**     | 128  | 192  | 224  | 240  | 248  | 252  | 254  | 255  |
| **CIDR**       | /25  | /26  | /27  | /28  | /29  | /30  | /31  | /32  |
| **CIDR (3rd octet)** | /17 | /18 | /19 | /20 | /21 | /22 | /23 | /24 |

**How to use it:** Each column ties together — the group size is the block size (how many IPs per subnet), the subnet row is the mask octet value, and the CIDR rows give you the prefix length for the 4th and 3rd octets respectively.

---

## Subnetting

### Key Formulas

- **Usable hosts per subnet** = 2^(host bits) − 2
- **Number of subnets** = 2^(borrowed bits)
- **Block size** = 256 − subnet mask octet value

### Subnet Mask Reference

| CIDR | Subnet Mask       | Block Size | Usable Hosts |
|------|-------------------|------------|--------------|
| /24  | 255.255.255.0     | 256        | 254          |
| /25  | 255.255.255.128   | 128        | 126          |
| /26  | 255.255.255.192   | 64         | 62           |
| /27  | 255.255.255.224   | 32         | 30           |
| /28  | 255.255.255.240   | 16         | 14           |
| /29  | 255.255.255.248   | 8          | 6            |
| /30  | 255.255.255.252   | 4          | 2            |
| /31  | 255.255.255.254   | 2          | 0 (point-to-point) |
| /32  | 255.255.255.255   | 1          | 0 (host route)     |

### Subnetting Example

Given: `192.168.1.0/26`

- Subnet mask: `255.255.255.192`
- Block size: 256 − 192 = **64**
- Subnets: `192.168.1.0`, `192.168.1.64`, `192.168.1.128`, `192.168.1.192`
- Hosts per subnet: 2^6 − 2 = **62**
- First subnet usable range: `192.168.1.1` – `192.168.1.62`, broadcast `192.168.1.63`

---

## Wildcard Masks

Used in ACLs and OSPF to define address ranges. Calculated as `255.255.255.255 − subnet mask`.

| Subnet Mask       | Wildcard Mask     |
|-------------------|-------------------|
| 255.255.255.0     | 0.0.0.255         |
| 255.255.255.128   | 0.0.0.127         |
| 255.255.255.192   | 0.0.0.63          |
| 255.255.255.224   | 0.0.0.31          |
| 255.255.255.240   | 0.0.0.15          |
| 255.255.255.252   | 0.0.0.3           |

---

## IPv6

### Address Format

- 128-bit address written in eight groups of four hex digits: `2001:0db8:0000:0000:0000:0000:0000:0001`
- **Shortening rules:** drop leading zeros, replace consecutive all-zero groups with `::` (once per address)
- Shortened: `2001:db8::1`

### IPv6 Address Types

| Type           | Prefix        | Description                        |
|----------------|---------------|------------------------------------|
| Global Unicast | 2000::/3      | Routable on the internet           |
| Link-Local     | FE80::/10     | Local link only, auto-configured   |
| Unique Local   | FC00::/7      | Private addresses (like RFC 1918)  |
| Multicast      | FF00::/8      | One-to-many                        |
| Loopback       | ::1/128       | Localhost                          |

### IPv6 Configuration

```
ipv6 unicast-routing

interface GigabitEthernet0/0
 ipv6 address 2001:db8:1::1/64
 ipv6 address fe80::1 link-local
 no shutdown
```

### EUI-64

Automatically generates the interface ID from the MAC address:

1. Split MAC in half: `AA:BB:CC` | `DD:EE:FF`
2. Insert `FFFE` in the middle: `AA:BB:CC:FF:FE:DD:EE:FF`
3. Flip the 7th bit of the first byte

---

## VLSM (Variable Length Subnet Masking)

Without VLSM, every subnet in a network uses the **same mask** (classful or FLSM). That wastes addresses — a point-to-point link with 2 hosts gets the same size subnet as a LAN with 200 hosts. VLSM lets you use **different prefix lengths** within the same address space so each subnet is sized to fit.

### The Process

1. List all subnets you need, sorted **largest first** (most hosts → fewest hosts)
2. Pick the smallest prefix that fits each subnet's host count
3. Assign subnets sequentially — the next subnet starts where the previous one ends
4. Verify no subnets overlap

### How to Pick the Right Prefix

Use the formula: **2^(host bits) − 2 ≥ required hosts**

| Hosts Needed | Host Bits | Prefix | Block Size | Usable Hosts |
|-------------|-----------|--------|------------|--------------|
| 1–2         | 2         | /30    | 4          | 2            |
| 3–6         | 3         | /29    | 8          | 6            |
| 7–14        | 4         | /28    | 16         | 14           |
| 15–30       | 5         | /27    | 32         | 30           |
| 31–62       | 6         | /26    | 64         | 62           |
| 63–126      | 7         | /25    | 128        | 126          |
| 127–254     | 8         | /24    | 256        | 254          |

### IPv4 VLSM Example

**Given:** `192.168.1.0/24` — design subnets for:

| Subnet      | Hosts Needed |
|-------------|-------------|
| LAN A       | 100         |
| LAN B       | 50          |
| LAN C       | 25          |
| WAN link    | 2           |

**Step 1 — Start with the largest subnet (LAN A: 100 hosts)**

- Need 100 hosts → /25 gives 126 usable
- Subnet: `192.168.1.0/25`
- Range: `192.168.1.1` – `192.168.1.126`
- Broadcast: `192.168.1.127`
- Next available: `192.168.1.128`

**Step 2 — LAN B: 50 hosts**

- Need 50 hosts → /26 gives 62 usable
- Subnet: `192.168.1.128/26`
- Range: `192.168.1.129` – `192.168.1.190`
- Broadcast: `192.168.1.191`
- Next available: `192.168.1.192`

**Step 3 — LAN C: 25 hosts**

- Need 25 hosts → /27 gives 30 usable
- Subnet: `192.168.1.192/27`
- Range: `192.168.1.193` – `192.168.1.222`
- Broadcast: `192.168.1.223`
- Next available: `192.168.1.224`

**Step 4 — WAN link: 2 hosts**

- Need 2 hosts → /30 gives 2 usable
- Subnet: `192.168.1.224/30`
- Range: `192.168.1.225` – `192.168.1.226`
- Broadcast: `192.168.1.227`

**Summary:**

| Subnet | Network Address      | Usable Range                      | Broadcast        |
|--------|----------------------|-----------------------------------|-------------------|
| LAN A  | 192.168.1.0/25       | 192.168.1.1 – 192.168.1.126      | 192.168.1.127     |
| LAN B  | 192.168.1.128/26     | 192.168.1.129 – 192.168.1.190    | 192.168.1.191     |
| LAN C  | 192.168.1.192/27     | 192.168.1.193 – 192.168.1.222    | 192.168.1.223     |
| WAN    | 192.168.1.224/30     | 192.168.1.225 – 192.168.1.226    | 192.168.1.227     |

All four subnets fit inside the original /24 with no overlap and room to spare (`192.168.1.228` – `192.168.1.255` is unused).

### Common Mistakes

- **Not sorting largest first** — if you assign small subnets first, you may fragment the space and not have a large enough contiguous block later
- **Forgetting the −2** — network and broadcast addresses are not usable (except /31 point-to-point links)
- **Overlapping subnets** — always verify the next subnet starts **after** the previous subnet's broadcast address

---

## IPv6 Subnetting

IPv6 subnetting works differently than IPv4 — there's no shortage of addresses, so the focus is on clean, hierarchical allocation rather than conserving space.

### IPv6 Address Structure

A typical /48 allocation breaks down as:

```
|---- 48 bits ----|-- 16 bits --|-------- 64 bits --------|
|   Global Prefix |  Subnet ID  |      Interface ID        |
|  (from ISP)     | (you assign)|  (host portion)          |
```

- **Global prefix (/48):** assigned by your ISP
- **Subnet ID (16 bits):** gives you **65,536 subnets** to work with
- **Interface ID (64 bits):** always 64 bits for hosts (EUI-64 or manual)

### Standard Subnet: /64

The vast majority of IPv6 subnets use **/64** — this is the standard for any segment with hosts. SLAAC (Stateless Address Autoconfiguration) requires /64 to work.

### IPv6 Subnetting Example

**Given:** `2001:db8:ABCD::/48` — create subnets for four departments.

You have 16 bits of subnet ID (bits 49–64) to work with:

| Subnet       | Network Address            |
|--------------|----------------------------|
| Engineering  | `2001:db8:ABCD:0001::/64`  |
| Sales        | `2001:db8:ABCD:0002::/64`  |
| HR           | `2001:db8:ABCD:0003::/64`  |
| Management   | `2001:db8:ABCD:0004::/64`  |

Each /64 subnet has 2^64 addresses — enough that you never need to worry about host count.

### IPv6 Point-to-Point Links

For router-to-router links, you can use:

- **/64** — standard and simplest (recommended by RFC 6164 alternative below is also fine)
- **/127** — conserves addresses on point-to-point links (RFC 6164), avoids the ping-pong issue with /128
- **/126** — mimics IPv4's /30 (less common, but works)

```
! /127 point-to-point link
interface GigabitEthernet0/1
 ipv6 address 2001:db8:ABCD:FFFF::0/127

! Other side
interface GigabitEthernet0/0
 ipv6 address 2001:db8:ABCD:FFFF::1/127
```

### Hierarchical IPv6 Allocation

With 16 subnet bits, you can create a hierarchy using the hex digits of the subnet ID:

```
2001:db8:ABCD: [XX] [YY] ::/64
                |    |
                |    └── Sub-department or floor (256 values)
                └─────── Site or building (256 values)
```

**Example plan:**

| Site       | Subnet ID Range | Example Subnet               |
|------------|-----------------|-------------------------------|
| HQ         | `01xx`          | `2001:db8:ABCD:0100::/64`    |
| Branch 1   | `02xx`          | `2001:db8:ABCD:0200::/64`    |
| Branch 2   | `03xx`          | `2001:db8:ABCD:0300::/64`    |
| WAN links  | `FFxx`          | `2001:db8:ABCD:FF00::/127`   |

This makes firewall rules and route summarization much cleaner — you can summarize all of HQ as `2001:db8:ABCD:0100::/56`.

### IPv6 VLSM — Key Differences from IPv4

| Aspect              | IPv4 VLSM                          | IPv6 VLSM                          |
|---------------------|-------------------------------------|--------------------------------------|
| Goal                | Conserve addresses                  | Organize cleanly                     |
| Typical LAN prefix  | /24, /25, /26, etc.                | /64 (always)                         |
| Host count matters? | Yes — drives prefix selection       | No — /64 has 2^64 hosts             |
| Sorting by size?    | Required (largest first)            | Not needed                           |
| Point-to-point      | /30 (2 usable) or /31              | /64 or /127                          |
| Subnet bits         | Borrowed from host portion          | Dedicated 16-bit subnet field        |

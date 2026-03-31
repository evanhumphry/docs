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

VLSM allows using different subnet masks within the same network to efficiently allocate addresses.

**Steps:**

1. List subnets needed, sorted by size (largest first)
2. Assign the smallest subnet mask that fits each requirement
3. Ensure subnets don't overlap

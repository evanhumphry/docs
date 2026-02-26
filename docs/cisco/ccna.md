# CCNA Study Notes

A running collection of notes from CCNA study material.

---

## Network Fundamentals

### OSI Model

| Layer | Name         | Description                              |
|-------|--------------|------------------------------------------|
| 7     | Application  | User-facing protocols (HTTP, DNS, SMTP)  |
| 6     | Presentation | Data format, encryption                  |
| 5     | Session      | Session management                       |
| 4     | Transport    | End-to-end delivery (TCP, UDP)           |
| 3     | Network      | Logical addressing, routing (IP)         |
| 2     | Data Link    | MAC addressing, framing (Ethernet)       |
| 1     | Physical     | Bits over wire/wireless                  |

### TCP vs UDP

| Feature       | TCP                | UDP               |
|---------------|--------------------|-------------------|
| Connection    | Connection-oriented | Connectionless   |
| Reliability   | Guaranteed delivery | Best-effort      |
| Speed         | Slower             | Faster            |
| Use cases     | HTTP, SSH, FTP     | DNS, DHCP, VoIP  |

---

## IP Addressing & Subnetting

### IPv4 Address Classes

| Class | Range                       | Default Subnet Mask |
|-------|-----------------------------|---------------------|
| A     | 1.0.0.0 – 126.255.255.255   | /8 (255.0.0.0)      |
| B     | 128.0.0.0 – 191.255.255.255 | /16 (255.255.0.0)   |
| C     | 192.0.0.0 – 223.255.255.255 | /24 (255.255.255.0) |

### Private IP Ranges (RFC 1918)

| Range                        | CIDR Notation   |
|------------------------------|-----------------|
| 10.0.0.0 – 10.255.255.255   | 10.0.0.0/8      |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12   |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 |

### Subnetting Quick Reference

- **Hosts per subnet** = 2^(host bits) - 2
- **Number of subnets** = 2^(borrowed bits)

---

## Switching

### VLANs

### Spanning Tree Protocol (STP)

### EtherChannel

---

## Routing

### Static Routes

### OSPF

### EIGRP

---

## WAN Technologies

---

## Security

### Access Control Lists (ACLs)

### Port Security

---

## Network Services

### DHCP

### DNS

### NAT / PAT

---

## Wireless

---

## Additional Notes


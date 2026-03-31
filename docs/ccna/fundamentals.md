# Network Fundamentals

---

## OSI Model

| Layer | Name         | Description                              | Protocols / Examples        |
|-------|--------------|------------------------------------------|-----------------------------|
| 7     | Application  | User-facing protocols                    | HTTP, DNS, SMTP, FTP, SSH   |
| 6     | Presentation | Data format, encryption, compression     | SSL/TLS, JPEG, ASCII        |
| 5     | Session      | Session management                       | NetBIOS, PPTP               |
| 4     | Transport    | End-to-end delivery, segmentation        | TCP, UDP                    |
| 3     | Network      | Logical addressing, routing              | IP, ICMP, OSPF, EIGRP       |
| 2     | Data Link    | MAC addressing, framing, error detection | Ethernet, 802.11, ARP       |
| 1     | Physical     | Bits over wire/wireless                  | Cables, hubs, connectors    |

### Encapsulation

Data is wrapped with headers as it moves down the stack:

| Layer     | PDU Name   |
|-----------|------------|
| Layer 7-5 | Data       |
| Layer 4   | Segment    |
| Layer 3   | Packet     |
| Layer 2   | Frame      |
| Layer 1   | Bits       |

---

## TCP/IP Model

| Layer          | OSI Equivalent | Protocols                |
|----------------|----------------|--------------------------|
| Application    | Layers 5-7     | HTTP, DNS, DHCP, FTP     |
| Transport      | Layer 4        | TCP, UDP                 |
| Internet       | Layer 3        | IP, ICMP, ARP            |
| Network Access | Layers 1-2     | Ethernet, 802.11         |

---

## TCP vs UDP

| Feature        | TCP                  | UDP                |
|----------------|----------------------|--------------------|
| Connection     | Connection-oriented  | Connectionless     |
| Reliability    | Guaranteed delivery  | Best-effort        |
| Ordering       | In-order delivery    | No ordering        |
| Flow control   | Yes (windowing)      | No                 |
| Speed          | Slower               | Faster             |
| Header size    | 20 bytes             | 8 bytes            |
| Use cases      | HTTP, SSH, FTP, SMTP | DNS, DHCP, VoIP, TFTP |

### TCP Three-Way Handshake

1. **SYN** — Client sends SYN to server
2. **SYN-ACK** — Server responds with SYN-ACK
3. **ACK** — Client sends ACK, connection established

### TCP Connection Teardown

1. **FIN** — Initiator sends FIN
2. **ACK** — Receiver acknowledges
3. **FIN** — Receiver sends its own FIN
4. **ACK** — Initiator acknowledges, connection closed

---

## Common Port Numbers

| Port  | Protocol | Service            |
|-------|----------|--------------------|
| 20    | TCP      | FTP Data           |
| 21    | TCP      | FTP Control        |
| 22    | TCP      | SSH                |
| 23    | TCP      | Telnet             |
| 25    | TCP      | SMTP               |
| 53    | TCP/UDP  | DNS                |
| 67    | UDP      | DHCP Server        |
| 68    | UDP      | DHCP Client        |
| 69    | UDP      | TFTP               |
| 80    | TCP      | HTTP               |
| 110   | TCP      | POP3               |
| 143   | TCP      | IMAP               |
| 161   | UDP      | SNMP               |
| 443   | TCP      | HTTPS              |
| 514   | UDP      | Syslog             |
| 3389  | TCP      | RDP                |

---

## Ethernet

### Cable Types

| Type       | Standard    | Max Distance | Speed        |
|------------|-------------|--------------|--------------|
| Cat 5e     | 1000BASE-T  | 100 m        | 1 Gbps       |
| Cat 6      | 1000BASE-T  | 100 m        | 1 Gbps (10G at 55m) |
| Cat 6a     | 10GBASE-T   | 100 m        | 10 Gbps      |
| MMF Fiber  | 1000BASE-SX | 550 m        | 1 Gbps       |
| SMF Fiber  | 1000BASE-LX | 5 km         | 1 Gbps       |

### Straight-Through vs Crossover

- **Straight-through** — unlike devices (PC to switch, router to switch)
- **Crossover** — like devices (switch to switch, PC to PC)
- Most modern devices support **Auto-MDIX** and detect cable type automatically

---

## Duplex and Speed

- **Half duplex** — can send or receive, not both simultaneously (hubs)
- **Full duplex** — can send and receive simultaneously (switches)
- Mismatched duplex settings cause collisions and poor performance

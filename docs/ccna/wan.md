# WAN Technologies

---

## WAN Overview

WANs connect geographically separated LANs. Key WAN concepts for the CCNA:

| Term    | Description                                           |
|---------|-------------------------------------------------------|
| CPE     | Customer Premises Equipment (router, modem)           |
| DCE     | Data Communications Equipment (provides clocking)     |
| DTE     | Data Terminal Equipment (connects to DCE)             |
| Demarcation | Point where ISP responsibility ends and yours begins |

---

## WAN Connection Types

| Type                  | Description                                      |
|-----------------------|--------------------------------------------------|
| Leased Line           | Dedicated point-to-point circuit (T1, T3)        |
| Metro Ethernet        | Ethernet-based MAN/WAN service from provider     |
| MPLS                  | Label-switched paths through provider network    |
| Broadband (DSL/Cable) | Shared, asymmetric connections                   |
| Cellular (4G/5G)      | Wireless WAN backup or primary                   |
| Satellite             | High latency, remote area connectivity           |

---

## VPN (Virtual Private Network)

VPNs create secure tunnels over public networks.

### VPN Types

| Type        | Description                                        |
|-------------|----------------------------------------------------|
| Site-to-Site | Connects two networks (router to router)          |
| Remote Access | Individual users connect to corporate network    |
| DMVPN       | Dynamic multipoint VPN (hub-and-spoke, spoke-to-spoke) |

### IPsec

IPsec provides encryption, integrity, and authentication for VPN tunnels.

| Protocol | Purpose                     | Port/Protocol |
|----------|-----------------------------|---------------|
| IKE      | Key exchange, SA negotiation | UDP 500       |
| ESP      | Encryption + authentication  | IP protocol 50 |
| AH       | Authentication only (no encryption) | IP protocol 51 |

### GRE Tunnel

Generic Routing Encapsulation — encapsulates packets in IP. Not encrypted by itself, often combined with IPsec.

```
interface Tunnel0
 ip address 10.0.0.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 203.0.113.2
```

---

## PPP and HDLC

### HDLC (High-Level Data Link Control)

- Default serial encapsulation on Cisco routers
- Cisco's version is proprietary (adds a protocol type field)
- Simple, no authentication

### PPP (Point-to-Point Protocol)

- Open standard, works between any vendors
- Supports authentication: **PAP** (plain text) and **CHAP** (challenge-based, more secure)
- Supports multilink (bundle serial links)

```
! PPP with CHAP authentication
interface Serial0/0
 encapsulation ppp
 ppp authentication chap
```

---

## QoS Basics

Quality of Service prioritizes certain traffic types.

### Traffic Categories

| Category      | Examples          | Priority |
|---------------|-------------------|----------|
| Voice         | VoIP (RTP)        | Highest  |
| Video         | Streaming, video calls | High |
| Critical Data | ERP, databases    | Medium   |
| Best Effort   | Web, email        | Default  |
| Scavenger     | Torrents, gaming  | Lowest   |

### QoS Mechanisms

- **Classification & Marking** — identify and tag traffic (DSCP, CoS)
- **Queuing** — prioritize marked traffic (LLQ, CBWFQ)
- **Policing** — drop traffic exceeding a rate limit
- **Shaping** — buffer traffic exceeding a rate limit (smoother)

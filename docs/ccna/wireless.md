# Wireless

---

## 802.11 Standards

| Standard  | Frequency   | Max Speed    | Name       |
|-----------|-------------|--------------|------------|
| 802.11a   | 5 GHz       | 54 Mbps      | —          |
| 802.11b   | 2.4 GHz     | 11 Mbps      | —          |
| 802.11g   | 2.4 GHz     | 54 Mbps      | —          |
| 802.11n   | 2.4 / 5 GHz | 600 Mbps    | Wi-Fi 4    |
| 802.11ac  | 5 GHz       | 6.9 Gbps     | Wi-Fi 5    |
| 802.11ax  | 2.4 / 5 / 6 GHz | 9.6 Gbps | Wi-Fi 6/6E |

### 2.4 GHz vs 5 GHz

| Feature    | 2.4 GHz                | 5 GHz                  |
|------------|------------------------|------------------------|
| Range      | Longer                 | Shorter                |
| Speed      | Slower                 | Faster                 |
| Channels   | 3 non-overlapping (1, 6, 11) | 24 non-overlapping |
| Interference | More (microwaves, Bluetooth) | Less            |

---

## Wireless Architecture

### Autonomous APs

- Each AP is configured and managed independently
- Suitable for small deployments
- Each AP handles its own security, QoS, and roaming

### Controller-Based (WLC)

- **Wireless LAN Controller (WLC)** centrally manages all APs
- APs are "lightweight" — they forward traffic to the WLC via **CAPWAP** tunnels
- WLC handles configuration, security policies, roaming, and firmware updates
- Scalable for enterprise deployments

### CAPWAP (Control and Provisioning of Wireless Access Points)

| Tunnel         | Port     | Purpose                          |
|----------------|----------|----------------------------------|
| Control tunnel | UDP 5246 | Management, configuration        |
| Data tunnel    | UDP 5247 | Client data traffic              |

### AP Modes

| Mode        | Purpose                                            |
|-------------|----------------------------------------------------|
| Local       | Default — serves clients and monitors channels      |
| FlexConnect | Allows local switching at branch offices            |
| Monitor     | Passive monitoring only (IDS, rogue detection)      |
| Sniffer     | Captures wireless frames for analysis               |
| Bridge      | Point-to-point or point-to-multipoint bridging      |

---

## Wireless Security

| Standard | Encryption | Authentication         | Notes                    |
|----------|------------|------------------------|--------------------------|
| WEP      | RC4        | Shared key             | Deprecated, easily cracked |
| WPA      | TKIP       | PSK or 802.1X          | Interim improvement      |
| WPA2     | AES-CCMP   | PSK or 802.1X          | Current standard         |
| WPA3     | AES-GCMP   | SAE (Personal) or 802.1X | Strongest, forward secrecy |

### Authentication Methods

- **PSK (Pre-Shared Key)** — shared password, suitable for home/small office
- **802.1X (Enterprise)** — uses a RADIUS server for individual user authentication (EAP)

### EAP Types

| Type       | Description                                     |
|------------|-------------------------------------------------|
| EAP-TLS   | Certificate on both client and server (most secure) |
| PEAP      | Server certificate + username/password           |
| EAP-FAST  | Cisco proprietary, uses PAC for fast reconnection |

---

## Wireless Troubleshooting

### Common Issues

| Symptom              | Possible Cause                              |
|----------------------|---------------------------------------------|
| No connectivity      | Wrong SSID, wrong password, AP down         |
| Slow speeds          | Interference, too many clients, wrong band  |
| Intermittent drops   | Co-channel interference, low signal         |
| Can't roam           | VLAN mismatch, controller misconfiguration  |

### RF Concepts

- **RSSI** — Received Signal Strength Indicator (signal power in dBm)
- **SNR** — Signal-to-Noise Ratio (higher is better, aim for >25 dB)
- **Co-channel interference** — neighboring APs on the same channel
- **Adjacent channel interference** — overlapping channels (e.g., channels 1 and 3 on 2.4 GHz)

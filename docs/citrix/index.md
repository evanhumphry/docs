# Citrix Virtual Apps and Desktops

Citrix Virtual Apps and Desktops (CVAD) delivers Windows or Linux applications and desktops from centralized machines to users on almost any endpoint. **Citrix DaaS** provides similar delivery capabilities with Citrix-hosted cloud management services.

This section is a beginner-first map of the platform. It explains what each category and component is for, how a user connection works, and where **Citrix Provisioning (PVS)** fits.

!!! tip "Keep these three planes separate"
    - **Control plane:** decides who may connect and brokers the session.
    - **Resource plane:** runs the user’s apps or desktop on a VDA.
    - **Access plane:** gives the user an entry point and secures external access.

## Suggested learning order

1. [Product categories and delivery models](delivery-models.md)
2. [Architecture and core components](architecture.md)
3. [Connection flow](connection-flow.md)
4. [Machine catalogs and delivery groups](catalogs-delivery-groups.md)
5. [Machine Creation Services](mcs.md)
6. [Citrix Provisioning (PVS)](pvs.md)
7. [Policies, profiles, and application delivery](policies-profiles.md)
8. [Operations and troubleshooting](operations-troubleshooting.md)
9. [Glossary and study checklist](glossary.md)

## The platform in one picture

```text
User endpoint
  └─ Citrix Workspace app or browser
       └─ StoreFront / Citrix Workspace
            └─ Citrix Gateway or NetScaler Gateway (external access)
                 └─ Delivery Controller / Citrix DaaS broker
                      └─ VDA on a session host or desktop VM
                           ├─ applications and desktop
                           ├─ user profile and policies
                           └─ machine image supplied by MCS, PVS, or other tools
```

The user normally sees an app or desktop. The administrator sees layers: identity, access, brokering, machine provisioning, workload execution, policy, monitoring, and profile management.

## On-premises CVAD and Citrix DaaS

| Question | On-premises CVAD | Citrix DaaS |
|---|---|---|
| Who operates the management services? | Your organization | Citrix operates the cloud control plane |
| What connects the control plane to resources? | Delivery Controllers inside the site | Cloud Connectors or supported direct connections |
| Where do VDAs run? | Your data center or supported cloud | Your resource locations in data centers or clouds |
| Where is configuration managed? | Web Studio and site databases | Citrix Cloud management consoles and services |
| Who still manages workloads, apps, images, identity, and capacity? | Your organization | Your organization |

DaaS removes much of the control-plane infrastructure work; it does **not** remove the need to manage images, VDAs, applications, profiles, security, and capacity.

## Official references

- [Citrix Virtual Apps and Desktops technical overview](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/technical-overview)
- [Citrix DaaS product documentation](https://docs.citrix.com/en-us/citrix-daas)
- [Citrix Provisioning documentation](https://docs.citrix.com/en-us/provisioning)

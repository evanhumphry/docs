# User Connection Flow

Understanding the launch sequence makes troubleshooting much easier. The exact details vary by on-premises or DaaS design, authentication method, Gateway configuration, and whether rendezvous or direct connection features are enabled.

## Internal launch: simplified flow

1. **User opens Workspace app or a browser.** The endpoint contacts StoreFront or Citrix Workspace.
2. **User authenticates.** Identity might be validated by Active Directory, an identity provider, multifactor authentication, or another configured method.
3. **Resources are enumerated.** StoreFront or Workspace asks the brokering service what the user is entitled to see.
4. **User selects an app or desktop.** A launch request is sent to the broker.
5. **Broker selects a VDA.** The controller considers registration, maintenance mode, load, assignment, power state, and availability.
6. **Machine starts if required.** For power-managed catalogs, the controller asks the hosting platform to start a machine.
7. **Launch information is returned.** The endpoint receives the information required to connect to the selected VDA.
8. **HDX session is established.** Workspace app connects to the VDA using the permitted transport and security path.
9. **Session initializes.** The VDA applies computer and user policy, builds the user environment and profile, and starts the desktop or published application.
10. **Monitoring data is collected.** Controllers and monitoring services record session state and performance data for Director.

## External launch

For a remote user, Gateway is normally inserted into the access path:

```text
Workspace app → public DNS → Gateway → StoreFront/Workspace and broker
                                      └→ authorized HDX path → VDA
```

Gateway should be the controlled edge; VDAs should not simply be exposed to the public internet.

## Registration versus launch

**VDA registration** happens before a user launch. The VDA announces itself to a controller or cloud service path and remains in communication. An unregistered VDA cannot normally accept a new brokered session.

Registration depends on items such as:

- correct controller or cloud connector discovery;
- DNS and network reachability;
- compatible VDA and control-plane configuration;
- machine identity and time synchronization;
- required services and certificates where applicable.

## Brokering versus HDX

| Function | Purpose |
|---|---|
| **Authentication** | Prove the user’s identity. |
| **Enumeration** | List resources the user may access. |
| **Brokering** | Select an appropriate VDA and authorize the launch. |
| **HDX transport** | Carry display, keyboard, mouse, audio, printing, USB, and other virtual-channel traffic. |
| **Session initialization** | Load the profile, apply policy, map resources, and start the shell or app. |

A successful login to StoreFront does not prove that a VDA can register or that HDX traffic can reach it. Troubleshoot each phase separately.

## Launch failure map

| Symptom | Start with |
|---|---|
| Store or Workspace page unavailable | DNS, certificates, load balancer, StoreFront/Workspace service, Gateway |
| Authentication rejected | Identity provider, Active Directory, MFA, account state, time sync |
| No apps or desktops displayed | Delivery-group entitlement, application assignment, broker communication |
| “Cannot start” or no machine available | VDA registration, maintenance mode, capacity, assignment, power management |
| Launch begins then disconnects | Gateway/HDX path, firewall, certificates, transport, VDA services |
| Long blank screen or slow logon | Profile, group policy, logon scripts, printers, WEM, application startup |
| Existing session reconnects unexpectedly | Session reliability, reconnect policy, lingering session, assignment behavior |

## Session states

- **Active:** user is connected and interacting.
- **Disconnected:** session still exists on the VDA, but no endpoint is attached.
- **Logged off:** user processes and the session have ended.

Disconnecting is not the same as logging off. This distinction matters for capacity, application state, and maintenance.

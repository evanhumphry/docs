# Policies, Profiles, and Application Delivery

Provisioning gives a machine its base image. Policies and profile tools shape what happens when a user signs in.

## Citrix policies

Citrix policies control session behavior. Settings cover areas such as:

- graphics quality, encoding, and display limits;
- audio, webcam, microphone, and multimedia redirection;
- client drives, clipboard, USB, and device redirection;
- printers and printing behavior;
- session limits, reliability, and reconnect behavior;
- bandwidth and virtual-channel behavior;
- security and access restrictions.

Policies can be filtered to users, groups, delivery groups, tags, organizational units, client addresses, and other supported criteria. The effective result depends on policy priority, filters, defaults, and Windows policy interactions.

### Policy practice

1. Start with the default behavior and a small number of clearly named policies.
2. Change one purpose at a time.
3. Use narrow filters for exceptions.
4. Document priority and intended recipients.
5. Verify the **effective** policy in the actual user session rather than only reading the console.

## User profiles

A user profile contains settings and user-specific data such as registry state, application preferences, and user-shell configuration.

On pooled nonpersistent machines, a purely local profile is unreliable because the next session may run on a different or reset machine. A profile-management design externalizes the needed state.

### Citrix Profile Management

Citrix Profile Management can capture selected user-profile data and synchronize it with a profile store. Depending on the design, profile containers and related features can improve compatibility and logon performance.

Profile planning asks:

- Which settings must roam?
- Which caches should be excluded or containerized?
- Where is the profile store, and is it highly available?
- How are profile versions separated across operating-system versions?
- What happens when a profile is locked, corrupt, or unavailable?
- Which data belongs in a file service or cloud storage instead of the profile?

## Workspace Environment Management (WEM)

WEM can manage user-environment actions and optimize resource use. Common uses include:

- mapping drives and printers;
- creating shortcuts and environment variables;
- applying contextual user settings;
- CPU and process optimization;
- controlling startup behavior;
- improving logon consistency.

WEM is not a substitute for understanding Group Policy, Citrix policy, profiles, or application requirements. Map ownership so two systems do not repeatedly fight over the same setting.

## Application delivery categories

| Method | Meaning | Use case |
|---|---|---|
| **Installed in the master image** | App is part of the base MCS image or PVS vDisk. | Stable applications needed by most machines in the catalog. |
| **Installed on persistent machines** | App is maintained on individual dedicated systems. | Specialized cases where machine persistence is intentional. |
| **Application layering / attachment** | App content is separated from the base image using supported layering or attachment technology. | Reduce the number of base images or dynamically associate apps. |
| **Published from a VDA** | App executable on the VDA is exposed as a remote application. | Deliver only the application window to entitled users. |

“Published” describes how the user accesses the app. It does not by itself describe how the application was installed on the VDA.

## Slow-logon decomposition

Measure the phases instead of calling the entire delay “Citrix slowness”:

1. brokering and machine availability;
2. HDX connection establishment;
3. Windows authentication and Group Policy;
4. profile load or container attach;
5. logon scripts, drive and printer mapping;
6. WEM actions;
7. shell or published-application startup.

Director, Windows event logs, profile logs, policy results, and controlled test accounts help isolate the phase.

## Official references

- [Citrix policies](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/policies)
- [Citrix Profile Management](https://docs.citrix.com/en-us/profile-management)
- [Workspace Environment Management](https://docs.citrix.com/en-us/workspace-environment-management)

# RHCSA Skills Checklist

Use this page to track hands-on readiness for the **Red Hat Certified System Administrator (RHCSA), EX200** exam. It follows the current [official Red Hat exam objectives](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam), which are based on **Red Hat Enterprise Linux 10**.

!!! warning "Check before scheduling"
    Red Hat may revise the objectives or exam environment. Recheck the official page and practice on the RHEL version named for your scheduled exam.

## How to Use This Checklist

Check an item only when you can complete it on a disposable RHEL system:

1. **Without outside notes:** Use only documentation available on the system, such as `man`, `info`, `--help`, and `/usr/share/doc`.
2. **From the command line:** Do not depend on a graphical interface.
3. **With verification:** Confirm the result using a different command or inspection method.
4. **Persistently:** When required, make the configuration survive a reboot.
5. **Safely:** Inspect the current state first and avoid damaging unrelated configuration or data.

A completed checkbox means **I can perform, verify, troubleshoot, and explain this task**.

---

## Essential Tools

- [ ] Access a shell and run commands with correct syntax, quoting, paths, variables, command substitution, and exit-status handling.
- [ ] Redirect standard input, standard output, and standard error using `>`, `>>`, `<`, `2>`, `2>&1`, pipes, and `tee`.
- [ ] Search and analyze text with `grep`, common regular expressions, sorting, and pipelines.
- [ ] Connect to a remote system with SSH and select a nondefault user or port when required.
- [ ] Log in, identify active sessions, and switch users with `su` and `sudo` in a multiuser environment.
- [ ] Create, list, extract, compress, and decompress archives with `tar`, `gzip`, and `bzip2`.
- [ ] Create and edit text files from the terminal using an available text editor.
- [ ] Create, delete, copy, move, and rename files and directory trees.
- [ ] Create hard links and symbolic links, then explain and verify how they differ.
- [ ] Read, set, and change standard user/group/other permissions and ownership.
- [ ] Locate files by name, owner, type, size, or modification time.
- [ ] Find answers with `man`, `info`, `--help`, `apropos`, and files under `/usr/share/doc`.

## Software Management

- [ ] Inspect enabled and disabled RPM repositories.
- [ ] Create or modify a DNF repository definition and verify that its metadata can be read.
- [ ] Search for, install, update, remove, inspect, and verify RPM packages with DNF and RPM tools.
- [ ] Determine which package provides a command or file and which installed package owns a file.
- [ ] Install a local RPM while resolving dependencies.
- [ ] Install and update packages from the Red Hat Content Delivery Network or another remote repository.
- [ ] Add, inspect, and remove Flatpak repositories.
- [ ] Search for, install, update, run, list, and remove Flatpak applications.

## Simple Shell Scripts

- [ ] Create an executable Bash script with a valid shebang.
- [ ] Use `if`, `test`, `[ ]`, exit statuses, and logical operators for conditional execution.
- [ ] Use a `for` loop to process files, command output, or command-line input.
- [ ] Safely process positional parameters such as `$1`, `$2`, `$#`, and `"$@"`.
- [ ] Capture and process command output with command substitution.
- [ ] Validate script syntax and return useful exit codes and error messages.

## Running Systems

- [ ] Boot, reboot, shut down, and cancel a scheduled shutdown safely.
- [ ] Boot or switch manually into rescue, emergency, multiuser, or graphical targets.
- [ ] Interrupt the boot process to regain access to a system, including resetting the root password and handling SELinux relabeling.
- [ ] Identify CPU-intensive and memory-intensive processes.
- [ ] Terminate processes gracefully and use forced termination only when necessary.
- [ ] Adjust process scheduling priority with `nice` and `renice`.
- [ ] Inspect, select, and verify system tuning profiles.
- [ ] Locate and interpret traditional log files and systemd journal entries.
- [ ] Query logs by boot, unit, time range, and priority.
- [ ] Configure persistent systemd journal storage and verify logs remain available after reboot.
- [ ] Start, stop, restart, reload, enable, disable, and inspect network services.
- [ ] Transfer files securely between systems with SSH-based tools.

## Local Storage

!!! danger "Practice only on disposable storage"
    Partitioning, formatting, swap creation, and LVM commands can destroy data. Verify every device with `lsblk`, `blkid`, and `findmnt` before making changes.

- [ ] Inspect disks, partitions, file systems, mounts, swap, and LVM layout.
- [ ] List, create, and delete partitions on a GPT disk.
- [ ] Create and remove LVM physical volumes.
- [ ] Create volume groups, add physical volumes to them, and remove empty volume groups.
- [ ] Create, inspect, extend, and remove logical volumes.
- [ ] Create and label VFAT, ext4, and XFS file systems.
- [ ] Mount, use, verify, and unmount VFAT, ext4, and XFS file systems.
- [ ] Configure file systems to mount at boot by UUID or label.
- [ ] Validate `/etc/fstab` before rebooting.
- [ ] Add a new partition, logical volume, file system, or swap area without damaging existing data.
- [ ] Activate swap now, configure it persistently, and verify it.
- [ ] Mount and unmount an NFS export manually.
- [ ] Configure a persistent NFS mount with appropriate network-dependent options.
- [ ] Configure and verify an autofs indirect or wildcard map.
- [ ] Extend an existing logical volume and grow its XFS or ext4 file system.
- [ ] Diagnose file access failures involving ownership, mode bits, parent-directory traversal, ACLs, SELinux, mount options, or a read-only file system.

## System Deployment, Configuration, and Maintenance

- [ ] Schedule, list, and remove one-time jobs with `at`.
- [ ] Create and verify recurring user or system cron jobs.
- [ ] Create, enable, inspect, and troubleshoot a systemd timer and its service unit.
- [ ] Configure a service to start automatically at boot and verify both enablement and runtime state.
- [ ] Configure the system to boot into a specified default target.
- [ ] Configure the timezone and a chrony time-service client, then verify synchronization.
- [ ] Install and update software from a remote repository or local package file.
- [ ] Inspect and safely modify persistent bootloader or kernel arguments.
- [ ] Verify a bootloader change in the saved configuration and after reboot.

## Networking

- [ ] Inspect interfaces, addresses, routes, listening sockets, connection profiles, hostname, and name resolution.
- [ ] Configure a persistent static IPv4 address, prefix, gateway, and DNS servers with NetworkManager.
- [ ] Configure a persistent IPv6 address, prefix, gateway, and DNS servers with NetworkManager.
- [ ] Configure a connection to use DHCP or IPv6 autoconfiguration and remove obsolete static settings.
- [ ] Set a persistent hostname and configure or verify hostname resolution.
- [ ] Configure a network connection and network service to activate automatically at boot.
- [ ] Verify local addressing, routing, DNS resolution, remote reachability, and listening services.
- [ ] Inspect active firewalld zones and their interface or source assignments.
- [ ] Add and remove runtime and permanent firewalld service or port rules.
- [ ] Reload firewalld and verify that required access survives a reboot.

## Users and Groups

- [ ] Create, inspect, modify, lock, unlock, and delete local user accounts.
- [ ] Set or change passwords and force a password change at next login.
- [ ] Configure minimum age, maximum age, warning period, and account expiration.
- [ ] Create, inspect, rename, and delete local groups.
- [ ] Add or remove supplementary group memberships without unintentionally replacing existing memberships.
- [ ] Configure restricted privileged access with `sudoers` or `/etc/sudoers.d`.
- [ ] Validate sudo policy safely with `visudo` and verify the granted command as the target user.

## Security

- [ ] Calculate and configure default file and directory permissions with `umask`.
- [ ] Configure and explain setuid, setgid, and sticky-bit behavior.
- [ ] Create, inspect, modify, and remove access and default ACLs.
- [ ] Generate an SSH key pair and configure key-based authentication.
- [ ] Diagnose SSH key authentication failures involving ownership, permissions, configuration, or SELinux labels.
- [ ] Inspect SELinux status and switch between enforcing and permissive modes temporarily and persistently.
- [ ] List and interpret SELinux file, process, and user contexts.
- [ ] Restore default SELinux file contexts.
- [ ] Create and apply a persistent custom file-context rule with `semanage fcontext` and `restorecon`.
- [ ] List, add, modify, and remove SELinux port-label assignments.
- [ ] Inspect and persistently change SELinux Boolean settings.
- [ ] Use journal and audit records to diagnose an SELinux denial without disabling SELinux.
- [ ] Configure firewalld rules that allow required traffic while limiting unnecessary access.

---

## Full Practice Drills

These drills combine objectives the way a performance-based exam task may.

- [ ] **New server:** Configure hostname, static IPv4 and IPv6, DNS, time synchronization, updates, and SSH key access. Reboot and verify everything.
- [ ] **Shared project space:** Create users and a group, configure membership and sudo access, build a setgid directory with suitable permissions or ACLs, and verify access as each user.
- [ ] **Storage expansion:** Create a GPT partition and LVM stack, format and label a file system, mount it persistently, extend it, and confirm the new capacity after reboot.
- [ ] **Network storage:** Configure a persistent NFS mount and an autofs map, then verify on-demand access and recovery after reboot.
- [ ] **Web service:** Install and enable a service on a nondefault port, configure firewalld and SELinux correctly, and verify remote access without disabling security controls.
- [ ] **Automation:** Write a script that processes arguments and command output, then run it on a schedule with cron or a systemd timer and verify its logs.
- [ ] **Recovery:** Repair a deliberately broken boot target, `/etc/fstab` entry, service, file permission, and SELinux label using local documentation and logs.
- [ ] **Final persistence check:** Reboot the lab and verify storage, network, services, firewall, SELinux, scheduled tasks, users, and time synchronization without manual intervention.

## Ready-for-the-Exam Standard

You are ready when you can complete every item accurately on a fresh RHEL 10 lab, recover from mistakes without reinstalling, and finish multi-objective drills under a time limit. The official requirement applies to every section: **configurations must persist after reboot without intervention**.

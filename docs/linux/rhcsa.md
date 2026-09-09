# RHCSA Study Guide

A command-focused supplement for the **Red Hat Certified System Administrator (RHCSA), EX200** performance-based exam. This page follows the current [official Red Hat exam objectives](https://www.redhat.com/en/services/training/ex200-red-hat-certified-system-administrator-rhcsa-exam).

!!! warning "Check the objectives before the exam"
    Red Hat can revise EX200. Confirm the official objectives and the RHEL version used by your scheduled exam. Practice on that version whenever possible.

## How to Prepare

The RHCSA is practical: you configure real systems instead of answering multiple-choice questions. Practice each task until you can complete it from a plain shell, verify it, and make it survive a reboot.

For every lab:

1. Read the task carefully and note whether the change must be permanent.
2. Inspect the current state before changing it.
3. Make the smallest correct change.
4. Verify with a second command.
5. Reboot when practical and verify again.

Know how to find help locally when you forget syntax:

```bash
# Open the command's manual page; press / to search and q to quit
man command
# Show the command's built-in usage summary
command --help
# Search manual-page descriptions for a keyword
apropos keyword
man -k keyword                    # Equivalent keyword search through man
info command                      # Open the GNU Info documentation
ls /usr/share/doc                 # List package-supplied documentation
```

---

## 1. Understand and Use Essential Tools

### Shell syntax and command discovery

```bash
# Identify commands and shell built-ins
type cd                           # Report whether cd is a built-in, alias, or file
command -v useradd                # Print what the shell would execute
which ssh                         # Locate the executable found in PATH

# Quote strings and expand variables
name="Evan Humphry"
printf '%s\n' "$name"             # %s prints a string; \n adds a newline
echo "$HOME"                     # Double quotes allow $HOME expansion

# Run sequentially, on success, or on failure
command1 ; command2               # Run command2 regardless of command1's status
command1 && command2              # Run command2 only if command1 succeeds
command1 || command2              # Run command2 only if command1 fails
```

Memorize:

- **Absolute path:** begins with `/`; **relative path:** begins from the current directory.
- `.` is the current directory, `..` is its parent, and `~` is the current user's home.
- Single quotes preserve text literally; double quotes still expand variables and command substitutions.
- Exit status `0` means success; nonzero means failure. Check it with `echo $?`.

### Redirection and pipelines

| Operator | Meaning |
|---|---|
| `>` | Replace a file with standard output |
| `>>` | Append standard output |
| `<` | Read standard input from a file |
| `2>` | Redirect standard error |
| `2>&1` | Send standard error to the same place as standard output |
| `|` | Send one command's output to another command |
| `tee` | Write to a file and display output |

```bash
# Save normal output and errors in separate files
find /etc -name '*.conf' > /tmp/configs 2> /tmp/find-errors
# &> redirects both standard output and standard error
find /etc -name '*.conf' &> /tmp/all-output
# -i ignores case; uniq -c counts adjacent duplicate lines after sorting
grep -i error /var/log/messages | sort | uniq -c
# tee -a appends as root while also displaying the line
printf '%s\n' 'line' | sudo tee -a /etc/example.conf
```

### Search text with grep and regular expressions

```bash
grep root /etc/passwd                   # Print lines containing root
grep -i warning file                    # -i: ignore letter case
grep -n '^server' file                  # -n: include matching line numbers
grep -v '^#' file                       # -v: invert the match; exclude comments
grep -r 'PermitRootLogin' /etc/ssh      # -r: search directories recursively
grep -E '^(root|wheel):' /etc/group     # -E: use extended regular expressions
```

Regular-expression anchors and wildcards to memorize:

| Pattern | Meaning |
|---|---|
| `^text` | `text` at the beginning of a line |
| `text$` | `text` at the end of a line |
| `.` | Any one character |
| `*` | Zero or more of the previous item |
| `[0-9]` | One character in the range |
| `[^0-9]` | One character not in the range |
| `word\+` | One or more in basic regex; use `word+` with `grep -E` |

Shell globs are not regular expressions: `*.log` is a filename pattern interpreted by the shell.

### Remote access and user switching

```bash
ssh user@server                         # Open a remote shell as user
ssh -p 2222 user@server                 # -p: connect to TCP port 2222
sudo command                            # Run one command with delegated privileges
sudo -i                                 # -i: start root's login shell
su - user                               # -: load the target user's login environment
who                                     # Show currently logged-in sessions
w                                       # Show logged-in users and their activity
last                                    # Show login history from the wtmp database
```

The `-` in `su - user` loads the target user's login environment. Without it, environment variables and the working directory may be inherited.

### Archive and compression

```bash
# Create and extract an uncompressed tar archive
tar -cvf backup.tar /etc                 # -c create, -v list files, -f name archive
mkdir /tmp/restore && tar -xvf backup.tar -C /tmp/restore
                                         # -x extract; -C change directory first

# gzip
tar -czvf backup.tar.gz /etc             # -z: compress with gzip
tar -xzvf backup.tar.gz -C /tmp/restore  # -z: decompress gzip archive

# bzip2
tar -cjvf backup.tar.bz2 /etc            # -j: compress with bzip2
tar -xjvf backup.tar.bz2 -C /tmp/restore # -j: decompress bzip2 archive

# Inspect without extracting
tar -tvf backup.tar.gz                   # -t: list archive contents

gzip file
gunzip file.gz
bzip2 file
bunzip2 file.bz2
```

Tar letters: `c` create, `x` extract, `t` list, `v` verbose, `f` archive file, `z` gzip, `j` bzip2, `C` change extraction directory.

### Create and manage files

```bash
touch file                               # Create an empty file or update its timestamps
mkdir -p project/{docs,data}             # -p creates parents; braces create both subdirs
cp file copy                             # Copy a file
cp -a source_dir destination_dir         # -a preserves metadata and copies recursively
mv old new                               # Move or rename a path
rm file                                  # Remove one file
rm -r directory                          # -r: remove a directory tree recursively
install -m 0640 source /path/to/destination
                                         # Copy and set mode 0640 in one operation

# Inspect content
cat file
less file
head -n 20 file                          # -n 20: show the first 20 lines
tail -n 20 file                          # -n 20: show the last 20 lines
tail -f /var/log/messages                # -f: follow appended log entries

# Locate files
find /var/log -type f -name '*.log'      # Regular files whose names end in .log
find /home -user student -type f         # Regular files owned by student
find /tmp -type f -mtime +7              # Files modified more than seven days ago
locate filename                     # Database-backed; may need updatedb
```

### Hard and symbolic links

```bash
ln source hardlink                       # Create another hard link to the same inode
ln -s /absolute/path/to/source symlink   # -s: create a symbolic link storing a path
ls -li source hardlink symlink           # -i: display inode numbers; -l: long format
readlink -f symlink                      # -f: resolve every link to a canonical path
```

Memorize:

- A **hard link** is another directory entry for the same inode. It normally cannot cross file systems or link directories.
- A **symbolic link** stores a path. It can cross file systems and becomes dangling if its target disappears.
- Removing one hard-link name does not remove the data while another hard link exists.

### Standard permissions

```bash
ls -ld file directory                    # -l long format; -d inspect directory itself
chmod 640 file                           # Owner rw, group r, others no access
chmod u=rw,g=r,o= file                   # Same mode expressed symbolically
chmod -R g+rX directory                  # -R recursive; X adds execute only where useful
chown user:group file                    # Change both owner and group
chgrp group file                         # Change only the group
```

Permission values: `r=4`, `w=2`, `x=1`.

Directory permissions differ from file permissions:

- `r`: list names in the directory.
- `w`: create or remove entries.
- `x`: traverse/access entries.

---

## 2. Manage Software

### RPM and DNF repositories

```bash
# Inspect repositories
dnf repolist --all                       # Include enabled and disabled repositories
dnf repoinfo                             # Show details for enabled repositories
cat /etc/yum.repos.d/*.repo

# Add a repository (dnf-plugins-core may be required)
sudo dnf config-manager --add-repo https://example.com/repo.repo
                                         # Download and create a repository definition

# Minimal .repo file
# sudo gives tee permission to write; quoted 'EOF' preserves DNF variables literally
sudo tee /etc/yum.repos.d/example.repo >/dev/null <<'EOF'
[example]
name=Example Repository
baseurl=https://repo.example.com/rhel/$releasever/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.example.com/RPM-GPG-KEY-example
EOF

sudo dnf clean all                       # Remove all cached repository metadata/packages
sudo dnf makecache                       # Download fresh repository metadata
```

### Install, remove, update, and inspect packages

```bash
dnf search keyword                       # Search package names and descriptions
dnf provides '*/semanage'                # Find which package supplies this path/name
dnf info httpd                           # Show package metadata
sudo dnf install httpd                   # Install package and dependencies
sudo dnf install ./package.rpm           # Install a local RPM with dependencies
sudo dnf remove httpd                    # Remove package and unneeded dependencies
sudo dnf update                          # Upgrade all installed packages

dnf list installed                       # List installed packages
rpm -q bash                              # -q: query whether bash is installed
rpm -qi bash                             # -i: show package information
rpm -ql bash                             # -l: list files owned by the package
rpm -qf /usr/bin/ssh                     # -f: identify the package owning a file
rpm -V package-name                      # -V: verify installed files against RPM metadata
```

Use `dnf` for installation because it resolves dependencies. Use `rpm` mainly to query or verify package contents.

On registered systems, know the basic subscription commands:

```bash
subscription-manager status              # Show registration/subscription status
subscription-manager repos --list-enabled # List currently enabled Red Hat repositories
subscription-manager repos --enable=REPOSITORY_ID
                                         # Enable the repository persistently
```

### Flatpak repositories and software

```bash
flatpak remotes                           # List configured Flatpak repositories
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
                                          # Add Flathub only if it is not configured
flatpak search APPLICATION                # Search remotes for an application
flatpak install flathub APP_ID             # Install APP_ID from the flathub remote
flatpak list                               # List installed runtimes and applications
flatpak run APP_ID                         # Launch an installed application
flatpak update                             # Update installed Flatpaks
flatpak uninstall APP_ID                   # Remove an application
flatpak remote-delete REMOTE               # Remove a configured remote
```

System-wide is the default when run as root; `--user` installs for only the current user.

---

## 3. Create Simple Shell Scripts

Start scripts with a shebang and make them executable:

```bash
#!/bin/bash
set -u                                  # Treat an unset variable as an error

name=${1:-world}                        # Use $1, or "world" when $1 is unset/empty
printf 'Hello, %s\n' "$name"
```

```bash
chmod +x script.sh                       # Add execute permission
./script.sh Evan                         # Run from the current directory with argument $1
bash -n script.sh                        # -n: parse only; check syntax without running
```

### Arguments, tests, conditionals, loops, and command output

```bash
#!/bin/bash

if [ "$#" -lt 1 ]; then                 # Require at least one positional argument
    echo "Usage: $0 USER..." >&2          # >&2 sends the diagnostic to standard error
    exit 2                               # Return a nonzero status for invalid usage
fi

for user in "$@"; do                     # Iterate over arguments without losing spaces
    if id "$user" &>/dev/null; then      # Test existence; discard normal output and errors
        home=$(getent passwd "$user" | cut -d: -f6)
                                            # -d: colon delimiter; -f6: home field
        printf '%s: %s\n' "$user" "$home"
    else
        printf 'User not found: %s\n' "$user" >&2
    fi
done
```

Memorize:

- `$0`: script name; `$1`, `$2`: positional parameters.
- `$#`: number of parameters; `"$@"`: each argument preserved as a separate word.
- `$(command)`: command substitution.
- String tests: `-z`, `-n`, `=`, `!=`.
- Integer tests: `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`.
- File tests: `-e`, `-f`, `-d`, `-r`, `-w`, `-x`.
- Quote variable expansions unless word splitting is specifically intended.

---

## 4. Operate Running Systems

### Boot, reboot, shut down, and targets

```bash
systemctl reboot                          # Ask systemd to reboot now
systemctl poweroff                        # Shut down and power off now
shutdown -r +5 "Maintenance reboot"       # -r reboot in five minutes; notify users
shutdown -c                              # -c: cancel a pending shutdown

systemctl get-default                     # Show the target used at boot
systemctl set-default multi-user.target   # Persistently select non-graphical boot
systemctl isolate rescue.target           # Switch the running system to rescue mode
systemctl isolate multi-user.target       # Return to non-graphical multiuser mode
systemctl list-units --type=target        # List currently loaded target units
```

Common targets:

- `multi-user.target`: non-graphical, multiuser system.
- `graphical.target`: multiuser system with graphical login.
- `rescue.target`: single-user recovery with local file systems.
- `emergency.target`: minimal shell with few services and the root file system often read-only.

### Interrupt boot to reset the root password

Practice this exact workflow on the exam's RHEL version:

1. At GRUB, press `e` on the kernel entry.
2. Append `rd.break` to the line beginning with `linux`.
3. Press `Ctrl+x` to boot.
4. Remount the real root file system read-write, chroot, reset the password, and request relabeling:

```bash
mount -o remount,rw /sysroot              # Remount the real root read-write
chroot /sysroot                           # Make /sysroot the shell's apparent /
passwd root                               # Set a new root password
touch /.autorelabel                       # Request a full SELinux relabel next boot
exit                                     # Leave the chroot
exit                                     # Leave the rd.break shell and continue booting
```

SELinux relabeling can make the next boot take longer. The exact recovery flow can change by RHEL release, so verify it in the documentation available for the version used by your exam.

### Processes, signals, priority, and tuning

```bash
ps aux                                    # BSD-style snapshot of all users' processes
ps -ef                                    # POSIX-style full-format process snapshot
pgrep -a process-name                     # -a: show PIDs and full command lines
top
systemctl status service

kill PID                 # SIGTERM: request graceful termination
kill -15 PID
kill -9 PID              # SIGKILL: immediate; use only when needed
pkill process-name                        # Send SIGTERM to processes matching the name

nice -n 10 command                        # Start with nice value 10 (lower priority)
renice 5 -p PID                           # Set an existing process's nice value to 5
ps -o pid,ni,pri,cmd -p PID               # -o selects columns; -p selects one PID

systemctl status tuned
tuned-adm list                            # List available performance profiles
tuned-adm active                          # Show the active profile
sudo tuned-adm profile throughput-performance
sudo tuned-adm recommend                  # Show the profile tuned recommends
```

Lower nice values mean higher CPU scheduling priority. Ordinary users can increase the nice value (lower priority); raising priority generally requires root.

### Logs and persistent journals

```bash
journalctl
journalctl -b                             # -b: current boot only
journalctl -b -1                          # -1: boot immediately before current boot
journalctl -u sshd                        # -u: messages from the sshd unit
journalctl --since today                  # Limit entries by start time
journalctl -p err                         # -p: err priority and more severe
journalctl -f                             # -f: follow new entries live
systemctl status systemd-journald
ls /var/log
```

Enable persistent journal storage:

```bash
sudo mkdir -p /var/log/journal            # Create the persistent journal directory
sudo systemd-tmpfiles --create --prefix /var/log/journal
                                          # Apply tmpfiles ownership/mode rules to it
sudo systemctl restart systemd-journald
journalctl --list-boots                   # Verify that boot journals are retained
```

Alternatively set `Storage=persistent` under `[Journal]` in `/etc/systemd/journald.conf`, restart `systemd-journald`, and verify after a reboot.

### Services and secure transfers

```bash
systemctl status sshd
systemctl start sshd                      # Start now; does not imply boot enablement
systemctl stop sshd                       # Stop now
systemctl restart sshd                    # Stop and start the service
systemctl reload sshd                     # Re-read configuration without a full restart
systemctl enable --now sshd               # Enable at boot and start immediately
systemctl disable --now sshd              # Disable at boot and stop immediately
systemctl is-enabled sshd                 # Query boot enablement
systemctl is-active sshd                  # Query current runtime state

scp file user@server:/path/               # Copy a file over SSH
sftp user@server                          # Open an interactive SSH file-transfer session
rsync -a file user@server:/path/          # -a: archive mode; preserve key metadata
```

`enable` affects future boots; `start` affects the current boot. `enable --now` does both.

---

## 5. Configure Local Storage

!!! danger "Identify devices before changing storage"
    Partitioning, formatting, and PV creation can destroy data. In labs and on the exam, confirm device names with `lsblk`, `blkid`, and `findmnt` before acting.

### Inspect disks and file systems

```bash
lsblk -f                                  # Show block-device filesystems, labels, and UUIDs
blkid                                     # Probe block-device attributes such as UUID/type
findmnt                                   # Show the mount tree
findmnt --verify                          # Validate /etc/fstab syntax and usability
df -hT                                    # -h human sizes; -T filesystem types
du -sh /path                              # -s total only; -h human-readable size
fdisk -l                                  # -l: list disk partition tables
pvs; vgs; lvs                             # Summarize LVM physical, volume, logical volumes
```

### GPT partitions

With `parted`:

```bash
parted /dev/vdb print                     # Inspect the disk before changing it
parted /dev/vdb --script mklabel gpt      # Noninteractive: create a GPT table
parted /dev/vdb --script mkpart primary xfs 1MiB 2GiB
                                          # Create partition 1 from 1 MiB through 2 GiB
partprobe /dev/vdb                        # Ask the kernel to reread the partition table
udevadm settle                            # Wait until pending udev device events finish
lsblk /dev/vdb
```

Interactive `fdisk` also supports GPT (`g` creates a GPT table; `n` adds a partition; `d` deletes; `p` prints; `w` writes). Always inspect first.

### LVM: PVs, VGs, and LVs

```bash
pvcreate /dev/vdb1                        # Initialize the partition as an LVM PV
vgcreate vgdata /dev/vdb1                 # Create VG vgdata containing that PV
lvcreate -L 2G -n lvfiles vgdata          # -L exact size; -n logical-volume name
lvcreate -l 100%FREE -n lvrest vgdata     # -l extents; consume all free VG extents

pvs
vgs
lvs -a -o +devices                       # Include hidden LVs and append backing devices
```

Add capacity and extend an LV:

```bash
pvcreate /dev/vdc1
vgextend vgdata /dev/vdc1                 # Add the new PV to the existing VG
lvextend -L +1G /dev/vgdata/lvfiles       # Grow the LV by 1 GiB; not the filesystem yet
```

Remove in reverse dependency order after unmounting and removing persistent mount entries:

```bash
lvremove /dev/vgdata/lvfiles              # Remove the logical volume first
vgremove vgdata                           # Then remove the empty volume group
pvremove /dev/vdb1                        # Finally erase LVM metadata from the PV
```

### Create and mount file systems

```bash
mkfs.xfs /dev/vgdata/lvfiles              # Create an XFS filesystem (destroys old data)
mkfs.ext4 /dev/vdb2                      # Create an ext4 filesystem
mkfs.vfat /dev/vdb3                      # Create a FAT filesystem

mkdir -p /srv/files                       # Create the mount point and missing parents
mount /dev/vgdata/lvfiles /srv/files      # Mount for the current boot
findmnt /srv/files                        # Verify the source, target, type, and options
umount /srv/files                         # Unmount by mount point
```

Get the UUID and configure `/etc/fstab`:

```bash
blkid /dev/vgdata/lvfiles
```

```fstab
UUID=11111111-2222-3333-4444-555555555555 /srv/files xfs defaults 0 0
LABEL=archive /archive ext4 defaults 0 2
```

```bash
mount -a                                  # Attempt every eligible /etc/fstab entry
findmnt --verify                          # Report fstab parse or source/target problems
findmnt /srv/files
```

Never assume an `/etc/fstab` edit works. Run `mount -a` and `findmnt --verify` before rebooting.

Labels:

```bash
xfs_admin -L files /dev/vgdata/lvfiles    # -L: set the XFS label
e2label /dev/vdb2 archive                 # Set the ext2/3/4 label
fatlabel /dev/vdb3 USBSTORE               # Set the FAT label
```

### Add swap non-destructively

```bash
mkswap /dev/vgdata/lvswap                 # Write a swap-area signature
swapon /dev/vgdata/lvswap                 # Activate swap for the current boot
swapon --show                             # List active swap areas
free -h                                   # -h: show human-readable memory/swap totals
```

```fstab
UUID=SWAP-UUID none swap defaults 0 0
```

```bash
swapoff /dev/vgdata/lvswap                # Deactivate the swap area
```

### Extend a file system

XFS grows while mounted and cannot shrink:

```bash
lvextend -L +1G /dev/vgdata/lvfiles       # Add 1 GiB to the logical volume
xfs_growfs /srv/files                     # Grow mounted XFS to fill the larger device
```

Ext4 grows by device name and can be grown while mounted:

```bash
lvextend -L +1G /dev/vgdata/lvext4        # Add 1 GiB to the logical volume
resize2fs /dev/vgdata/lvext4              # Grow ext4 to fill the larger device
```

For LVM file systems, `lvextend -r -L +1G LV_PATH` asks LVM to resize the LV and file system together. Still verify with `lvs`, `findmnt`, and `df -hT`.

### NFS mounts

```bash
dnf install nfs-utils                     # Install NFS client commands
showmount -e nfs.example.com              # -e: list exports advertised by the server
mkdir -p /mnt/projects
mount -t nfs nfs.example.com:/exports/projects /mnt/projects
                                          # -t nfs: explicitly select the NFS type
findmnt /mnt/projects
```

Persistent `/etc/fstab` entry:

```fstab
nfs.example.com:/exports/projects /mnt/projects nfs defaults,_netdev 0 0
```

### autofs

```bash
dnf install autofs
```

Master map `/etc/auto.master.d/projects.autofs`:

```text
/projects /etc/auto.projects
```

Indirect map `/etc/auto.projects`:

```text
team -rw,sync nfs.example.com:/exports/team
```

```bash
systemctl enable --now autofs             # Enable at boot and start now
ls /projects/team                         # Access triggers the on-demand mount
mount | grep /projects/team
```

For a wildcard map, `* -rw nfs.example.com:/exports/&` substitutes the requested key for `&`.

### Diagnose file-permission problems

```bash
namei -l /srv/app/data/file                  # -l: show owner/mode for every path component
ls -ldZ /srv /srv/app /srv/app/data /srv/app/data/file
                                            # -d inspect dirs; -Z include SELinux contexts
id username                                 # Show the user's UID and all group memberships
getfacl /srv/app/data/file                  # Display ACL entries and the effective mask
sudo -u username test -r /srv/app/data/file && echo readable
                                            # Test readability as username; print on success
ausearch -m AVC -ts recent                  # AVC denials (-m) from a recent time (-ts)
```

Check every layer: ownership, mode bits, parent-directory execute permission, ACLs, SELinux context, mount options, and whether the file system is read-only.

---

## 6. Deploy, Configure, and Maintain Systems

### Schedule one-time and recurring tasks

```bash
# at
systemctl enable --now atd                 # Enable and start the one-time job daemon
echo '/usr/local/bin/report.sh' | at 17:00 # Queue input as a one-time job for 5 p.m.
atq                                      # List the current user's queued jobs
atrm JOB_NUMBER                          # Remove a queued job by number

# Per-user cron
crontab -e                                # Edit the current user's crontab
crontab -l                                # -l: list the current user's entries
crontab -u username -l                    # -u: select another user (root required)
```

Cron fields:

```text
minute hour day-of-month month day-of-week command
```

Examples:

```cron
*/15 * * * * /usr/local/bin/check.sh
30 2 * * 1-5 /usr/local/bin/backup.sh
```

Use absolute command paths in scheduled jobs and redirect output explicitly. Also know `/etc/crontab`, `/etc/cron.d/`, and `/etc/cron.{hourly,daily,weekly,monthly}/`.

### systemd timer units

`/etc/systemd/system/report.service`:

```ini
[Unit]
Description=Generate report

[Service]
Type=oneshot
ExecStart=/usr/local/bin/report.sh
```

`/etc/systemd/system/report.timer`:

```ini
[Unit]
Description=Run report daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl daemon-reload                    # Re-read unit files after creating/editing them
systemctl enable --now report.timer        # Start timer now and enable it at boot
systemctl list-timers                      # Show next and previous timer activations
systemctl status report.timer              # Inspect timer state and next trigger
journalctl -u report.service               # View output from the service the timer runs
```

`Persistent=true` runs a missed calendar event after the machine returns. It does not apply to monotonic timers such as `OnBootSec=`.

### Service enablement and default boot target

```bash
systemctl enable --now UNIT
systemctl disable --now UNIT
systemctl get-default
systemctl set-default multi-user.target
```

### Time synchronization

```bash
timedatectl                               # Show time, timezone, RTC, and NTP status
timedatectl set-timezone America/Los_Angeles # Persistently set the system timezone
timedatectl list-timezones                # List valid timezone names
systemctl enable --now chronyd            # Enable and start the NTP client/server
chronyc sources -v                        # -v: verbose NTP source state and legend
chronyc tracking                          # Show synchronization and clock statistics
```

Configure NTP sources in `/etc/chrony.conf`, then:

```bash
systemctl restart chronyd
chronyc sources -v
```

### Bootloader changes

Inspect kernel arguments:

```bash
cat /proc/cmdline                         # Show arguments used for the running kernel
grubby --default-kernel                   # Show the default kernel image path
grubby --info=ALL                         # Show saved entries for all installed kernels
```

Add or remove an argument from all installed kernels:

```bash
grubby --update-kernel=ALL --args="console=ttyS0"
                                          # Add the argument to every kernel entry
grubby --update-kernel=ALL --remove-args="console=ttyS0"
                                          # Remove it from every kernel entry
```

Common GRUB paths differ by firmware and RHEL version. Prefer tools such as `grubby` when the task permits, and verify the resulting kernel entry before rebooting.

---

## 7. Manage Basic Networking

### Inspect networking

```bash
ip -br address                            # -br: brief address summary
ip route                                  # Show the IPv4 routing table
ip -6 route                               # -6: show the IPv6 routing table
ss -tulpn                                 # -t TCP, -u UDP, -l listening, -p process, -n numeric
nmcli device status                       # Show interfaces and NetworkManager state
nmcli connection show                     # List saved NetworkManager profiles
hostnamectl                               # Show hostname and system identity
getent hosts server.example.com           # Resolve through configured NSS sources
```

### Configure IPv4 with NetworkManager

First identify the connection name:

```bash
nmcli connection show
```

Configure a static address, gateway, and DNS:

```bash
# Use static addressing, then set the address/prefix, gateway, and DNS list
nmcli connection modify 'System eth0' \
  ipv4.method manual \
  ipv4.addresses 192.0.2.10/24 \
  ipv4.gateway 192.0.2.1 \
  ipv4.dns '192.0.2.53 1.1.1.1'           # Set an ordered DNS server list

nmcli connection up 'System eth0'         # Activate the changed profile immediately
```

Return to DHCP:

```bash
# Switch to DHCP and clear values left from the static configuration
nmcli connection modify 'System eth0' \
  ipv4.method auto \
  ipv4.addresses '' \
  ipv4.gateway '' \
  ipv4.dns ''                              # Clear the saved static DNS list
nmcli connection up 'System eth0'
```

### Configure IPv6

```bash
# Configure a static IPv6 address, default gateway, and DNS server
nmcli connection modify 'System eth0' \
  ipv6.method manual \
  ipv6.addresses 2001:db8:1::10/64 \
  ipv6.gateway 2001:db8:1::1 \
  ipv6.dns 2001:4860:4860::8888           # Set an IPv6 DNS server
nmcli connection up 'System eth0'
```

Verify configuration and boot persistence:

```bash
nmcli -f GENERAL.STATE,IP4,IP6 connection show 'System eth0'
                                          # -f: display only the selected fields
ip -br address                            # Confirm assigned IPv4/IPv6 addresses
ip route
ping -c 3 192.0.2.1                       # -c 3: stop after three echo requests
getent hosts example.com
nmcli connection modify 'System eth0' connection.autoconnect yes
                                          # Activate this profile automatically at boot
```

### Hostname resolution

```bash
hostnamectl set-hostname server1.example.com # Set the persistent static hostname
hostnamectl
getent hosts server1.example.com
```

`/etc/hosts` format:

```text
192.0.2.10 server1.example.com server1
```

NetworkManager normally manages `/etc/resolv.conf`; configure DNS through the active connection rather than manually overwriting that file.

### firewalld

```bash
systemctl enable --now firewalld
firewall-cmd --get-active-zones            # Show zones currently bound to interfaces/sources
firewall-cmd --get-default-zone            # Show the zone used when none is specified
firewall-cmd --zone=public --list-all      # Show all runtime settings in public
firewall-cmd --get-services                # List predefined service definitions

# Permanent and immediate service rule
firewall-cmd --permanent --zone=public --add-service=http
                                           # Save HTTP allowance for future reloads/boots
firewall-cmd --zone=public --add-service=http
                                           # Add HTTP to the current runtime only

# Or make permanent changes and reload once
firewall-cmd --permanent --zone=public --add-port=8080/tcp
                                           # Persistently allow TCP destination port 8080
firewall-cmd --reload                      # Replace runtime rules with permanent rules
firewall-cmd --zone=public --list-all
```

Runtime rules disappear after reload or reboot. Permanent rules do not take effect in the runtime configuration until reload, unless you also add the runtime rule.

---

## 8. Manage Users and Groups

```bash
# Users
# Creation alternatives: run one, not both
useradd student                              # Create an account using system defaults
useradd -m -s /bin/bash student              # -m home directory; -s login shell
usermod -c 'Student User' student             # -c: set the GECOS/comment field
usermod -s /bin/bash student                  # -s: change the login shell
usermod -L student                            # -L: lock password authentication
usermod -U student                            # -U: unlock the password
passwd student                                # Set or change the user's password
id student                                    # Show UID, primary GID, and groups
getent passwd student                         # Query the configured account databases

# Deletion alternatives: run one, not both
userdel student                               # Remove account; leave home/data intact
userdel -r student                            # -r: also remove home and mail spool

# Groups
groupadd project                              # Create a group
groupmod -n newproject project                # -n: rename the group
groupdel newproject                           # Delete the group
usermod -aG wheel,project student             # -a append; -G supplementary groups
gpasswd -a student project                    # -a: add one user to one group
gpasswd -d student project                    # -d: delete one user from one group
getent group project                          # Query the configured group databases
```

Do not omit `-a` when adding supplementary groups with `usermod -aG`; `-G` by itself replaces the existing supplementary group list.

### Password aging

```bash
chage -l student                              # -l: list current password-aging values
chage -M 90 -m 1 -W 7 student                 # Max 90 days, min 1, warn for 7 days
chage -E 2026-12-31 student                   # -E: expire the account on this date
passwd -e student                             # -e: expire password now; change at login
```

Key files and defaults:

- `/etc/passwd`: account information; password field is normally `x`.
- `/etc/shadow`: password hashes and aging data.
- `/etc/group`: group membership.
- `/etc/login.defs`: account defaults.
- `/etc/skel`: files copied into a new home directory.

### Privileged access with sudo

Always edit sudo policy safely:

```bash
visudo                                        # Safely edit and syntax-check /etc/sudoers
visudo -f /etc/sudoers.d/project-admins       # -f: edit a specified sudoers file
visudo -cf /etc/sudoers.d/project-admins      # -c check only; -f select the file
```

Example `/etc/sudoers.d/project-admins`:

```sudoers
%project ALL=(ALL) /usr/bin/systemctl restart httpd, /usr/bin/systemctl status httpd
```

Use exact absolute command paths in sudo rules. Files under `/etc/sudoers.d` should normally be owned by root and mode `0440`.

---

## 9. Manage Security

### Default permissions and special modes

```bash
umask                                         # Display the current creation mask
umask 027                                     # Remove group write and all other access
```

Default mode calculation starts from `0666` for regular files and `0777` for directories, then removes the bits selected by the umask. With `umask 027`, typical results are files `0640` and directories `0750`.

Special permission bits:

| Bit | Numeric | Effect |
|---|---:|---|
| setuid | `4000` | Executable runs with file owner's effective UID |
| setgid | `2000` | Executable uses file group; directory causes new entries to inherit its group |
| sticky | `1000` | In a shared directory, users normally remove only their own entries |

```bash
chgrp project /srv/project                    # Make project the directory's group
chmod 2770 /srv/project                       # setgid; rwx for owner/group, none others
chmod 1777 /srv/dropbox                       # sticky bit on a world-writable directory
```

For ACLs when standard mode bits are not enough:

```bash
setfacl -m u:student:rw file                  # -m: add/modify a named-user ACL
setfacl -m g:project:rwx directory            # Add/modify a named-group ACL
setfacl -m d:g:project:rwx directory          # d: default ACL inherited by new entries
getfacl directory                             # Display access and default ACLs
setfacl -x u:student file                     # -x: remove the named-user ACL entry
```

### SSH key authentication

```bash
ssh-keygen -t ed25519                         # -t: create an Ed25519 key pair
ssh-copy-id student@server                    # Install the public key in authorized_keys
ssh student@server
```

Server-side checks:

```bash
ls -ldZ ~/.ssh                                # Inspect directory mode and SELinux label
ls -lZ ~/.ssh/authorized_keys                 # Inspect key-file mode and label
chmod 700 ~/.ssh                              # Owner rwx; no group/other access
chmod 600 ~/.ssh/authorized_keys              # Owner read/write only
restorecon -Rv ~/.ssh                         # -R recursive; -v report restored labels
sshd -t                                       # Test sshd configuration syntax
systemctl reload sshd
```

### SELinux modes and status

```bash
getenforce                                    # Print Enforcing, Permissive, or Disabled
sestatus                                      # Show detailed SELinux status and policy
setenforce 0                    # Permissive until reboot
setenforce 1                    # Enforcing until reboot
```

Persistent mode is controlled by `SELINUX=enforcing` or `SELINUX=permissive` in `/etc/selinux/config`. Disabled mode is different and usually requires a reboot; do not disable SELinux to solve a labeling problem.

### Contexts and restoring labels

```bash
ls -lZ /var/www/html                          # -Z: include SELinux contexts
ps -eZ | grep httpd                           # -e all processes; -Z include contexts
id -Z                                         # Show the current process/user context
matchpathcon /var/www/html/index.html         # Show the policy's expected file context
restorecon -Rv /var/www/html                  # Recursively restore expected labels verbosely
```

Temporary label change:

```bash
chcon -t httpd_sys_content_t /srv/site/index.html
                                               # -t: temporarily change the SELinux type
```

Persistent custom file-context rule:

```bash
dnf install policycoreutils-python-utils
semanage fcontext -a -t httpd_sys_content_t '/srv/site(/.*)?'
                                               # -a add rule; -t assign type to tree regex
restorecon -Rv /srv/site                       # Apply the policy rule recursively
semanage fcontext -l | grep /srv/site          # -l: list saved file-context rules
```

`chcon` can be overwritten by `restorecon` or a relabel. Use `semanage fcontext` plus `restorecon` for persistent policy-based labeling.

### SELinux port labels

```bash
semanage port -l | grep http_port_t             # -l: list known port-label rules
semanage port -a -t http_port_t -p tcp 8080     # -a add; -t type; -p protocol
semanage port -m -t http_port_t -p tcp 8080     # -m: modify an existing port rule
semanage port -d -t http_port_t -p tcp 8080     # -d: delete the matching port rule
```

Use `-a` to add a new port and `-m` when the port already exists under another type.

### SELinux Booleans and troubleshooting

```bash
getsebool -a | grep httpd                       # -a: list all SELinux Booleans
getsebool httpd_can_network_connect             # Query one Boolean's state
setsebool -P httpd_can_network_connect on       # -P: persist the change in policy

ausearch -m AVC -ts recent                      # AVC records since a recent time
journalctl -t setroubleshoot                    # -t: filter by syslog identifier
sealert -a /var/log/audit/audit.log             # -a: analyze the entire audit log
```

Troubleshooting order:

1. Confirm the Unix owner, group, permissions, and parent-directory traversal.
2. Check the process and file labels with `ps -eZ` and `ls -Z`.
3. Look for AVC denials with `ausearch`.
4. Restore expected labels or enable an appropriate existing Boolean.
5. Do not generate a custom policy until you understand why the access was denied.

---

## Concepts to Memorize

### Filesystem hierarchy

| Path | Purpose |
|---|---|
| `/etc` | System configuration |
| `/var` | Variable data such as logs, queues, and service state |
| `/home` | Regular user home directories |
| `/root` | Root user's home directory |
| `/tmp` | Temporary files; often cleaned automatically |
| `/run` | Runtime state since boot |
| `/usr` | Installed programs, libraries, and shared data |
| `/boot` | Kernel, initramfs, and bootloader data |
| `/dev` | Device nodes |
| `/proc` | Process and kernel information virtual filesystem |
| `/sys` | Device and kernel object virtual filesystem |

### Systemd unit states

- **active/inactive:** current runtime state.
- **enabled/disabled:** whether the unit starts automatically through install links.
- **masked:** cannot be started until unmasked.
- After creating or changing a unit file, run `systemctl daemon-reload`.

### Configuration persistence

Be able to distinguish a temporary change from a persistent one:

| Task | Temporary | Persistent |
|---|---|---|
| SELinux mode | `setenforce` | `/etc/selinux/config` |
| Firewall rule | Runtime `firewall-cmd` | `firewall-cmd --permanent` plus reload |
| Mount | `mount` | `/etc/fstab` or autofs map |
| Swap | `swapon` | `/etc/fstab` |
| Service | `systemctl start` | `systemctl enable` |
| Hostname | `hostname` | `hostnamectl set-hostname` |
| Network | `ip` command | NetworkManager connection with `nmcli` |
| Kernel argument | Edit one GRUB boot | Update saved kernel configuration |

### High-risk exam mistakes

- Formatting or partitioning the wrong disk.
- Editing `/etc/fstab` without running `mount -a` and `findmnt --verify`.
- Creating only a runtime firewall rule when persistence is required.
- Starting a service but forgetting to enable it.
- Forgetting `-a` in `usermod -aG`.
- Using `chmod 777` or disabling SELinux instead of diagnosing access.
- Using `chcon` when a persistent `semanage fcontext` rule is needed.
- Forgetting to reload a service, firewalld, NetworkManager connection, or systemd after configuration changes.
- Rebooting before checking syntax and persistent configuration.

---

## Final Practice Checklist

Use the complete, interactive [RHCSA Skills Checklist](rhcsa-checklist.md) to track every current RHEL 10 exam objective and combined practice drill.

Complete these capstone tasks from memory on disposable RHEL virtual machines:

- [ ] Configure static IPv4, IPv6, hostname, DNS, and autoconnect with `nmcli`.
- [ ] Create a user, supplementary group membership, password-aging policy, and restricted sudo rule.
- [ ] Create GPT partitions, an LVM stack, XFS and ext4 file systems, and swap.
- [ ] Mount local file systems persistently by UUID or label and validate `/etc/fstab`.
- [ ] Extend XFS and ext4 logical volumes without destroying data.
- [ ] Configure an NFS mount in `/etc/fstab` and an autofs indirect map.
- [ ] Schedule jobs with `at`, cron, and a systemd timer.
- [ ] Configure, enable, start, and verify a service.
- [ ] Add persistent firewalld service and port rules and verify the active zone.
- [ ] Configure SSH key authentication and correct its permissions and SELinux labels.
- [ ] Diagnose and repair an SELinux context, port, and Boolean issue.
- [ ] Enable persistent journaling and query current, previous-boot, service, and priority logs.
- [ ] Identify and terminate processes, adjust nice values, and select a tuned profile.
- [ ] Configure DNF and Flatpak repositories and install/remove software.
- [ ] Write scripts using tests, conditionals, loops, arguments, and command substitution.
- [ ] Recover root access by interrupting boot, then confirm SELinux relabeling.
- [ ] Reboot and confirm that every required configuration survives.

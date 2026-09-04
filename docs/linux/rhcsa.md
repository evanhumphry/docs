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
man command
command --help
apropos keyword
man -k keyword
info command
ls /usr/share/doc
```

---

## 1. Understand and Use Essential Tools

### Shell syntax and command discovery

```bash
# Identify commands and shell built-ins
type cd
command -v useradd
which ssh

# Quote strings and expand variables
name="Evan Humphry"
printf '%s\n' "$name"
echo "$HOME"

# Run sequentially, on success, or on failure
command1 ; command2
command1 && command2
command1 || command2
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
find /etc -name '*.conf' > /tmp/configs 2> /tmp/find-errors
find /etc -name '*.conf' &> /tmp/all-output
grep -i error /var/log/messages | sort | uniq -c
printf '%s\n' 'line' | sudo tee -a /etc/example.conf
```

### Search text with grep and regular expressions

```bash
grep root /etc/passwd
grep -i warning file                    # Ignore case
grep -n '^server' file                  # Show matching line numbers
grep -v '^#' file                       # Invert: exclude comments
grep -r 'PermitRootLogin' /etc/ssh      # Recursive search
grep -E '^(root|wheel):' /etc/group     # Extended regular expression
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
ssh user@server
ssh -p 2222 user@server
sudo command
sudo -i                         # Root login shell
su - user                       # Login shell as another user
who
w
last
```

The `-` in `su - user` loads the target user's login environment. Without it, environment variables and the working directory may be inherited.

### Archive and compression

```bash
# Create and extract an uncompressed tar archive
tar -cvf backup.tar /etc
mkdir /tmp/restore && tar -xvf backup.tar -C /tmp/restore

# gzip
tar -czvf backup.tar.gz /etc
tar -xzvf backup.tar.gz -C /tmp/restore

# bzip2
tar -cjvf backup.tar.bz2 /etc
tar -xjvf backup.tar.bz2 -C /tmp/restore

# Inspect without extracting
tar -tvf backup.tar.gz

gzip file
gunzip file.gz
bzip2 file
bunzip2 file.bz2
```

Tar letters: `c` create, `x` extract, `t` list, `v` verbose, `f` archive file, `z` gzip, `j` bzip2, `C` change extraction directory.

### Create and manage files

```bash
touch file
mkdir -p project/{docs,data}
cp file copy
cp -a source_dir destination_dir
mv old new
rm file
rm -r directory
install -m 0640 source /path/to/destination

# Inspect content
cat file
less file
head -n 20 file
tail -n 20 file
tail -f /var/log/messages

# Locate files
find /var/log -type f -name '*.log'
find /home -user student -type f
find /tmp -type f -mtime +7
locate filename                     # Database-backed; may need updatedb
```

### Hard and symbolic links

```bash
ln source hardlink
ln -s /absolute/path/to/source symlink
ls -li source hardlink symlink
readlink -f symlink
```

Memorize:

- A **hard link** is another directory entry for the same inode. It normally cannot cross file systems or link directories.
- A **symbolic link** stores a path. It can cross file systems and becomes dangling if its target disappears.
- Removing one hard-link name does not remove the data while another hard link exists.

### Standard permissions

```bash
ls -ld file directory
chmod 640 file
chmod u=rw,g=r,o= file
chmod -R g+rX directory
chown user:group file
chgrp group file
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
dnf repolist --all
dnf repoinfo
cat /etc/yum.repos.d/*.repo

# Add a repository (dnf-plugins-core may be required)
sudo dnf config-manager --add-repo https://example.com/repo.repo

# Minimal .repo file
sudo tee /etc/yum.repos.d/example.repo >/dev/null <<'EOF'
[example]
name=Example Repository
baseurl=https://repo.example.com/rhel/$releasever/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.example.com/RPM-GPG-KEY-example
EOF

sudo dnf clean all
sudo dnf makecache
```

### Install, remove, update, and inspect packages

```bash
dnf search keyword
dnf provides '*/semanage'
dnf info httpd
sudo dnf install httpd
sudo dnf install ./package.rpm
sudo dnf remove httpd
sudo dnf update

dnf list installed
rpm -q bash
rpm -qi bash
rpm -ql bash
rpm -qf /usr/bin/ssh
rpm -V package-name
```

Use `dnf` for installation because it resolves dependencies. Use `rpm` mainly to query or verify package contents.

On registered systems, know the basic subscription commands:

```bash
subscription-manager status
subscription-manager repos --list-enabled
subscription-manager repos --enable=REPOSITORY_ID
```

### Flatpak repositories and software

```bash
flatpak remotes
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak search APPLICATION
flatpak install flathub APP_ID
flatpak list
flatpak run APP_ID
flatpak update
flatpak uninstall APP_ID
flatpak remote-delete REMOTE
```

System-wide is the default when run as root; `--user` installs for only the current user.

---

## 3. Create Simple Shell Scripts

Start scripts with a shebang and make them executable:

```bash
#!/bin/bash
set -u

name=${1:-world}
printf 'Hello, %s\n' "$name"
```

```bash
chmod +x script.sh
./script.sh Evan
bash -n script.sh                    # Syntax check
```

### Arguments, tests, conditionals, loops, and command output

```bash
#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 USER..." >&2
    exit 2
fi

for user in "$@"; do
    if id "$user" &>/dev/null; then
        home=$(getent passwd "$user" | cut -d: -f6)
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
systemctl reboot
systemctl poweroff
shutdown -r +5 "Maintenance reboot"
shutdown -c

systemctl get-default
systemctl set-default multi-user.target
systemctl isolate rescue.target
systemctl isolate multi-user.target
systemctl list-units --type=target
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
mount -o remount,rw /sysroot
chroot /sysroot
passwd root
touch /.autorelabel
exit
exit
```

SELinux relabeling can make the next boot take longer. The exact recovery flow can change by RHEL release, so verify it in the documentation available for the version used by your exam.

### Processes, signals, priority, and tuning

```bash
ps aux
ps -ef
pgrep -a process-name
top
systemctl status service

kill PID                 # SIGTERM: request graceful termination
kill -15 PID
kill -9 PID              # SIGKILL: immediate; use only when needed
pkill process-name

nice -n 10 command
renice 5 -p PID
ps -o pid,ni,pri,cmd -p PID

systemctl status tuned
tuned-adm list
tuned-adm active
sudo tuned-adm profile throughput-performance
sudo tuned-adm recommend
```

Lower nice values mean higher CPU scheduling priority. Ordinary users can increase the nice value (lower priority); raising priority generally requires root.

### Logs and persistent journals

```bash
journalctl
journalctl -b                         # Current boot
journalctl -b -1                      # Previous boot
journalctl -u sshd
journalctl --since today
journalctl -p err
journalctl -f
systemctl status systemd-journald
ls /var/log
```

Enable persistent journal storage:

```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
journalctl --list-boots
```

Alternatively set `Storage=persistent` under `[Journal]` in `/etc/systemd/journald.conf`, restart `systemd-journald`, and verify after a reboot.

### Services and secure transfers

```bash
systemctl status sshd
systemctl start sshd
systemctl stop sshd
systemctl restart sshd
systemctl reload sshd
systemctl enable --now sshd
systemctl disable --now sshd
systemctl is-enabled sshd
systemctl is-active sshd

scp file user@server:/path/
sftp user@server
rsync -a file user@server:/path/
```

`enable` affects future boots; `start` affects the current boot. `enable --now` does both.

---

## 5. Configure Local Storage

!!! danger "Identify devices before changing storage"
    Partitioning, formatting, and PV creation can destroy data. In labs and on the exam, confirm device names with `lsblk`, `blkid`, and `findmnt` before acting.

### Inspect disks and file systems

```bash
lsblk -f
blkid
findmnt
findmnt --verify
df -hT
du -sh /path
fdisk -l
pvs; vgs; lvs
```

### GPT partitions

With `parted`:

```bash
parted /dev/vdb print
parted /dev/vdb --script mklabel gpt
parted /dev/vdb --script mkpart primary xfs 1MiB 2GiB
partprobe /dev/vdb
udevadm settle
lsblk /dev/vdb
```

Interactive `fdisk` also supports GPT (`g` creates a GPT table; `n` adds a partition; `d` deletes; `p` prints; `w` writes). Always inspect first.

### LVM: PVs, VGs, and LVs

```bash
pvcreate /dev/vdb1
vgcreate vgdata /dev/vdb1
lvcreate -L 2G -n lvfiles vgdata
lvcreate -l 100%FREE -n lvrest vgdata

pvs
vgs
lvs -a -o +devices
```

Add capacity and extend an LV:

```bash
pvcreate /dev/vdc1
vgextend vgdata /dev/vdc1
lvextend -L +1G /dev/vgdata/lvfiles
```

Remove in reverse dependency order after unmounting and removing persistent mount entries:

```bash
lvremove /dev/vgdata/lvfiles
vgremove vgdata
pvremove /dev/vdb1
```

### Create and mount file systems

```bash
mkfs.xfs /dev/vgdata/lvfiles
mkfs.ext4 /dev/vdb2
mkfs.vfat /dev/vdb3

mkdir -p /srv/files
mount /dev/vgdata/lvfiles /srv/files
findmnt /srv/files
umount /srv/files
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
mount -a
findmnt --verify
findmnt /srv/files
```

Never assume an `/etc/fstab` edit works. Run `mount -a` and `findmnt --verify` before rebooting.

Labels:

```bash
xfs_admin -L files /dev/vgdata/lvfiles
e2label /dev/vdb2 archive
fatlabel /dev/vdb3 USBSTORE
```

### Add swap non-destructively

```bash
mkswap /dev/vgdata/lvswap
swapon /dev/vgdata/lvswap
swapon --show
free -h
```

```fstab
UUID=SWAP-UUID none swap defaults 0 0
```

```bash
swapoff /dev/vgdata/lvswap
```

### Extend a file system

XFS grows while mounted and cannot shrink:

```bash
lvextend -L +1G /dev/vgdata/lvfiles
xfs_growfs /srv/files
```

Ext4 grows by device name and can be grown while mounted:

```bash
lvextend -L +1G /dev/vgdata/lvext4
resize2fs /dev/vgdata/lvext4
```

For LVM file systems, `lvextend -r -L +1G LV_PATH` asks LVM to resize the LV and file system together. Still verify with `lvs`, `findmnt`, and `df -hT`.

### NFS mounts

```bash
dnf install nfs-utils
showmount -e nfs.example.com
mkdir -p /mnt/projects
mount -t nfs nfs.example.com:/exports/projects /mnt/projects
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
systemctl enable --now autofs
ls /projects/team                    # Access triggers the mount
mount | grep /projects/team
```

For a wildcard map, `* -rw nfs.example.com:/exports/&` substitutes the requested key for `&`.

### Diagnose file-permission problems

```bash
namei -l /srv/app/data/file
ls -ldZ /srv /srv/app /srv/app/data /srv/app/data/file
id username
getfacl /srv/app/data/file
sudo -u username test -r /srv/app/data/file && echo readable
ausearch -m AVC -ts recent
```

Check every layer: ownership, mode bits, parent-directory execute permission, ACLs, SELinux context, mount options, and whether the file system is read-only.

---

## 6. Deploy, Configure, and Maintain Systems

### Schedule one-time and recurring tasks

```bash
# at
systemctl enable --now atd
echo '/usr/local/bin/report.sh' | at 17:00
atq
atrm JOB_NUMBER

# Per-user cron
crontab -e
crontab -l
crontab -u username -l
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
systemctl daemon-reload
systemctl enable --now report.timer
systemctl list-timers
systemctl status report.timer
journalctl -u report.service
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
timedatectl
timedatectl set-timezone America/Los_Angeles
timedatectl list-timezones
systemctl enable --now chronyd
chronyc sources -v
chronyc tracking
```

Configure NTP sources in `/etc/chrony.conf`, then:

```bash
systemctl restart chronyd
chronyc sources -v
```

### Bootloader changes

Inspect kernel arguments:

```bash
cat /proc/cmdline
grubby --default-kernel
grubby --info=ALL
```

Add or remove an argument from all installed kernels:

```bash
grubby --update-kernel=ALL --args="console=ttyS0"
grubby --update-kernel=ALL --remove-args="console=ttyS0"
```

Common GRUB paths differ by firmware and RHEL version. Prefer tools such as `grubby` when the task permits, and verify the resulting kernel entry before rebooting.

---

## 7. Manage Basic Networking

### Inspect networking

```bash
ip -br address
ip route
ip -6 route
ss -tulpn
nmcli device status
nmcli connection show
hostnamectl
getent hosts server.example.com
```

### Configure IPv4 with NetworkManager

First identify the connection name:

```bash
nmcli connection show
```

Configure a static address, gateway, and DNS:

```bash
nmcli connection modify 'System eth0' \
  ipv4.method manual \
  ipv4.addresses 192.0.2.10/24 \
  ipv4.gateway 192.0.2.1 \
  ipv4.dns '192.0.2.53 1.1.1.1'

nmcli connection up 'System eth0'
```

Return to DHCP:

```bash
nmcli connection modify 'System eth0' \
  ipv4.method auto \
  ipv4.addresses '' \
  ipv4.gateway '' \
  ipv4.dns ''
nmcli connection up 'System eth0'
```

### Configure IPv6

```bash
nmcli connection modify 'System eth0' \
  ipv6.method manual \
  ipv6.addresses 2001:db8:1::10/64 \
  ipv6.gateway 2001:db8:1::1 \
  ipv6.dns 2001:4860:4860::8888
nmcli connection up 'System eth0'
```

Verify configuration and boot persistence:

```bash
nmcli -f GENERAL.STATE,IP4,IP6 connection show 'System eth0'
ip -br address
ip route
ping -c 3 192.0.2.1
getent hosts example.com
nmcli connection modify 'System eth0' connection.autoconnect yes
```

### Hostname resolution

```bash
hostnamectl set-hostname server1.example.com
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
firewall-cmd --get-active-zones
firewall-cmd --get-default-zone
firewall-cmd --zone=public --list-all
firewall-cmd --get-services

# Permanent and immediate service rule
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --zone=public --add-service=http

# Or make permanent changes and reload once
firewall-cmd --permanent --zone=public --add-port=8080/tcp
firewall-cmd --reload
firewall-cmd --zone=public --list-all
```

Runtime rules disappear after reload or reboot. Permanent rules do not take effect in the runtime configuration until reload, unless you also add the runtime rule.

---

## 8. Manage Users and Groups

```bash
# Users
useradd student
useradd -m -s /bin/bash student
usermod -c 'Student User' student
usermod -s /bin/bash student
usermod -L student
usermod -U student
userdel student
userdel -r student
passwd student
id student
getent passwd student

# Groups
groupadd project
groupmod -n newproject project
groupdel newproject
usermod -aG wheel,project student
gpasswd -a student project
gpasswd -d student project
getent group project
```

Do not omit `-a` when adding supplementary groups with `usermod -aG`; `-G` by itself replaces the existing supplementary group list.

### Password aging

```bash
chage -l student
chage -M 90 -m 1 -W 7 student
chage -E 2026-12-31 student
passwd -e student
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
visudo
visudo -f /etc/sudoers.d/project-admins
visudo -cf /etc/sudoers.d/project-admins
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
umask
umask 027
```

Default mode calculation starts from `0666` for regular files and `0777` for directories, then removes the bits selected by the umask. With `umask 027`, typical results are files `0640` and directories `0750`.

Special permission bits:

| Bit | Numeric | Effect |
|---|---:|---|
| setuid | `4000` | Executable runs with file owner's effective UID |
| setgid | `2000` | Executable uses file group; directory causes new entries to inherit its group |
| sticky | `1000` | In a shared directory, users normally remove only their own entries |

```bash
chmod 2770 /srv/project
chgrp project /srv/project
chmod 1777 /srv/dropbox
```

For ACLs when standard mode bits are not enough:

```bash
setfacl -m u:student:rw file
setfacl -m g:project:rwx directory
setfacl -m d:g:project:rwx directory
getfacl directory
setfacl -x u:student file
```

### SSH key authentication

```bash
ssh-keygen -t ed25519
ssh-copy-id student@server
ssh student@server
```

Server-side checks:

```bash
ls -ldZ ~/.ssh
ls -lZ ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
restorecon -Rv ~/.ssh
sshd -t
systemctl reload sshd
```

### SELinux modes and status

```bash
getenforce
sestatus
setenforce 0                    # Permissive until reboot
setenforce 1                    # Enforcing until reboot
```

Persistent mode is controlled by `SELINUX=enforcing` or `SELINUX=permissive` in `/etc/selinux/config`. Disabled mode is different and usually requires a reboot; do not disable SELinux to solve a labeling problem.

### Contexts and restoring labels

```bash
ls -lZ /var/www/html
ps -eZ | grep httpd
id -Z
matchpathcon /var/www/html/index.html
restorecon -Rv /var/www/html
```

Temporary label change:

```bash
chcon -t httpd_sys_content_t /srv/site/index.html
```

Persistent custom file-context rule:

```bash
dnf install policycoreutils-python-utils
semanage fcontext -a -t httpd_sys_content_t '/srv/site(/.*)?'
restorecon -Rv /srv/site
semanage fcontext -l | grep /srv/site
```

`chcon` can be overwritten by `restorecon` or a relabel. Use `semanage fcontext` plus `restorecon` for persistent policy-based labeling.

### SELinux port labels

```bash
semanage port -l | grep http_port_t
semanage port -a -t http_port_t -p tcp 8080
semanage port -m -t http_port_t -p tcp 8080
semanage port -d -t http_port_t -p tcp 8080
```

Use `-a` to add a new port and `-m` when the port already exists under another type.

### SELinux Booleans and troubleshooting

```bash
getsebool -a | grep httpd
getsebool httpd_can_network_connect
setsebool -P httpd_can_network_connect on

ausearch -m AVC -ts recent
journalctl -t setroubleshoot
sealert -a /var/log/audit/audit.log
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

Complete these from memory on disposable RHEL virtual machines:

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

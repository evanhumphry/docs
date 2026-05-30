# Linux Commands

A reference for common Linux, Vim, and Tmux commands.

---

## Aliases

Edit `~/.bashrc` (or `~/.zshrc` for Zsh):

```bash
vim ~/.bashrc
```

Add the alias at the end of the file:

```bash
alias mycommand='cd ~/some/directory/'
```

Apply the changes:

```bash
source ~/.bashrc
```

---

## Vim

### Mode Switching

| Key     | Action                                     |
|---------|--------------------------------------------|
| `Esc`   | Switch to command mode                     |
| `i`     | Insert before cursor                       |
| `a`     | Insert after cursor                        |
| `o`     | Open new line below and enter insert mode  |

### Navigation

| Key     | Action                    |
|---------|---------------------------|
| `gg`    | Go to first line          |
| `G`     | Go to last line           |
| `^`     | Go to start of line       |
| `$`     | Go to end of line         |

### Editing

| Key     | Action                          |
|---------|---------------------------------|
| `dd`    | Delete (cut) current line       |
| `yy`    | Copy (yank) current line        |
| `p`     | Paste                           |
| `u`     | Undo                            |
| `Ctrl+r`| Redo                            |
| `v`     | Visual select mode              |

### Commands

| Command            | Action                            |
|--------------------|-----------------------------------|
| `:wq`              | Save and quit                     |
| `:q!`              | Quit without saving               |
| `:w filename`      | Save as filename                  |
| `/text`            | Search forward                    |
| `?text`            | Search backward                   |
| `:%s/old/new/g`    | Replace all occurrences           |
| `!ls`              | Insert output of `ls` into file   |

---

## Tmux

### Sessions

| Command                          | Action                     |
|----------------------------------|----------------------------|
| `tmux`                           | New session                |
| `tmux ls`                        | List sessions              |
| `tmux a`                         | Attach to last session     |
| `tmux a -t name`                 | Attach to named session    |
| `tmux kill-session -t name`      | Kill a session             |
| `pkill -f tmux`                  | Kill all tmux processes    |

### Key Bindings (prefix: `Ctrl+b`)

| Binding        | Action                    |
|----------------|---------------------------|
| `d`            | Detach from session       |
| `s`            | List sessions             |
| `%`            | Split pane vertically     |
| `"`            | Split pane horizontally   |
| `arrow key`    | Navigate between panes    |
| `:`            | Command mode              |

---

## SSH

### Generate a Key

```bash
ssh-keygen -t ed25519
```

Follow the prompts (defaults are fine). The public key is saved to `~/.ssh/id_ed25519.pub`.

### Copy Key to Remote Server

```bash
ssh-copy-id user@remoteserver
```

The key will be added to `~/.ssh/authorized_keys` on the remote host.

### View Public Key

```bash
# Mac
open -e ~/.ssh/id_ed25519.pub

# Windows
notepad .ssh/id_ed25519.pub
```

---

## SCP (Secure Copy)

```bash
# Local to remote
scp /path/to/file user@host:/destination/path/

# Remote to local
scp user@host:/remote/path/file /local/path/

# Copy directory
scp -r /path/to/dir user@host:/destination/path/
```

---

## Rsync

Rsync copies and synchronizes files locally or over SSH. Unlike `scp`, it only transfers **what has changed**, making it much faster for repeated syncs.

### Install

```bash
# Debian/Ubuntu
sudo apt install rsync

# RHEL/CentOS/Fedora
sudo dnf install rsync

# Mac (pre-installed, or update via Homebrew)
brew install rsync
```

### Basic Syntax

```
rsync [options] source destination
```

### Common Flags

| Flag            | Description                                                    |
|-----------------|----------------------------------------------------------------|
| `-a`            | Archive mode — preserves permissions, timestamps, symlinks, etc. (most common) |
| `-v`            | Verbose — shows files being transferred                        |
| `-z`            | Compress data during transfer (useful over slow connections)   |
| `-h`            | Human-readable file sizes                                      |
| `-P`            | Shows progress bar + keeps partially transferred files         |
| `--delete`      | Delete files in destination that don't exist in source (true mirror) |
| `-n` / `--dry-run` | Simulate the transfer — shows what would happen without doing it |
| `-e ssh`        | Specify SSH as the transport (default for remote transfers)    |
| `--exclude`     | Skip files matching a pattern                                  |
| `--include`     | Override an exclude for specific files                         |

### Local Sync

```bash
# Sync a directory to another location
rsync -avh /home/evan/projects/ /backup/projects/

# Sync and delete files in destination that are no longer in source
rsync -avh --delete /home/evan/projects/ /backup/projects/
```

**Trailing slash matters:**

- `projects/` — syncs the **contents** of the directory
- `projects` (no slash) — syncs the directory **itself**, creating `destination/projects/`

### Remote Sync Over SSH

```bash
# Push local to remote
rsync -avzP /home/evan/projects/ user@server:/backup/projects/

# Pull remote to local
rsync -avzP user@server:/var/www/html/ /local/backup/html/
```

### Using a Non-Standard SSH Port

```bash
rsync -avzP -e 'ssh -p 2222' /home/evan/projects/ user@server:/backup/projects/
```

### Exclude Files and Directories

```bash
# Exclude a single directory
rsync -avh --exclude 'node_modules' /home/evan/project/ /backup/project/

# Exclude multiple patterns
rsync -avh --exclude 'node_modules' --exclude '.git' --exclude '*.log' \
  /home/evan/project/ /backup/project/

# Exclude from a file
rsync -avh --exclude-from='exclude-list.txt' /home/evan/project/ /backup/project/
```

Example `exclude-list.txt`:

```
node_modules
.git
*.log
.env
__pycache__
```

### Dry Run (Preview Before Syncing)

Always a good idea before using `--delete`:

```bash
rsync -avhn --delete /home/evan/projects/ /backup/projects/
```

The `-n` flag shows exactly what would be transferred or deleted without actually doing it.

### Useful Examples

```bash
# Back up home directory to external drive, skip cache
rsync -avhP --exclude '.cache' /home/evan/ /mnt/external/home-backup/

# Mirror a website to a local backup (delete removed files)
rsync -avzP --delete user@server:/var/www/html/ /local/www-backup/

# Sync only specific file types
rsync -avh --include '*.conf' --exclude '*' /etc/ /backup/configs/

# Resume a large interrupted transfer
rsync -avzP user@server:/data/largefile.iso /local/downloads/
```

### Automate with Cron

```bash
# Edit crontab
crontab -e

# Run a backup every night at 2:00 AM
0 2 * * * rsync -az --delete /home/evan/projects/ user@server:/backup/projects/
```

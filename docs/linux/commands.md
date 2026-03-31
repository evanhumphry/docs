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

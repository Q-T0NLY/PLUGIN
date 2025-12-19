# 🚀 NEXUS AI STUDIO v3.1 - ZSH Configuration

> **Comprehensive Terminal Configuration for macOS Big Sur Intel**  
> Production-ready with AI integration, system monitoring, and advanced utilities

---

## 📋 Quick Links

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Commands](#commands)
- [Project Structure](#project-structure)

---

## Overview

**NEXUS AI Studio** is a unified, production-grade ZSH configuration designed specifically for macOS Big Sur Intel systems. It combines real-time system monitoring, AI integration, advanced tooling, and productivity features into one seamless experience.

---

## ✨ Features

### 🎨 Dashboard & Visualization
- Real-time system metrics dashboard with auto-refresh
- Live CPU, Memory, Disk, Battery monitoring
- Health score calculations
- TrueColor (24-bit) and 256-color support

### 🖥️ System Monitoring
- Comprehensive metrics display
- Process and network tracking
- Temperature monitoring
- Battery status and uptime

### 🤖 AI Intelligence
- Multi-provider support (OpenAI, Claude, Groq, DeepSeek, Google, Ollama)
- Code review, debugging, optimization
- Advanced prompt engineering

### 📦 Tool Management
- Database of 1000+ development tools
- Multiple installation methods per tool
- Batch installation support

### 📋 TODO Management
- Create, list, complete tasks
- Priority, due dates, tags support
- Statistical reporting

### ⚙️ Auto Systems
- Auto-healing and optimization
- Performance recommendations
- Smart backup creation

### 🛡️ Security & Privacy
- File encryption/decryption
- Permission auditing
- Security hardening

---

## 🚀 Quick Start

### Installation (One Command)

```bash
# Clone and install
git clone https://github.com/bigolivenyc-cloud/ZSH.git
cd ZSH
bash install.sh

# Reload your shell
source ~/.zshrc
```

### First Commands

```bash
quantum-help          # Display help menu
quantum-dashboard     # View system dashboard
quantum-metrics       # Show system metrics
quantum-stats         # Quick statistics
```

---

## 📥 Installation

### Prerequisites
- macOS Big Sur or later
- zsh 5.0+
- Terminal with 256-color support

### Step-by-Step

1. **Clone Repository**
   ```bash
   git clone https://github.com/bigolivenyc-cloud/ZSH.git
   cd ZSH
   ```

2. **Run Installer**
   ```bash
   chmod +x install.sh
   bash install.sh
   ```

3. **Reload Configuration**
   ```bash
   source ~/.zshrc
   ```

4. **Verify Installation**
   ```bash
   quantum-help
   ```

---

## 🎯 Commands Reference

### Dashboard & Monitoring
| Command | Description |
|---------|-------------|
| `quantum-dashboard` | Live system dashboard |
| `quantum-metrics` | Detailed system metrics |
| `quantum-stats` | Quick statistics |
| `quantum-help` | Help menu |

### Git Shortcuts
| Alias | Command |
|-------|---------|
| `gs` | `git status` |
| `ga` | `git add` |
| `gc` | `git commit` |
| `gp` | `git pull` |
| `gph` | `git push` |

### System Management
```bash
quantum-heal          # Auto-fix system
quantum-backup        # Create backup
quantum-update        # Check updates
```

---

## 📁 Project Structure

```
ZSH/
├── install.sh                    # ⭐ Run this to install
├── README.md                     # Documentation
└── zsh-config/
    ├── zsh/
    │   └── zshrc.txt            # Enhanced zshrc
    └── ultra-zsh/
        ├── nexus_bootstrap.zsh  # Bootstrap script
        ├── modules/             # Core modules
        │   ├── system_metrics.zsh
        │   ├── enhanced_dashboard.zsh
        │   └── help_system.zsh
        └── plugins/             # Plugin system
```

### After Installation
```
~/.config/ultra-zsh/
├── modules/         # Loaded modules
├── plugins/         # User plugins
├── backups/         # Configuration backups
├── logs/            # Activity logs
├── cache/           # Temporary cache
├── ai/              # AI configurations
├── security/        # Security data
└── dashboard/       # Dashboard configs
```

---

## 🔧 Configuration

### Main Configuration
- **Location**: `~/.zshrc`
- **Backup**: `~/.config/ultra-zsh/backups/`

### Customize Settings

Edit `~/.zshrc`:
```bash
# Change editor
export EDITOR="vim"

# Set terminal type
export TERM="xterm-256color"

# Adjust dashboard refresh
quantum-dashboard 2    # 2-second refresh
```

---

## 🆘 Troubleshooting

### Commands not found
```bash
source ~/.zshrc
```

### Colors not displaying
```bash
export TERM=xterm-256color
```

### Permission denied
```bash
chmod +x install.sh
bash install.sh
```

### Restore original zshrc
```bash
cp ~/.config/ultra-zsh/backups/.zshrc.backup ~/.zshrc
source ~/.zshrc
```

---

## 📚 Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `NEXUS_HOME` | `~/.config/ultra-zsh` | Config directory |
| `EDITOR` | `nvim` | Default editor |
| `TERM` | `xterm-256color` | Terminal type |
| `HISTSIZE` | `50000` | History size |

---

## 🎓 Advanced Usage

### Create Custom Module

```bash
cat > ~/.config/ultra-zsh/modules/my_module.zsh << 'EOF'
#!/usr/bin/env zsh
# My custom module

my_command() {
    echo "Hello from my module"
}

alias my-cmd='my_command'
EOF
```

### Add Custom Aliases

Edit `~/.zshrc` and add:
```bash
alias myalias='your command here'
source ~/.zshrc
```

---

## 🗑️ Uninstallation

```bash
# Restore original config
cp ~/.config/ultra-zsh/backups/.zshrc.backup ~/.zshrc

# Remove configuration
rm -rf ~/.config/ultra-zsh

# Reload
source ~/.zshrc
```

---

## 📝 Changelog

### v3.1.0 (Current)
- ✨ Unified build and installation system
- ✨ Enhanced dashboard with TrueColor support
- ✨ Optimized metrics for Big Sur Intel
- ✨ Comprehensive help system
- ✨ Production-ready configuration

### v3.0.0
- Initial release with core features

---

## 📄 License

Open source under MIT License

---

## 🙏 Support

- **Documentation**: See README.md and `quantum-help`
- **Issues**: [GitHub Issues](https://github.com/bigolivenyc-cloud/ZSH)
- **Logs**: `~/.config/ultra-zsh/logs/`

---

## Archived Documentation

To reduce clutter, non-critical, duplicate, or delivery-focused documents have been moved to `archived_docs/`. This includes historical specs, installers, and delivery manifests.

### Examples of Archived Files:
- `00_START_HERE.md`
- `QUICKSTART.md`
- `NEXUS_QUANTUM_*` files
- `PROJECT_*` summaries

To restore any file, use:
```bash
git mv archived_docs/<filename>.md ./
git commit -m "restore <filename> from archive"
```

---

**Made with ❤️ for terminal enthusiasts | [GitHub](https://github.com/bigolivenyc-cloud/ZSH)**

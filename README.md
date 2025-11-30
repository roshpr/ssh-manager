# 🔐 SSH Manager

A beautiful, modern TUI (Text User Interface) application for managing SSH configurations with ease.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)

## ✨ Features

- **🔍 Fuzzy Search** - Quickly find hosts with intelligent fuzzy matching
- **📋 Host Management** - Add, view, and manage SSH hosts with a clean interface
- **🎨 Beautiful UI** - Modern Material Design with soft colors and smooth interactions
- **⌨️ Keyboard Navigation** - Efficient keyboard shortcuts for power users
- **🎯 Visual Selection** - Clear arrow indicator shows selected host
- **🔗 Quick Connect** - Press Enter to instantly SSH into selected host
- **📊 Alternating Rows** - Easy-to-read host list with alternating colors
- **💾 Auto-save** - Changes are automatically saved to `~/.ssh/config`

## 🖼️ Interface

The SSH Manager features:
- **Light green header** with app title and copyright
- **Centered layout** (75% width) for focused viewing
- **Black background** for reduced eye strain
- **White content area** with green borders
- **Orange arrow indicator** for selected hosts
- **Soft grey alternating rows** for better readability

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Install from source

```bash
# Clone or navigate to the project directory
cd ssh_manager

# Install using make
make install
```

### Add to PATH

After installation, add the Python bin directory to your PATH:

```bash
# For current session
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# For permanent use (add to ~/.zshrc or ~/.bashrc)
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 🚀 Usage

### Starting the application

```bash
ssh_manager
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate through hosts |
| `Enter` | Connect to selected host |
| `/` | Focus search box |
| `d` | View host details |
| `a` | Add new host |
| `q` | Quit application |

### Adding a Host

1. Press `a` to open the Add Host form
2. Fill in the required fields:
   - **Host Alias**: Friendly name for the host
   - **Hostname**: IP address or domain name
   - **User**: SSH username
   - **IdentityFile**: SSH key file (optional)
   - **ProxyJump**: Jump host (optional)
   - **ForwardAgent**: Enable agent forwarding (optional)
3. Press `Tab` to navigate between fields
4. Click "Save" or press `Enter` to save

### Searching for Hosts

1. Press `/` to focus the search box
2. Type to filter hosts using fuzzy matching
3. Example: typing "srv" will match "my-server", "srv-prod", etc.

### Connecting to a Host

1. Navigate to the desired host using arrow keys
2. Press `Enter` to initiate SSH connection
3. The TUI will close and SSH will take over

## 🏗️ Project Structure

```
ssh_manager/
├── ssh_manager/
│   ├── __init__.py
│   ├── main.py              # Main application and entry point
│   ├── tui.py               # TUI components (widgets, screens)
│   ├── config_parser.py     # SSH config file parser
│   └── ssh_manager.css      # Styling and theme
├── setup.py                 # Package configuration
├── Makefile                 # Build and install commands
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎨 Customization

### Changing Colors

Edit `ssh_manager/ssh_manager.css` to customize colors:

- **Header background**: `#a5d6a7` (light green)
- **Selection arrow**: `#ff6f00` (orange)
- **Borders**: `#4caf50` (green)
- **Background**: `#000000` (black)

### Changing Layout

Modify the `#app-container` width in CSS to adjust the centered container size (default: 75%).

## 🛠️ Development

### Requirements

- `textual` - TUI framework

### Building

```bash
make install
```

### Testing

Run the application with a test config:

```bash
python3 -m ssh_manager.main /path/to/test/config
```

## 📝 Configuration

The SSH Manager reads and writes to `~/.ssh/config`. All changes are automatically saved to this file in standard SSH config format.

### Example SSH Config Entry

```
Host my-server
    HostName 192.168.1.100
    User admin
    IdentityFile ~/.ssh/id_rsa
    ProxyJump bastion
    ForwardAgent yes
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

Copyright © 2024 Rosh PR

## 🙏 Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual) - An amazing TUI framework
- Inspired by modern Material Design principles

## 📞 Support

For issues, questions, or suggestions, please open an issue on the project repository.

---

**Made with ❤️ by Rosh PR**

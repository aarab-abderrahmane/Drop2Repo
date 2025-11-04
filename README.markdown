# Drop2Repo – Version 8.0.1 (Ultimate Edition) 🚀  
**A sleek, secure, and powerful GUI tool for managing GitHub repositories with a modernized interface and cutting-edge features!**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Version](https://img.shields.io/badge/version-8.0.1-blue.svg)](https://github.com/aarab-abderrahmane/Drop2Repo/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://github.com/aarab-abderrahmane/Drop2Repo)

---

## 📷 Screenshots

<img width="1365" height="724" alt="Drop2Repo Main Interface" src="https://github.com/user-attachments/assets/94ae12bd-e4ba-49bc-9a9c-46c66d27fb77" />

### Resizable Window Interface
<img width="1366" height="724" alt="Drop2Repo Resizable Window" src="https://github.com/user-attachments/assets/5ba1bdc8-fea7-40bb-a5e9-e65093364ed9" />

---

## 📌 Overview  

Drop2Repo is a state-of-the-art desktop application designed to streamline Git operations for developers of all skill levels. With its modern, eye-friendly dark interface, intuitive controls, and advanced features, managing GitHub repositories has never been easier. Version 8.0.1 introduces significant performance improvements, a revamped UI design with modern icons, and a powerful path history feature for enhanced productivity.

### Why Choose Drop2Repo?

- 🚀 **Fast & Efficient:** Multi-threaded Git operations for lightning-fast performance
- 🔒 **Secure & Safe:** No data collection, local storage only, secure credential handling
- 🎨 **User-Friendly:** Modern UI with intuitive controls and contemporary design
- ⚡ **Real-Time Updates:** Live file tracking with instant status updates
- 🛠 **Advanced Tools:** Comprehensive commit management and Git operations

---

## ✨ Key Features

### Core Functionality
- ⚡ **Enhanced Performance:** Optimized multi-threaded Git operations for maximum speed
- 📂 **Smart File Management:** Real-time tracking of staged and unstaged files with visual indicators
- ✅ **Batch Operations:** Stage and commit multiple files simultaneously with ease
- 🔄 **Seamless Push & Pull:** Reliable operations with detailed output and error handling
- 📌 **Path History:** Save and quickly access frequently used repository paths

### Commit Management
- 🛠 **Advanced Commit Tools:** Edit, delete, or revert commits with built-in safeguards
- 📝 **Message Reuse:** Auto-fill commit messages with your last used message
- 🔍 **Interactive History:** Search, filter, sort, and manage commits in a dynamic table
- 🔐 **Protection:** Pushed commits are automatically protected from accidental deletion

### Interface & Design
- 🎨 **Modernized UI:** Dark-themed interface with comfortable 925x525 window size
- 🖼 **Updated Icons:** Larger, modern icons for better visual clarity
- 📊 **Visual Feedback:** Progress bars and status indicators for all operations
- 🌓 **Eye-Friendly:** Carefully selected colors to reduce eye strain

### Security & Authentication
- 🔐 **Secure Credentials:** Git credentials stored securely via Git's global configuration
- 🔑 **GPG Support:** Optional GPG signing with bypass toggle for flexibility
- 🛡 **Safety First:** Confirmation dialogs for destructive operations

### Additional Tools
- 📜 **Built-In Documentation:** Integrated PDF viewer for quick reference
- 📧 **Direct Support:** Send feedback via integrated Gmail support
- ⚙ **Customizable Settings:** Toggle features like GPG bypass and advanced tools
- 🔬 **Git Clone:** Built-in repository cloning functionality

---

## 🆕 What's New in Version 8.0.1

| Feature | Description |
|---------|-------------|
| 🎨 **Redesigned Interface** | Larger window (925x525), modernized dark theme, rounded corners |
| 🖼 **New Icons** | Contemporary, larger icons throughout the application |
| 📂 **Path History** | Dedicated page for saving and reusing repository paths |
| ⚡ **Performance Boost** | Optimized multi-threaded operations for faster Git commands |
| 📊 **Enhanced Commit History** | Improved search, filter, and sort capabilities |
| 🔄 **Better File Tracking** | More intuitive staged/unstaged file visualization |
| 🛡 **Safety Improvements** | Additional safeguards for commit deletion and editing |

---

## 💻 System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11 (cross-platform support planned) or Linux , MacOs
- **Git Version:** 2.47.1 or higher (required)
- **Memory:** 4GB RAM minimum


---

## 🚀 Installation & Setup

### Step 1: Install Git
Ensure Git is installed on your system. Download from [git-scm.com](https://git-scm.com/downloads)

```bash
# Verify Git installation
git --version
```

### Step 2: Download Drop2Repo
Download the latest release from [GitHub Releases](https://github.com/aarab-abderrahmane/Drop2Repo/releases)

### Step 3: First Launch
1. Launch Drop2Repo
2. Accept the terms of use
3. Enter your GitHub email and username
4. Start managing your repositories!

---

## 📖 User Guide

### 🎯 Getting Started

#### 1. Splash Screen
- Review and accept the terms of use
- Animated presentation with modern typing effect
- First-time setup wizard

#### 2. Registration
- Enter your GitHub email and username
- Credentials are saved securely in Git's global config
- Automatic validation of email format
- One-time setup process

#### 3. Main Interface

**Repository Selection:**
- Click the folder icon to browse for a Git repository
- Use the path history icon to access saved paths
- Manually enter repository paths

**File Management:**
- View all modified files in real-time
- Select files individually or use "Select All"
- Right-click files to copy filename to commit message
- Visual indicators for file status (modified, deleted, untracked)

**Making Commits:**
1. Select files to stage
2. Enter commit message (or reuse last message if enabled)
3. Click "commit" to stage and commit changes
4. Use "Push to GitHub" to upload your changes

### 🔧 Advanced Features

#### Commit History Viewer
- **View All Commits:** See complete commit history with details
- **Search & Filter:** Find specific commits quickly
- **Sort Options:** By date or message length
- **Manage Commits:** Delete unpushed commits or revert to specific versions
- **Safety Features:** Protection for pushed commits

#### Path History
- Save frequently used repository paths
- Quick access via checkbox selection
- Automatic path loading
- No more repetitive navigation

#### Settings Panel
- **Get Last Commit:** Auto-fill commit messages
- **Bypass GPG:** Toggle GPG signing requirement
- **Advanced Tools:** Show/hide commit management buttons
- **Persistent Settings:** All preferences saved between sessions

---

## ⚙️ Configuration Options

### Git Settings
```bash
# View current Git configuration
git config --global user.name
git config --global user.email

# Manually configure Git (optional)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### GPG Signing
Drop2Repo supports GPG commit signing with an easy bypass option:
- Enable in Settings for secure commit verification
- Disable for faster operations without GPG overhead

---

## 🛡️ Security & Privacy

### Data Protection
- ✅ **No Data Collection:** Zero telemetry or analytics
- ✅ **Local Storage Only:** All data stored on your machine
- ✅ **Secure Credentials:** Uses Git's native credential storage
- ✅ **No External Servers:** All operations are local

### Database Storage
Drop2Repo uses SQLite databases for local settings:
- `modifs.db` - Repository paths and preferences
- `app_settings.db` - Application settings and terms acceptance

These databases are stored locally and never transmitted.

---

## ❌ Error Handling

Drop2Repo includes comprehensive error handling:

| Error Type | Handling |
|------------|----------|
| Git Not Installed | Exit with installation prompt |
| Invalid Repository | Warning before operations blocked |
| Empty Commit Message | User notification before commit |
| GPG Signing Errors | Option to bypass with clear notification |
| Push/Pull Failures | Detailed error messages with guidance |
| Protected Commits | Prevention of destructive operations |

---

## 📝 Best Practices

### Recommended Workflow
1. **Regular Commits:** Commit frequently with descriptive messages
2. **Review Changes:** Always review staged files before committing
3. **Pull Before Push:** Check for remote changes before pushing
4. **Descriptive Messages:** Write clear, concise commit messages
5. **Use Path History:** Save commonly used repository paths

### Tips for Success
- 🔄 Use the refresh button to update file status
- 📝 Enable "Get Last Commit" for repetitive commits
- 🔍 Use commit history search to find specific changes
- 💾 Save repository paths for quick access
- ⚡ Leverage batch staging for multiple files

---

## 🔄 Feature Comparison

| Feature | Old Versions 🌱 | Version 8.0.1 💎 |
|---------|-----------------|------------------|
| Basic Git Operations | ✅ (Add, Push) | ✅ (Enhanced Features) |
| Real-Time File Tracking | ❌ | ✅ (Improved Visuals) |
| Batch Staging | ❌ | ✅ (Streamlined UI) |
| Commit History Viewer | ✅ | ✅ (Search, Sort, Revert) |
| Advanced Search & Filter | ❌ | ✅ (Multiple Options) |
| GPG Signing Support | ❌ | ✅ (With Bypass Option) |
| Multi-Repository Support | ❌ | ❌ (Planned) |
| Commit Edit/Delete | ✅ | ✅ (Enhanced Safety) |
| Documentation Viewer | ✅ | ✅ (Integrated PDF) |
| Email Support | ✅ | ✅ (Gmail Integration) |
| Customizable Settings | ✅ | ✅ (More Options) |
| Path History Feature | ❌ | ✅ (New!) |
| Modernized UI Design | ✅ (Basic Dark Theme) | ✅ (Enhanced Aesthetics) |
| Updated Icons | ❌ | ✅ (Larger, Modern) |
| Performance Optimization | ❌ | ✅ (Multi-threaded) |

---

## 🔮 Roadmap

### Planned Features
- 🔄 **Multi-Repository Support:** Manage multiple repositories simultaneously
- 🌿 **Branch Management:** Create, switch, and merge branches interactively
- 🔑 **OAuth & SSH Support:** Additional authentication methods
- 📊 **Performance Dashboard:** Visualize Git operation metrics
- 🌐 **Multi-Language Support:** Interface localization
- 🍎 **macOS Support:** Cross-platform compatibility
- 🐧 **Linux Support:** Full Linux desktop integration
- 📱 **Mobile Companion:** Repository monitoring on mobile devices

---

## 📜 Terms of Use

By using Drop2Repo, you agree to:

- ⚫ **Personal Use Only:** For individual use; commercial use requires explicit permission
- ⚫ **User Responsibility:** You are responsible for all actions performed
- ⚫ **No Data Collection:** Only Git credentials and local settings are stored
- ⚫ **Free Usage:** Free for personal use; premium features may be added
- ⚫ **No Warranty:** Provided "as is" without guarantees
- ⚫ **GitHub Compliance:** Must comply with GitHub's terms of service
- ⚫ **Termination Rights:** Developer may restrict access for misuse

[Full Terms](https://github.com/aarab-abderrahmane/python/releases/tag/6)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
- Use GitHub Issues for bug reports
- Include system information and steps to reproduce
- Attach screenshots when relevant

### Suggesting Features
- Open a feature request on GitHub
- Describe the use case and benefits
- Discuss implementation approaches

### Development
- Fork the repository
- Create a feature branch
- Submit pull requests with clear descriptions

---

## 📧 Support & Contact

### Get Help
- 📖 **Documentation:** Built-in PDF viewer
- 📧 **Email Support:** [abderrahmanerb.contact@gmail.com](mailto:abderrahmanerb.contact@gmail.com)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/aarab-abderrahmane/Drop2Repo/issues)
- 💡 **Feature Requests:** [GitHub Discussions](https://github.com/aarab-abderrahmane/Drop2Repo/discussions)

### Developer
**@aarab-abderrahmane**  
📩 [abderrahmanerb.contact@gmail.com](mailto:abderrahmanerb.contact@gmail.com)  
🌐 [Portfolio](https://abderrahmane-aarab.carrd.co/)

---

## 📦 Download

### Latest Release
<a href="https://github.com/aarab-abderrahmane/Drop2Repo/releases" target="_blank">
  <img src="https://img.shields.io/badge/Download-Latest%20Release-blue?style=for-the-badge&logo=github" alt="Download Latest Release">
</a>

### Version History
- [Version 8.0.1](https://github.com/aarab-abderrahmane/Drop2Repo/releases) - Latest
- [Version 7.1.1](https://github.com/aarab-abderrahmane/Drop2Repo/releases/tag/7.1.1) - Previous
- [All Releases](https://github.com/aarab-abderrahmane/Drop2Repo/releases)

---

## 📄 License

This project is licensed under the MIT License with additional terms - see the [LICENSE.txt](LICENSE.txt) file for details.

**Key Points:**
- ✅ Free for personal use
- ✅ Modification allowed with attribution
- ❌ Commercial use requires written permission

---

## 🙏 Acknowledgments

Built with:
- **Python** - Core programming language
- **CustomTkinter** - Modern UI framework
- **Git** - Version control system
- **SQLite** - Local database storage

Special thanks to the open-source community for their invaluable tools and libraries.

---

## ⭐ Show Your Support

If you find Drop2Repo helpful:
- ⭐ Star this repository
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📢 Share with other developers

---

<div align="center">

**Drop2Repo – Your Ultimate Git Companion!** 🚀

Made with ❤️ by [@aarab-abderrahmane](https://github.com/aarab-abderrahmane)

[Website](https://abderrahmane-aarab.carrd.co/) • [Download](https://github.com/aarab-abderrahmane/Drop2Repo/releases) • [Issues](https://github.com/aarab-abderrahmane/Drop2Repo/issues) • [License](LICENSE.txt)

</div>

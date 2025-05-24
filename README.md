# GitHelper GUI – Version 7x (Ultimate Edition) 🚀  
**A powerful, secure, and user-friendly GUI tool for managing GitHub repositories with advanced features and unparalleled performance!**  

---

📷 **Pictures from inside the app:**  
![Photo Graphy2](https://github.com/user-attachments/assets/5b41ab6e-4a8e-4911-9c95-465d5121e381)



---

# ✅ **GitHelper GUI - Detailed Explanation**  

## 📌 **Overview**  
GitHelper GUI is a modern, secure, and efficient tool designed to simplify Git operations for both beginners and advanced users. With its intuitive interface and powerful features, you can manage your GitHub repositories effortlessly. Version 6.0.0 introduces significant enhancements in usability, performance, and functionality, making it the ultimate Git management companion.

---

## 🚀 **New Features in Version 7x**  
- ⚡ **Blazing Fast Performance:** Optimized Git operations with multi-threading for up to **10x faster** execution.  
- 🎨 **Modern UI Design:** Sleek dark-themed interface with improved responsiveness and accessibility.  
- 📂 **Enhanced Repository Management:** Real-time repository tracking with folder selection via GUI or manual input.  
- 📌 **Real-Time File Tracking:** Automatically detects and displays modified files with live updates.  
- ✨ **Batch Staging & Committing:** Stage and commit multiple files with a single click, including staged file visualization.  
- 🔄 **Optimized Push & Pull Mechanism:** Faster, more reliable Git operations with detailed pull output and error handling.  
- 🔐 **Secure Authentication Handling:** Enhanced Git credential verification and secure storage.  
- 🛠 **Advanced Commit Tools:** Edit or delete the last commit, with safeguards for pushed commits.  
- 📝 **Last Commit Message Reuse:** Option to auto-fill the commit message field with the last used message.  
- 🔍 **Advanced Commit History Viewer:** Search, filter, sort, delete, or revert commits with an interactive table.  
- 📜 **Documentation Viewer:** Built-in PDF viewer for app documentation.  
- 📧 **Integrated Email Support:** Send feedback or inquiries directly from the app via Gmail.  
- ⚙ **Customizable Settings:** Toggle advanced features like GPG bypass and commit deletion tools.  
- 🌐 **Multi-Language Support:** Foundation laid for future multi-language expansion.  

---

## 🛠 **Requirements**  
### 💻 **System Requirements**  
- 🖥 **Operating System:** Windows (with potential cross-platform support in future updates).  
- 🛠 **Git:** Git must be installed on your system (Preferred version: 2.47.1 or higher).  
! Version of the core libraries used in this app (customtkinter : 5.2.2 | Pillow : 10.4.0)
---

## 🛡 **Security Assurance**  
- 🔒 **No Harmful Content:** GitHelper GUI is completely safe, free of malware, viruses, or harmful code.  
- 🔐 **Secure Credential Handling:** Git credentials are stored securely using Git’s global configuration.  
- 🛑 **No Unauthorized Access:** The app only accesses Git repositories and settings with explicit user permission.  
- 📁 **SQLite Security:** User preferences are stored locally in a secure SQLite database.  

---

## 📜 **Terms of Use**  
By using GitHelper GUI, you agree to the following terms:  
- ⚫ **Personal Use Only:** GitHelper GUI is intended for personal use only. Any commercial use, redistribution, or modification of the application without explicit written permission from the developer is strictly prohibited.  
- ⚫ **User Responsibility:** You are solely responsible for all actions performed using this tool, including but not limited to staging, committing, pushing, pulling, and deleting commits from your GitHub repositories. The developer is not liable for any data loss, repository corruption, or unintended consequences resulting from the use of this application.  
- ⚫ **No Data Collection:** GitHelper GUI does not collect, store, or transmit any personal data beyond what is necessary for its operation (e.g., Git credentials and local settings). All data remains stored locally on your device and is not shared with any third parties.  
- ⚫ **Free Usage:** The application is provided free of charge for personal use. Optional premium features may be introduced in future updates, which could involve additional terms or costs.  
- ⚫ **No Warranty:** GitHelper GUI is provided "as is" without any warranties, express or implied. The developer does not guarantee uninterrupted operation, compatibility with all systems, or the absence of errors.  
- ⚫ **Compliance with GitHub Policies:** You agree to use GitHelper GUI in compliance with GitHub’s terms of service and any applicable laws. Any misuse of the tool to violate these policies is your responsibility.  
- ⚫ **Termination:** The developer reserves the right to terminate or restrict access to the application at any time, particularly in cases of misuse or violation of these terms.  

---

## 🖥 **User Interface Walkthrough**  

### 1️⃣ **Splash Screen**  
- 📜 Displays terms of use with an animated typing effect.  
- ✅ Accept terms to proceed; acceptance is saved locally for future sessions.  
- 🔗 Links to detailed terms on GitHub.  

### 2️⃣ **Registration Window**  
- 📝 Prompts for GitHub email and username if not already configured.  
- ✉ Validates email format before saving.  
- 💾 Securely stores credentials using Git’s global config.  
- 🔄 Auto-switches to the main interface if credentials are pre-configured.  

### 3️⃣ **Git Push Interface**  
- 📂 **Repository Selection:** Choose a Git repository via file explorer or manual path entry.  
- 🔍 **Live File Tracking:** Displays staged and unstaged files with real-time updates.  
- ✅ **Batch Operations:** Select multiple files for staging, committing, and pushing.  
- ✍ **Commit Tools:** Edit or delete the last commit, with options to reuse messages.  
- 🚀 **Push to GitHub:** Optimized push with progress bar and error handling.  
- 🔄 **Pull Changes:** Pull from remote with detailed output in a separate window.  
- ⚙ **Settings Access:** Customize GPG signing, commit message reuse, and advanced tools visibility.  
- 📧 **Help Option:** Compose and send emails directly to the developer.  

### 4️⃣ **Commit History Viewer**  
- 📊 **Interactive Table:** View commit hash, author, date, message, and status (pushed/unpushed).  
- 🔍 **Search & Sort:** Filter by text or sort by date/message length.  
- 🛠 **Commit Management:** Double-click to delete unpushed commits; right-click to revert to a commit.  
- ⚠ **Safety Checks:** Prevents deletion of pushed commits.  

### 5️⃣ **Documentation Viewer**  
- 📜 Displays app documentation in a built-in PDF viewer.  
- 🔙 Easy navigation back to the main interface.  

---

## ⚠ **Error Handling**  
- ❌ **Git Not Installed:** Exits with a clear error message prompting Git installation.  
- ❗ **No Repository Selected:** Prompts user to select a valid Git repository.  
- 🚫 **No Commit Message:** Warns if the commit message is empty.  
- 🛑 **Invalid Repository:** Prevents actions on non-Git directories.  
- 🔐 **GPG Errors:** Option to bypass GPG signing with user notification.  
- 🔄 **Pull/Push Failures:** Displays detailed error messages with actionable feedback.  

---

## 📝 **Notes**  
- ✅ Ensure Git is installed and configured correctly before running.  
- 🔐 GPG signing is optional and can be bypassed via settings.  
- 📁 SQLite database (`modifs.db` and `app_settings.db`) stores preferences and settings locally.  
- ⚙ Advanced tools (e.g., commit deletion) are toggleable for a streamlined experience.  

---

## 🔮 **Future Enhancements**  
- 🔄 **Multi-Repository Support:** Manage multiple repositories in one session.  
- 🌿 **Branch Management:** Create, switch, and merge branches interactively.  
- 🔑 **OAuth & SSH Support:** Add alternative authentication methods.  
- 📊 **Performance Dashboard:** Display metrics for Git operations.  
- 🌐 **Full Multi-Language Support:** Expand language options for global accessibility.  

---

# **Comparison Between Old Version  and Version 7x 🚀**  

| Feature                  | Old Version 🌱           | Version 7x 💎        |
|--------------------------|--------------------------|--------------------------|
| Basic Git Operations     | ✅ (Add, Commit, Push)   | ✅ (Enhanced Features)   |
| Real-Time File Tracking  | ✅                       | ✅ (With Staged/Unstaged) |
| Batch Staging            | ✅                       | ✅ (Improved UI)         |
| Commit History Viewer    | ✅                       | ✅ (Search, Sort, Revert)|
| Advanced Search & Filter | ❌                       | ✅ (More Options)        |
| GPG Signing Support      | ❌                       | ✅ (Bypass Option)       |
| Multi-Repository Support | ❌                       | ❌ (Planned)             |
| Commit Edit/Delete       | ❌                       | ✅                       |
| Documentation Viewer     | ❌                       | ✅                       |
| Email Support            | ❌                       | ✅                       |
| Customizable Settings    | ❌                       | ✅                       |

---

## 👤 **Author**  
Developed by **@aarab-abderrahmane**  
📩 **Contact:** [abderrahmanerb.contact@gmail.com](mailto:abderrahmanerb.contact@gmail.com)  

---

📢 **Feedback & Contributions:**  
Feel free to **report issues**, **suggest improvements**, or **contribute** to this project on GitHub! 🎉  

---

**Get the latest version here:**  
<a href="https://github.com/aarab-abderrahmane/GitHelper/releases" target="_blank">Click Here</a>  

---

### **Why Choose GitHelper GUI?**  
- 🚀 **Fast & Efficient:** Multi-threaded operations for maximum speed.  
- 🔒 **Secure & Safe:** No harmful content or unauthorized access.  
- 🎨 **User-Friendly:** Modern UI with intuitive controls and advanced tools.  

---

**GitHelper GUI – Your Ultimate Git Companion!** 🚀  

# 🧠 Volatility 3 Installation (Global Setup - Kali Linux)

## 🎯 Goal

Install **Volatility 3** cleanly and run it globally using:

```bash
vol -f memory.img windows.pslist
```

---

## ⚠️ Common Issues (Avoid These)

- ❌ Installing in `/opt` → permission errors
    
- ❌ Using `sudo pip` → breaks system (PEP 668)
    
- ❌ Mixing root + user installs → causes failures
    

---

## 🥇 Method 1 — Recommended (pipx - Easiest)

### 📦 Install pipx

```bash
sudo apt update
sudo apt install pipx -y
pipx ensurepath
```

Restart terminal OR:

```bash
source ~/.zshrc
```

---

### 📦 Install Volatility 3

```bash
pipx install volatility3
```

---

### ✅ Usage (Global)

```bash
vol -f ram_capture.bin windows.pslist
```

---

### 🧪 Test

```bash
vol --help
```

---

## 🥈 Method 2 — Manual (More Control)

### 📁 Clone Repo

```bash
cd ~
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
```

---

### 🐍 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📦 Install Dependencies

```bash
pip install -e ".[full]"
```

---

## 🌍 Make Global Command (Wrapper)

### Create wrapper script:

```bash
sudo nano /usr/local/bin/vol
```

Paste:

```bash
#!/bin/bash
source ~/volatility3/venv/bin/activate
python3 ~/volatility3/vol.py "$@"
```

---

### Make executable:

```bash
sudo chmod +x /usr/local/bin/vol
```

---

### ✅ Usage

```bash
vol -f ram_capture.bin windows.pslist
```

---

## 🧠 Basic Workflow (CTF)

```bash
vol -f ram_capture.bin windows.info
vol -f ram_capture.bin windows.pslist
vol -f ram_capture.bin windows.cmdline
vol -f ram_capture.bin windows.filescan
```

---

## 📦 Optional: Download Symbols (Important)

```bash
mkdir ~/volatility3/symbols
cd ~/volatility3/symbols

wget https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip
unzip windows.zip
```

---

## 🔥 Pro Tips

- Use `windows.info` first to verify image
- If plugin fails → missing symbols
- Use `--help` to list plugins
- Always keep tool in user directory (`~`)

---

## 💯 Final Recommendation

👉 Use **pipx method** for:

- clean install
- global command
- zero dependency issues

---

## 🚀 Example

```bash
vol -f memory.raw windows.pslist
```

---

## 🏁 Done

You now have a **global, stable Volatility 3 setup** ready for CTF 🔥
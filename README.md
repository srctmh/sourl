<div align="center">

# ◆ SOURL ◆

**.so URL Editor for Android / Termux**

*Replace URLs inside native libraries — fast, safe, professional.*

**by SRCTMH**

</div>

---

## ⚡ One-Line Install

Open **Termux** and run:

```bash
bash <(curl -sL https://raw.githubusercontent.com/SRCTMH/sourl/main/install.sh)
```

After install, just type:

```bash
sourl
```

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | 🔍 Show All URLs | List every URL inside a `.so` file |
| 2 | ✏️ Replace URLs | Change one or many URLs — each with its own new value |
| 3 | ⚡ Auto Patch | Replace every URL with one new URL |
| 4 | 🧠 Encoded Strings | Detect Base64 / Hex strings |
| 5 | 🧬 Decode Base64 | Decode Base64 content inside the file |
| 6 | 🕵️ Deep Scan | Find hidden URLs (even inside Base64) |
| 7 | ⚠️ Smart Scan | Detect tokens, keys, passwords, auth strings |

---

## 📖 Usage

### Step 1 — Run
```bash
sourl
```

### Step 2 — Enter file path
```
📂 Enter full path of .so file
➜ /storage/emulated/0/libdripclient.so
```

### Step 3 — Choose option
For URL replacement → type `2`

### Step 4 — Select URLs
- Single → `2`
- Multiple → `135`
- All → `12345`

### Step 5 — Enter new URL for each
```
[1] OLD : https://oldsite.com/api
    NEW : https://newsite.com
```

### Step 6 — Preview & Save
Tool creates `mod_libdripclient.so` next to the original.

---

## ⚠️ Important Rules

| Rule | Why |
|------|-----|
| New URL must be **shorter or equal** in length | `.so` strings are fixed-length |
| Original file is **never overwritten** | Safe patching — `mod_` copy is made |
| Always keep a **backup** | In case you need the original |

---

## 🔒 Where Files Are Stored

| Item | Location |
|------|----------|
| Python tool | `~/.cache/.sl/.sl.py` (hidden) |
| Command | `$PREFIX/bin/sourl` |
| Alias | `~/.bashrc` |

---

## 🧑‍💻 Author

**SRCTMH**
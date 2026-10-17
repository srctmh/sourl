# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════╗
║                    S O U R L                         ║
║                  .SO URL EDITOR                      ║
║                   by SRCTMH                          ║
║               ENHANCED EDITION  v3.0                 ║
╚══════════════════════════════════════════════════════╝
"""
import os, re, sys, time, base64, shutil, struct
from datetime import datetime

AUTHOR  = "SRCTMH"
VERSION = "3.0"

# ═══════════════════════════════════════════════════════
#   COLORS + UI
# ═══════════════════════════════════════════════════════
class Clr:
    RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"
    RED="\033[91m"; GREEN="\033[92m"; YELLOW="\033[93m"
    BLUE="\033[94m"; MAGENTA="\033[95m"; CYAN="\033[96m"; WHITE="\033[97m"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def line(width=58, char="─", color=Clr.CYAN):
    print(f"{color}{char * width}{Clr.RESET}")

def box_top(w=58, color=Clr.CYAN):   print(f"{color}╭{'─' * (w-2)}╮{Clr.RESET}")
def box_bot(w=58, color=Clr.CYAN):   print(f"{color}╰{'─' * (w-2)}╯{Clr.RESET}")

def box_line(text, w=58, color=Clr.CYAN, txt_color=Clr.WHITE):
    inner = f" {text}"
    pad = max(0, w - 2 - len(inner))
    print(f"{color}│{Clr.RESET}{txt_color}{inner}{' ' * pad}{Clr.RESET}{color}│{Clr.RESET}")

def box_center(text, w=58, color=Clr.CYAN, txt_color=Clr.WHITE):
    pad = max(0, w - 2 - len(text))
    pl = pad // 2; pr = pad - pl
    print(f"{color}│{Clr.RESET}{txt_color}{' '*pl}{text}{' '*pr}{Clr.RESET}{color}│{Clr.RESET}")

def ok(msg):   print(f"  {Clr.GREEN}✔{Clr.RESET}  {msg}")
def err(msg):  print(f"  {Clr.RED}✘{Clr.RESET}  {msg}")
def warn(msg): print(f"  {Clr.YELLOW}⚠{Clr.RESET}  {msg}")
def info(msg): print(f"  {Clr.CYAN}➜{Clr.RESET}  {msg}")

def loader(text="Loading", duration=0.8):
    frames = ["◐","◓","◑","◒"]
    end = time.time() + duration; i = 0
    while time.time() < end:
        sys.stdout.write(f"\r  {Clr.CYAN}{frames[i%4]}{Clr.RESET}  {text}...")
        sys.stdout.flush(); time.sleep(0.08); i += 1
    sys.stdout.write(f"\r  {Clr.GREEN}✔{Clr.RESET}  {text}      \n")

def progress_bar(duration=0.8, width=30, label="Processing"):
    steps = 40
    if duration <= 0:
        duration = 0.01
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * i / steps)
        sys.stdout.write(f"\r  {Clr.CYAN}{label}{Clr.RESET} {Clr.GREEN}{bar}{Clr.RESET} {pct}%")
        sys.stdout.flush(); time.sleep(duration / steps)
    print()

def banner():
    clear()
    print()
    print(f"{Clr.CYAN}{Clr.BOLD}")
    print("    ╔══════════════════════════════════════════════╗")
    print("    ║                                              ║")
    print(f"    ║          {Clr.MAGENTA}◆{Clr.CYAN}  S O U R L  {Clr.MAGENTA}◆{Clr.CYAN}                     ║")
    print(f"    ║           {Clr.WHITE}.SO  URL  EDITOR{Clr.CYAN}                 ║")
    print(f"    ║           {Clr.DIM}Enhanced Edition  v{VERSION}{Clr.CYAN}              ║")
    print("    ║                                              ║")
    print(f"    ║          {Clr.YELLOW}by  {Clr.GREEN}{AUTHOR:<28}{Clr.CYAN}║")
    print("    ║                                              ║")
    print("    ╚══════════════════════════════════════════════╝")
    print(Clr.RESET)

def header(path, size, url_count):
    print()
    box_top(58)
    box_center("📦  FILE INFO", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    line(58, "─", Clr.CYAN)
    box_line(f"File  :  {os.path.basename(path)}", 58)
    box_line(f"Size  :  {size:,} bytes", 58)
    box_line(f"URLs  :  {url_count}", 58)
    box_bot(58)

def menu():
    print()
    print(f"{Clr.CYAN}  ╭────────────────────  MAIN MENU  ────────────────────╮{Clr.RESET}")
    items = [
        (Clr.GREEN,  "1",  "🔍", "Show All URLs"),
        (Clr.GREEN,  "2",  "✏️ ", "Replace URLs  (per-URL)"),
        (Clr.GREEN,  "3",  "⚡", "Auto Patch    (all → 1 URL)"),
        (Clr.MAGENTA,"4",  "📁", "Folder Scan   (all .so)"),
        (Clr.MAGENTA,"5",  "🚀", "Folder Patch  (all .so → 1 URL)"),
        (Clr.GREEN,  "6",  "🧠", "Encoded Strings (B64 / Hex)"),
        (Clr.GREEN,  "7",  "🧬", "Decode Base64"),
        (Clr.GREEN,  "8",  "🕵️ ", "Deep Scan     (hidden URLs)"),
        (Clr.GREEN,  "9",  "⚠️ ", "Smart Scan    (tokens / keys)"),
        (Clr.BLUE,   "10", "🔎", "Keyword Search   [NEW]"),
        (Clr.BLUE,   "11", "🔁", "Keyword Replace  [NEW]"),
        (Clr.BLUE,   "12", "🧩", "Regex Search     [NEW]"),
        (Clr.BLUE,   "13", "🧪", "Regex Replace    [NEW]"),
        (Clr.CYAN,   "14", "📜", "String Viewer    [NEW]"),
        (Clr.CYAN,   "15", "📊", "Statistics       [NEW]"),
        (Clr.CYAN,   "16", "📤", "Export URLs      [NEW]"),
        (Clr.YELLOW, "17", "♻️ ", "Restore Backup   [NEW]"),
        (Clr.YELLOW, "18", "📂", "Change File"),
        (Clr.RED,    "0",  "🚪", "Exit"),
    ]
    for color, num, icon, label in items:
        n = num.rjust(2)
        lbl = label.ljust(40)
        print(f"{Clr.CYAN}  │{Clr.RESET}   {color}[{n}]{Clr.RESET}  {icon}  {lbl}{Clr.CYAN}│{Clr.RESET}")
    print(f"{Clr.CYAN}  ╰──────────────────────────────────────────────────────╯{Clr.RESET}")
    print()

# ═══════════════════════════════════════════════════════
#   REGEX / EXTRACTION
# ═══════════════════════════════════════════════════════
URL_RE = re.compile(rb"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+")
_TRAIL = b".,;:)'\"]}"

def _clean_url(u: bytes) -> bytes:
    return u.rstrip(_TRAIL)

def extract_urls(data: bytes):
    raw = URL_RE.findall(data)
    seen, out = set(), []
    for u in raw:
        u = _clean_url(u)
        if u and u not in seen:
            seen.add(u); out.append(u)
    return out

def extract_strings(data: bytes, min_len=6):
    return re.findall(rb"[ -~]{%d,}" % min_len, data)

def find_so_files(folder, skip_mod=True):
    out = []
    for root, _, files in os.walk(folder):
        for f in files:
            low = f.lower()
            if skip_mod and low.startswith("mod_"):   continue
            if low.endswith(".bak") or low.endswith(".sourl.bak"): continue
            if low.endswith(".so") or ".so." in low:
                out.append(os.path.join(root, f))
    return sorted(out)

def is_elf(data: bytes) -> bool:
    return len(data) >= 4 and data[:4] == b"\x7fELF"

def find_all(data: bytes, pattern: bytes):
    out, start = [], 0
    while True:
        i = data.find(pattern, start)
        if i < 0: break
        out.append(i); start = i + 1
    return out

def parse_elf(data: bytes):
    if not is_elf(data): return None
    info = {}
    ei_class, ei_data = data[4], data[5]
    info["class"]  = {1:"32-bit", 2:"64-bit"}.get(ei_class, "?")
    info["endian"] = {1:"little", 2:"big"}.get(ei_data, "?")
    fmt = "<H" if ei_data == 1 else ">H"
    try:
        e_type = struct.unpack(fmt, data[16:18])[0]
        e_mach = struct.unpack(fmt, data[18:20])[0]
    except struct.error:
        return info
    info["type"]    = {0:"NONE",1:"REL",2:"EXEC",3:"DYN",4:"CORE"}.get(e_type, f"0x{e_type:x}")
    info["machine"] = {3:"x86",8:"MIPS",20:"PowerPC",40:"ARM",62:"x86-64",
                       183:"AArch64",243:"RISC-V"}.get(e_mach, f"0x{e_mach:x}")
    return info

def fmt_ctx(b: bytes) -> str:
    return "".join(chr(c) if 32 <= c < 127 else "." for c in b)

def show_match_context(data, offset, length, ctx=20):
    start = max(0, offset - ctx)
    end   = min(len(data), offset + length + ctx)
    before = data[start:offset]
    match  = data[offset:offset+length]
    after  = data[offset+length:end]
    return (f"...{fmt_ctx(before)} "
            f"{Clr.GREEN}[{fmt_ctx(match)}]{Clr.RESET} "
            f"{fmt_ctx(after)}...")

# ═══════════════════════════════════════════════════════
#   FILE / FOLDER IO
# ═══════════════════════════════════════════════════════
def load_file():
    print()
    print(f"  {Clr.CYAN}╭─────────────────────────────────────────────────────╮{Clr.RESET}")
    print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.WHITE}📂  Enter full path of .so file{Clr.RESET}                     {Clr.CYAN}│{Clr.RESET}")
    print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.DIM}Example: /storage/emulated/0/libdripclient.so{Clr.RESET}  {Clr.CYAN}│{Clr.RESET}")
    print(f"  {Clr.CYAN}╰─────────────────────────────────────────────────────╯{Clr.RESET}")
    path = input(f"  {Clr.GREEN}➜{Clr.RESET}  ").strip().strip('"').strip("'")
    if not path:
        err("Empty path"); return None, None
    if not os.path.exists(path):
        err(f"File not found: {path}"); return None, None
    if not os.path.isfile(path):
        err(f"Not a file: {path}"); return None, None
    try:
        with open(path, "rb") as f:
            data = f.read()
    except Exception as e:
        err(f"Read failed: {e}"); return None, None
    loader("Reading binary", 0.6)
    if is_elf(data):
        ok(f"Loaded ELF  ({len(data):,} bytes)")
    else:
        warn(f"Not an ELF file — proceeding anyway ({len(data):,} bytes)")
    return path, data

def ask_folder():
    print()
    print(f"  {Clr.CYAN}╭─────────────────────────────────────────────────────╮{Clr.RESET}")
    print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.WHITE}📁  Enter folder path (jisme .so files hain){Clr.RESET}        {Clr.CYAN}│{Clr.RESET}")
    print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.DIM}Example: /storage/emulated/0/MyApp/lib/arm64-v8a{Clr.RESET} {Clr.CYAN}│{Clr.RESET}")
    print(f"  {Clr.CYAN}╰─────────────────────────────────────────────────────╯{Clr.RESET}")
    folder = input(f"  {Clr.GREEN}➜{Clr.RESET}  ").strip().strip('"').strip("'")
    if not folder or not os.path.isdir(folder):
        err(f"Invalid folder: {folder}"); return None
    return folder

def save_mod(path, data):
    out = os.path.join(os.path.dirname(path), "mod_" + os.path.basename(path))
    try:
        with open(out, "wb") as f:
            f.write(data)
        print()
        line(58, "═", Clr.GREEN)
        ok(f"Saved  →  {out}")
        info("Original file safe hai, 'mod_' file use karo")
        line(58, "═", Clr.GREEN)
        return True
    except Exception as e:
        err(f"Save failed: {e}")
        return False

def make_backup(path):
    bak = path + ".sourl.bak"
    if os.path.exists(bak): return bak
    try:
        shutil.copy2(path, bak)
        return bak
    except Exception:
        return None

def restore_backup(path):
    bak = path + ".sourl.bak"
    if not os.path.exists(bak):
        err("Backup file nahi mila (missing .sourl.bak)"); return False
    try:
        shutil.copy2(bak, path)
        ok(f"Restored from {bak}")
        return True
    except Exception as e:
        err(f"Restore failed: {e}"); return False

# ═══════════════════════════════════════════════════════
#   INPUT HELPERS
# ═══════════════════════════════════════════════════════
def ask_selection(max_num):
    while True:
        s = input(f"  {Clr.GREEN}➜{Clr.RESET}  ").strip()
        if not s:
            err("Type something (e.g. 1  or  1,3,5  or  1-5)"); continue
        nums = []
        try:
            for part in s.replace(" ", ",").split(","):
                part = part.strip()
                if not part: continue
                if "-" in part:
                    a, b = part.split("-", 1)
                    a, b = int(a), int(b)
                    if a > b: a, b = b, a
                    nums.extend(range(a, b + 1))
                else:
                    nums.append(int(part))
        except ValueError:
            err("Invalid format. Try: 1  |  1,3,5  |  1-5"); continue
        nums = list(dict.fromkeys(nums))
        bad = [n for n in nums if n < 1 or n > max_num]
        if bad:
            err(f"Invalid: {bad}  (1 to {max_num})"); continue
        if not nums:
            err("Kuch select nahi kiya"); continue
        return nums

def ask_new_url(old_bytes, label):
    old_len = len(old_bytes)
    old_str = old_bytes.decode(errors="ignore")
    while True:
        print()
        print(f"  {Clr.CYAN}╭─ [{label}]  OLD URL  ({old_len} chars){Clr.RESET}")
        print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.DIM}{old_str}{Clr.RESET}")
        print(f"  {Clr.CYAN}╰─{Clr.RESET}")
        new = input(f"  {Clr.GREEN}NEW URL ➜{Clr.RESET}  ").strip().strip('"').strip("'")
        if new == "":
            if input(f"  {Clr.YELLOW}Empty = null-out (delete) URL? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                ok("Null-out accepted")
                return b""
            continue
        nb = new.encode()
        if len(nb) > old_len:
            err(f"Too long!  {len(nb)} > {old_len}")
            warn(f"Enter {old_len} chars or less")
            continue
        ok(f"Accepted  ({len(nb)}/{old_len} chars)")
        return nb

def ask_new_keyword(old_bytes, label):
    old_len = len(old_bytes)
    old_str = old_bytes.decode(errors="ignore")
    while True:
        print()
        print(f"  {Clr.CYAN}╭─ [{label}]  OLD KEYWORD  ({old_len} chars){Clr.RESET}")
        print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.DIM}{old_str}{Clr.RESET}")
        print(f"  {Clr.CYAN}╰─{Clr.RESET}")
        new = input(f"  {Clr.GREEN}NEW KEYWORD ➜{Clr.RESET}  ").strip()
        if new == "":
            if input(f"  {Clr.YELLOW}Empty = null-out (delete)? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                return b""
            continue
        nb = new.encode()
        if len(nb) > old_len:
            err(f"Too long!  {len(nb)} > {old_len}")
            warn(f"Enter {old_len} chars or less (null-padded)")
            continue
        ok(f"Accepted  ({len(nb)}/{old_len} chars, null-padded)")
        return nb

# ═══════════════════════════════════════════════════════
#   CORE PATCHERS
# ═══════════════════════════════════════════════════════
def patch_data(data: bytes, urls: list, new_bytes: bytes):
    okc, skipc, skipped = 0, 0, []
    for u in sorted(urls, key=len, reverse=True):
        if len(new_bytes) > len(u):
            skipc += 1; skipped.append(u); continue
        padded = new_bytes + b"\x00" * (len(u) - len(new_bytes))
        if u in data:
            data = data.replace(u, padded); okc += 1
    return data, okc, skipc, skipped

def keyword_replace(data, keyword, replacement, case_sensitive=True):
    if isinstance(keyword, str): keyword = keyword.encode()
    if isinstance(replacement, str): replacement = replacement.encode()
    if len(replacement) > len(keyword):
        return data, 0, "replacement longer than keyword"
    padded = replacement + b"\x00" * (len(keyword) - len(replacement))
    if case_sensitive:
        count = data.count(keyword)
        return data.replace(keyword, padded), count, None
    lower_data = data.lower()
    lower_kw   = keyword.lower()
    result = bytearray(data); count = 0; start = 0
    while True:
        i = lower_data.find(lower_kw, start)
        if i < 0: break
        result[i:i+len(keyword)] = padded
        count += 1; start = i + len(keyword)
    return bytes(result), count, None

def regex_replace(data, pattern, replacement, case_sensitive=True):
    try:
        flags = 0 if case_sensitive else re.IGNORECASE
        rx = re.compile(pattern if isinstance(pattern, bytes) else pattern.encode(), flags)
    except re.error as e:
        return data, 0, f"Regex error: {e}"
    if isinstance(replacement, str): replacement = replacement.encode()
    matches = list(rx.finditer(data))
    if not matches: return data, 0, "no matches"
    result = bytearray(data); applied = 0; skipped = 0
    for m in reversed(matches):
        old_len = m.end() - m.start()
        if len(replacement) > old_len:
            skipped += 1; continue
        padded = replacement + b"\x00" * (old_len - len(replacement))
        result[m.start():m.end()] = padded
        applied += 1
    msg = None if skipped == 0 else f"{skipped} matches skipped (replacement too long)"
    return bytes(result), applied, msg

# ═══════════════════════════════════════════════════════
#   FEATURES — single file
# ═══════════════════════════════════════════════════════
def feat_show(data):
    urls = extract_urls(data)
    if not urls: err("No URLs found"); return
    print()
    box_top(58)
    box_center(f"🌐  {len(urls)} URLs FOUND", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    print()
    for i, u in enumerate(urls, 1):
        print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.WHITE}{u.decode(errors='ignore')}{Clr.RESET}")
    print()

def feat_replace(data):
    urls = extract_urls(data)
    if not urls: err("No URLs found"); return data
    print()
    box_top(58)
    box_center(f"🌐  {len(urls)} URLs FOUND", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    print()
    for i, u in enumerate(urls, 1):
        print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.WHITE}{u.decode(errors='ignore')}{Clr.RESET}")
    print()
    print(f"  {Clr.YELLOW}╭─── SELECT URLs ───────────────────────────────╮{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.WHITE}Single  :  2{Clr.RESET}                              {Clr.YELLOW}│{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.WHITE}Multiple:  1,3,5{Clr.RESET}                          {Clr.YELLOW}│{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.WHITE}Range   :  1-5{Clr.RESET}                            {Clr.YELLOW}│{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.WHITE}All     :  1-{len(urls)}{Clr.RESET}                             {Clr.YELLOW}│{Clr.RESET}")
    print(f"  {Clr.YELLOW}╰───────────────────────────────────────────────╯{Clr.RESET}")
    nums = ask_selection(len(urls))
    repl = {}
    print()
    line(58, "─", Clr.MAGENTA)
    print(f"  {Clr.MAGENTA}{Clr.BOLD}✏️  ENTER NEW URL FOR EACH{Clr.RESET}")
    line(58, "─", Clr.MAGENTA)
    for n in nums:
        repl[n] = ask_new_url(urls[n - 1], n)
    print()
    box_top(58, Clr.GREEN)
    box_center("📋  PREVIEW CHANGES", 58, Clr.GREEN, Clr.GREEN + Clr.BOLD)
    line(58, "─", Clr.GREEN)
    for n in nums:
        old = urls[n-1].decode(errors="ignore")
        new = repl[n].decode(errors="ignore") or "(null-out)"
        print(f"  {Clr.CYAN}[{n}]{Clr.RESET} {Clr.DIM}{old}{Clr.RESET}")
        print(f"       {Clr.GREEN}➜  {new}{Clr.RESET}")
    box_bot(58, Clr.GREEN)
    if input(f"\n  {Clr.YELLOW}Apply changes? (y/n) ➜{Clr.RESET}  ").strip().lower() != "y":
        err("Cancelled"); return data
    progress_bar(0.7, 30, "Patching ")
    for n in sorted(nums, key=lambda x: -len(urls[x-1])):
        old = urls[n - 1]; nb = repl[n]
        padded = nb + b"\x00" * (len(old) - len(nb))
        if old in data:
            data = data.replace(old, padded)
    ok(f"{len(nums)} URL(s) replaced")
    return data

def feat_auto_patch(data):
    urls = extract_urls(data)
    if not urls: err("No URLs found"); return data
    print()
    box_top(58)
    box_center(f"🌐  {len(urls)} URLs — all will change", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    for i, u in enumerate(urls, 1):
        print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.WHITE}{u.decode(errors='ignore')}{Clr.RESET}")
    new = input(f"\n  {Clr.GREEN}NEW URL (same for all) ➜{Clr.RESET}  ").strip().strip('"').strip("'")
    if not new: err("Empty"); return data
    nb = new.encode()
    skipped_preview = [u for u in urls if len(nb) > len(u)]
    if skipped_preview:
        print()
        warn(f"{len(skipped_preview)} URL(s) skip honge (naya URL lamba):")
        for u in skipped_preview:
            print(f"      {Clr.DIM}{u.decode(errors='ignore')}{Clr.RESET}")
    if input(f"\n  {Clr.YELLOW}Confirm patch? (y/n) ➜{Clr.RESET}  ").strip().lower() != "y":
        err("Cancelled"); return data
    data, okc, skipc, _ = patch_data(data, urls, nb)
    progress_bar(0.6, 30, "Patching ")
    ok(f"{okc} replaced   |   {skipc} skipped")
    return data

# ═══════════════════════════════════════════════════════
#   FEATURES — folder
# ═══════════════════════════════════════════════════════
def feat_folder_scan():
    folder = ask_folder()
    if not folder: return
    print(); loader("Scanning folder", 0.6)
    so_files = find_so_files(folder)
    if not so_files:
        warn("Koi .so file nahi mili"); return
    print(); ok(f"{len(so_files)} .so file(s) mili")
    print(); line(58, "─", Clr.MAGENTA)
    total_urls = 0
    report = []
    for idx, fp in enumerate(so_files, 1):
        rel = os.path.relpath(fp, folder)
        try:
            with open(fp, "rb") as fh: data = fh.read()
        except Exception as e:
            print(f"\n  {Clr.CYAN}[{idx}/{len(so_files)}]{Clr.RESET}  {Clr.WHITE}{rel}{Clr.RESET}")
            err(f"Read failed: {e}"); report.append((rel, [])); continue
        urls = extract_urls(data)
        total_urls += len(urls)
        report.append((rel, urls))
        print(f"\n  {Clr.CYAN}[{idx}/{len(so_files)}]{Clr.RESET}  {Clr.WHITE}{rel}{Clr.RESET}")
        if not urls:
            print(f"      {Clr.DIM}no URLs{Clr.RESET}"); continue
        for i, u in enumerate(urls, 1):
            print(f"      {Clr.GREEN}[{i:>2}]{Clr.RESET}  {Clr.WHITE}{u.decode(errors='ignore')}{Clr.RESET}")
    print(); line(58, "═", Clr.GREEN)
    ok(f"Files scanned : {len(so_files)}")
    ok(f"URLs found    : {total_urls}")
    line(58, "═", Clr.GREEN)
    if input(f"\n  {Clr.YELLOW}💾  Save report to .txt? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
        out = os.path.join(folder, "sourl_scan_report.txt")
        try:
            with open(out, "w", encoding="utf-8", newline="") as fh:
                fh.write(f"SOURL FOLDER SCAN — by {AUTHOR}\n")
                fh.write(f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                fh.write(f"Folder : {folder}\nFiles  : {len(so_files)}\n")
                fh.write(f"URLs   : {total_urls}\n")
                fh.write("=" * 60 + "\n\n")
                for rel, urls in report:
                    fh.write(f"[{rel}]\n")
                    for u in urls:
                        fh.write(f"  {u.decode(errors='ignore')}\n")
                    fh.write("\n")
            ok(f"Saved → {out}")
        except Exception as e:
            err(f"Save failed: {e}")

def feat_folder_patch():
    folder = ask_folder()
    if not folder: return
    print(); loader("Scanning folder", 0.6)
    so_files = find_so_files(folder)
    if not so_files:
        warn("Koi .so file nahi mili"); return
    file_urls, total_urls = {}, 0
    for fp in so_files:
        try:
            with open(fp, "rb") as fh: d = fh.read()
            us = extract_urls(d); file_urls[fp] = us; total_urls += len(us)
        except Exception: file_urls[fp] = []
    print(); ok(f"{len(so_files)} .so file(s) mili  |  {total_urls} total URL(s)")
    print(); line(58, "─", Clr.MAGENTA)
    for fp in so_files:
        rel = os.path.relpath(fp, folder); cnt = len(file_urls[fp])
        mark = f"{Clr.GREEN}✔{Clr.RESET}" if cnt else f"{Clr.DIM}·{Clr.RESET}"
        print(f"  {mark}  {Clr.WHITE}{rel:<48}{Clr.RESET}  {Clr.CYAN}{cnt}{Clr.RESET}")
    line(58, "─", Clr.MAGENTA)
    if total_urls == 0:
        err("Kisi bhi file me URL nahi mila"); return
    new = input(f"\n  {Clr.GREEN}NEW URL (same for all) ➜{Clr.RESET}  ").strip().strip('"').strip("'")
    if not new: err("Empty"); return
    nb = new.encode()
    print()
    print(f"  {Clr.YELLOW}╭─── PATCH PREVIEW ──────────────────────────────╮{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  Files to patch : {Clr.WHITE}{sum(1 for v in file_urls.values() if v)}{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  Total URLs     : {Clr.WHITE}{total_urls}{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  New URL        : {Clr.GREEN}{new}{Clr.RESET}")
    print(f"  {Clr.YELLOW}│{Clr.RESET}  Backup         : {Clr.DIM}.sourl.bak (only if changed){Clr.RESET}")
    print(f"  {Clr.YELLOW}╰────────────────────────────────────────────────╯{Clr.RESET}")
    if input(f"\n  {Clr.YELLOW}⚠  Confirm patch? (y/n) ➜{Clr.RESET}  ").strip().lower() != "y":
        err("Cancelled"); return
    print(); progress_bar(1.0, 30, "Patching ")
    grand_ok, grand_skip, files_changed = 0, 0, 0
    for fp in so_files:
        urls = file_urls[fp]
        if not urls: continue
        try:
            with open(fp, "rb") as fh: data = fh.read()
        except Exception: continue
        data2, okc, skipc, _ = patch_data(data, urls, nb)
        if okc == 0:
            grand_skip += skipc
            continue
        make_backup(fp)
        out = os.path.join(os.path.dirname(fp), "mod_" + os.path.basename(fp))
        try:
            with open(out, "wb") as fh: fh.write(data2)
            files_changed += 1; grand_ok += okc; grand_skip += skipc
            print(f"  {Clr.GREEN}✔{Clr.RESET}  {os.path.relpath(fp, folder)}  {Clr.DIM}({okc} URL){Clr.RESET}")
        except Exception as e:
            err(f"Save failed {os.path.basename(fp)}: {e}")
    print(); line(58, "═", Clr.GREEN)
    ok(f"Files patched : {files_changed}")
    ok(f"URLs replaced : {grand_ok}")
    if grand_skip: warn(f"URLs skipped  : {grand_skip}")
    info("Har changed file ke saath .sourl.bak aur mod_ file bani hai")
    line(58, "═", Clr.GREEN)

# ═══════════════════════════════════════════════════════
#   FEATURES — analysis
# ═══════════════════════════════════════════════════════
def feat_encoded(data):
    print(); box_top(58)
    box_center("🧠  ENCODED STRINGS", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    count = 0
    for s in extract_strings(data)[:500]:
        t = s.decode(errors="ignore")
        if re.fullmatch(r"[A-Za-z0-9+/=]{20,}", t):
            print(f"  {Clr.MAGENTA}Base64{Clr.RESET}  {Clr.WHITE}{t[:70]}{Clr.RESET}"); count += 1
        elif re.fullmatch(r"[0-9a-fA-F]{16,}", t):
            print(f"  {Clr.BLUE}Hex   {Clr.RESET}  {Clr.WHITE}{t[:70]}{Clr.RESET}"); count += 1
    if not count: warn("Nothing found")

def feat_decode(data):
    print(); box_top(58)
    box_center("🧬  DECODED BASE64", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    count = 0
    for s in extract_strings(data, min_len=8):
        if len(s) > 3000: continue
        if not re.fullmatch(rb"[A-Za-z0-9+/=]+", s): continue
        try:
            d = base64.b64decode(s, validate=True).decode(errors="ignore")
            if d.strip() and any(c.isprintable() for c in d):
                print(f"  {Clr.GREEN}🔓{Clr.RESET}  {Clr.WHITE}{d[:90]}{Clr.RESET}")
                count += 1
        except Exception:
            pass
    if not count: warn("Nothing decoded")

def feat_deep(data):
    print(); box_top(58)
    box_center("🕵️   DEEP SCAN — HIDDEN URLs", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    found = set()
    for s in extract_strings(data):
        for u in URL_RE.findall(s):
            found.add(_clean_url(u).decode(errors="ignore"))
        try:
            d = base64.b64decode(s, validate=True).decode(errors="ignore")
            for u in re.findall(r"https?://[^\s\"']+", d):
                found.add(u.rstrip(".,;:)'\"]}"))
        except Exception:
            pass
    print(); ok(f"Total: {len(found)}")
    print()
    for i, u in enumerate(sorted(found), 1):
        print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.WHITE}{u}{Clr.RESET}")

def feat_smart(data):
    print(); box_top(58)
    box_center("⚠️   SMART SCAN — TOKENS / KEYS", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    keys = ["token","key","auth","pass","login","secret","bearer","apikey","api_key",
            "aws","AKIA","AIza","sk_live","sk_test","private","credential"]
    hits = 0
    for s in extract_strings(data):
        t = s.decode(errors="ignore"); low = t.lower()
        if any(k in low for k in keys) and len(t) < 200:
            print(f"  {Clr.YELLOW}⚠{Clr.RESET}  {Clr.WHITE}{t[:100]}{Clr.RESET}"); hits += 1
    if not hits: warn("Nothing found")

def feat_keyword_search(data):
    print(); box_top(58)
    box_center("🔎  CUSTOM KEYWORD SEARCH", 58, Clr.BLUE, Clr.BLUE + Clr.BOLD)
    box_bot(58)
    print()
    kw = input(f"  {Clr.GREEN}Keyword ➜{Clr.RESET}  ").strip()
    if not kw:
        err("Empty keyword"); return
    cs = input(f"  {Clr.YELLOW}Case sensitive? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y"
    kw_b = kw.encode()
    if cs:
        offsets = find_all(data, kw_b)
    else:
        offsets = find_all(data.lower(), kw_b.lower())
    if not offsets:
        warn(f"'{kw}' not found"); return
    print(); ok(f"{len(offsets)} match(es) for '{kw}'")
    print()
    show = min(len(offsets), 50)
    for i, off in enumerate(offsets[:show], 1):
        print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.DIM}0x{off:08x}{Clr.RESET}  "
              f"{show_match_context(data, off, len(kw_b))}")
    if len(offsets) > show:
        warn(f"... {len(offsets) - show} more (showing first {show})")

def feat_keyword_replace(data):
    print(); box_top(58)
    box_center("🔁  CUSTOM KEYWORD REPLACE", 58, Clr.BLUE, Clr.BLUE + Clr.BOLD)
    box_bot(58)
    print()
    print(f"  {Clr.CYAN}╭─── MODE ──────────────────────────────────────╮{Clr.RESET}")
    print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.GREEN}[1]{Clr.RESET}  Single keyword replace              {Clr.CYAN}│{Clr.RESET}")
    print(f"  {Clr.CYAN}│{Clr.RESET}  {Clr.GREEN}[2]{Clr.RESET}  Multi-keyword replace (bullet list)  {Clr.CYAN}│{Clr.RESET}")
    print(f"  {Clr.CYAN}╰────────────────────────────────────────────────╯{Clr.RESET}")
    mode = input(f"  {Clr.GREEN}➜{Clr.RESET}  ").strip()
    if mode == "1":
        kw = input(f"  {Clr.GREEN}OLD keyword ➜{Clr.RESET}  ").strip()
        if not kw:
            err("Empty"); return data
        cs = input(f"  {Clr.YELLOW}Case sensitive? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y"
        kw_b = kw.encode()
        if cs:
            occurrences = data.count(kw_b)
        else:
            occurrences = data.lower().count(kw_b.lower())
        if occurrences == 0:
            warn(f"'{kw}' not found"); return data
        ok(f"{occurrences} occurrence(s) found")
        nb = ask_new_keyword(kw_b, "kw")
        print()
        print(f"  {Clr.YELLOW}╭─── PREVIEW ────────────────────────────────────╮{Clr.RESET}")
        print(f"  {Clr.YELLOW}│{Clr.RESET}  Old       : {Clr.DIM}{kw}{Clr.RESET}")
        new_str = nb.decode(errors="ignore") or "(null-out)"
        print(f"  {Clr.YELLOW}│{Clr.RESET}  New       : {Clr.GREEN}{new_str}{Clr.RESET}")
        print(f"  {Clr.YELLOW}│{Clr.RESET}  Count     : {Clr.WHITE}{occurrences}{Clr.RESET}")
        print(f"  {Clr.YELLOW}│{Clr.RESET}  Mode      : null-padded")
        print(f"  {Clr.YELLOW}╰────────────────────────────────────────────────╯{Clr.RESET}")
        if input(f"\n  {Clr.YELLOW}Apply? (y/n) ➜{Clr.RESET}  ").strip().lower() != "y":
            err("Cancelled"); return data
        data2, cnt, errmsg = keyword_replace(data, kw, nb, cs)
        if errmsg:
            err(errmsg); return data
        progress_bar(0.6, 30, "Patching ")
        ok(f"{cnt} occurrence(s) replaced")
        return data2
    elif mode == "2":
        print()
        info("Enter key=value pairs (one per line, blank to finish)")
        info("Format:  old_keyword=new_keyword")
        pairs = []
        while True:
            ln = input(f"  {Clr.GREEN}➜{Clr.RESET}  ").strip()
            if not ln: break
            if "=" not in ln:
                err("Missing '=' — skip"); continue
            old, new = ln.split("=", 1)
            old, new = old.strip(), new.strip()
            if not old:
                err("Empty old — skip"); continue
            if len(new.encode()) > len(old.encode()):
                err(f"'{new}' longer than '{old}' — skip"); continue
            pairs.append((old, new))
        if not pairs:
            warn("Nothing to do"); return data
        print(); ok(f"{len(pairs)} pair(s) queued")
        print()
        for o, n in pairs:
            print(f"  {Clr.CYAN}→{Clr.RESET}  {Clr.DIM}{o}{Clr.RESET}  ➜  {Clr.GREEN}{n or '(null)'}{Clr.RESET}")
        if input(f"\n  {Clr.YELLOW}Apply all? (y/n) ➜{Clr.RESET}  ").strip().lower() != "y":
            err("Cancelled"); return data
        progress_bar(0.6, 30, "Patching ")
        total = 0
        for old, new in pairs:
            data, cnt, errmsg = keyword_replace(data, old, new, True)
            if errmsg:
                err(f"'{old}': {errmsg}"); continue
            if cnt == 0:
                warn(f"'{old}' not found"); continue
            ok(f"'{old}' → {cnt} replaced"); total += cnt
        ok(f"Total: {total} replacement(s)")
        return data
    else:
        err("Invalid"); return data

def feat_regex_search(data):
    print(); box_top(58)
    box_center("🧩  REGEX SEARCH", 58, Clr.BLUE, Clr.BLUE + Clr.BOLD)
    box_bot(58)
    print()
    pat = input(f"  {Clr.GREEN}Regex ➜{Clr.RESET}  ").strip()
    if not pat:
        err("Empty"); return
    target = input(f"  {Clr.YELLOW}Search in:  [s]trings / [r]aw bytes  ➜{Clr.RESET}  ").strip().lower()
    try:
        if target == "r":
            rx = re.compile(pat.encode())
            matches = [(m.start(), m.end() - m.start(), m.group()) for m in rx.finditer(data)]
        else:
            text = data.decode("latin-1")
            rx = re.compile(pat)
            matches = [(m.start(), m.end() - m.start(), m.group().encode("latin-1"))
                       for m in rx.finditer(text)]
    except re.error as e:
        err(f"Regex error: {e}"); return
    if not matches:
        warn("No matches"); return
    print(); ok(f"{len(matches)} match(es)")
    print()
    show = min(len(matches), 50)
    for i, (off, ln, m) in enumerate(matches[:show], 1):
        print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.DIM}0x{off:08x}  len={ln}{Clr.RESET}")
        print(f"       {Clr.GREEN}{m.decode(errors='ignore')[:80]}{Clr.RESET}")
    if len(matches) > show:
        warn(f"... {len(matches) - show} more")

def feat_regex_replace(data):
    print(); box_top(58)
    box_center("🧪  REGEX REPLACE", 58, Clr.BLUE, Clr.BLUE + Clr.BOLD)
    box_bot(58)
    print()
    pat = input(f"  {Clr.GREEN}Regex pattern ➜{Clr.RESET}  ").strip()
    if not pat:
        err("Empty"); return data
    new = input(f"  {Clr.GREEN}Replacement (literal) ➜{Clr.RESET}  ").strip()
    nb = new.encode()
    cs = input(f"  {Clr.YELLOW}Case sensitive? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y"
    try:
        flags = 0 if cs else re.IGNORECASE
        rx = re.compile(pat.encode(), flags)
        matches = list(rx.finditer(data))
    except re.error as e:
        err(f"Regex error: {e}"); return data
    if not matches:
        warn("No matches"); return data
    print(); ok(f"{len(matches)} match(es)")
    print()
    print(f"  {Clr.YELLOW}╭─── PREVIEW (first 10) ─────────────────────────╮{Clr.RESET}")
    for m in matches[:10]:
        old = m.group().decode(errors="ignore")[:40]
        print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.DIM}{old}{Clr.RESET}")
        print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.GREEN}➜  {new or '(null)'}{Clr.RESET}")
    if len(matches) > 10:
        print(f"  {Clr.YELLOW}│{Clr.RESET}  {Clr.DIM}... {len(matches)-10} more{Clr.RESET}")
    print(f"  {Clr.YELLOW}╰────────────────────────────────────────────────╯{Clr.RESET}")
    warn("Matches shorter than replacement will be skipped (null-pad safety)")
    if input(f"\n  {Clr.YELLOW}Apply? (y/n) ➜{Clr.RESET}  ").strip().lower() != "y":
        err("Cancelled"); return data
    data2, cnt, errmsg = regex_replace(data, pat, nb, cs)
    progress_bar(0.6, 30, "Patching ")
    if errmsg: warn(errmsg)
    ok(f"{cnt} match(es) replaced")
    return data2

def feat_string_viewer(data):
    print(); box_top(58)
    box_center("📜  STRING VIEWER (with offsets)", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    print()
    min_len_s = input(f"  {Clr.GREEN}Min length (default 6) ➜{Clr.RESET}  ").strip() or "6"
    try:
        min_len = max(1, int(min_len_s))
    except ValueError:
        err("Invalid number"); return
    strings = []
    for m in re.finditer(rb"[ -~]{%d,}" % min_len, data):
        strings.append((m.start(), m.group()))
    if not strings:
        warn("No strings found"); return
    print(); ok(f"{len(strings)} string(s) (min len {min_len})")
    print()
    page_size = 40
    page = 0
    while True:
        start = page * page_size
        end = min(start + page_size, len(strings))
        print(f"  {Clr.CYAN}── Page {page+1} / {(len(strings)-1)//page_size + 1} "
              f"(showing {start+1}-{end} of {len(strings)}) ──{Clr.RESET}")
        print()
        for i in range(start, end):
            off, s = strings[i]
            disp = s.decode(errors="ignore")
            if len(disp) > 60: disp = disp[:57] + "..."
            print(f"  {Clr.CYAN}[{i+1:>4}]{Clr.RESET}  {Clr.DIM}0x{off:08x}{Clr.RESET}  "
                  f"{Clr.WHITE}{disp}{Clr.RESET}")
        print()
        cmd = input(f"  {Clr.GREEN}[n]ext  [p]rev  [f]ilter  [q]uit ➜{Clr.RESET}  ").strip().lower()
        if cmd == "n":
            if end >= len(strings): warn("Last page"); continue
            page += 1
        elif cmd == "p":
            if page == 0: warn("First page"); continue
            page -= 1
        elif cmd == "f":
            sub = input(f"  {Clr.GREEN}Substring filter ➜{Clr.RESET}  ").strip().lower()
            if sub:
                strings = [(o, s) for o, s in strings if sub in s.decode(errors="ignore").lower()]
                page = 0
                ok(f"{len(strings)} string(s) match '{sub}'")
                if not strings: return
        elif cmd == "q":
            return

def feat_statistics(data):
    print(); box_top(58)
    box_center("📊  STATISTICS", 58, Clr.CYAN, Clr.CYAN + Clr.BOLD)
    box_bot(58)
    print()
    # ELF
    elf = parse_elf(data)
    if elf:
        ok(f"ELF        : {elf.get('class')} / {elf.get('endian')} endian")
        ok(f"Type       : {elf.get('type')}")
        ok(f"Machine    : {elf.get('machine')}")
    else:
        warn("Not a valid ELF file")
    print()
    # URLs
    urls = extract_urls(data)
    domains = set()
    for u in urls:
        try:
            from urllib.parse import urlparse
            d = urlparse(u.decode(errors="ignore")).netloc
            if d: domains.add(d)
        except Exception:
            pass
    ok(f"URLs       : {len(urls)}")
    ok(f"Domains    : {len(domains)}")
    # Strings
    strs = extract_strings(data, min_len=4)
    ok(f"Strings    : {len(strs)}")
    if strs:
        longest = max(strs, key=len)
        ok(f"Longest str: {len(longest)} bytes")
        print(f"              {Clr.DIM}{longest[:80].decode(errors='ignore')}{Clr.RESET}")
    # Encoded
    b64c = sum(1 for s in strs if re.fullmatch(rb"[A-Za-z0-9+/=]{20,}", s))
    hexc = sum(1 for s in strs if re.fullmatch(rb"[0-9a-fA-F]{16,}", s))
    ok(f"Base64-like: {b64c}")
    ok(f"Hex-like   : {hexc}")
    if domains:
        print(); line(58, "─", Clr.MAGENTA)
        print(f"  {Clr.MAGENTA}{Clr.BOLD}DOMAINS ({len(domains)}):{Clr.RESET}")
        for i, d in enumerate(sorted(domains), 1):
            print(f"  {Clr.CYAN}[{i:>2}]{Clr.RESET}  {Clr.WHITE}{d}{Clr.RESET}")
    line(58, "─", Clr.MAGENTA)

def feat_export(data, path):
    urls = extract_urls(data)
    if not urls:
        warn("No URLs to export"); return
    print()
    out = os.path.join(os.path.dirname(path), "sourl_urls.txt")
    try:
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write(f"SOURL URL EXPORT — by {AUTHOR}\n")
            f.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"File : {os.path.basename(path)}\n")
            f.write(f"Total: {len(urls)}\n")
            f.write("=" * 60 + "\n\n")
            for i, u in enumerate(urls, 1):
                f.write(f"[{i:>3}]  {u.decode(errors='ignore')}\n")
        ok(f"Exported {len(urls)} URL(s) → {out}")
    except Exception as e:
        err(f"Export failed: {e}")

# ═══════════════════════════════════════════════════════
#   MAIN
# ═══════════════════════════════════════════════════════
def main():
    banner()
    print(f"  {Clr.DIM}Initializing secure environment...{Clr.RESET}")
    time.sleep(0.3)
    path, data = load_file()
    if not path: return

    while True:
        banner()
        urls = extract_urls(data)
        header(path, os.path.getsize(path), len(urls))
        menu()
        ch = input(f"  {Clr.GREEN}😈 ➜{Clr.RESET}  ").strip()

        if ch == "1":
            feat_show(data)
        elif ch == "2":
            new_data = feat_replace(data)
            if new_data != data:
                data = new_data
                if input(f"\n  {Clr.YELLOW}💾  Save file? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                    make_backup(path); save_mod(path, data)
        elif ch == "3":
            new_data = feat_auto_patch(data)
            if new_data != data:
                data = new_data
                if input(f"\n  {Clr.YELLOW}💾  Save file? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                    make_backup(path); save_mod(path, data)
        elif ch == "4":
            feat_folder_scan()
        elif ch == "5":
            feat_folder_patch()
        elif ch == "6":
            feat_encoded(data)
        elif ch == "7":
            feat_decode(data)
        elif ch == "8":
            feat_deep(data)
        elif ch == "9":
            feat_smart(data)
        elif ch == "10":
            feat_keyword_search(data)
        elif ch == "11":
            new_data = feat_keyword_replace(data)
            if new_data != data:
                data = new_data
                if input(f"\n  {Clr.YELLOW}💾  Save file? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                    make_backup(path); save_mod(path, data)
        elif ch == "12":
            feat_regex_search(data)
        elif ch == "13":
            new_data = feat_regex_replace(data)
            if new_data != data:
                data = new_data
                if input(f"\n  {Clr.YELLOW}💾  Save file? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                    make_backup(path); save_mod(path, data)
        elif ch == "14":
            feat_string_viewer(data)
        elif ch == "15":
            feat_statistics(data)
        elif ch == "16":
            feat_export(data, path)
        elif ch == "17":
            if input(f"\n  {Clr.YELLOW}♻️  Restore {os.path.basename(path)} from backup? (y/n) ➜{Clr.RESET}  ").strip().lower() == "y":
                if restore_backup(path):
                    try:
                        with open(path, "rb") as f: data = f.read()
                        ok(f"Reloaded  ({len(data):,} bytes)")
                    except Exception as e:
                        err(f"Reload failed: {e}")
        elif ch == "18":
            path, data = load_file()
            if not path: return
            continue
        elif ch == "0":
            print()
            line(58, "═", Clr.MAGENTA)
            print(f"  {Clr.MAGENTA}{Clr.BOLD}👋  Thanks for using SOURL  —  by {AUTHOR}{Clr.RESET}")
            line(58, "═", Clr.MAGENTA)
            print()
            return
        else:
            err("Invalid option")
        input(f"\n  {Clr.DIM}Press Enter to continue...{Clr.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Clr.YELLOW}⚠  Interrupted. Bye!{Clr.RESET}\n")
        sys.exit(0)
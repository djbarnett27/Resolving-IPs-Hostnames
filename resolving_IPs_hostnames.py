# resolving_IPs-hostnames.py

''' 
This program will resolve one, or several, IP addresses to their respective hostnames, or resolve hostnames into to their respective IP addresses.

'''

import socket
from pathlib import Path
from typing import List

def read_multiline_input(prompt: str = "Paste IPs/hostnames (one per line). End with an empty line:\n") -> List[str]:  
    print(prompt)
    lines = []
    try:
        while True:
            line = input().strip()
            if line == "":
                break
            lines.append(line)
    except KeyboardInterrupt:
        print("\nInterrupted, saving what was entered so far.")
    # clean duplicates and blanks, preserve order
    seen = set()
    cleaned = []
    for l in lines:
        if not l or l in seen:
            continue
        seen.add(l)
        cleaned.append(l)
    return cleaned

def save_entries(entries: List[str], filename: str = "temp_file") -> Path:
    script_dir = Path(__file__).resolve().parent
    out_path = script_dir / filename
    out_path.write_text("\n".join(entries) + ("\n" if entries else ""), encoding="utf-8")
    return out_path

def resolve_ip_to_name(ip: str) -> str:
    try:
        name = socket.gethostbyaddr(ip)[0]
        return name
    except (socket.herror, socket.gaierror):
        return "<no PTR / reverse DNS>"

def resolve_name_to_ips(name: str) -> List[str]:
    try:
        # gethostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        ips = socket.gethostbyname_ex(name)[2]
        return ips if ips else ["<no A/AAAA records>"]
    except socket.gaierror:
        return ["<resolution failed>"]

def run_reverse(entries: List[str]) -> None:
    print("\nReverse lookup (IP -> hostname):")
    for e in entries:
        result = resolve_ip_to_name(e)
        print(f"{e:40s} -> {result}")

def run_forward(entries: List[str]) -> None:
    print("\nForward lookup (hostname -> IPs):")
    for e in entries:
        ips = resolve_name_to_ips(e)
        print(f"{e:40s} -> {', '.join(ips)}")

def main():
    entries = read_multiline_input()
    if not entries:
        print("No entries provided. Exiting.")
        return
    out_path = save_entries(entries, filename="temp_file")
    print(f"\nSaved {len(entries)} entries to: {out_path}")

    # choose action
    print("\nChoose an action:")
    print("  1) Resolve IP addresses to hostnames (reverse DNS)")
    print("  2) Resolve hostnames to IP addresses (forward DNS)")
    print("  3) Run both")
    print("  4) Exit")
    choice = input("Enter 1, 2, 3 or 4: ").strip()
    if choice == "1":
        run_reverse(entries)
    elif choice == "2":
        run_forward(entries)
    elif choice == "3":
        run_reverse(entries)
        run_forward(entries)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()

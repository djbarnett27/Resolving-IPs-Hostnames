# resolving_IPs-hostnames.py

''' 
This program will resolve IP addresses to their respective hostnames, 
or resolve hostnames into to their respective IP addresses.

'''

import socket
import ipaddress
from pathlib import Path
from typing import List

class HostIdentifiers:
    def __init__(self, host_ids: List[str]):
        self.host_ids = host_ids

    def save(self, filename: str = "temp_file") -> Path:
        script_dir = Path(__file__).resolve().parent
        out_path = script_dir / filename
        out_path.write_text("\n".join(self.host_ids) + ("\n" if self.host_ids else ""), encoding="utf-8")
        return out_path

    def run_reverse(self) -> None:
        print("\nReverse lookup (IP -> hostname):")
        for host_id in self.host_ids:
            result = resolve_ip_to_name(host_id)
            print(f"{host_id:40s} -> {result}")

    def run_forward(self) -> None:
        print("\nForward lookup (hostname -> IPs):")
        for host_id in self.host_ids:
            ips = resolve_name_to_ips(host_id)
            print(f"{host_id:40s} -> {', '.join(ips)}")

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
    for entry in lines:
        if not entry or entry in seen:
            continue
        seen.add(entry)
        cleaned.append(entry)
    return cleaned

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

def main():
    while True:
        host_ids = read_multiline_input()
        if not host_ids:
            print("No host_ids provided.")
        else:
            out_path = HostIdentifiers(host_ids).save(filename="temp_file")
            print(f"\nSaved {len(host_ids)} host_ids to: {out_path}\n")
            print("Resolving input items:")
            for host_id in host_ids:
                # determine whether the input is an IP address or a hostname
                try:
                    ipaddress.ip_address(host_id)
                    # it's an IP -> reverse lookup
                    result = resolve_ip_to_name(host_id)
                    print(f"{host_id:40s} -> {result}")
                except ValueError:
                    # not an IP -> forward lookup
                    ips = resolve_name_to_ips(host_id)
                    print(f"{host_id:40s} -> {', '.join(ips)}")

        cont = input("\nDo you want to continue? (y/N): ").strip().lower()
        if cont not in ("y", "yes"):
            print("Exiting.")
            break

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# pstree_to_dot.py — Volatility3 pstree JSON → Graphviz DOT
# Usage: vol -f memdump.mem -r json windows.pstree | python3 pstree_to_dot.py
#    or: python3 pstree_to_dot.py -i pstree.json -o pstree.dot

import json
import sys
import argparse
from pathlib import Path

# ── Suspicious process rules ──────────────────────────────────────────────────

SUSPICIOUS_NAMES = [
    "cmd.exe", "powershell.exe", "pwsh.exe",
    "wscript.exe", "cscript.exe", "mshta.exe",
    "rundll32.exe", "regsvr32.exe", "certutil.exe",
]

CRITICAL_NAMES = [
    "lazagne", "mimikatz", "procdump", "pwdump",
    "wce.exe", "gsecdump", "fgdump",
]

# svchost/lsass must come from these parents
LEGIT_PARENTS = {
    "svchost.exe": [612],
    "lsass.exe":   [524],
    "lsm.exe":     [524],
}

# ── Color scheme ──────────────────────────────────────────────────────────────

COLORS = {
    "critical":   "#ffcccc",   # red   — known malicious tool
    "suspicious": "#fff3cc",   # amber — suspicious process
    "anomaly":    "#ffd9ee",   # pink  — wrong parent
    "normal":     "#f9f9f9",   # light gray — clean
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def classify(name: str, ppid: int) -> str:
    n = name.lower()
    if any(c in n for c in CRITICAL_NAMES):
        return "critical"
    if n in LEGIT_PARENTS and ppid not in LEGIT_PARENTS[n]:
        return "anomaly"
    if n in SUSPICIOUS_NAMES:
        return "suspicious"
    return "normal"


def walk(node: dict, f):
    pid   = node["PID"]
    ppid  = node["PPID"]
    name  = node["ImageFileName"]
    thds  = node.get("Threads", "?")
    time  = str(node.get("CreateTime", "")).split(".")[0]

    status = classify(name, ppid)
    color  = COLORS[status]
    border = "2" if status != "normal" else "1"
    label  = f"{name}\\nPID: {pid}  |  Threads: {thds}\\n{time}"

    f.write(f'  {pid} [label="{label}" fillcolor="{color}" penwidth={border}]\n')

    if ppid:
        f.write(f'  {ppid} -> {pid}\n')

    for child in node.get("__children", []):
        walk(child, f)


def export_dot(data: list, output_path: str):
    total = 0

    with open(output_path, "w") as f:
        f.write("digraph pstree {\n")
        f.write('  graph [rankdir=TB splines=ortho fontname=monospace]\n')
        f.write('  node  [shape=box fontname=monospace fontsize=10 style=filled]\n')
        f.write('  edge  [color="#aaaaaa"]\n\n')

        # Legend
        f.write('  subgraph cluster_legend {\n')
        f.write('    label="Legend" fontname=monospace fontsize=10\n')
        f.write('    style=dashed color="#cccccc"\n')
        f.write(f'    L1 [label="Critical IOC"   fillcolor="{COLORS["critical"]}"   shape=box style=filled fontsize=9]\n')
        f.write(f'    L2 [label="Suspicious"     fillcolor="{COLORS["suspicious"]}" shape=box style=filled fontsize=9]\n')
        f.write(f'    L3 [label="Anomalous parent" fillcolor="{COLORS["anomaly"]}"  shape=box style=filled fontsize=9]\n')
        f.write(f'    L4 [label="Normal"         fillcolor="{COLORS["normal"]}"     shape=box style=filled fontsize=9]\n')
        f.write('  }\n\n')

        for root in data:
            walk(root, f)
            total += 1

        f.write("}\n")

    return total


def count_all(data: list) -> int:
    total = 0
    for node in data:
        total += 1
        total += count_all(node.get("__children", []))
    return total


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert Volatility3 pstree JSON to Graphviz DOT"
    )
    parser.add_argument("-i", "--input",  default=None,            help="Input JSON file (default: stdin)")
    parser.add_argument("-o", "--output", default="/tmp/pstree.dot", help="Output DOT file")
    args = parser.parse_args()

    # Load JSON
    if args.input:
        with open(args.input) as f:
            data = json.load(f)
    else:
        print("[*] Reading from stdin...", file=sys.stderr)
        data = json.load(sys.stdin)

    total = count_all(data)
    print(f"[+] Loaded {total} processes")

    # Export
    export_dot(data, args.output)
    print(f"[+] DOT saved → {args.output}")
    print(f"[+] Render:  dot -Tsvg {args.output} -o pstree.svg")
    print(f"[+] Preview: xdot {args.output}")


if __name__ == "__main__":
    main()

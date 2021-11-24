from archpy import Cmd, Message
from re import sub
from pathlib import Path


class SystemInfo:
    def __init__(self):
        self.sysinfo = {
            'cpu_vendor': None,
            'gfx_cards': {},
            'total_ram': None,
            'storage_devices': [],
            'firmware_interface': None
        }

        if "intel" in Cmd('cat /proc/cpuinfo').stdout.lower():
            self.sysinfo['cpu_vendor'] = 'intel'
        elif "amd" in Cmd('cat /proc/cpuinfo').stdout.lower():
            self.sysinfo['cpu_vendor'] = 'amd'
        else:
            Message('red_alert').print("Couldn't fetch CPU info.")
            exit()
        for line in Cmd('lspci').stdout.split('\n'):
            if ' VGA ' in line or ' 3D ' in line:
                _, identifier = line.split(': ', 1)
                self.sysinfo['gfx_cards'][identifier.strip()] = line
        self.sysinfo['total_ram'] = int(Cmd("grep MemTotal /proc/meminfo", "awk '{print $2}'").stdout)
        self.sysinfo['storage_devices'] = [device for device in
                                           sub(r'[0-9]+', '', Cmd('lsblk -dp', 'grep -o "^/dev[^ ]*"').stdout).split(
                                               '\n') if device not in ['/dev/loop', '/dev/sr']]
        if Path('/sys/firmware/efi').exists():
            self.sysinfo['firmware_interface'] = 'UEFI'
        else:
            self.sysinfo['firmware_interface'] = 'BIOS'

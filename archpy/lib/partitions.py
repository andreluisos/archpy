from math import ceil

from archpy import Cmd, SystemInfo, Message


class Partition:
    def __init__(self, config, diskpw=None):
        self.config = config
        self.diskpw = diskpw

    def layout1(self, filesystem='BTRFS', swap_partition=False):
        # This layout uses 2 or 3 partitions: EFI; SWAP, if enabled (same size as RAM, for hibernation);
        # and SYSTEM, on the top of LUKS dm-crypt or not, holding root and home data, formatted as BTRFS and
        # Using subvolumes to manage snapshots of the current root and home contents.

        if self.config['raid'] and filesystem == 'BTRFS':
            Cmd(f'mkfs.btrfs -L raid -d {self.config["raid"]} -m {self.config["raid"]} -f '
                f'{" ".join(self.config["storage_devices"])}')

        Cmd(f'sgdisk '
            f'--clear '
            f'--new=1:0:+550MiB '
            f'--typecode=1:ef00 '
            f'--change-name=1:EFI {self.config["storage_devices"][0]}',
            msg=Message.message('install_40', self.config['language']))

        # Formating EFI.
        Cmd('mkfs.fat -F32 -n EFI /dev/disk/by-partlabel/EFI',
            msg=Message.message('install_21', self.config['language'], 'system', 'FAT32'))

        # Partitioning.
        if swap_partition:
            Cmd(f'sgdisk '
                f'--new=2:0:+{ceil(SystemInfo().sysinfo["total_ram"] * 1000 / 1024 ** 3)}GiB '
                f'--typecode=2:8200 '
                f'--change-name=2:swap '
                f'--new=3:0:0 '
                f'--typecode=3:8300 '
                f'--change-name=3:system {self.config["storage_devices"][0]}',
                msg=Message.message('install_16', self.config['language']))
        else:
            Cmd(f'sgdisk '
                f'--new=2:0:0 '
                f'--typecode=2:8300 '
                f'--change-name=2:system {self.config["storage_devices"][0]}',
                msg=Message.message('install_16', self.config['language']))

        # Handles the disk encryption.
        if self.config['disk_encryption']:
            Cmd(f'cryptsetup luksFormat --batch-mode --align-payload=8192 -s 256 -c aes-xts-plain64 '
                f'/dev/disk/by-partlabel/system --key-file {str(self.diskpw)}',
                msg=Message.message('install_17', self.config['language'], '/dev/disk/by-partlabel/system'))
            Cmd(f'cryptsetup open --key-file {str(self.diskpw)} /dev/disk/by-partlabel/system system',
                msg=Message.message('install_18', self.config['language'], '/dev/disk/by-partlabel/system'))
            if swap_partition:
                Cmd(f'cryptsetup open --type plain --key-file /dev/urandom /dev/disk/by-partlabel/swap swap',
                    msg=Message.message('install_18', self.config['language'], '/dev/disk/by-partlabel/swap'))

        # Setting up the swap partition.
        if swap_partition:
            if self.config['disk_encryption']:
                Cmd(f'mkswap -L swap /dev/mapper/swap', msg=Message.message('install_19', self.config['language']))
            else:
                Cmd(f'mkswap -L swap /dev/disk/by-partlabel/swap',
                    msg=Message.message('install_19', self.config['language']))
            Cmd(f'swapon -L swap',
                msg=Message.message('install_20', self.config['language']))

        # Handles BTRFS partitioning and subvolumes.
        # ADD RAID SUPPORT
        if filesystem == 'BTRFS':
            if self.config['disk_encryption']:
                Cmd(f'mkfs.btrfs --force --label system /dev/mapper/system',
                    msg=Message.message('install_21', self.config['language'], 'system', 'BTRFS'))
            else:
                Cmd(f'mkfs.btrfs --force --label system /dev/disk/by-partlabel/system',
                    msg=Message.message('install_21', self.config['language'], 'system', 'BTRFS'))
            Cmd(f'mount -t btrfs LABEL=system /mnt',
                msg=Message.message('install_22', self.config['language'], 'system', '/mnt'))
            Cmd(f'btrfs subvolume create /mnt/root',
                msg=Message.message('install_23', self.config['language'], '/mnt/root'))
            Cmd(f'btrfs subvolume create /mnt/home',
                msg=Message.message('install_23', self.config['language'], '/mnt/home'))
            Cmd(f'btrfs subvolume create /mnt/snapshots',
                msg=Message.message('install_23', self.config['language'], '/mnt/snapshots'))
            Cmd(f'umount -R /mnt',
                msg=Message.message('install_24', self.config['language']))
            mountpoint = None
            for subvolume in ['root', 'home', 'snapshots']:
                if subvolume == 'root':
                    mountpoint = '/mnt'
                if subvolume == 'home':
                    mountpoint = '/mnt/home'
                if subvolume == 'snapshots':
                    mountpoint = '/mnt/.snapshots'
                Cmd(f'mount -t btrfs -o subvol={subvolume},defaults,x-mount.mkdir,compress=lzo,ssd,noatime'
                    f' LABEL=system {mountpoint}',
                    msg=Message.message('install_22', self.config['language'], subvolume, mountpoint))

        # Removes the diskpw file.
        if self.config['disk_encryption']:
            Cmd(f'rm {str(self.diskpw)}', quiet=True)

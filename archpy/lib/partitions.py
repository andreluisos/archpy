from math import ceil

from archpy import Cmd, SystemInfo, Message


class Partition:
    def __init__(self, config, diskpw=None):
        self.config = config
        self.diskpw = diskpw
        self.sysinfo = SystemInfo().sysinfo

    def mklabel(self, device: str, label: str):
        Cmd(f'parted -s {device} -s mklabel {label}',
            msg=Message.message('91', self.config['language'], label, device))

    def mkpart(self, device: str, pformat: str, start_size: str, end_size: str, align='optimal'):
        Cmd(f'parted -s {device} -s -a {align} mkpart primary {pformat} {start_size} {end_size}',
            msg=Message.message('92', self.config['language'], pformat, device))

    def set_boot(self, device: str, part: int):
        Cmd(f'parted -s {device} -s set {part} {"boot" if self.sysinfo["firmware_interface"] == "BIOS" else "esp"} on',
            msg=Message.message('93', self.config['language'], f'{device}{part}'))

    def wipe(self):
        # Erases everything in the disk to prevent partitioning errors.
        # NEEDS TO DO IT BETTER.
        Cmd('swapoff -a', quiet=True)
        Cmd('umount -l /mnt', quiet=True)
        Cmd('umount -l /mnt/boot', quiet=True)
        Cmd('cryptsetup close --batch-mode swap', quiet=True)
        Cmd('cryptsetup close --batch-mode system', quiet=True)
        Cmd('cryptsetup luksErase --batch-mode /dev/disk/by-partlabel/system', quiet=True)
        for device in self.config['storage_devices']:
            Cmd(f'sgdisk --zap-all {device}', msg=Message.message('46', self.config['language'], device))

    def layout1(self, filesystem='BTRFS', swap_partition=False):
        self.wipe()
        system_partitions = []
        for index, device in enumerate(self.config["storage_devices"]):
            # Creates the device's partition table.
            self.mklabel(device, 'msdos' if self.sysinfo['firmware_interface'] == 'BIOS' else 'gpt')
            if index == 0:
                # Creates the boot partition.
                self.mkpart(
                    device,
                    'fat32',
                    '1MiB',
                    '550MiB'
                )
                Cmd(f'mkfs.fat -F32 -n EFI {device}1',
                    msg=Message.message('52', self.config['language'], 'EFI', 'FAT32'))
                self.set_boot(device, 1)
                self.mkpart(
                    device,
                    filesystem.lower(),
                    '551MiB',
                    '100%'
                )
                system_partitions.append(f'{device}2')
            else:
                self.mkpart(
                    device,
                    filesystem.lower(),
                    '1MiB',
                    '100%'
                )
                system_partitions.append(f'{device}1')

        print(system_partitions)
        exit()

        if filesystem == 'BTRFS':
            if self.config['disk_encryption']:
                Cmd(f'mkfs.btrfs --force --label system{index} {device}2',
                    msg=Message.message('87', self.config['language'], device, 'BTRFS'))
            else:
                Cmd(f'mkfs.btrfs --force --label system{index} {device}2',
                    msg=Message.message('87', self.config['language'], device, 'BTRFS'))
        system_partitions.append(f'{device}2')

        if self.config['raid'] and filesystem == 'BTRFS':
            Cmd(f'mkfs.btrfs -L {self.config["hostname"]} -d {self.config["raid"]} -m {self.config["raid"]} -f '
                f'{" ".join(system_partitions)}',
                msg=Message.message('83', self.config['language'], " ".join(self.config["storage_devices"])))


        # Handles the disk encryption.
        # for partition in self.system_partitions:
        #
        #     Cmd(f'cryptsetup luksFormat --batch-mode --align-payload=8192 -s 256 -c aes-xts-plain64 '
        #         f'/dev/disk/by-partlabel/system0 --key-file {str(self.diskpw)}',
        #         msg=Message.message('48', self.config['language'], '/dev/disk/by-partlabel/system0'))
        #     Cmd(f'cryptsetup open --key-file {str(self.diskpw)} /dev/disk/by-partlabel/system0 system0',
        #         msg=Message.message('49', self.config['language'], '/dev/disk/by-partlabel/system0'))

        # Handles BTRFS partitioning and subvolumes.
        # if filesystem == 'BTRFS':
        #     Cmd(f'mount -t btrfs {system_partitions[0]} /mnt',
        #         msg=Message.message('86', self.config['language'], '/mnt'))
        #     Cmd(f'btrfs subvolume create /mnt/root',
        #         msg=Message.message('54', self.config['language'], '/mnt/root'))
        #     Cmd(f'btrfs subvolume create /mnt/home',
        #         msg=Message.message('54', self.config['language'], '/mnt/home'))
        #     Cmd(f'btrfs subvolume create /mnt/snapshots',
        #         msg=Message.message('54', self.config['language'], '/mnt/snapshots'))
        #     Cmd(f'umount -R /mnt',
        #         msg=Message.message('55', self.config['language']))
        #     mountpoint = None
        #     for subvolume in ['root', 'home', 'snapshots']:
        #         if subvolume == 'root':
        #             mountpoint = '/mnt'
        #         if subvolume == 'home':
        #             mountpoint = '/mnt/home'
        #         if subvolume == 'snapshots':
        #             mountpoint = '/mnt/.snapshots'
        #         Cmd(f'mount -t btrfs -o subvol={subvolume},defaults,x-mount.mkdir,compress=lzo,ssd,noatime '
        #             f'{system_partitions[0]} {mountpoint}',
        #             msg=Message.message('53', self.config['language'], subvolume, mountpoint))
        #
        # # Removes the diskpw file.
        # if self.config['disk_encryption']:
        #     Cmd(f'rm {str(self.diskpw)}', quiet=True)

    def layout2(self, filesystem='BTRFS', swap_partition=False):
        # This layout uses 2 or 3 partitions: EFI; SWAP, if enabled (same size as RAM, for hibernation);
        # and SYSTEM, on the top of LUKS dm-crypt or not, holding root and home data, formatted as BTRFS and
        # Using subvolumes to manage snapshots of the current root and home contents.

        self.wipe()

        # Partitioning.
        system_partitions = []
        for index, device in enumerate(self.config["storage_devices"]):
            if index == 0:
                # Create and format EFI partition.

                Cmd(f'sgdisk '
                    f'--clear '
                    f'--new=1:0:+550MiB '
                    f'--typecode=1:ef00 '
                    f'--change-name=1:EFI {device}',
                    msg=Message.message('71', self.config['language'], device))
                Cmd('mkfs.fat -F32 -n EFI /dev/disk/by-partlabel/EFI',
                    msg=Message.message('52', self.config['language'], 'EFI', 'FAT32'))
                if swap_partition:
                    # Create swap and setup partition.
                    Cmd(f'sgdisk '
                        f'--new=2:0:+{ceil(SystemInfo().sysinfo["total_ram"] * 1000 / 1024 ** 3)}GiB '
                        f'--typecode=2:8200 '
                        f'--change-name=2:swap {device}',
                        msg=Message.message('81', self.config['language'], device))
                    if self.config['disk_encryption']:
                        Cmd(f'cryptsetup open --type plain --key-file /dev/urandom /dev/disk/by-partlabel/swap swap',
                            msg=Message.message('49', self.config['language'], '/dev/disk/by-partlabel/swap'))
                        Cmd(f'mkswap -L swap /dev/mapper/swap', msg=Message.message('50', self.config['language']))
                    else:
                        Cmd(f'mkswap -L swap /dev/disk/by-partlabel/swap',
                            msg=Message.message('50', self.config['language']))
                    Cmd(f'swapon -L swap',
                        msg=Message.message('51', self.config['language']))
            # Create and format system partition on all disks.
            Cmd(f'sgdisk '
                f'--new={"3" if swap_partition else "2"}:0:0 '
                f'--typecode={"3" if swap_partition else "2"}:8300 '
                f'--change-name={"3" if swap_partition else "2"}:system{index} {device}',
                msg=Message.message('82', self.config['language'], device))
            if filesystem == 'BTRFS':
                if self.config['disk_encryption']:
                    Cmd(f'mkfs.btrfs --force --label system /dev/mapper/system{index}',
                        msg=Message.message('87', self.config['language'], device, 'BTRFS'))
                else:
                    Cmd(f'mkfs.btrfs --force --label system{index} /dev/disk/by-partlabel/system{index}',
                        msg=Message.message('87', self.config['language'], device, 'BTRFS'))
            system_partitions.append(f'/dev/disk/by-partlabel/system{index}')

        if self.config['raid'] and filesystem == 'BTRFS':
            Cmd(f'mkfs.btrfs -L {self.config["hostname"]} -d {self.config["raid"]} -m {self.config["raid"]} -f '
                f'{" ".join(system_partitions)}',
                msg=Message.message('83', self.config['language'], " ".join(self.config["storage_devices"])))

        # Handles the disk encryption.
        if self.config['disk_encryption']:
            Cmd(f'cryptsetup luksFormat --batch-mode --align-payload=8192 -s 256 -c aes-xts-plain64 '
                f'/dev/disk/by-partlabel/system0 --key-file {str(self.diskpw)}',
                msg=Message.message('48', self.config['language'], '/dev/disk/by-partlabel/system0'))
            Cmd(f'cryptsetup open --key-file {str(self.diskpw)} /dev/disk/by-partlabel/system0 system0',
                msg=Message.message('49', self.config['language'], '/dev/disk/by-partlabel/system0'))

        # Handles BTRFS partitioning and subvolumes.
        if filesystem == 'BTRFS':
            Cmd(f'mount -t btrfs {system_partitions[0]} /mnt',
                msg=Message.message('86', self.config['language'], '/mnt'))
            Cmd(f'btrfs subvolume create /mnt/root',
                msg=Message.message('54', self.config['language'], '/mnt/root'))
            Cmd(f'btrfs subvolume create /mnt/home',
                msg=Message.message('54', self.config['language'], '/mnt/home'))
            Cmd(f'btrfs subvolume create /mnt/snapshots',
                msg=Message.message('54', self.config['language'], '/mnt/snapshots'))
            Cmd(f'umount -R /mnt',
                msg=Message.message('55', self.config['language']))
            mountpoint = None
            for subvolume in ['root', 'home', 'snapshots']:
                if subvolume == 'root':
                    mountpoint = '/mnt'
                if subvolume == 'home':
                    mountpoint = '/mnt/home'
                if subvolume == 'snapshots':
                    mountpoint = '/mnt/.snapshots'
                Cmd(f'mount -t btrfs -o subvol={subvolume},defaults,x-mount.mkdir,compress=lzo,ssd,noatime '
                    f'{system_partitions[0]} {mountpoint}',
                    msg=Message.message('53', self.config['language'], subvolume, mountpoint))

        # Removes the diskpw file.
        if self.config['disk_encryption']:
            Cmd(f'rm {str(self.diskpw)}', quiet=True)

from datetime import datetime

from archpy import Cmd, Message, SystemInfo


class Bootloader:
    def __init__(self, config):
        self.config = config
        self.sysinfo = SystemInfo().sysinfo

    def systemd_boot(self, disk_encryption=False):
        Cmd('arch-chroot /mnt bootctl install', msg=Message.message('66', self.config['language']))
        Cmd('arch-chroot /mnt rm /boot/loader/loader.conf')
        Cmd('arch-chroot /mnt touch /boot/loader/loader.conf /boot/loader/entries/arch.conf')
        Cmd('touch /mnt/boot/loader/entries/arch.conf')
        with open('/mnt/boot/loader/loader.conf', 'w') as fh:
            fh.write('timeout      3\n'
                     'console-mod  keep\n'
                     'default      arch.conf\n')
        with open('/mnt/boot/loader/entries/arch.conf', 'w') as fh:
            fh.write(
                f'# Created on: {datetime.now().replace(microsecond=0)}\n'
                f'title     ARCH LINUX\n'
                f'linux     /vmlinuz-{self.config["kernels"][0]}\n'
                f'initrd    /{self.sysinfo["cpu_vendor"]}-ucode.img\n'
                f'initrd    /initramfs-{self.config["kernels"][0]}.img\n'
                f'options   '
            )
        if disk_encryption:
            with open('/mnt/boot/loader/entries/arch.conf', 'a') as fh:
                fh.write(
                    f'rd.luks.name="{Cmd("blkid /dev/disk/by-partlabel/system0 -o value -s UUID").stdout}='
                    f'system" root="UUID={Cmd("blkid /dev/mapper/system0 -o value -s UUID").stdout}" '
                    f'rw rootflags=subvol=root {"intel_iommu=on" if self.sysinfo["cpu_vendor"] == "intel" else ""} '
                    f'iommu=pt\n'.replace('  ', ' ')
                )
        else:
            with open('/mnt/boot/loader/entries/arch.conf', 'a') as fh:
                fh.write(
                    f'root="PARTUUID={Cmd("blkid /dev/disk/by-partlabel/system0 -o value -s PARTUUID").stdout}" '
                    f'rw rootflags=subvol=root {"intel_iommu=on" if self.sysinfo["cpu_vendor"] == "intel" else ""} '
                    f'iommu=pt\n'.replace('  ', ' ')
                )

    def grub(self):
        Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm grub',
            msg=Message.message('90', self.config['language'], Message.message('77', self.config['language'])))
        Cmd(f'grub-install {self.config["storage_devices"][0]}')
        Cmd('grub-mkconfig -o /boot/grub/grub.cfg')

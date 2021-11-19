from pathlib import Path

from inquirer import confirm
from glob import glob

from archpy import Cmd, Message, SystemInfo, Partition, File, Packages, Bootloader


class Setup:

    def __init__(self, config):
        self.config = config[0]
        self.userpw = config[1]
        self.diskpw = config[2]
        self.sysinfo = SystemInfo().sysinfo
        self.services = []
        self.initramfs_modules = []
        self.core_packages = Packages(self.config).core_packages
        self.util_packages = Packages(self.config).util_packages
        if self.config['swap'] == "Swap on ZRAM":
            self.util_packages.append('zram-generator')

    def install(self):

        print(
            f"{Message.message('install_01', self.config['language'])}\n"
            f"{Message.message('install_02', self.config['language'])} "
            f"{Message.BOLD}{self.config['install_type']}{Message.RESET}\n"
            f"{Message.message('install_41', self.config['language'])} "
            f"{Message.BOLD}{self.config['swap']}{Message.RESET}\n"
            f"{Message.message('install_03', self.config['language'])} "
            f"{Message.BOLD}{self.config['filesystem']}{Message.RESET}\n"
            f"{Message.message('install_04', self.config['language'])} "
            f"{Message.BOLD}{self.config['username']}{Message.RESET}\n"
            f"{Message.message('install_05', self.config['language'])} "
            f"{Message.BOLD}{self.config['full_name']}{Message.RESET}\n"
            f"{Message.message('install_06', self.config['language'])} "
            f"{Message.BOLD}{self.config['hostname']}{Message.RESET}\n"
            f"{Message.message('install_07', self.config['language'])} "
            f"{Message.BOLD}{self.config['keyboard_layout']}{Message.RESET}\n"
            f"{Message.message('install_08', self.config['language'])} "
            f"{Message.BOLD}{self.config['timezone']}{Message.RESET}\n"
            f"{Message.message('install_09', self.config['language'])} "
            f"{Message.BOLD}{self.config['mirror']}{Message.RESET}\n"
            f"{Message.message('install_10', self.config['language'])} "
            f"{Message.BOLD}{self.config['kernels'][0]}{Message.RESET}\n"
            f"{Message.message('install_11', self.config['language'])} "
            f"{Message.BOLD}{', '.join(self.config['storage_devices'])}{Message.RESET}\n"
            f"{Message.message('install_43', self.config['language'])} "
            f"{Message.BOLD}{', '.join(self.core_packages)}{Message.RESET}\n"
            f"{Message.message('install_45', self.config['language'])} "
            f"{Message.BOLD}{', '.join(self.util_packages)}{Message.RESET}\n"
            f"{Message.message('install_47', self.config['language'])} "
            f"{Message.BOLD}{', '.join(self.config['extra_packages'])}{Message.RESET}\n"
        )

        # Prompts user to confirm installation.
        if not confirm(Message.message('install_12', self.config['language'])):
            Message('red_alert').print('Aborting installation!')
            exit()

        # Loads keyboard layout.
        Cmd(f"loadkeys {self.config['keyboard_layout']}",
            msg=Message.message('user_input_17', self.config['language'], self.config['keyboard_layout']), quiet=False)

        # Defining the mirrorlist.
        Cmd('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bkp',
            msg=Message.message('install_13', self.config['language']))
        Cmd(f"reflector -c '{self.config['mirror']}' --a 24 --delay 24 --p https,http --sort rate -f 10 -l 10 "
            f"--save /etc/pacman.d/mirrorlist",
            msg=Message.message('install_14', self.config['language']))

        # Partition layout.
        if self.config['filesystem'] == 'BTRFS':
            self.initramfs_modules.append('btrfs')
        if self.config['swap'] == 'Swap on partition':
            Partition(self.config, self.diskpw).layout1(filesystem=self.config['filesystem'],
                                                        swap_partition=True)
        if self.config['swap'] == 'Swap on ZRAM':
            Partition(self.config, self.diskpw).layout1(filesystem=self.config['filesystem'],
                                                        swap_partition=False)

        # Mounts the EFI partition.
        Cmd(f'mkdir /mnt/boot', msg=Message.message('install_25', self.config['language'], '/mnt/boot'))
        Cmd(f'mount LABEL=EFI /mnt/boot',
            msg=Message.message('install_22', self.config['language'], 'EFI', '/mnt/boot'))

        # Install core packages.
        Cmd(f'pacstrap /mnt {" ".join(self.core_packages)}',
            msg=Message.message(
                'install_26',
                self.config['language'],
                Message.message('install_44', self.config['language'], " ".join(self.core_packages))))

        # Fstab generation and edition.
        Cmd(f'genfstab -L -p /mnt >> /mnt/etc/fstab', shell=True,
            msg=Message.message('install_27', self.config['language']))
        if self.config['swap'] == 'Swap on partition' and self.config['disk_encryption']:
            Cmd(f'sed -i s+LABEL=swap+/dev/mapper/swap+ /mnt/etc/fstab',
                msg=Message.message('install_28', self.config['language']))

        # Locale
        if self.config['language'] != "en_US":
            Cmd("sed -i '/en_US5.UTF-8 UTF-8/s/^#//g' /mnt/etc/locale.gen", quiet=True)
        Cmd(f"sed -i '/{self.config['language']}.UTF-8 UTF-8/s/^#//g' /mnt/etc/locale.gen", quiet=True)
        Cmd("arch-chroot /mnt locale-gen", msg=Message.message('install_29', self.config['language']))
        Cmd('touch /mnt/etc/locale.conf /mnt/etc/vconsole.conf')
        with open('/mnt/etc/locale.conf', 'wt') as fh:
            fh.write(f'LANG={self.config["language"]}.UTF-8')
        with open('/mnt/etc/vconsole.conf', 'wt') as fh:
            fh.write(f'KEYMAP={self.config["keyboard_layout"]}')

        # Adjtime and NTP sync.
        Cmd('arch-chroot /mnt hwclock --systohc', msg=Message.message('install_30', self.config['language']))
        Cmd('arch-chroot /mnt timedatectl set-ntp true', msg=Message.message('install_31', self.config['language']))

        # Hostname.
        Cmd('touch /mnt/etc/hostname /mnt/etc/hosts', msg=Message.message('install_32', self.config['language']))
        with open('/mnt/etc/hostname', 'wt') as fh:
            fh.write(f'{self.config["hostname"]}')
        with open('/mnt/etc/hosts', 'wt') as fh:
            fh.write(f'127.0.0.1    localhost.localdomain           localhost\n'
                     f'::1	        localhost.localdomain           localhost\n'
                     f'127.0.0.1    {self.config["hostname"]}.localdomain     {self.config["hostname"]}')

        # Install util packages.
        Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm {" ".join(self.util_packages)}',
            msg=Message.message(
                'install_26',
                self.config['language'],
                Message.message('install_46', self.config['language'], " ".join(self.core_packages))))
        self.services.extend(['NetworkManager', 'sshd'])

        # Initramfs.
        if any('amd' in x.lower() for x in self.sysinfo['gfx_cards']):
            self.initramfs_modules.append('amdgpu')
        if any('nvidia' in x.lower() for x in self.sysinfo['gfx_cards']):
            self.util_packages.append('xorg')
            self.initramfs_modules.extend(['nvidia', 'nvidia_modeset', 'nvidia_uvm', 'nvidia_drm'])
            Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm nvidia cuda nvidia-settings',
                msg=Message.message('install_33', self.config['language']))
        if any('intel' in x.lower() for x in self.sysinfo['gfx_cards']):
            self.initramfs_modules.extend(['intel_agp', 'i915'])
        File('/mnt/etc/mkinitcpio.conf', backup=True).replace('MODULES=()', f'MODULES=('
                                                                            f'{" ".join(self.initramfs_modules)})')
        File('/mnt/etc/mkinitcpio.conf').replace('BINARIES=()', f'BINARIES=(/usr/bin/btrfs)')
        if self.config['disk_encryption']:
            Cmd("sed -i 's/HOOKS=(base udev autodetect modconf block filesystems keyboard fsck)/HOOKS=(base systemd "
                "autodetect keyboard sd-vconsole modconf block sd-encrypt filesystems fsck)/g' "
                "/mnt/etc/mkinitcpio.conf")
        Cmd(f'arch-chroot /mnt mkinitcpio -p {self.config["kernels"][0]}',
            msg=Message.message('install_34', self.config['language']))

        # User.
        Cmd(f'arch-chroot /mnt useradd -m -G wheel -c "{self.config["full_name"]}" "{self.config["username"]}"',
            msg=Message.message('install_36', self.config['language'], self.config['username']), shell=True)
        Cmd(f'echo "{self.config["username"]}:{self.userpw}" | arch-chroot /mnt chpasswd',
            msg=Message.message('install_37', self.config['language'], self.config['username']), shell=True)
        with open('/mnt/etc/sudoers', 'rt') as fh:
            sudoers_data = fh.read().replace('# %wheel ALL=(ALL) ALL', '%wheel ALL=(ALL) ALL')
        with open('/mnt/etc/sudoers', 'wt') as fh:
            fh.write(sudoers_data + '\n')
        Cmd(f'touch /mnt/etc/subuid /mnt/etc/subgid')
        Cmd(
            f'arch-chroot /mnt usermod --add-subuids 100000-165535 --add-subgids 100000-165535 '
            f'{self.config["username"]}',
            msg=Message.message('install_36', self.config['language'], self.config['username']))

        # Zram
        if self.config['swap'] == 'Swap on ZRAM':
            Cmd('touch /mnt/etc/systemd/zram-generator.conf')
            with open('/mnt/etc/systemd/zram-generator.conf', 'a') as fh:
                fh.write('[zram0]')
            Cmd(f'arch-chroot /mnt systemctl enable systemd-zram-setup@.service',
                msg=Message.message('install_42', self.config['language'], " ".join(self.services)))

        # Bootloader.
        if self.config['disk_encryption']:
            Bootloader(self.config).systemd_boot(disk_encryption=True)
        else:
            Bootloader(self.config).systemd_boot()

        # Extra packages.
        if self.config['install_type'] in ['Minimal Gnome', 'Gnome']:
            self.services.append('gdm')
        if self.config['install_type'] in ['KDE Plasma', 'KDE Plasma']:
            self.services.append('sddm')
        if self.config['install_type'] in ['Minimal Gnome', 'Gnome', 'KDE Plasma', 'KDE Plasma']:
            Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm {" ".join(Packages(self.config).audio_packages)}',
                msg=Message.message('install_26', self.config['language'], "Pipewire"))
        if self.config['install_type'] == 'Minimal Gnome':
            Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm {" ".join(Packages(self.config).minimal_gnome)}',
                msg=Message.message('install_26', self.config['language'], "Gnome"))
        elif self.config['install_type'] == 'Gnome':
            Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm gnome gnome-software-packagekit-plugin',
                msg=Message.message('install_26', self.config['language'], "Gnome"))
        elif self.config['install_type'] == 'Minimal KDE Plasma':
            Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm plasma-meta plasma-wayland-session',
                msg=Message.message('install_26', self.config['language'], "KDE Plasma"))
        elif self.config['install_type'] == 'KDE Plasma':
            Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm plasma plasma-wayland-session kde-applications',
                msg=Message.message('install_26', self.config['language'], "KDE Plasma"))
        Cmd(f'arch-chroot /mnt pacman -Sq --noconfirm {" ".join(self.config["extra_packages"])}',
            msg=Message.message(
                'install_26',
                self.config['language'],
                Message.message('install_48', self.config['language'], " ".join(self.core_packages))))

        # Services
        Cmd(f'arch-chroot /mnt systemctl enable {" ".join(self.services)}',
            msg=Message.message('install_38', self.config['language'], " ".join(self.services)))

        if self.config['install_type'] in ['Minimal Gnome']:
            for file in glob(f'/mnt/usr/share/applications/*.desktop'):
                if file in ['/mnt/usr/share/applications/system-config-printer.desktop',
                            '/mnt/usr/share/applications/bvnc.desktop', '/mnt/usr/share/applications/cups.desktop',
                            '/mnt/usr/share/applications/cups.desktop', '/mnt/usr/share/applications/bssh.desktop',
                            '/mnt/usr/share/applications/avahi-discover.desktop',
                            '/mnt/usr/share/applications/qv4l2.desktop', '/mnt/usr/share/applications/qvidcap.desktop',
                            '/mnt/usr/share/applications/lstopo.desktop']:
                    Path(file).unlink(missing_ok=True)

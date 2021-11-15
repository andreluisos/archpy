import json
import ssl
import urllib.error
import urllib.parse
import urllib.request

from archpy import SystemInfo


class Packages:
    def __init__(self, config):
        self.config = config
        self.sysinfo = SystemInfo().sysinfo
        self.base_url = 'https://archlinux.org/packages/search/json/?name={package}'
        self.base_group_url = 'https://archlinux.org/groups/x86_64/{group}/'
        self.core_packages = ['base', 'base-devel', self.config['kernels'][0], f"{self.config['kernels'][0]}-headers",
                              'linux-firmware']
        self.util_packages = [f'{self.sysinfo["cpu_vendor"]}-ucode', 'packagekit', 'btrfs-progs', 'dosfstools',
                              'efibootmgr', 'gptfdisk', 'util-linux', 'man-pages', 'man-db', 'nano', 'openssh',
                              'networkmanager', 'wireless_tools', 'wpa_supplicant', 'pacman-contrib', 'moreutils']
        self.audio_packages = ["pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-media-session", "pipewire-pulse",
                               "gst-plugin-pipewire", "libpulse"]
        self.minimal_gnome = ['evince', 'gdm', 'gnome-backgrounds', 'gnome-color-manager',
                              'gnome-control-center', 'gnome-disk-utility', 'gnome-keyring', 'gnome-menus',
                              'gnome-remote-desktop', 'gnome-session', 'gnome-settings-daemon', 'gnome-shell',
                              'gnome-software', 'gnome-system-monitor', 'gnome-terminal', 'gnome-themes-extra',
                              'gnome-user-docs', 'gvfs', 'gvfs-google', 'gvfs-afc', 'gvfs-goa', 'gvfs-gphoto2',
                              'gvfs-mtp', 'gvfs-smb', 'mutter', 'nautilus', 'orca', 'tracker',
                              'tracker-miners', 'tracker-miners', 'xdg-user-dirs-gtk', 'yelp',
                              'gnome-software-packagekit-plugin']
        self.personal_packages = ['mesa', 'mesa-demos', 'fuse', 'ufw', 'git', 'curl', 'wget', 'awk', 'podman', 'rclone',
                                  'ffmpeg', 'zsh', 'python3', 'python-pip', 'tar' 'cockpit', 'cockpit-podman',
                                  'cockpit-machines', 'cockpit-pcp', 'udisks2']
        self.personal_packages_gui = ['cups', 'cups-pdf', 'system-config-printer', 'qemu', 'virt-manager', 'gufw',
                                      'bridge-utils', 'gnome-tweak-tool', 'flatpak', 'firefox', 'libreoffice-fresh',
                                      'libvirt', 'libreoffice-fresh-pt-br', 'dnsmasq', 'edk2-ovmf', 'gnome', 'gdm',
                                      'gnome-software-packagekit-plugin']
        self.audio = ["pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-media-session", "pipewire-pulse",
                      "gst-plugin-pipewire", "libpulse"]

    def find_group(self, name):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        try:
            response = urllib.request.urlopen(self.base_group_url.format(group=name), context=ssl_context)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return False
            else:
                raise err
        if response.code == 200:
            return True

    def find_package(self, name):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        response = urllib.request.urlopen(self.base_url.format(package=name), context=ssl_context)
        data = response.read().decode('UTF-8')
        return json.loads(data)

    def find_packages(self, *names):
        return {package: self.find_package(package) for package in names}

    def validate_package_list(self, packages: list):
        invalid_packages = [
            package
            for package in packages
            if not self.find_package(package)['results'] and not self.find_group(package)
        ]
        if invalid_packages:
            return invalid_packages
        else:
            return True

import urllib.error
import urllib.request
from pathlib import Path
from random import getrandbits
from re import match
from json import loads

from inquirer import list_input, text, confirm, checkbox, password
from unidecode import unidecode

from archpy import Cmd, Message, File, SystemInfo, TZ_COUNTRY, Packages


class Config:

    def __init__(self):
        self.sysinfo = SystemInfo().sysinfo
        if self.sysinfo == 'BIOS':
            Message('red_alert').print('You are using BIOS, but only UEFI is supported at this moment. Leaving.')
        self.config = {
            "language": None,
            "keyboard_layout": None,
            "timezone": None,
            "mirror": None,
            "install_type": None,
            "swap": None,
            "filesystem": None,
            "storage_devices": [],
            "raid": None,
            "kernels": [],
            "username": None,
            "full_name": None,
            "hostname": None,
            "disk_encryption": None,
            "extra_packages": [],
        }
        self.mirrorlist_url = "https://archlinux.org/mirrorlist/?protocol=https&protocol=http&ip_version=4&" \
                              "ip_version=6&use_mirror_status=on"
        self.available_locales = [
            language.replace('#', '').split('.')[0] for language in Cmd('cat /etc/locale.gen').stdout.split('\n')
            if not language.startswith('# ') and '.UTF-8 UTF-8' in language]
        self.available_keymaps = Cmd('localectl list-keymaps').stdout.split('\n')
        self.available_timezones = Cmd('timedatectl list-timezones').stdout.split('\n')
        self.available_regions = []
        try:
            response = urllib.request.urlopen(self.mirrorlist_url)
            mirrorlist = response.read().decode('utf-8')
            for country in mirrorlist.split('\n'):
                if country == '##' or country == '' or any(
                        item in country for item in ['Arch Linux', 'Generated on', '#Server', 'Filtered by']):
                    continue
                else:
                    country = country.replace('## ', '')
                if country not in self.available_regions:
                    self.available_regions.append(country)
            self.available_regions = sorted(self.available_regions)
        except urllib.error.URLError:
            Message('red_alert').print(Message.message('user_input_22', self.config['language'],
                                                       'https://archlinux.org/mirrorlist/'))
        self.available_install_types = ['Minimal', 'Minimal Gnome', 'Minimal KDE Plasma', 'Gnome', 'KDE Plasma']
        self.available_kernels = {'Stable': "linux", 'Longterm': "linux-lts", 'Hardened': "linux-hardened",
                                  'Zen': "linux-zen"}
        self.available_devices = self.sysinfo['storage_devices']
        self.available_swaps = ['Swap on ZRAM', 'Swap on partition']
        self.available_filesystems = ['BTRFS']
        self.available_raids = ['RAID0', 'RAID1', 'RAID3', 'RAID5', 'RAID10']
        self.userpw = None
        self.diskpw = None

    def set_language(self):
        return list_input('Choose a language for the setup (not the system language)',
                          choices=self.available_locales,
                          default='en_US')

    def set_kb_layout(self):
        default = None
        language = self.config['language'].lower().split('_')[1]
        for keymap in self.available_keymaps:
            if language in keymap.lower():
                default = keymap
        return list_input(
            message=Message.message('user_input_01', self.config['language']),
            choices=self.available_keymaps,
            default=default if default is not None else 'us'
        )

    def set_timezone(self):
        return list_input(
            message=Message.message('user_input_02', self.config['language']),
            choices=self.available_timezones,
            default='America/Sao_Paulo' if self.config['language'] == 'pt_BR' else 'America/New_York'
        )

    def set_mirrors(self):
        return list_input(Message.message('user_input_24', self.config['language'],
                                          TZ_COUNTRY[self.config['timezone']]), choices=self.available_regions,
                          default=TZ_COUNTRY[self.config['timezone']] if TZ_COUNTRY[self.config[
                              'timezone']] in self.available_regions else 'United States')

    def set_install_type(self):
        return list_input(Message.message('user_input_03', self.config['language']),
                          choices=self.available_install_types,
                          default='Minimal Gnome')

    def set_kernels(self):
        return [self.available_kernels[kernel] for kernel in
                checkbox(Message.message('user_input_04', self.config['language']),
                         choices=self.available_kernels,
                         default='Stable') if kernel in self.available_kernels]

    def set_disk_encryption(self):
        while True:
            disk_encryption1 = password(Message.message('user_input_15', self.config['language'],
                                                        self.config['username']))
            disk_encryption2 = password(Message.message('user_input_11', self.config['language']))
            if disk_encryption1 != disk_encryption2:
                Message('red_alert').print(Message.message('user_input_12', self.config['language']))
                continue
            else:
                if type(disk_encryption1) != bytes:
                    disk_encryption1 = bytes(disk_encryption1, 'UTF-8')
                    self.diskpw = Path(f'/tmp/{getrandbits(128)}.diskpw')
                    File(self.diskpw).save(disk_encryption1)
                return self.diskpw

    def set_swap(self):
        return list_input(
            message=Message.message('user_input_26', self.config['language']),
            choices=self.available_swaps,
            default='Swap on ZRAM'
        )

    def set_filesystem(self):
        return list_input(
            message=Message.message('user_input_25', self.config['language']),
            choices=self.available_filesystems,
            default='BTRFS'
        )

    def set_devices(self):
        while True:
            storage_devices = checkbox(
                message=Message.message('user_input_05', self.config['language']),
                choices=self.available_devices
            )
            if not storage_devices:
                Message('red_alert').print(Message.message('user_input_06', self.config['language']))
                continue
            else:
                self.config['storage_devices'] = storage_devices
                break
        if len(self.config['storage_devices']) > 1 and self.config['filesystem'] == "BTRFS":
            if confirm(Message.message('user_input_30', self.config['language']), default=False):
                self.config['raid'] = list_input(
                    message=Message.message('user_input_31', self.config['language']),
                    choices=self.available_raids,
                    default='RAID1'
                ).lower()
        else:
            self.config['raid'] = False

    def set_username(self):
        fullname = unidecode(self.config['full_name']).split(' ')
        if len(fullname) >= 2:
            default = (fullname[0] + fullname[1]).lower()
        else:
            default = fullname[0].lower()
        while True:
            username = text(Message.message('user_input_07', self.config['language']), default=default)
            if match(r'^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$', username):
                return username
            else:
                Message('red_alert').print(Message.message('user_input_08', self.config['language']))
                continue

    def set_full_name(self):
        return text(Message.message('user_input_09', self.config['language']))

    def set_user_password(self):
        while True:
            pass1 = password(Message.message('user_input_10', self.config['language'],
                                             self.config['username']))
            pass2 = password(Message.message('user_input_11', self.config['language']))
            if pass1 != pass2:
                Message('red_alert').print(Message.message('user_input_12', self.config['language']))
                continue
            else:
                return pass1

    def set_hostname(self):
        while True:
            hostname = text(Message.message('user_input_13', self.config['language']),
                            default=self.config['username'])
            if match(r'^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$', hostname):
                return hostname
            else:
                Message('red_alert').print(Message.message('user_input_14', self.config['language']))
                continue

    def set_flatpak(self):
        if confirm(Message.message('user_input_27', self.config['language']), default=True):
            self.config['extra_packages'].append('flatpak')
        else:
            pass

    def set_extra_packages(self):
        packages = text(Message.message('user_input_29', self.config['language'])).split(' ')
        invalid_packages = Packages(self.config).validate_package_list(packages)
        if not invalid_packages:
            packages = [item for item in packages if item not in invalid_packages]
        self.config['extra_packages'].extend(packages)

    def new(self, generate=False):

        self.config['language'] = self.set_language()

        self.config['keyboard_layout'] = self.set_kb_layout()

        Cmd(f"loadkeys {self.config['keyboard_layout']}", quiet=True)

        self.config['timezone'] = self.set_timezone()

        self.config['mirror'] = self.set_mirrors()

        self.config['install_type'] = self.set_install_type()

        self.config['kernels'] = self.set_kernels()

        self.config['disk_encryption'] = confirm(Message.message('user_input_16', self.config['language']),
                                                 default=False)

        if self.config['disk_encryption'] and not generate:
            self.diskpw = self.set_disk_encryption()

        self.config['swap'] = self.set_swap()

        self.config['filesystem'] = self.set_filesystem()

        self.set_devices()

        self.config['full_name'] = self.set_full_name()

        self.config['username'] = self.set_username()

        if not generate:
            self.userpw = self.set_user_password()

        self.config['hostname'] = self.set_hostname()

        self.set_flatpak()

        self.set_extra_packages()

        return [self.config, self.userpw, self.diskpw]

    def generate(self):
        self.config = Config().new(generate=True)[0]
        full_path = Path(text(Message.message('user_input_18', self.config['language'])))
        if full_path.is_dir() and full_path.exists():
            File(full_path.joinpath('archpy.json')).save(self.config)

    def load(self, path):
        if 'http' in path or 'https' in path:
            self.config = loads(urllib.request.urlopen(path).read().decode('utf-8'))
        else:
            while True:
                full_path = Path(path)
                if full_path == "" or (not Path(full_path).is_file() or not Path(full_path).exists()):
                    Message('red_alert').print(Message.message('user_input_20', self.config['language']))
                    break
                else:
                    self.config = File(full_path).load()
                    break

        if self.config['language'] not in self.available_locales:
            self.config['language'] = self.set_language()

        if self.config['keyboard_layout'] not in self.available_keymaps:
            self.config['keyboard_layout'] = self.set_kb_layout()
            Cmd(f"loadkeys {self.config['keyboard_layout']}", quiet=True)

        if self.config['timezone'] not in self.available_timezones:
            self.config['timezone'] = self.set_timezone()

        if self.config['mirror'] not in self.available_regions:
            self.config['timezone'] = self.set_mirrors()

        if self.config['install_type'] not in self.available_install_types:
            self.config['install_type'] = self.set_install_type()

        if self.config['swap'] not in self.available_swaps:
            self.config['swap'] = self.set_swap()

        if self.config['filesystem'] not in self.available_filesystems:
            self.config['filesystem'] = self.set_filesystem()

        if any(item not in self.available_kernels.values() for item in self.config['kernels']):
            self.config['kernels'] = self.set_kernels()

        if any(item not in self.available_devices for item in self.config['storage_devices']):
            self.set_devices()

        if self.config['full_name'] is None:
            self.config['full_name'] = self.set_full_name()

        if self.config['username'] is None or not match(r'^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$',
                                                        self.config['username']):
            self.config['username'] = self.set_username()

        if self.config['hostname'] is None or not match(r'^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$',
                                                        self.config['hostname']):
            self.config['hostname'] = self.set_hostname()

        if type(self.config['disk_encryption']) is not bool:
            self.config['disk_encryption'] = self.set_disk_encryption()

        if self.config['disk_encryption']:
            self.diskpw = self.set_disk_encryption()
        self.userpw = self.set_user_password()

        return [self.config, self.userpw, self.diskpw]

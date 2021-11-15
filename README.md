# Purpose
The purpose is to bring more people to Arch Linux by providing a working, flexible, easier and faster installer 
than the one officially provided by Arch Linux.

# Installation

Once booted into Arch installer iso:
```shell
pacman -Syq --noconfirm python3 python-pip git
```
```shell
pip install archpy
```
For the latest version:
```shell
pip install git+https://github.com/andreluisos/archpy.git
```

# Hardware requirements
**I've only tested this on UEFI with SSD**.
Need people to test on other hardware and report issues [here](https://github.com/andreluisos/archpy/issues).


# Software requirements
Only two non official Python packages are being used: [inquirer](https://github.com/magmax/python-inquirer) and 
[unidecode](https://github.com/avian2/unidecode).

I'm working on a way to get rid of them.

# Usage

### archpy install [path|url]
- The install command can start a new installation (if no path or url is passed in) or
load a installation parameters from a local or remote json file.
- Absolute path or url is necessary.

### archpy generate config
- Creates a new installation parameters json file on the desired directory.
- In the end, user will be prompted to insert the full directory path. A json file called
archpy.json will be created on that path.

## Usage examples

```shell
archpy install
```
```shell
archpy install /home/me/archpy.json
```
```shell
archpy install https://raw.githubusercontent.com/andreluisos/archpy/main/examples/archpy.json
```
```shell
archpy generate config
```

# Goals
- Fix bugs.
- Add more options to the installer.
- Cool post installation automator, which might also work with any other Linux distribution.

# Help
Need people to test and report bugs [here](https://github.com/andreluisos/archpy/issues).
class Message:
    LANGUAGES = ["en_US", "pt_BR"]
    BOLD = '\033[1m'
    BLUE = '\033[94m'
    BLUE_BOLD = BLUE + BOLD
    GREEN = '\033[92m'
    GREEN_BOLD = GREEN + BOLD
    YELLOW = '\033[93m'
    YELLOW_BOLD = YELLOW + BOLD
    RED = '\033[91m'
    RED_BOLD = RED + BOLD
    RESET = '\033[0m'
    RED_ALERT = f'[{RED}!{RESET}]'
    YELLOW_ALERT = f'[{YELLOW}!{RESET}]'

    def __init__(self, color):
        self.colorname = color
        self.reset = Message.RESET
        if self.colorname == 'bold':
            self.color = Message.BOLD
        elif self.colorname == 'blue':
            self.color = Message.BLUE
        elif self.colorname == 'blue_bold':
            self.color = Message.BLUE_BOLD
        elif self.colorname == 'green':
            self.color = Message.GREEN
        elif self.colorname == 'green_bold':
            self.color = Message.GREEN_BOLD
        elif self.colorname == 'yellow':
            self.color = Message.YELLOW
        elif self.colorname == 'yellow_bold':
            self.color = Message.YELLOW_BOLD
        elif self.colorname == 'red':
            self.color = Message.RED
        elif self.colorname == 'red_bold':
            self.color = Message.RED_BOLD
        elif self.colorname == 'red_alert':
            self.color = Message.RED_ALERT
        elif self.colorname == 'yellow_alert':
            self.color = Message.YELLOW_ALERT

    def print(self, message):
        if self.colorname in ['red_alert', 'yellow_alert']:
            print(f'{self.color} {message}{self.reset}')
        else:
            print(f'{self.color}{message}{self.reset}')

    @staticmethod
    def message(*args):
        # arg[0] = the message
        # arg[1] = the language

        if args[1] not in Message.LANGUAGES:
            Message('red_alert').print('This language is not yet available!')

        messages = {

            "01": {
                "en_US": "Select the desired keyboard layout",
                "pt_BR": "Selecione o layout de teclado desejado",
            },

            "02": {
                "en_US": "Select the desired timezone",
                "pt_BR": "Selecione o timezone desejado",
            },

            "03": {
                "en_US": "Choose the instalation type",
                "pt_BR": "Selecione o tipo de instalação",
            },

            "04": {
                "en_US": "Choose the desired kernel (it's possible to select more than one - the first one will be the "
                         "main one)",
                "pt_BR": "Selecione o kernel desejado (é possível selecionar mais de um - o primeiro selecionado será o"
                         " padrão)",
            },

            "05": {
                "en_US": "Choose the desired storage device (if multiple devices selected, RAID will be used)",
                "pt_BR": "Selecione o dispositivo de armazenamento desejado (se mais de um for escolhido, RAID será "
                         "usado)",
            },

            "06": {
                "en_US": "Use space to choose at least one storage device!",
                "pt_BR": "Utilize espaço para escolher ao menos um dispositivo de armazenamento!",
            },

            "07": {
                "en_US": "Enter an username (no spaces or special characters)",
                "pt_BR": "Digite um nome de usuário (sem espaço ou caracteres especiais)",
            },

            "08": {
                "en_US": "Invalid username characters! Read useradd's man page and try again!",
                "pt_BR": "Carácteres inválidos! Leia o man page do comando useradd e tente novamente!",
            },

            "09": {
                "en_US": f"Type a full name for your username (space and special characters allowed)",
                "pt_BR": f'Digite o nome completo para o usuário (espaço e caracteres especiais permitido)',
            },

            "10": {
                "en_US": f'Type a password for user "{args[2] if len(args) > 2 else None}"',
                "pt_BR": f'Digite uma senha para o usuário "{args[2] if len(args) > 2 else None}"',
            },

            "11": {
                "en_US": f"Type the same password again to confirm",
                "pt_BR": f"Digite a mesma senha novamente para confirmar",
            },

            "12": {
                "en_US": f"The passwords doesn't match! Try again.",
                "pt_BR": f"As senhas não coincidem! Tente novamente.",
            },

            "13": {
                "en_US": f"Type the desired hostname",
                "pt_BR": f"Digite o hostname desejado",
            },

            "14": {
                "en_US": "Invalid hostname! It follows the same rules for useradd. Read it's man page for allowed "
                         "characters and try again.",
                "pt_BR": "Hostname inválido! Ele deve seguir as mesmas regras para a criação de usuário. Leia o "
                         "man page do useradd para saber quais caracteres são permitidos e tente novamente.",
            },

            "15": {
                "en_US": "Type the disk encryption password",
                "pt_BR": "Digite a senha da criptografia de disco",
            },

            "16": {
                "en_US": "Would you like to encrypt the disk?",
                "pt_BR": "Você gostaria de criptografar o disco?",
            },

            "17": {
                "en_US": f'Loading keyboard layout "{args[2] if len(args) > 2 else None}"',
                "pt_BR": f'Carregando o layout de teclado "{args[2] if len(args) > 2 else None}"',
            },

            "18": {
                "en_US": "Type the full path of the destination directory",
                "pt_BR": "Digite o caminho do diretório de destino completo",
            },

            "19": {
                "en_US": "Type the full path of the json file",
                "pt_BR": "Digite o caminho completo do arquivo json",
            },

            "20": {
                "en_US": "The file doesn't exist!",
                "pt_BR": "O arquivo não existe!",
            },

            "21": {
                "en_US": "The choosen language differs from the loaded file. Which one would you like to proceed with?",
                "pt_BR": "O idioma escolhido difere daquela salva no arquivo. Com qual delas você deseja prosseguir?",
            },

            "22": {
                "en_US": "No mirror avaialble for your region!",
                "pt_BR": "Nenhum mirror disponível para sua região!",
            },

            "23": {
                "en_US": f"Failed to pull the data from {args[2] if len(args) > 2 else None}!",
                "pt_BR": f"Falha ao baixar as informaçoes de {args[2] if len(args) > 2 else None}",
            },

            "24": {
                "en_US": f'Choose which country you would like to use mirrors from',
                "pt_BR": f'Escolha o país de onde você quer usar as mirrors',
            },

            "25": {
                "en_US": f'Choose the desired filesystem',
                "pt_BR": f'Escolha o filysystem desejado',
            },

            "26": {
                "en_US": f'Choose the swap type',
                "pt_BR": f'Escolha o tipo de swap desejado',
            },

            "27": {
                "en_US": f'Would you like to enable Flatpak repository?',
                "pt_BR": f'Você gostaria de ativar o repositório Flatpak?',
            },

            "28": {
                "en_US": f'Your installation file is too old... Consider making a new one.',
                "pt_BR": f'O seu arquivo de instalação é muito antigo... Por favor, faça um novo.',
            },

            "29": {
                "en_US": f'Extra packages, if you want (separated by space)',
                "pt_BR": f'Pacotes extras, se desejar (separados por espaço)',
            },

            "30": {
                "en_US": f"Would you like to create a raid array?",
                "pt_BR": f'Gostaria de criar um raid array?',
            },

            "31": {
                "en_US": f"What raid mode would you like to use?",
                "pt_BR": f'Qual modo de raid você gostaria de usar?',
            },

            "32": {
                "en_US": "##### INSTALATION PARAMETERS #####",
                "pt_BR": "##### PARÂMETROS DE INSTALAÇÃO #####",
            },

            "33": {
                "en_US": "Installation type:",
                "pt_BR": "Tipo de instalação:",
            },

            "34": {
                "en_US": "Filesystem:",
                "pt_BR": "Filesystem:",
            },

            "35": {
                "en_US": "Username:",
                "pt_BR": "Usuário:",
            },

            "36": {
                "en_US": "Full name:",
                "pt_BR": "Nome completo:",
            },

            "37": {
                "en_US": "Hostname:",
                "pt_BR": "Hostname:",
            },

            "38": {
                "en_US": "Keyboard layout:",
                "pt_BR": "Layout do teclado:",
            },

            "39": {
                "en_US": "Timezone:",
                "pt_BR": "Timezone:",
            },

            "40": {
                "en_US": "Mirror:",
                "pt_BR": "Mirror:",
            },

            "41": {
                "en_US": "Kernel:",
                "pt_BR": "Kernel:",
            },

            "42": {
                "en_US": "Storage devices:",
                "pt_BR": "Dispositivos de armazenamento:",
            },

            "43": {
                "en_US": "Would you like to proceed with the installation?",
                "pt_BR": "Você gostaria de continuar com a instalação?",
            },

            "44": {
                "en_US": "Backing up current mirrorlist",
                "pt_BR": "Fazendo backup da mirrorlist atual",
            },

            "45": {
                "en_US": "Generating a new mirrorlist",
                "pt_BR": "Gerando uma nova mirrorlist",
            },

            "46": {
                "en_US": f"Wiping {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Limpando {args[2] if len(args) > 2 else None}",
            },

            "47": {
                "en_US": "Creating partition layout",
                "pt_BR": "Criando layout de partição",
            },

            "48": {
                "en_US": f"Encrypting {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criptografando {args[2] if len(args) > 2 else None}",
            },

            "49": {
                "en_US": f"Opening encrypted partition {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Entrando na partição criptografada {args[2] if len(args) > 2 else None}",
            },

            "50": {
                "en_US": f"Making swap",
                "pt_BR": f"Criando swap",
            },

            "51": {
                "en_US": f"Activating swap",
                "pt_BR": f"Ativando swap",
            },

            "52": {
                "en_US": f"Formatting {args[2] if len(args) > 2 else None} using "
                         f"{args[3] if len(args) > 3 else None}",
                "pt_BR": f"Formatando {args[2] if len(args) > 2 else None} usando "
                         f"{args[3] if len(args) > 3 else None}",
            },

            "53": {
                "en_US": f"Mounting {args[2] if len(args) > 2 else None} on "
                         f"{args[3] if len(args) > 3 else None}",
                "pt_BR": f"Montando {args[2] if len(args) > 2 else None} em "
                         f"{args[3] if len(args) > 3 else None}",
            },

            "54": {
                "en_US": f"Creating BTRFS subvolume {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando subvolume BTRFS {args[2] if len(args) > 2 else None}",
            },

            "55": {
                "en_US": f"Unmounting everything",
                "pt_BR": f"Desmontando tudo",
            },

            "56": {
                "en_US": f"Making directory {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando diretório {args[2] if len(args) > 2 else None}",
            },

            "57": {
                "en_US": f"Installing {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Instalando {args[2] if len(args) > 2 else None}",
            },

            "58": {
                "en_US": f"Generating fstab",
                "pt_BR": f"Gerando fstab",
            },

            "59": {
                "en_US": f"Making needed fstab modifications",
                "pt_BR": f"Fazendo as modificações necessárias no fstab",
            },

            "60": {
                "en_US": f"Generating locale",
                "pt_BR": f"Gerando locale",
            },

            "61": {
                "en_US": f"Generating adjtime",
                "pt_BR": f"Gerando adjtime",
            },

            "62": {
                "en_US": f"Enabling NTP synchronization",
                "pt_BR": f"Ativando sincronização NTP",
            },

            "63": {
                "en_US": f"Setting up hostname",
                "pt_BR": f"Configurando hostname",
            },

            "64": {
                "en_US": f"Installing Nvidia drivers",
                "pt_BR": f"Instalando drivers Nvidia",
            },

            "65": {
                "en_US": f"Recreating initramfs",
                "pt_BR": f"Recriando initramfs",
            },

            "66": {
                "en_US": f"Installing bootloader",
                "pt_BR": f"Instalando bootloader",
            },

            "67": {
                "en_US": f'Creating user "{args[2] if len(args) > 2 else None}"',
                "pt_BR": f'Criando usuário "{args[2] if len(args) > 2 else None}"',
            },

            "68": {
                "en_US": f"Setting {args[2] if len(args) > 2 else None}'s password",
                "pt_BR": f'Definindo a senha para o usuário "{args[2] if len(args) > 2 else None}"',
            },

            "69": {
                "en_US": f"Adding subuids and subgids",
                "pt_BR": f"Atribuindo subuids e subgids",
            },

            "70": {
                "en_US": f"Enabling services {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Ativando serviços {args[2] if len(args) > 2 else None}",
            },

            "71": {
                "en_US": f"Creating EFI partition in {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando partição EFI em {args[2] if len(args) > 2 else None}",
            },

            "72": {
                "en_US": "Swap:",
                "pt_BR": "Swap:",
            },

            "73": {
                "en_US": "Enabling ZRAM",
                "pt_BR": "Ativando ZRAM",
            },

            "74": {
                "en_US": "Core packages:",
                "pt_BR": "Pacotes núcleo:",
            },

            "75": {
                "en_US": "core packages",
                "pt_BR": "pacotes núcleo",
            },

            "76": {
                "en_US": "Util packages:",
                "pt_BR": "Pacotes utilitários:",
            },

            "77": {
                "en_US": "util packages",
                "pt_BR": "pacotes utilitários",
            },

            "78": {
                "en_US": "Extra packages:",
                "pt_BR": "Pacotes extras:",
            },

            "79": {
                "en_US": "extra packages",
                "pt_BR": "pacotes extras",
            },

            "80": {
                "en_US": "extra packages",
                "pt_BR": "pacotes extras",
            },

            "81": {
                "en_US": f"Creating swap partition in {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando partição swap in {args[2] if len(args) > 2 else None}",
            },

            "82": {
                "en_US": f"Creating system partition in {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando partição do sistema em {args[2] if len(args) > 2 else None}",
            },

            "83": {
                "en_US": f"Setting up raid system between {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Configurando sistema raid entre {args[2] if len(args) > 2 else None}",
            },

            "84": {
                "en_US": f"Formatting EFI partition using {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Formatando partição EFI usando {args[2] if len(args) > 2 else None}",
            },

            "86": {
                "en_US": f"Mounting main partition at {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Motando partição principal em {args[2] if len(args) > 2 else None}",
            },

            "87": {
                "en_US": f"Formatting main partition in {args[2] if len(args) > 2 else None} "
                         f"using {args[3] if len(args) > 3 else None}",
                "pt_BR": f"Formatando partição principal em {args[2] if len(args) > 2 else None} "
                         f"usando {args[3] if len(args) > 3 else None}",
            },

        }

        return messages[args[0]][args[1]]

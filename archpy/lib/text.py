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

            "user_input_01": {
                "en_US": "Select the desired keyboard layout",
                "pt_BR": "Selecione o layout de teclado desejado",
            },

            "user_input_02": {
                "en_US": "Select the desired timezone",
                "pt_BR": "Selecione o timezone desejado",
            },

            "user_input_03": {
                "en_US": "Choose the instalation type",
                "pt_BR": "Selecione o tipo de instalação",
            },

            "user_input_04": {
                "en_US": "Choose the desired kernel (it's possible to select more than one - the first one will be the "
                         "main one)",
                "pt_BR": "Selecione o kernel desejado (é possível selecionar mais de um - o primeiro selecionado será o"
                         " padrão)",
            },

            "user_input_05": {
                "en_US": "Choose the desired storage device (if multiple devices selected, RAID will be used)",
                "pt_BR": "Selecione o dispositivo de armazenamento desejado (se mais de um for escolhido, RAID será "
                         "usado)",
            },

            "user_input_06": {
                "en_US": "Use space to choose at least one storage device!",
                "pt_BR": "Utilize espaço para escolher ao menos um dispositivo de armazenamento!",
            },

            "user_input_07": {
                "en_US": "Enter an username (no spaces or special characters)",
                "pt_BR": "Digite um nome de usuário (sem espaço ou caracteres especiais)",
            },

            "user_input_08": {
                "en_US": "Invalid username characters! Read useradd's man page and try again!",
                "pt_BR": "Carácteres inválidos! Leia o man page do comando useradd e tente novamente!",
            },

            "user_input_09": {
                "en_US": f"Type a full name for your username (space and special characters allowed)",
                "pt_BR": f'Digite o nome completo para o usuário (espaço e caracteres especiais permitido)',
            },

            "user_input_10": {
                "en_US": f'Type a password for user "{args[2] if len(args) > 2 else None}"',
                "pt_BR": f'Digite uma senha para o usuário "{args[2] if len(args) > 2 else None}"',
            },

            "user_input_11": {
                "en_US": f"Type the same password again to confirm",
                "pt_BR": f"Digite a mesma senha novamente para confirmar",
            },

            "user_input_12": {
                "en_US": f"The passwords doesn't match! Try again.",
                "pt_BR": f"As senhas não coincidem! Tente novamente.",
            },

            "user_input_13": {
                "en_US": f"Type the desired hostname",
                "pt_BR": f"Digite o hostname desejado",
            },

            "user_input_14": {
                "en_US": "Invalid hostname! It follows the same rules for useradd. Read it's man page for allowed "
                         "characters and try again.",
                "pt_BR": "Hostname inválido! Ele deve seguir as mesmas regras para a criação de usuário. Leia o "
                         "man page do useradd para saber quais caracteres são permitidos e tente novamente.",
            },

            "user_input_15": {
                "en_US": "Type the disk encryption password",
                "pt_BR": "Digite a senha da criptografia de disco",
            },

            "user_input_16": {
                "en_US": "Would you like to encrypt the disk?",
                "pt_BR": "Você gostaria de criptografar o disco?",
            },

            "user_input_17": {
                "en_US": f'Loading keyboard layout "{args[2] if len(args) > 2 else None}"',
                "pt_BR": f'Carregando o layout de teclado "{args[2] if len(args) > 2 else None}"',
            },

            "user_input_18": {
                "en_US": "Type the full path of the destination directory",
                "pt_BR": "Digite o caminho do diretório de destino completo",
            },

            "user_input_19": {
                "en_US": "Type the full path of the json file",
                "pt_BR": "Digite o caminho completo do arquivo json",
            },

            "user_input_20": {
                "en_US": "The file doesn't exist!",
                "pt_BR": "O arquivo não existe!",
            },

            "user_input_21": {
                "en_US": "The choosen language differs from the loaded file. Which one would you like to proceed with?",
                "pt_BR": "O idioma escolhido difere daquela salva no arquivo. Com qual delas você deseja prosseguir?",
            },

            "user_input_22": {
                "en_US": "No mirror avaialble for your region!",
                "pt_BR": "Nenhum mirror disponível para sua região!",
            },

            "user_input_23": {
                "en_US": f"Failed to pull the data from {args[2] if len(args) > 2 else None}!",
                "pt_BR": f"Falha ao baixar as informaçoes de {args[2] if len(args) > 2 else None}",
            },

            "user_input_24": {
                "en_US": f'Choose which country you would like to use mirrors from',
                "pt_BR": f'Escolha o país de onde você quer usar as mirrors',
            },

            "user_input_25": {
                "en_US": f'Choose the desired filesystem',
                "pt_BR": f'Escolha o filysystem desejado',
            },

            "user_input_26": {
                "en_US": f'Choose the swap type',
                "pt_BR": f'Escolha o tipo de swap desejado',
            },

            "user_input_27": {
                "en_US": f'Would you like to enable Flatpak repository?',
                "pt_BR": f'Você gostaria de ativar o repositório Flatpak?',
            },

            "user_input_28": {
                "en_US": f'Your installation file is too old... Consider making a new one.',
                "pt_BR": f'O seu arquivo de instalação é muito antigo... Por favor, faça um novo.',
            },

            "user_input_29": {
                "en_US": f'Extra packages, if you want (separated by space)',
                "pt_BR": f'Pacotes extras, se desejar (separados por espaço)',
            },

            "user_input_30": {
                "en_US": f"Would you like to create a raid array?",
                "pt_BR": f'Gostaria de criar um raid array?',
            },

            "user_input_31": {
                "en_US": f"What raid mode would you like to use?",
                "pt_BR": f'Qual modo de raid você gostaria de usar?',
            },

            "install_01": {
                "en_US": "##### INSTALATION PARAMETERS #####",
                "pt_BR": "##### PARÂMETROS DE INSTALAÇÃO #####",
            },

            "install_02": {
                "en_US": "Installation type:",
                "pt_BR": "Tipo de instalação:",
            },

            "install_03": {
                "en_US": "Filesystem:",
                "pt_BR": "Filesystem:",
            },

            "install_04": {
                "en_US": "Username:",
                "pt_BR": "Usuário:",
            },

            "install_05": {
                "en_US": "Full name:",
                "pt_BR": "Nome completo:",
            },

            "install_06": {
                "en_US": "Hostname:",
                "pt_BR": "Hostname:",
            },

            "install_07": {
                "en_US": "Keyboard layout:",
                "pt_BR": "Layout do teclado:",
            },

            "install_08": {
                "en_US": "Timezone:",
                "pt_BR": "Timezone:",
            },

            "install_09": {
                "en_US": "Mirror:",
                "pt_BR": "Mirror:",
            },

            "install_10": {
                "en_US": "Kernel:",
                "pt_BR": "Kernel:",
            },

            "install_11": {
                "en_US": "Storage devices:",
                "pt_BR": "Dispositivos de armazenamento:",
            },

            "install_12": {
                "en_US": "Would you like to proceed with the installation?",
                "pt_BR": "Você gostaria de continuar com a instalação?",
            },

            "install_13": {
                "en_US": "Backing up current mirrorlist",
                "pt_BR": "Fazendo backup da mirrorlist atual",
            },

            "install_14": {
                "en_US": "Generating a new mirrorlist",
                "pt_BR": "Gerando uma nova mirrorlist",
            },

            "install_15": {
                "en_US": f"Wiping {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Limpando {args[2] if len(args) > 2 else None}",
            },

            "install_16": {
                "en_US": "Creating partition layout",
                "pt_BR": "Criando layout de partição",
            },

            "install_17": {
                "en_US": f"Encrypting {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criptografando {args[2] if len(args) > 2 else None}",
            },

            "install_18": {
                "en_US": f"Opening encrypted partition {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Entrando na partição criptografada {args[2] if len(args) > 2 else None}",
            },

            "install_19": {
                "en_US": f"Making swap",
                "pt_BR": f"Criando swap",
            },

            "install_20": {
                "en_US": f"Activating swap",
                "pt_BR": f"Ativando swap",
            },

            "install_21": {
                "en_US": f"Formatting {args[2] if len(args) > 2 else None} partition using "
                         f"{args[3] if len(args) > 3 else None}",
                "pt_BR": f"Formatando partição {args[2] if len(args) > 2 else None} usando "
                         f"{args[3] if len(args) > 3 else None}",
            },

            "install_22": {
                "en_US": f"Mounting {args[2] if len(args) > 2 else None} on "
                         f"{args[3] if len(args) > 3 else None}",
                "pt_BR": f"Montando {args[2] if len(args) > 2 else None} em "
                         f"{args[3] if len(args) > 3 else None}",
            },

            "install_23": {
                "en_US": f"Creating BTRFS subvolume {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando subvolume BTRFS {args[2] if len(args) > 2 else None}",
            },

            "install_24": {
                "en_US": f"Unmounting everything",
                "pt_BR": f"Desmontando tudo",
            },

            "install_25": {
                "en_US": f"Making directory {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando diretório {args[2] if len(args) > 2 else None}",
            },

            "install_26": {
                "en_US": f"Installing {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Instalando {args[2] if len(args) > 2 else None}",
            },

            "install_27": {
                "en_US": f"Generating fstab",
                "pt_BR": f"Gerando fstab",
            },

            "install_28": {
                "en_US": f"Making needed fstab modifications",
                "pt_BR": f"Fazendo as modificações necessárias no fstab",
            },

            "install_29": {
                "en_US": f"Generating locale",
                "pt_BR": f"Gerando locale",
            },

            "install_30": {
                "en_US": f"Generating adjtime",
                "pt_BR": f"Gerando adjtime",
            },

            "install_31": {
                "en_US": f"Enabling NTP synchronization",
                "pt_BR": f"Ativando sincronização NTP",
            },

            "install_32": {
                "en_US": f"Setting up hostname",
                "pt_BR": f"Configurando hostname",
            },

            "install_33": {
                "en_US": f"Installing Nvidia drivers",
                "pt_BR": f"Instalando drivers Nvidia",
            },

            "install_34": {
                "en_US": f"Recreating initramfs",
                "pt_BR": f"Recriando initramfs",
            },

            "install_35": {
                "en_US": f"Installing bootloader",
                "pt_BR": f"Instalando bootloader",
            },

            "install_36": {
                "en_US": f'Creating user "{args[2] if len(args) > 2 else None}"',
                "pt_BR": f'Criando usuário "{args[2] if len(args) > 2 else None}"',
            },

            "install_37": {
                "en_US": f"Setting {args[2] if len(args) > 2 else None}'s password",
                "pt_BR": f'Definindo a senha para o usuário "{args[2] if len(args) > 2 else None}"',
            },

            "install_38": {
                "en_US": f"Adding subuids and subgids",
                "pt_BR": f"Atribuindo subuids e subgids",
            },

            "install_39": {
                "en_US": f"Enabling services {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Ativando serviços {args[2] if len(args) > 2 else None}",
            },

            "install_40": {
                "en_US": f"Creating EFI partition in {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando partição EFI em {args[2] if len(args) > 2 else None}",
            },

            "install_41": {
                "en_US": "Swap:",
                "pt_BR": "Swap:",
            },

            "install_42": {
                "en_US": "Enabling ZRAM",
                "pt_BR": "Ativando ZRAM",
            },

            "install_43": {
                "en_US": "Core packages:",
                "pt_BR": "Pacotes núcleo:",
            },

            "install_44": {
                "en_US": "core packages",
                "pt_BR": "pacotes núcleo",
            },

            "install_45": {
                "en_US": "Util packages:",
                "pt_BR": "Pacotes utilitários:",
            },

            "install_46": {
                "en_US": "util packages",
                "pt_BR": "pacotes utilitários",
            },

            "install_47": {
                "en_US": "Extra packages:",
                "pt_BR": "Pacotes extras:",
            },

            "install_48": {
                "en_US": "extra packages",
                "pt_BR": "pacotes extras",
            },

            "install_49": {
                "en_US": "extra packages",
                "pt_BR": "pacotes extras",
            },

            "install_50": {
                "en_US": f"Creating swap partition in {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando partição swap in {args[2] if len(args) > 2 else None}",
            },

            "install_51": {
                "en_US": f"Creating system partition in {args[2] if len(args) > 2 else None}",
                "pt_BR": f"Criando partição do sistema em {args[2] if len(args) > 2 else None}",
            },

        }

        return messages[args[0]][args[1]]

import sys
import os
import subprocess as sp
import colorama
from colorama import Fore, Style
from time import sleep

colorama.init(autoreset=True)

params = sys.argv
theme_name = None
theme_path = None
watch_mode = False
errors = [
    'Subject not specified.',
    'Exceeded the maximum of 2 parameters',
    'The specified theme does not exist.',
    'Missing requirement: NodeJS.\n>> Download: https://nodejs.org/en/download',
    'Unable to install the library, try installing manually:\n>> npm install bootstrap',
    'Unable to install the library, try installing manually:\n>> npm install -g sass',
    'Error compiling scss file.',
    'Error installing packages, try installing manually:\n>> npm install'
]


def main() -> None:
    clear_screen = sp.run('cls' if os.name == 'nt' else 'clear', shell=True)
    check_first_run()
    install_libs()
    get_param()
    sleep(1)
    clear_screen = sp.run('cls' if os.name == 'nt' else 'clear', shell=True)
    build()


def help():
    pass


def error(code: str) -> None:
    print(Fore.RED + Style.BRIGHT + f'[Error: {code}] {errors[code]}')
    exit()


def check_first_run() -> None:
    npm = sp.run(['npm', '--version'], shell=True, capture_output=True, text=True)
    if npm.returncode != 0:
        error(3)
    if not os.path.exists('./node_modules'):
        print('First run detected, installing packages...')
        npm_install = sp.run(['npm', 'install'], shell=True)
        if npm_install.returncode != 0:
            error(7)
        else:
            print(Fore.GREEN, Style.BRIGHT, 'Modules installed.')


def install_libs() -> None:
    bs = sp.run(['npm', 'list'], shell=True, capture_output=True, text=True)
    if 'bootstrap@' not in bs.stdout:
        print(Fore.YELLOW + Style.BRIGHT + 'Bootstrap library not found, trying to install...')
        bs_version = input(Fore.CYAN + Style.BRIGHT + 'Qual versão do bootstrap deseja instalar? (5.3.0-alpha1): ')
        if not bs_version:
            bs_version = '5.3.0-alpha1'
        bs = sp.run(['npm', 'install', f'bootstrap@{bs_version}'], shell=True, capture_output=True, text=True)
        if bs.returncode != 0:
            error(4)
        else:
            print(Fore.GREEN + Style.BRIGHT + 'Bootstrap library successfully installed!')
    sass = sp.run(['sass', '--version'], shell=True, capture_output=True, text=True)
    if sass.returncode != 0:
        print(Fore.YELLOW + Style.BRIGHT + 'SASS library not found, trying to install...')
        sass = sp.run(['npm', 'install', '-g', 'sass'], shell=True, capture_output=True, text=True)
        if sass.returncode != 0:
            error(5)
        else:
            print(Fore.GREEN + Style.BRIGHT + 'SASS library successfully installed!')


def get_param() -> None:
    global theme_name, watch_mode, params
    if len(params) <= 1:
        error(0)
    elif len(params) > 3:
        error(1)
    else:
        if '--watch' in params:
            watch_mode = True
        for index, param in enumerate(params):
            if not param.startswith('--') and index > 0:
                if theme_exists(f'{param}.scss'):
                    theme_name = f'{param}.scss'
                else:
                    print(param)
                    error(2)


def theme_exists(theme_name: str) -> bool:
    if os.path.isfile(f'./themes/{theme_name}'):
        return True
    else:
        return False


def build():
    global theme_name, theme_path, watch_mode
    theme_path = f'.\\themes\\{theme_name}'
    output_dir = f'.\\themes\\dist\\{theme_name}'.replace('scss', 'css')
    if watch_mode:
        sass_command = ['sass', '--watch', theme_path, output_dir]
    else:
        sass_command = ['sass', theme_path, output_dir]
    scss_compile = sp.run(sass_command, shell=True, capture_output=True, text=True)
    if scss_compile.returncode != 0:
        print(scss_compile.stderr)
        error(6)
    else:
        print(Fore.GREEN + Style.BRIGHT + f'Tema compilado com sucesso!\n>> ./themes/dist/')


if __name__ == '__main__':
    main()
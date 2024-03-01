import subprocess
from subprocess import PIPE
from subprocess import DEVNULL
from checker import Checker


class UserInterface:

    def __init__(self):
        self.error_count = 0
        self.command_as_list = ['curl', 'ipinfo.io/ip']
        self.loop_length = 0
        self.window_size = [500, 500]
        self.checker = Checker(self.window_size)
        self.headless_flag = 'Off'
        self.login_cookie_flag = 'Off'
        self.user_options = None
        self.counter = 0

    def title(self):
        print("\x1bc")
        print('\33[38;5;39m███╗   ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗██████╗ ███╗   ██╗')
        print('\33[38;5;45m████╗  ██║██╔═══██╗██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║')
        print('\33[38;5;75m██╔██╗ ██║██║   ██║██████╔╝██║  ██║██║   ██║██████╔╝██╔██╗ ██║')
        print('\33[38;5;81m██║╚██╗██║██║   ██║██╔══██╗██║  ██║╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║')
        print('\33[38;5;75m██║ ╚████║╚██████╔╝██║  ██║██████╔╝ ╚████╔╝ ██║     ██║ ╚████║')
        print('\33[38;5;45m╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝     ╚═╝  ╚═══╝')
        print('\33[38;5;45m---------- by Roberto Toledo (github.com/g3th) ---------------')

    def menu(self):
        print('[1] Start Checker')
        print('[2] Choose a Window Size (default: 500 x 500)')
        print('[3] Headless mode [{}]'.format(self.headless_flag))
        print('[4] Save Log-in Cookie [{}]'.format(self.login_cookie_flag))
        print('[5] Quit')
        self.user_options = input("Pick an option: ")

    def checker_running(self):
        self.title()
        command = subprocess.run(self.command_as_list, shell=False, stdout=PIPE, stderr= DEVNULL)
        print('Checker is Running - Current IP: {}'.format(str(command.stdout).split("b'")[1].replace("'","")))

    def options(self):
        while True:
            self.title()
            self.menu()
            match self.user_options:
                case "1":
                    self.loop_length = self.checker.get_credentials()
                    self.checker_running()
                    while self.counter < self.loop_length:
                        checker = self.checker.start(self.counter)
                        if checker == 1:
                            if self.error_count > 5:
                                print("\nToo many errors. \nStatus is either 429 or there are other connection problems.")
                                print("Ending.")
                                exit()
                            self.error_count += 1
                        else:
                            self.error_count = 0
                            self.counter += 1
                case "2":
                    self.window_size_options()
                case "3":
                    if self.headless_flag == 'Off':
                        self.headless_flag = 'On'
                    else:
                        self.headless_flag = 'Off'
                case "4":
                    if self.login_cookie_flag == 'Off':
                        self.login_cookie_flag = 'On'
                    else:
                        self.login_cookie_flag = 'Off'
                case "5":
                    print("Goodbye.")
                    exit()
                case _:
                    print("Invalid Option.")
                    input("Press Enter...")

    def window_size_options(self):
        print("\x1bc")
        self.title()
        print("Pick a Window Size:")
        print("[1] Small")
        print("[2] Medium")
        print("[3] Large")
        window_size = input("> ")
        match window_size:
            case "1":
                self.window_size = 1200, 300
            case "2":
                self.window_size = 1200, 500
            case "3":
                self.window_size = 1200, 800
            case _:
                print("Invalid size")
        self.window_size = window_size

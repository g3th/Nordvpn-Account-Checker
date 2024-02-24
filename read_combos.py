import os
from pathlib import Path


class ComboReader:

    def __init__(self):
        self.user_directory = str(Path(__file__).parent) + "/nord.txt"
        self.save_directory = str(Path(__file__).parent) + "/valid_accounts"
        self.save_file = "/valid_accounts.txt"

    def start(self):
        user = []
        password = []
        try:
            os.remove(self.save_directory + self.save_file)
        except FileNotFoundError:
            pass
        try:
            with open(self.user_directory, 'r') as combos:
                for i in combos.readlines():
                    user.append(i.split(":")[0])
                    password.append(i.split(":")[1].split(" ")[0].strip())
        except FileNotFoundError as e:
            print("No combolist found in: " + self.user_directory + "\nPlease add 'nord.txt' and try again.\nPress Enter to end.")
            input()
            exit()
        return user, password

    def check_for_resume_file(self):
        index = 0
        for i in os.listdir(str(Path(__file__).parent)):
            if 'resume' in i:
                with open('resume_from', 'r') as read_resume_index:
                    index = int(read_resume_index.readline())
        return index

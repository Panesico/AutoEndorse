import sys
import os
import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import urllib.request
import zipfile
import tarfile
from colorama import init, Fore, Style

# Initialise the colours
init()

RED = Fore.RED
ORANGE = Fore.RED + Fore.YELLOW
GREEN = Fore.GREEN
LIGHT_BLUE = Style.BRIGHT + Fore.BLUE
PURPLE = Style.BRIGHT + Fore.MAGENTA
ERASE = Style.RESET_ALL

# Load the environment variables from the .env file
load_dotenv()

# Get the username and password from environment variables
iterations = int(os.getenv("E_ITERATIONS"))
last_execution = os.getenv("E_LAST_EXECUTION")
start_index = int(os.getenv("E_START_INDEX"))
endorsements_left = int(os.getenv("E_ENDORSEMENTS_LEFT"))
language = os.getenv("E_LANGUAGE")
first_time = os.getenv("FIRST_TIME").lower() == "true"
lines = open("buddies.txt", "r").readlines()
endorse_button_text = "Endorse"


def download_and_extract_chromium(url, extract_to):
    print(f"Downloading Chromium from {url}...")
    file_name = url.split('/')[-1]
    file_path = os.path.join(extract_to, file_name)

    urllib.request.urlretrieve(url, file_path)

    print("Extracting Chromium...")
    if file_name.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_name.endswith('.tar.xz'):
        with tarfile.open(file_path, 'r:xz') as tar_ref:
            tar_ref.extractall(extract_to)

    os.remove(file_path)
    print("Chromium is ready.")

def scroll_to_element(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

def smooth_scroll(driver, scroll_duration=5):
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Calculate the number of steps for smooth scrolling
    steps = 50
    step_height = total_height / steps

    # Calculate the time to wait between each step
    step_time = scroll_duration / steps

    # Perform the smooth scroll
    for i in range(steps):
        scroll_to = (i + 1) * step_height
        driver.execute_script(f"window.scrollTo(0, {scroll_to});")
        time.sleep(step_time)

# language

def esp_translate():
    global endorse_button_text
    endorse_button_text = "Validar"


if language is None:
    print("Please select a language with the number / Por favor seleccione un idioma con el numero:")
    print("1. English")
    print("2. Español")
    choice = input("--> ")
    if choice == "1":
        language = "english"
    elif choice == "2":
        language = "spanish"
    else:
        print("Invalid selection. Please run the script again and select 1 or 2.")
        sys.exit(1)

language = language.lower()

if language == "english":
    print("You have selected English.")
elif language == "spanish":
    print("Ha seleccionado Español.")
    esp_translate()
else:
    print("Invalid selection. Please run the script again and select 1 or 2.")
    sys.exit(1)

if len(lines) <= start_index:
    start_index = 0

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# If the last execution date is the same as the current date and no endorsements left, do not execute the script
if last_execution == current_date and endorsements_left == 0:
    sys.exit(1)

if last_execution != current_date:
    with open(".env", "w") as f:
        f.write("E_ITERATIONS=" + str(iterations) + "\n")
        f.write("E_START_INDEX=" + str(start_index) + "\n")
        f.write("E_LAST_EXECUTION=" + current_date + "\n")
        f.write("E_ENDORSEMENTS_LEFT=" + "150" + "\n")
        f.write("E_LANGUAGE=" + str(language) + "\n")
        f.write("FIRST_TIME=" + str(first_time) + "\n")
    endorsements_left = 150

current_endorsement_amount = endorsements_left

# Create a Chrome WebDriver instance with the specified path
# probably some are just bloat
options = Options()

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9292")

download_path = os.path.expanduser("./chromium")
os.makedirs(download_path, exist_ok=True)

if sys.platform.startswith("win"):
    print(f"Making a configuration for {RED}Windows{ERASE} 🤢🤢🤮")
    chromium_url = "https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/1029089/chrome-win.zip"
    chromium_path = os.path.join(download_path, "chrome-win", "chrome.exe")
    if not os.path.exists(chromium_path):
        download_and_extract_chromium(chromium_url, download_path)
    options.binary_location = chromium_path
    options.add_argument("--user-data-dir=.\\config\\my-google-chrome")
elif sys.platform.startswith("linux"):
    print(f"Making a configuration for {GREEN}Linux{ERASE} 😎")
    chromium_url = "https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1000000/chrome-linux.zip"
    chromium_path = os.path.join(download_path, "chrome-linux", "chrome")
    if not os.path.exists(chromium_path):
        download_and_extract_chromium(chromium_url, download_path)
    options.binary_location = chromium_path
    options.add_argument("--user-data-dir=./config/my-google-chrome")
elif sys.platform.startswith("darwin"):
    print(f"Making a configuration for {ORANGE}macOS{ERASE} 🤑🤑")
    chromium_url = "https://storage.googleapis.com/chromium-browser-snapshots/Mac/1020972/chrome-mac.zip"
    chromium_path = os.path.join(download_path, "chrome-mac", "Chromium.app", "Contents", "MacOS", "Chromium")
    if not os.path.exists(chromium_path):
        download_and_extract_chromium(chromium_url, download_path)
    options.binary_location = chromium_path
    options.add_argument("--user-data-dir=./config/my-google-chrome")
else:
    print("Unknown operating system.")
    # Handle unknown OS accordingly
    sys.exit(1)

options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

driver = webdriver.Chrome(options=options)

if first_time:
    driver.get("https://linkedin.com")
    try:
        signin = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, """//a[text()='
          Sign in
      ']""")))
        login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_key")))
    except:
        pass

    # Check if undefined and assign False is such
    signin = locals().get("signin", False)
    login = locals().get("login", False)

    if signin or login:
        print("Please, login on the opened browser")
    else:
        print(f"{RED}No login box found!{ERASE}")

print("Please, confirm that you are logged in and ready to start the script")
print("Type 'yes' to continue")
print("Type anything else to exit")
confirmation = input("--> ")
if (confirmation.lower() != "yes"):
    print("Exiting...")
    driver.quit()
    sys.exit(1)

print(f"{GREEN}Starting...{ERASE}")

success_counter = 0
row_counter = 0


def make_number(input_str):
    number = ""
    for char in input_str:
        if char.isdigit():
            number += char
    return int(number)


# Start the loop
for line in lines[start_index:]:
    if success_counter >= iterations:
        break
    line = line.strip()
    if line.startswith("http"):
        last_line = line
        driver.get(line + "/details/skills/")
    else:
        continue

    row_counter += 1

    delete_this_shi = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pv-profile-sticky-header-v2__actions-container"))
    )

    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", delete_this_shi)

    main_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "main"))
    )
    unclickable_button_counter = 0
    endorsement_per_person = 0
    while True:
        js_code = """
            document.addEventListener('orsedByViewer', function(event) {
                event.preventDefault();
            }, true);
        """
        driver.execute_script(js_code)

        while True:
            try:
                delete_this_shi_2 = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "artdeco-tabpanel--hidden"))
                )

                class_to_remove = "artdeco-tabpanel--hidden"
                driver.execute_script("arguments[0].classList.remove(arguments[1]);", delete_this_shi_2,
                                      class_to_remove)
            except:
                break

        try:
            endorse_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                f"//button[contains(@class, 'artdeco-button')]//span[normalize-space()='{endorse_button_text}']/.."))
            )
            print(f"{GREEN}{current_endorsement_amount - endorsements_left + 1} endorsements done{ERASE}")
            endorsement_per_person += 1
        except:
            if unclickable_button_counter > 6:
                print(f"{RED}Could not find any buttons{ERASE}")
                break
            unclickable_button_counter += 1

        try:
            if endorsements_left == 0:
                print(f"{RED}No endorsements left{ERASE}")
                break
            endorse_button.click()
            endorsements_left -= 1
        except:
            try:
                smooth_scroll(driver, 3)
                scroll_to_element(driver, endorse_button)
            except:
                pass
            if unclickable_button_counter > 7:
                print(f"{RED}Could not click the endorse button{ERASE}")
                break
            unclickable_button_counter += 1
        time.sleep(4)
    if endorsements_left == 0:
        print("You ran out of endorsements :(")
        break
    success_counter += 1
    person_name = driver.title.split("|")[1].strip()
    print(f"{PURPLE}{endorsement_per_person} endorsements were given to {person_name}{ERASE}")
    print(f"{LIGHT_BLUE}{success_counter} Profiles endorsed{ERASE}")

print(f"Iterated through {PURPLE}{row_counter}{ERASE} profiles")
print(f"Successfully processed {GREEN}{success_counter}{ERASE} profiles")

# Write updated environment variables to .env file
with open(".env", "w") as f:
    f.write("E_ITERATIONS=" + str(iterations) + "\n")
    f.write("E_START_INDEX=" + str(int(os.environ["E_START_INDEX"]) + success_counter) + "\n")
    f.write("E_LAST_EXECUTION=" + current_date + "\n")
    f.write("E_ENDORSEMENTS_LEFT=" + str(endorsements_left) + "\n")
    f.write("E_LANGUAGE=" + str(language) + "\n")
    f.write("FIRST_TIME=" + str(first_time) + "\n")

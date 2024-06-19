import sys
import os
import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Style

# Initialise the colours
init()

RED = Fore.RED
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

#language

def esp_translate():
    global endorse_button_text
    endorse_button_text = "Validar"

choice = language

if language is None:
    print("Please select a language with the number / Por favor seleccione un idioma con el numero:")
    print("1. English")
    print("2. Español")
    choice = input("--> ")

if choice == "1":
    print("You have selected English.")
elif choice == "2":
    print("Ha seleccionado Español.")
    esp_translate()
else:
    print("Invalid selection. Please run the script again and select 1 or 2.")
    sys.exit(1)

if len(lines) >= start_index:
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
        f.write("E_LANGUAGE=" + str(choice) + "\n")
        f.write("FIRST_TIME=" + str(first_time) + "\n")
    endorsements_left = 150
    
endorse_button_text = "Endorse"
current_endorsement_amount = endorsements_left

# Create a Chrome WebDriver instance with the specified path
# probably some are just bloat
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9292")
options.add_argument("--user-data-dir=.config/google-chrome")  # Always get the same chrome profile
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

    try:
        profile_info = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, "feed-identity-module__actor-meta")))
        print(f"{GREEN}Profile info found!{ERASE}")
    except:
        print(f"{RED}Login timeout! Exiting...{ERASE}")
        sys.exit(1)

    try:
        profile_name = WebDriverWait(profile_info, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "t-black")))
        print(f"\nNice to see you {PURPLE}{profile_name.text}{ERASE}")
    except:
        print(f"{RED}Profile name not found :({ERASE}")

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

    time.sleep(5)

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

        time.sleep(1)
        try:
            endorse_button = WebDriverWait(main_div, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[span[text()='" + endorse_button_text + "']]"))
            )
            print(f"{GREEN}{current_endorsement_amount - endorsements_left + 1} endorsements done{ERASE}")
            endorsement_per_person += 1
        except:
            print(f"{RED}Could not find any buttons{ERASE}")
            break

        try:
            if endorsements_left == 0:
                print(f"{RED}No endorsements left{ERASE}")
                break
            endorse_button.click()
            endorsements_left -= 1
        except:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if unclickable_button_counter > 2:
                print(f"{RED}Could not click the endorse button{ERASE}")
                break
            unclickable_button_counter += 1
        time.sleep(3)

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
    f.write("E_LANGUAGE=" + str(choice) + "\n")
    f.write("FIRST_TIME=" + str(first_time) + "\n")

import sys

from constants import *
from utils import start_chrome_browser, login_to_ui
from valid_login import login_with_valid_user


def edit_user_setup(browser, new_first_name, new_last_name, new_email, profile_image):
    login_with_valid_user(browser, DEFAULT_USERNAME, DEFAULT_PASSWORD)

    browser.get("http://0.0.0.0:8001/edit/")

    first_name_input = browser.find_element_by_xpath("//input[@id='firstName']")
    first_name_input.clear()
    first_name_input.send_keys(new_first_name)

    last_name_input = browser.find_element_by_xpath("//input[@id='lastName']")
    last_name_input.clear()
    last_name_input.send_keys(new_last_name)

    email_input = browser.find_element_by_xpath("//input[@id='email']")
    email_input.clear()
    email_input.send_keys(new_email)

    profile_picture = browser.find_element_by_xpath("//input[@id='profile_picture']")
    profile_picture.clear()
    profile_picture.send_keys(profile_image)

    button = browser.find_element_by_xpath("//input[@id='update-submit']")
    button.click()

def check_edit_user(browser,new_first_name, new_last_name, new_email):

    browser.get("http://0.0.0.0:8001/edit")

    browser.find_element_by_xpath("//input[@id='firstName']") == new_first_name
    browser.find_element_by_xpath("//input[@id='lastName']") == new_last_name
    browser.find_element_by_xpath("//input[@id='email']") == new_email

# ---------------------------------------------------- Main ------------------------------------------------------------

if __name__ == "__main__":
    try:
         chrm = start_chrome_browser()
         edit_user_setup(chrm, "Andres", "Haskel", "andihas@andihas.com", "/Users/andres/desktop/twilio.jpg")
         check_edit_user(chrm, "Andres", "Haskel", "andihas@andihas.com")
         chrm.close()
    except Exception as e:
        print "Failed to create campaign from the UI:"
        chrm.close()
        raise Exception(e)

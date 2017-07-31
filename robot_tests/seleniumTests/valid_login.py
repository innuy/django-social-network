import sys

from constants import *
from utils import start_chrome_browser

def login_with_valid_user(browser, user_name=DEFAULT_USERNAME, user_password=DEFAULT_PASSWORD):
    browser.get("http://0.0.0.0:8001/login")
    username_input = browser.find_element_by_xpath("//input[@id='username']")
    username_input.send_keys(user_name)
    password_input = browser.find_element_by_xpath("//input[@id='password']")
    password_input.send_keys(user_password)

    button = browser.find_element_by_xpath("//input[@id='login-submit']")
    button.click()


# ---------------------------------------------------- Main ------------------------------------------------------------

if __name__ == "__main__":
    try:
        kwargs = {arg.split("=")[0]: arg.split("=")[1] for arg in sys.argv if "=" in arg}
        chrm = start_chrome_browser()
        login_with_valid_user(chrm)
        chrm.close()
    except Exception as e:
        print "Test failed"
        chrm.close()
        raise Exception(e)

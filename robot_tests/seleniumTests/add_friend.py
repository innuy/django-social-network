import sys

from constants import *
from utils import start_chrome_browser, login_to_ui
from valid_login import login_with_valid_user
from time import sleep

def add_friend_setup(browser):
    browser.get("http://0.0.0.0:8001/register/")

    username_input = browser.find_element_by_xpath("//input[@id='username']")
    username_input.send_keys("John")

    password_input = browser.find_element_by_xpath("//input[@id='password']")
    password_input.send_keys("password")

    password_input = browser.find_element_by_xpath("//input[@id='email']")
    password_input.send_keys("email")

    password_input = browser.find_element_by_xpath("//input[@id='update-submit']")
    password_input.click()



def add_friend(browser, user_name):
    login_with_valid_user(browser, DEFAULT_USERNAME, DEFAULT_PASSWORD)

    browser.get("http://0.0.0.0:8001/users/")

    friend_to_add_button = browser.find_element_by_xpath('//div[@class="starter-template"]//li[contains(text(),"{}")]//'
                                                         'button'.format(user_name))
    friend_to_add_button.click()
    sleep(2)
    browser.get("http://0.0.0.0:8001/friends/")
    sleep(2)
    browser.find_element_by_xpath('//div[@class="container"]//ul[@class="list-group"]//li[contains(text(),"{}")]'.format(user_name))

# ---------------------------------------------------- Main ------------------------------------------------------------
def teardown_add_friend_function(browser,user_name):
    browser.get("http://0.0.0.0:8001/admin/socialNetworkApp/userfriend/")
    friend_added = browser.find_element_by_xpath('//table[@id="result_list"]//th[@class="field-__str__"]//a[.="{}"]'.format(user_name))
    friend_added.click()
    delete_button = browser.find_element_by_xpath('//a[@class="deletelink"]')
    delete_button.click()
    confirm_delete_button = browser.find_element_by_xpath('//input[@type="submit"]')
    confirm_delete_button.click()

if __name__ == "__main__":
    try:
         chrm = start_chrome_browser()
         add_friend_setup(chrm)
         add_friend(chrm, "John")
         teardown_add_friend_function(chrm, "John")
         chrm.close()
    except Exception as e:
        print "Failed to add friend"
        chrm.close()
        raise Exception(e)

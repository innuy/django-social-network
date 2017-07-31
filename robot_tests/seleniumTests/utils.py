from telnetlib import EC

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from constants import *

def start_chrome_browser(full_screen=True, hidden=False):
    options = None
    if full_screen:
        options = webdriver.ChromeOptions()
        options.add_argument("- -start-maximized")
    elif hidden:
        display = Display(visible=0, size=(800,600))
        display.start()
    return webdriver.Chrome(chrome_options=options)


def element_when_ready(browser,filter,value,delay=PAGE_DELAY):
    element = None
    try:
        wait = WebDriverWait(browser,delay)
        element = wait.until(EC.element_to_be_clickeable((filter,value)))
    finally:
        return element

def got_page(browser,page,domain=SERVER,add=False):
    element_when_ready(browser, By.CLASS_NAME, "")
    path = domain + "/" + page + add * '/add'
    print "trying to go to page: {0}".format(path)
    if browser.current_url == path:
        return
    browser.get(path)


def login_to_ui(browser, domain=SERVER, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
    browser.get(domain)

    user_input = browser.get_element_by_xpath("//input[@id='username']")
    user_input.send_keys(username)

    password_input = browser.get_element_by_xpath("//input[@id='password']")
    password_input.send_keys(password)

    button = browser.get_element_by_xpath("//input[@id='login-submit']")
    button.click()








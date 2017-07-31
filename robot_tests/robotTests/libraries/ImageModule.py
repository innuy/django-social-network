from robot.api.deco import keyword
from selenium import webdriver
from robot.libraries.BuiltIn import BuiltIn
import os



@keyword('Upload Image')
def UpladImage(user_id,image_path):
    # Set media root
    media_root = os.path.dirname(os.path.abspath(__file__))
    media_root = media_root.split("/")[:-2]
    media_root = "/".join(media_root)

    se2lib = BuiltIn().get_library_instance('Selenium2Library')
    current_browser = se2lib._current_browser()
    image_path_file = media_root + image_path
    print(image_path_file)
    link = current_browser.find_element_by_xpath("//input[@id='profile_picture']")
    link.send_keys(image_path_file)



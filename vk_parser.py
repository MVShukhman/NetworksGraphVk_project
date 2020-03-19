# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from constants import *


class VkParser(object):
    def __init__(self, driver_path):
        self.browser = webdriver.Firefox(executable_path=driver_path)

    def get_friends_list(self, id):
        self.browser.get('http://vk.com/friends?id=%s' % id)
        for i in range(100):  # without scrolling we won't get all elements; we hope, 100 scrolls down will be enough
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        all_friends = self.browser.find_elements_by_xpath('//div[@class="friends_user_row clear_fix"]')
        for friend in all_friends:
            id = friend.find_element_by_xpath(".//div[@id]").get_attribute('id')
            yield id[3:]  # id is in format 'res12345678' here, so we cut it to get '12345678'

    def login(self, login, password):
        self.browser.get('https://vk.com/')

        _login = self.browser.find_element_by_id("index_email")
        _password = self.browser.find_element_by_id("index_pass")
        submit_button = self.browser.find_element_by_id("index_login_button")

        _login.send_keys(login)
        _password.send_keys(password)
        submit_button.click()

        time.sleep(5)
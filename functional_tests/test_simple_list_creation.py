import sys

from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes and cheks its homepage
        self.browser.get(self.server_url)

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do litem straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        # User types "Buy peacock feathers" into a textbox
        inputbox.send_keys('Buy peacock feathers')

        # When hitting enter, user is redirected to its own URL and page lists:
        # "1. Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        user01_url = self.browser.current_url
        self.assertRegex(user01_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Buy peacock feathers')

        # There is still a textbox inviting the usert to add another item.
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on the list
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        self.check_for_row_in_list_table('2. Use peacock feathers to make a fly')

        # Now a second user (user02) enters the homepage.
        self.browser.quit()  # to ensure a new session is opened
        self.browser = webdriver.Firefox()

        # user02 visits the homepage and there's no sign of the original user
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # user02 starts a new list and enters some data
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # user02 gets its unique URL and there's no track of user01
        user02_url = self.browser.current_url
        self.assertRegex(user02_url, 'lists/.+')
        self.assertNotEqual(user02_url, user01_url)

        # Satisfied, goes to sleep

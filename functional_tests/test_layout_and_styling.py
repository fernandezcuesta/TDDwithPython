import sys
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # User logs in the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Check if inputbox is moderately centered in the screen
        inputbox = self.get_item_inputbox()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

import sys
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and accidentally tries to submit an empty
        # list item by hitting Enter on the empty inputbox

        # The homepage refreshes, and there is an error message saying that
        # list items cannot be blank

        # Tries again with some text for the item, now it works

        # Perversely, decides to submit yet another blank list item

        # A similar warning is shown

        # By filling it properly, it works again

        self.fail('write me!')

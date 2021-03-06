from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and accidentally tries to submit an empty
        # list item by hitting Enter on the empty inputbox
        self.browser.get(self.server_url)
        self.get_item_inputbox().send_keys('\n')

        # The homepage refreshes, and there is an error message saying that
        # list items cannot be blank
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # Tries again with some text for the item, now it works
        self.get_item_inputbox().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1. Buy milk')

        # Perversely, decides to submit yet another blank list item
        self.get_item_inputbox().send_keys('\n')

        # A similar warning is shown
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # By filling it properly, it works again
        self.get_item_inputbox().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1. Buy milk')
        self.check_for_row_in_list_table('2. Make tea')

    def test_cannot_add_duplicates(self):
        # User goes to the homepage and starts a new list
        self.browser.get(self.server_url)
        self.get_item_inputbox().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1. Buy wellies')

        # Accidentally tries to enter a duplicate item
        self.get_item_inputbox().send_keys('Buy wellies\n')

        # Sees a helpful error message
        self.check_for_row_in_list_table('1. Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # User starts a new list in a way that causes a validation error
        self.browser.get(self.server_url)
        self.get_item_inputbox().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # When starts typing the error is cleared
        self.get_item_inputbox().send_keys('An entry')
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

    def test_error_messages_are_cleared_on_form_selection(self):
        # User starts a new list in a way that causes a validation error
        self.browser.get(self.server_url)
        self.get_item_inputbox().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # When the user clicks on the form, the error is immediately cleared
        self.get_item_inputbox().click()
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
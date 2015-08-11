from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and accidentally tries to submit an empty
        # list item by hitting Enter on the empty inputbox
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # The homepage refreshes, and there is an error message saying that
        # list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error, "You can't have an empty list item")

        # Tries again with some text for the item, now it works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1. Buy milk')

        # Perversely, decides to submit yet another blank list item
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # A similar warning is shown
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error, "You can't have an empty list item")

        # By filling it properly, it works again
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1. Buy milk')
        self.check_for_row_in_list_table('2. Make tea')

import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes and cheks its homepage
        self.browser.get('http://localhost:8000')

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do litem straight away

        # User types "Buy peacock feathers" into a textbox

        # When hitting enter, the page updates, now the page lists:
        # "1. Buy peacock feathers" as an item in a to-do list

        # There is still a textbox inviting the usert to add another item.
        # enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on the list

        # User wonders wheter the site will remember the list. Then he sees
        # that the site has generated a unique URL -- there is some
        # explanatory text

        # User visits the URL, the to-do list still there

        # Satisfied, quits the browser session

if __name__ == '__main__':
    unittest.main(warnings='ignore')


from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
    ExistingListItemForm, ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR
)



class HomePageTest(TestCase):

    maxDiff = None  # assertMultiLineEqual does not crop long diffs

    def test_root_url_resoves_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_valid_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'form': ItemForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_homepage_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirect_after_POST_request(self):
        response = self.client.post('/lists/new',
                                    data={'text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        list_id = List.objects.first().id
        self.assertRedirects(response, '/lists/%d/' % list_id)

    def test_for_invalid_input_renders_hone_template(self):
        response = self.client.post('/lists/new',
                                    data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_homepage(self):
        response = self.client.post('/lists/new',
                                    data={'text': ''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new',
                                    data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)


    def test_invalid_list_items_arent_saved_to_database(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % (list_.id, ),
                                data={'text': ''})

    def test_validation_errors_are_passed_to_list_page(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        expected_error = escape(EMPTY_LIST_ERROR)
        self.assertContains(response, expected_error)

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="example")
        response = self.client.post('/lists/%d/' % (list_.id, ),
                                    data={'text': 'example'})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        response = self.client.get('/lists/%d/' % list_.id)

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, correct_list)
        self.assertEqual(new_item.text, 'A new item for an existing list')

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/' % correct_list.id,
                                    data={'text': 'My new list item'})
        self.assertEqual(response.status_code, 302)
        list_id = List.objects.first().id
        self.assertRedirects(response, '/lists/%d/' % list_id)

    def test_displays_item_forms(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.core.urlresolvers import resolve

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resoves_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_valid_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    # def test_homepage_only_saves_item_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirect_after_POST_request(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        list_id = List.objects.first().id
        self.assertRedirects(response, '/lists/%d/' % list_id)


class ListViewTest(TestCase):

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


class NewItemtest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, correct_list)
        self.assertEqual(new_item.text, 'A new item for an existing list')

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/add_item' % correct_list.id,
                                    data={'item_text': 'My new list item'})
        self.assertEqual(response.status_code, 302)
        list_id = List.objects.first().id
        self.assertRedirects(response, '/lists/%d/' % list_id)

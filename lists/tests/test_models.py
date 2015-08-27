from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

class ListAndItemModelsTest(TestCase):

    def test_defaul_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()  # Another way of creating a List object
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicate_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Hi')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='Hi')
            item.full_clean()

    def test_CAN_save_same_item_in_different_lists(self):
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        Item.objects.create(list=list_1, text='Hi')
        item = Item(list=list_2, text='Hi')
        item.full_clean()  # should not raise

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
    # def test_saving_and_retrieving_items(self):
        # list_ = List()
        # list_.save()
        #
        # first_item = Item()
        # first_item.text = 'The first (ever) list item'
        # first_item.list = list_
        # first_item.save()
        #
        # second_item = Item()
        # second_item.text = 'Item the second'
        # second_item.list = list_
        # second_item.save()
        #
        # saved_list = List.objects.first()
        # self.assertEqual(saved_list, list_)
        #
        # saved_items = Item.objects.all()
        # self.assertEqual(saved_items.count(), 2)
        #
        # first_saved_item = saved_items[0]
        # second_saved_item = saved_items[1]
        # self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        # self.assertEqual(first_saved_item.list, list_)
        # self.assertEqual(second_saved_item.text, 'Item the second')
        # self.assertEqual(second_saved_item.list, list_)

    def test_get_absolute_url(self):
        list_= List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{}/'.format(list_.id))

    def test_list_ordering(self):
        list_= List.objects.create()
        item1 = Item.objects.create(list=list_, text='item1')
        item2 = Item.objects.create(list=list_, text='item2')
        item3 = Item.objects.create(list=list_, text='item3')
        self.assertEqual(list(Item.objects.all())[::-1], [item1, item2, item3])

from datetime import date
from django.shortcuts import render, redirect
# from django.http import HttpResponse

from .models import Item, List


def home_page(request):
    # if request.method == 'POST':  # else take its default value: ''
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/_test_list/')
    # else:
        return render(request,'home.html')


def view_list(request, id):
    list_ = List.objects.get(id=id)
    return render(request,
                  'list.html',
                  {'list': list_, 'date': date.today()})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % list_.id)


def add_item(request, id):
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % list_.id)

from datetime import date
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    # if request.method == 'POST':  # else take its default value: ''
    #     Item.objects.create(text=request.POST['text'])
    #     return redirect('/lists/_test_list/')
    # else:
        return render(request,'home.html', {'form': ItemForm()})


def view_list(request, id):
    list_ = List.objects.get(id=id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
#            Item.objects.create(text=request.POST['text'], list=list_)
            form.save(for_list=list_)
#            return redirect('/lists/%d/' % list_.id)
            return redirect(list_)
    return render(request,
                  'list.html',
                  {'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():  # will validate and clean form fields, Item
        list_ = List.objects.create(author=request.user)
        form.save(for_list=list_)
        return redirect(list_)  # uses get_absolute_url
    else:
        return render(request, 'home.html', {'form': form})
#    list_ = List.objects.create(author=request.user)
#    item = Item.objects.create(text=request.POST['text'], list=list_)
#    try:
#        item.full_clean()
#        item.save()
#    except ValidationError:
#        list_.delete()
#        return render(request, 'home.html', {"error": "You can't have an empty list item"})
##    return redirect('/lists/%d/' % list_.id)
#    return redirect(list_)  # uses get_absolute_url


#def add_item(request, id):
#    list_ = List.objects.get(id=id)

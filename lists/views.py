from django.shortcuts import render, redirect
# from django.http import HttpResponse

from .models import Item


def home_page(request):
    # if request.method == 'POST':  # else take its default value: ''
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/_test_list/')
    # else:
        return render(request,'home.html')


def view_list(request):
    return render(request,
                  'list.html',
                  {'items': Item.objects.all()})


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/_test_list/')

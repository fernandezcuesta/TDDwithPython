from django.shortcuts import render, redirect
# from django.http import HttpResponse

from .models import Item


def home_page(request):
    if request.method == 'POST':  # else take its default value: ''
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    # else:
    #     new_item_text = ''

    return render(request,
                  'home.html',
                  {'items': Item.objects.all()})

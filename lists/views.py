from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request,
                  'home.html',
                  {
#                    'new_item_text': request.POST.get('item_text', ''),
                    'new_item_text': request.POST['item_text'] if request.method == 'POST' else '',
                  })
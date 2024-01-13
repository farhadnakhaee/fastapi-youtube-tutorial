from django.shortcuts import render
from django.http import HttpResponse
from store.models import OrderItem

def say_hello(request):
    return HttpResponse('Hello World')

def say_hello_html(request):
    query_set = OrderItem.objects.filter(product__collection__id=3)

    return render(request, 'hello.html', {'name': 'Farhad', 'order_items': list(query_set)})

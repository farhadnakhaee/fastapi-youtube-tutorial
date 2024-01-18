from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q, F, Func, Value, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from store.models import OrderItem, Product, Order, Customer, Collection
from tags.models import TaggedItem


def say_hello(request):
    return HttpResponse('Hello World')


# def say_hello_html(request):
#     query_set_1 = OrderItem.objects.values('product_id').distinct()
#     query_set_2 = Product.objects.filter(
#         id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
#     return render(request, 'hello.html', {'name': 'Farhad', 'products': list(query_set_2)})


# selecting related objects
# def say_hello_html(request):
#     queryset = Product.objects.prefetch_related('promotions').select_related('collection')
#     queryset_1 = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
#     return render(request, 'hello.html', {'name': 'Farhad', 'orders': list(queryset_1)})


# aggregating objects
# def say_hello_html(request):
#     result = Product.objects.filter(collection__id=3).aggregate(
#         count=Count(id), min_price=Min('unit_price'))
    
#     # How many orders do we have?
#     result1 = Order.objects.aggregate(count=Count(id))
#     # How many units of product 1 have we sold?
#     result2 = OrderItem.objects.filter(product_id=1).aggregate(sold_out=Sum('quantity'))
#     # How many orders has customer 1 placed?
#     result3 = Order.objects.filter(customer_id=1).aggregate(count=Count('id'))
#     # What is the min, max and average price of the products in collection 3?
#     result4 = Product.objects \
#     .filter(collection_id=3) \
#     .aggregate(
#         max_price=Max('unit_price'), 
#         min_price=Min('unit_price'), 
#         avg_price=Avg('unit_price'))
    
#     return render(request, 'hello.html', {'name': 'Farhad', 'result': result4})


# annotating object
# def say_hello_html(request):
#     queryset = Customer.objects.annotate(new_id=F('id')*2)
#     return render(request, 'hello.html', {'name': 'Farhad', 'result': queryset})


# calling database functions
# def say_hello_html(request):
#     queryset = Customer.objects.annotate(
#         full_name=Func(F('first_name'), Value(' '), F('last_name'), function='Concat')
#     )
#     return render(request, 'hello.html', {'name': 'Farhad', 'result': queryset})


# grouping data
# def say_hello_html(request):
#     queryset = Customer.objects.annotate(order_count=Count('order'))
#     return render(request, 'hello.html', {'name': 'Farhad', 'result': queryset})


# expression wrapper
# def say_hello_html(request):
#     discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
#     queryset = Product.objects.annotate(
#         discounted_price=discounted_price
#         )
#     return render(request, 'hello.html', {'name': 'Farhad', 'result': queryset})


# quering generic relationship
# def say_hello_html(request):
#     queryset = TaggedItem.objects.get_tags_for(Product, 1)

#     return render(request, 'hello.html', {'name': 'Farhad', 'result': queryset})


# creating objects
# def say_hello_html(request):
    # method 1
    # collection = Collection()
    # collection.title = 'video games'
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # method 2
    # collection = Collection.objects.create(title='a', featured_product_id=1)
    # return render(request, 'hello.html', {'name': 'Farhad'})


# updating objects
# def say_hello_html(request):
    # method 1
    # collection = Collection.objects.get(pk=12)
    # collection.featured_product = None
    # collection.save()

    # method 2
    # Collection.objects.filter(pk=13).update(title='games')

    # return render(request, 'hello.html', {'name': 'Farhad'})


# deleting
# def say_hello_html(request):
    # method 1
    # collectin = Collection(pk=11)
    # collectin.delete()
    # method 2
    # Collection.objects.filter(pk__gt=11).delete()
    # return render(request, 'hello.html', {'name': 'Farhad'})


# transaction
def say_hello_html(request):
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = -1
    #     item.unit_price = 10
    #     item.save()

        return render(request, 'hello.html', {'name': 'Farhad'})
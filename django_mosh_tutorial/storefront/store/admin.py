from typing import Any
from django.db.models import Count
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = \
            reverse('admin:store_product_changelist') \
            + '?' \
            + urlencode({'collection__id': str(collection.id)})
            
        return format_html('<a href={}>{}</a>', url, collection.products_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, Product):
        return Product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return 'LOW'
        return 'OK'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = \
            reverse('admin:store_order_changelist') \
            + '?' \
            + urlencode({'customer_id': str(customer.id)})
        return format_html('<a href={}>{}</a>', url, customer.order_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            order_count= Count('order')
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'payment_status', 'placed_at']
    list_per_page = 10
        
from .models import Collection, Product
from decimal import Decimal
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','inventory', 'slug', 'description', 'unit_price', 'price_with_tax', 'collection']
    

    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # collection = serializers.StringRelatedField()

    # collection = CollectionSerializer()

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail',
    # )
        
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
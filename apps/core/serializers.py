from rest_framework import serializers

from .models import Product, Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'rental_price', 'rental_duration', 'order']
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    orderproduct_set = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'start_date', 'end_date', 'total_cost', 'orderproduct_set']


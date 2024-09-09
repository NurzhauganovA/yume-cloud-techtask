from django_filters import rest_framework as filters

from .models import Product, Order


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price']


class OrderFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['start_date', 'end_date']

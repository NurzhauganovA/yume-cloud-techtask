from django.urls import path
from .views import ProductListView, ProductDetailView, OrderListView, OrderDetailView, OrderProductDetailView, \
    ProductSearchView, RentalSumPerProductView, AvailablePeriodsView, TotalRentalIncomeView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('orders/<int:order_pk>/products/<int:order_product_pk>/', OrderProductDetailView.as_view(), name='order_product_detail'),

    path('search/products/', ProductSearchView.as_view(), name='search_products'),

    path('stats/rental-sum/', RentalSumPerProductView.as_view(), name='rental_sum_per_product'),
    path('stats/product/<int:product_id>/availability/', AvailablePeriodsView.as_view(), name='available_periods'),
    path('stats/total-income/', TotalRentalIncomeView.as_view(), name='total_rental_income'),
]

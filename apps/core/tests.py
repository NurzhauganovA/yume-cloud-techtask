from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Product, Order, OrderProduct


class OrderProductDetailTests(APITestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.product = Product.objects.create(name="Product 1", price=100)
        self.order = Order.objects.create(start_date='2024-09-01', end_date='2024-09-10', total_price=300)
        self.order_product = OrderProduct.objects.create(order=self.order, product=self.product, rental_price=100,
                                                         rental_duration=9)

    def test_get_order_product_detail(self):
        url = reverse('order_product_detail',
                      kwargs={'order_pk': self.order.pk, 'order_product_pk': self.order_product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product']['name'], "Product 1")
        self.assertEqual(response.data['rental_price'], 100)

    def test_order_not_found(self):
        url = reverse('order_product_detail', kwargs={'order_pk': 9999, 'order_product_pk': self.order_product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_product_not_found(self):
        url = reverse('order_product_detail', kwargs={'order_pk': self.order.pk, 'order_product_pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RentalStatsTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product A', price=100)
        self.order = Order.objects.create(start_date='2024-09-01', end_date='2024-09-10', total_price=500)
        self.order_product = OrderProduct.objects.create(order=self.order, product=self.product, rental_price=50, rental_duration=10)

    def test_rental_sum_per_product(self):
        url = reverse('rental_sum_per_product')
        response = self.client.get(url, {'start_date': '2024-09-01', 'end_date': '2024-09-30'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['product_name'], 'Product A')
        self.assertEqual(response.data[0]['total_rental_income'], 500)

    def test_available_periods_for_product(self):
        url = reverse('available_periods', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_total_rental_income(self):
        url = reverse('total_rental_income')
        response = self.client.get(url, {'start_date': '2024-09-01', 'end_date': '2024-09-30'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_rental_income'], 500)

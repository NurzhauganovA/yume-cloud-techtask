from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .filters import ProductFilter, OrderFilter
from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer, OrderSerializer, OrderProductSerializer
from .permissions import IsAdminOrReadOnly
from .services import get_product_by_id, create_order_product, search_product, get_rental_sum_for_products, get_available_periods_for_product, get_total_rental_income
from .exceptions import ProductNotFoundException, OrderConflictException, OrderNotFoundException


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = OrderFilter

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderProductCreateView(APIView):
    def post(self, request) -> Response:
        product_id = request.data.get('product_id')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        rental_price = request.data.get('rental_price')
        rental_duration = request.data.get('rental_duration')
        if not all([product_id, start_date, end_date, rental_price, rental_duration]):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            order_product = create_order_product(product_id, start_date, end_date, rental_price, rental_duration)
        except OrderConflictException:
            raise OrderConflictException
        return Response({'id': order_product.id}, status=status.HTTP_201_CREATED)


class OrderProductDetailView(APIView):
    def get(self, request, order_pk: int, order_product_pk: int) -> Response:
        try:
            order = Order.objects.get(pk=order_pk)
        except Order.DoesNotExist:
            raise OrderNotFoundException(f'Заказ с ID {order_pk} не найден.')

        try:
            # Получаем продукт в аренде, связанный с заказом
            order_product = OrderProduct.objects.get(pk=order_product_pk, order=order)
        except OrderProduct.DoesNotExist:
            raise ProductNotFoundException(f'Продукт в аренде с ID {order_product_pk} не найден для заказа {order_pk}.')

        serializer = OrderProductSerializer(order_product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            raise ProductNotFoundException
        products = search_product(query)
        return Response(products, status=status.HTTP_200_OK)


class RentalSumPerProductView(APIView):
    def get(self, request) -> Response:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        result = get_rental_sum_for_products(start_date, end_date)
        data = [{'product_name': row[0], 'total_rental_income': row[1]} for row in result]
        return Response(data, status=status.HTTP_200_OK)


class AvailablePeriodsView(APIView):
    def get(self, request, product_id: int) -> Response:
        result = get_available_periods_for_product(product_id)
        data = [{'start_date': row[0], 'end_date': row[1]} for row in result]
        return Response(data, status=status.HTTP_200_OK)


class TotalRentalIncomeView(APIView):
    def get(self, request) -> Response:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        result = get_total_rental_income(start_date, end_date)
        return Response({'total_rental_income': result[0]}, status=status.HTTP_200_OK)

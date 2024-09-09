from rest_framework.exceptions import APIException


class ProductNotFoundException(APIException):
    status_code = 404
    default_detail = 'Продукт не найден'
    default_code = 'product_not_found'


class OrderConflictException(APIException):
    status_code = 400
    default_detail = 'Конфликт аренды: пересекающиеся заказы для одного продукта.'
    default_code = 'order_conflict'


class OrderNotFoundException(APIException):
    status_code = 404
    default_detail = 'Заказ не найден'
    default_code = 'order_not_found'

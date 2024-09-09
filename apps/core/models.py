from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_gte_0')
        ]
        ordering = ['price']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'product'


class Order(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id}"

    def calculate_total_cost(self):
        return sum([order_product.rental_price * order_product.rental_duration for order_product in self.orderproduct_set.all()])

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_cost()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gte=models.F('start_date')), name='end_date_gte_start_date')
        ]
        ordering = ['-start_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_duration = models.PositiveIntegerField()  # Время аренды в днях

    def __str__(self):
        return f"{self.product.name} in Order {self.order.id}"

    def save(self, *args, **kwargs):
        self.rental_price = self.product.price
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'
        db_table = 'order_product'

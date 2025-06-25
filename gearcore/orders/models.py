from django.db import models

from gearcore.goods.models import Motorcycle
from gearcore.users.models import User


class OrderItemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True,
                             verbose_name='Користувач')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення замовлення')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефону')
    requires_delivery = models.BooleanField(default=False, verbose_name='Потрібна доставка')
    delivery_address = models.TextField(verbose_name='Адреса доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при отримані')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обробці', verbose_name='Статус замовлення')

    class Meta:
        db_table = 'order'
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'

    def __str__(self):
        return f"Замовлення користувача {self.user.name()}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Замовлення')
    product = models.ForeignKey(to=Motorcycle, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None,
                                verbose_name='Товар')
    name = models.CharField(max_length=150, verbose_name='Назва')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість')
    create_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажі')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'проданий товар'
        verbose_name_plural = 'продані товари'

    objects = OrderItemQueryset.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} замовлення #{self.order.pk}"

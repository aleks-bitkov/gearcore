from django.db import models

from gearcore.goods.models import Products
from gearcore.users.models import User

class CartQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.product_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Користувач')
    product = models.ForeignKey(to=Products, on_delete=models.RESTRICT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість')
    session_key = models.CharField(blank=True, null=True, max_length=32, verbose_name='Ключ сесії')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')

    class Meta:
        db_table = 'cart'
        verbose_name = 'кошик'
        verbose_name_plural = 'Кошики'

    objects = CartQuerySet.as_manager()

    def product_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        elif self.session_key:
            return f"Cart for session {self.session_key[:8]}..."
        else:
            return f"Cart #{self.id}"


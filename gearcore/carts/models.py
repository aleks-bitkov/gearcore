from django.db import models

from gearcore.goods.models import Motorcycle
from gearcore.goods.models import MotorcycleVariant
from gearcore.users.models import User


class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.product_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Користувач",
    )

    product = models.ForeignKey(
        to=Motorcycle,
        on_delete=models.RESTRICT,
        verbose_name="Товар",
    )
    variant = models.ForeignKey(  # Добавить это поле
        to=MotorcycleVariant,
        on_delete=models.RESTRICT,
        verbose_name="Варіант (колір)",
        null=True,  # Можно сделать необязательным для совместимости
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")
    session_key = models.CharField(
        blank=True,
        default="",
        max_length=32,
        verbose_name="Ключ сесії",
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата додавання",
    )

    objects = CartQuerySet.as_manager()

    class Meta:
        db_table = "cart"
        verbose_name = "кошик"
        verbose_name_plural = "Кошики"

    def __str__(self):
        if self.user:
            return f"Кошик користувача {self.user.name()} | Товар {self.product.name}"
        return f"Анонімний кошик | Товар {self.product.name}"

    def product_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

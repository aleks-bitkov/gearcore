from django.core.exceptions import ValidationError
from django.db import models

from gearcore.goods.models import MotorcycleVariant
from gearcore.users.models import User


class Wishlist(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Список бажань"
        verbose_name_plural = "Список бажань"

    def __str__(self):
        return f"Бажання користувача {self.user.name()}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(to=Wishlist, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=MotorcycleVariant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "елемент списку бажань"
        verbose_name_plural = "елементи списку бажань"
        unique_together = ["wishlist", "variant"]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.wishlist.user.name()} - {self.variant}"

    def clean(self):
        if self.wishlist.user != self.wishlist.user:
            msg = "Неможливо додати товар до чужого списку бажань"
            raise ValidationError(msg)

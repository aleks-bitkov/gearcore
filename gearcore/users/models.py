
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import FileField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from docutils.nodes import label

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for GearCore.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    image = FileField(_('Зображення'),upload_to='users', null=True, blank=True)
    username =  CharField(_("username"), max_length=150, unique=True, blank=True, null=True) #  no required
    first_name = CharField(_("Ім'я"), max_length=255)
    last_name = CharField(_("Прізвище"), max_length=255)
    patronymic = CharField(_("По-батькові"), blank=True, null=True, max_length=255)
    phone_number = CharField(_("Номер телефону"), unique=True, max_length=20)
    email = EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        verbose_name = _("користувача")
        verbose_name_plural = _("Користувачі")

    def name(self):
        if self.first_name and self.last_name and self.patronymic:
            return f"{self.last_name} {self.first_name[0].upper()}. {self.patronymic[0].upper()}"
        elif self.first_name and self.last_name:
            return f"{self.last_name} {self.first_name}"
        elif self.email:
            return str(self.email)
        else:
            return 'Анонімний користувач'

    def __str__(self) -> str:
        return self.name()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail")

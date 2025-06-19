from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.contrib import messages

from allauth.account.views import LoginView as AllauthLoginView

from gearcore.carts.models import Cart
from gearcore.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self):
        assert self.request.user.is_authenticated  # type guard
        return self.request.user

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["last_name", "first_name", "patronymic", "phone_number", "email"]
    success_message = _("Інформацію успішно оновлено")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail")


user_redirect_view = UserRedirectView.as_view()

def user_cart(request):
    return render(request, "users/user_cart.html")


class AccountLoginView(AllauthLoginView):
    def form_valid(self, form):
        session_key = self.request.session.session_key
        response = super().form_valid(form)
        user = self.request.user

        if user.is_authenticated and session_key:
            forgot_carts = Cart.objects.filter(user=user)

            if forgot_carts.exists():
                forgot_carts.delete()

            Cart.objects.filter(session_key=session_key).update(user=user)


        return response

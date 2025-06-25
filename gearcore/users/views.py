from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet, Prefetch
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from allauth.account.views import LoginView as AllauthLoginView
from rest_framework.reverse import reverse_lazy

from gearcore.carts.models import Cart
from gearcore.common.mixins import CacheMixin
from gearcore.orders.models import Order, OrderItem
from gearcore.users.models import User

from gearcore.users.forms import UserProfileForm


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/user_detail.html'
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:detail')

    def get_object(self, queryset=None):
        assert self.request.user.is_authenticated  # type guard
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Дані профілю успішно оновлено'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("product")))

        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60)
        return context


user_profile_view = UserProfileView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["last_name", "first_name", "patronymic", "phone_number", "email"]
    success_message = _("Інформацію успішно оновлено")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
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


def user_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("product")))

    context = {
        "orders": orders,
    }

    return render(request, 'users/user_order.html', context)


class AccountLoginView(AllauthLoginView):
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('account_logout'):
            return redirect_page
        return reverse_lazy('users:redirect')

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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView
from rest_framework.reverse import reverse_lazy

from gearcore.carts.models import Cart
from gearcore.orders.forms import CreateOrderForm
from gearcore.orders.models import Order
from gearcore.orders.models import OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:detail")

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        initial["phone_number"] = self.request.user.phone_number
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

            if cart_items.exists():
                order = Order.objects.create(
                    user=user,
                    phone_number=form.cleaned_data["phone_number"],
                    delivery_address=form.cleaned_data["delivery_address"],
                    requires_delivery=form.cleaned_data["requires_delivery"],
                    payment_on_get=form.cleaned_data["payment_on_get"],
                )

                for cart_item in cart_items:
                    product = cart_item.product
                    name = cart_item.product.name
                    price = cart_item.product.sell_price()
                    quantity = cart_item.quantity

                    if product.quantity < quantity:
                        msg = f"Недостатня кількість товару {name} на складі. В наявності - {product.quantity}"
                        messages.error(self.request, msg)
                        return redirect("orders:create")

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )

                    product.quantity -= quantity
                    product.save()

                cart_items.delete()

                messages.success(self.request, "замовлення оформлено")
                return redirect("users:detail")
        except (ValidationError, IntegrityError, ValueError) as e:
            messages.error(self.request, str(e))
            return redirect("orders:create")
        except Exception:
            import logging

            logger = logging.getLogger(__name__)
            logger.exception("Неівдома помилка при оформлені замовлення")

    def form_invalid(self, form):
        messages.error(self.request, "заповніть усі обов'язкові поля")
        return redirect("orders:create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "GearCore | Офоромлення замовлення"
        return context


create_order_view = CreateOrderView.as_view()

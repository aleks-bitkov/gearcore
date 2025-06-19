from django.contrib import admin

from gearcore.orders.models import Order, OrderItem

class OrderItemTabAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'name', 'price', 'quantity')
    search_fields = ('name', 'product')
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "name", "price", "quantity")
    search_fields = ("created_timestamp", "product", "price")

class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = ('requires_delivery', 'status', 'payment_on_get')
    search_fields = ('status', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "requires_delivery", "is_paid")
    list_filter = ("user", "created_timestamp")
    search_fields = ("user", "status", "requires_delivery")

    readonly_fields = ("created_timestamp",)

    inlines = (OrderItemTabAdmin,)


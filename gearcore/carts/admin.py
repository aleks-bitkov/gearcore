from django.contrib import admin

from gearcore.carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("product", "quantity", "created_timestamp")
    search_fields = ("product",)
    readonly_fields = ("created_timestamp",)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user_display", "quantity", "created_timestamp")
    list_filter = ("created_timestamp", "user")
    readonly_fields = ("created_timestamp",)

    def user_display(self, obj):
        if obj.user:
            return obj.user
        return "Анонімний користувач"

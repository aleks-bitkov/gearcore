from django.contrib import admin
from django.utils.html import format_html

from gearcore.goods.models import AdditionalFeatures
from gearcore.goods.models import Brand
from gearcore.goods.models import BreakSystem
from gearcore.goods.models import Category
from gearcore.goods.models import Color
from gearcore.goods.models import Engine
from gearcore.goods.models import Motorcycle
from gearcore.goods.models import MotorcycleVariant
from gearcore.goods.models import SuspensionSystem
from gearcore.goods.models import Transmission
from gearcore.goods.models import VariantImage


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "color_preview", "hex_code")
    list_filter = ("name",)
    search_fields = ("name", "hex_code")

    @admin.display(
        description="Превью",
    )
    def color_preview(self, obj):
        if obj.hex_code:
            return format_html(
                '<div style="width: 30px; height: 30px; background-color: {};'
                'border: 1px solid #ccc; border-radius: 3px;"></div>',
                obj.hex_code,
            )
        return "-"


class EngineInline(admin.StackedInline):
    model = Engine
    extra = 0


class TransmissionInline(admin.StackedInline):
    model = Transmission
    extra = 0


class MotorcycleVariantInline(admin.TabularInline):
    model = MotorcycleVariant
    extra = 1
    fields = ("color", "price_modifier", "quantity", "is_available")


class VariantImageInline(admin.TabularInline):
    model = VariantImage
    fields = ("image", "title", "is_main", "sort_order")
    extra = 1


class AdditionalFeaturesInline(admin.TabularInline):
    model = AdditionalFeatures
    extra = 0


class SuspensionSystemInline(admin.TabularInline):
    model = SuspensionSystem
    extra = 0


class BreakSystemInline(admin.TabularInline):
    model = BreakSystem
    extra = 0


@admin.register(MotorcycleVariant)
class MotorcycleVariantAdmin(admin.ModelAdmin):
    list_display = ("motorcycle", "color", "final_price", "quantity", "is_available")
    list_filter = ("is_available", "color", "motorcycle__brand", "motorcycle__category")
    search_fields = ("motorcycle__name", "color__name")
    inlines = [VariantImageInline]

    @admin.display(
        description="Фінальна ціна",
    )
    def final_price(self, obj):
        return f"{obj.final_price()} грн"


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    inlines = [
        EngineInline,
        TransmissionInline,
        MotorcycleVariantInline,
        SuspensionSystemInline,
        BreakSystemInline,
        AdditionalFeaturesInline,
    ]
    list_display = ["name", "brand", "price", "is_new"]
    prepopulated_fields = {"slug": ("name",)}

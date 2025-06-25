from django.contrib import admin
from gearcore.goods.models import Categories, Brands, Motorcycle, Engine, Transmission, ChassisAndBrakes, MotorcycleImage


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class EngineInline(admin.StackedInline):
    model = Engine
    extra = 0


class TransmissionInline(admin.StackedInline):
    model = Transmission
    extra = 0


class ChassisInline(admin.StackedInline):
    model = ChassisAndBrakes
    extra = 0


class MotorcycleImageInline(admin.TabularInline):  # Табличний вигляд для зображень
    model = MotorcycleImage
    extra = 1
    fields = ['image', 'title', 'is_main']
    readonly_fields = ['created_at']


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    inlines = [
        EngineInline,
        TransmissionInline,
        ChassisInline,
        MotorcycleImageInline  # Додаємо зображення
    ]
    list_display = ['name', 'brand', 'price', 'is_new', 'image_count']
    prepopulated_fields = {"slug": ("name",)}

    def image_count(self, obj):
        """Показує кількість зображень в списку"""
        return obj.images.count()

    image_count.short_description = 'Кількість фото'

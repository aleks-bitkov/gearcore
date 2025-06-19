from django.contrib import admin

from gearcore.goods.models import Categories, Products, Brands, CategoryBrand

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "price", "discount")
    list_editable = ("price", "discount",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(CategoryBrand)

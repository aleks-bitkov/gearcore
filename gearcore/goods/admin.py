from django.contrib import admin

from gearcore.goods.models import Categories, Products, Brands, CategoryBrand

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Products)
admin.site.register(Brands)
admin.site.register(CategoryBrand)

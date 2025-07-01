from django.contrib import admin

from gearcore.main.models import MainPage
from gearcore.main.models import Slide

admin.site.register(Slide)


class SlideInline(admin.TabularInline):  # или admin.StackedInline
    model = Slide
    extra = 1
    fields = ("image", "alt", "order", "description")
    ordering = ("order",)


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    inlines = [SlideInline]
    list_display = ("description",)

from django.shortcuts import render
from django.views.generic import TemplateView

from gearcore.main.models import Slide


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["title"] = "GearCore | Головна"
        context["content"] = "GearCore - магазин байків"
        
        slides = Slide.objects.all()
        
        print(f'\n\n\n\n\n{slides=}\n\n\n\n\n\n')
        context["slides"] = slides        
        return context

index_view = IndexView.as_view()

class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context["title"] = "GearCore | Про нас"
        context["content"] = "про наш магазин якась дуже цікава інформація"
        return context

about_view = AboutView.as_view()
def about(request):
    return render(request, "main/about.html")

def contact(request):
    return render(request, "main/contact.html")

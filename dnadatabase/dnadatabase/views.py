from django.views.generic import DetailView, ListView, TemplateView


class HomepageView(TemplateView):
    template_name: str = "dnarecords/home.html"

from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse

class homepage_view(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['nonEstimateLinks'] = [reverse_lazy('homepage'), ]


        return context

class instructions_view(TemplateView):
    template_name = 'instructions.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['nonEstimateLinks'] = [reverse_lazy('homepage'), reverse_lazy('instructions') ]


        return context

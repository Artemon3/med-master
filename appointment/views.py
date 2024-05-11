from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.views.generic.base import View

from appointment.models import Visit, Card
from appointment.service import create_schedule
from .forms import VisitForm


class CardView(View):
    def get(self, request, **kwargs):
        cards = Card.objects.all()
        context = {
            'cards': cards,
        }
        return render(request, 'appointment/card_list.html', context)


class CardDetailView(LoginRequiredMixin, CreateView):
    form_class = VisitForm
    template_name = 'appointment/cabinets_detail.html'
    pk_url_kwarg = 'card_id'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Card, id=self.kwargs.get('card_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Visit.card_objects.filter(card_id=self.kwargs.get('card_id')).values()
        schedule = Paginator(create_schedule(events), 7)
        context['schedule'] = schedule
        context['cabinet'] = self.get_object()
        return context

    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.user = self.request.user
        new_event.card = self.get_object()

        try:
            new_event.save()
        except ValidationError as exp:
            form.add_error(None, str(exp))
            return render(self.request, 'appointment/cabinets_detail.html', self.get_context_data(form=form))
        return render(self.request, 'appointment/cabinets_detail.html', self.get_context_data())


class AboutView(View):
    def get(self, request, **kwargs):
        return render(request, 'homepage/about.html', )


class ContactView(View):
    def get(self, request, **kwargs):
        return render(request, 'homepage/contacts.html', )



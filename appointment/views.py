from django.contrib import messages
from django.http import Http404
from django.views.generic import CreateView
from appointment.models import TimeRecord
from .forms import PatientForm
from django.shortcuts import render, redirect
from django.views.generic.base import View
from appointment.service import create_record, create_cards_list
from .models import Card


class CardView(View):
    def get(self, request, **kwargs):
        cards = Card.objects.all().prefetch_related('card_time')
        create_record()
        print(cards)
        cards_list = create_cards_list(cards)
        context = {
            'cards': cards_list,
        }
        print(context)
        return render(request, 'appointment/card_list.html', context)


class RecordTimeView(View):
    def post(self, request, *args, **kwargs):
        form = PatientForm(request.POST or None)
        if form.is_valid():
            time = TimeRecord.objects.filter(
                daterecord__id=kwargs.get('p'),
                card__id=kwargs.get('pk'),
                id=kwargs.get('k')
            )
            new_form = form.save(commit=False)
            new_form.name = form.cleaned_data['name']
            new_form.insurance = form.cleaned_data['insurance']
            new_form.phone = form.cleaned_data['phone']
            new_form.user = request.user
            form.save()

            time.update(patient_id=new_form.id, recorded=True, card_id=kwargs.get('pk'))
            messages.info(request, 'Вы успешно записались')
            return redirect("card_list")
        form = PatientForm()
        context = {'form': form,
                   }
        return render(request, 'appointment/appointment-create.html', context)

    def get(self, request, *args, **kwargs):
        form = PatientForm()
        time = TimeRecord.objects.get(
            daterecord__id=kwargs.get('p'),
            card__id=kwargs.get('pk'),
            id=kwargs.get('k')
        )
        if time.recorded:
            raise Http404
        context = {'form': form,
                   }

        return render(request, 'appointment/appointment-create.html', context)

from datetime import timedelta, datetime

from django import forms
from django.conf import settings
from django.forms import ModelForm, TextInput, EmailInput

from appointment.service import create_date_choices, create_time_choices
from .models import Patient, Visit

BLANK_CHOICE = (('', '----'),)


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'insurance', 'phone']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ф.И.О"
            }),
            'phone': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "+7(___)-___-__-__"
            }),
            'insurance': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Cтраховой полис"
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "example@gmail.com"
            })
        }


class VisitForm(forms.ModelForm):
    start_time = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=BLANK_CHOICE + create_time_choices(),
        label='Выберите время начала'
    )

    date = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'input-field',
        }),
        choices=BLANK_CHOICE + create_date_choices(),
        label='Выберите дату'
    )
    end_time = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Visit
        fields = ('start_time', 'date', 'end_time')

    def clean(self):
        data = self.cleaned_data
        date = data['date']
        data['start_time'] = f"{date}T{data['start_time']}Z"
        end_time = datetime.fromisoformat(data['start_time'][:-1] + '+00:00') + timedelta(minutes=settings.STEP_TIME_MINUTES)
        data['end_time'] = end_time.isoformat()
        return data

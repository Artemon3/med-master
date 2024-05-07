from django.forms import ModelForm, TextInput, EmailInput
from .models import DateRecord, TimeRecord, Patient


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


class TimeRecordForm(ModelForm):
    class Meta:
        model = TimeRecord
        fields = ['patient', 'recorded']

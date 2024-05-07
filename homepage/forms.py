from django.forms import ModelForm, Textarea,TextInput,DateInput,EmailInput
from .models import Card_comments,Card


class Card_commentsForm(ModelForm):
    class Meta:
        model=Card_comments
        fields=['comment',]
        widgets = {

            'comment': Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Введите текст"
            })


        }



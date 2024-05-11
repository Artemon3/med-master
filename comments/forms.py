from django.forms import ModelForm, Textarea, TextInput, DateInput, EmailInput
from .models import Comments


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment', ]
        widgets = {

            'comment': Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Введите текст"
            })

        }

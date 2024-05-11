from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from comments.forms import CommentsForm
from appointment.models import Card


class CommentsDetailViews(View):
    def get(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)
        return render(request, 'comments/comments.html', {'card': card})


def create_comments(request, card_id):
    error = ''
    if request.method == 'POST':
        form = CommentsForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.card_id = card_id
            form.user = request.user
            form.save()
            return redirect('/')
        else:
            error = 'Форма заполнена неверно'

    form = CommentsForm()
    context = {'form': form,
               'error': error
               }
    return render(request, 'comments/creat_comments.html', context)

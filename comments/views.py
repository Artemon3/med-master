from django.shortcuts import render
from django.views import View

from homepage.models import Card


class CommentsDetailViews(View):
    def get(self, request, pk):
        card_comments = Card.objects.get(id=pk)
        return render(request, 'comments/comments.html', {'card_comments': card_comments})


def create_comments(request, pk):
    error = ''
    if request.method == 'POST':
        form = Card_commentsForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.card_id = pk
            form.user = request.user
            form.save()
            return redirect('/')
        else:
            error = 'Форма заполнена неверно'

    form = Card_commentsForm()
    context = {'form': form,
               'error': error
               }
    return render(request, 'comments/creat_comments.html', context)

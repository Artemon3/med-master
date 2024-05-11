from django.urls import path

from . import views


urlpatterns = [
    path('<int:card_id>/', views.CommentsDetailViews.as_view(), name='comments'),
    path('<int:card_id>/create/', views.create_comments, name='create_comments'),

]

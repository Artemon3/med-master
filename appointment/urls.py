from django.urls import path

from . import views

urlpatterns = [
    path('specialists/', views.CardView.as_view(), name='card_list'),
    path('create-record/<int:pk>/<int:p>/<int:k>/', views.RecordTimeView.as_view(), name='record-create'),
]

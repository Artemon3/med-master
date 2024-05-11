from . import views
from django.urls import path

from appointment.views import CardDetailView, AboutView, ContactView

urlpatterns = [
    path('', views.CardView.as_view(), name='home'),
    path("specialists/<int:card_id>/", CardDetailView.as_view(), name="booking"),
    path("about/", AboutView.as_view(), name="about"),
    path("contacts/", ContactView.as_view(), name="contacts"),


]


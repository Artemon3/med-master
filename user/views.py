from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView, PasswordChangeView
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, CreateView

from .forms import ProfilePatientForm, RegistrationForm, LoginForm, PasswordResetUserForm, SetPasswordUserForm, \
    PasswordChangeUserForm
from .models import ProfilePatient


class LoginUserView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return f"/account/"


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class PasswordChangeUserView(PasswordChangeView):
    form_class = PasswordChangeUserForm


class PasswordResetUserView(PasswordResetView):
    form_class = PasswordResetUserForm
    email_template_name = 'send_mail/password_reset_email.html'


class PasswordResetConfirmUserView(PasswordResetConfirmView):
    form_class = SetPasswordUserForm


class ProfileActivate(View):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = ProfilePatient.objects.get(pk=uid)
            if user is not None and default_token_generator.check_token(user, kwargs.get('token')):
                user.is_active = True
                user.save()
        except:
            raise Http404
        return render(request, 'registration/confirm_account.html')


class ProfileDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user,
        }
        return render(request, 'user/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfilePatientForm
    template_name = 'user/profile_update.html'

    def get_success_url(self):
        return f"/account/"

    def get_object(self):
        return self.request.user

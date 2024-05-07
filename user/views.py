from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView, PasswordChangeView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.views.generic import UpdateView, CreateView

from .forms import ProfilePatientForm, RegistrationForm, LoginForm, PasswordResetUserForm, SetPasswordUserForm, \
    PasswordChangeUserForm
from .models import ProfilePatient
from .service import create_mail_activate_account


class LoginUserView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return f"/account/{self.request.POST.get('username', '')}"


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = 'activate'



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


class ProfileDetail(View):
    def get(self, request, *args, **kwargs):
        try:
            user = ProfilePatient.objects.prefetch_related(
                'patient_record__time_patient',
                'patient_record__time_patient__daterecord',
                'patient_record__time_patient__card',
            ).get(username=request.user.username, is_active=True)
        except:
            raise Http404
        context = {
            'user': user,
        }
        return render(request, 'user/profile.html', context)


class ProfileUpdateView(UpdateView):
    form_class = ProfilePatientForm
    template_name = 'user/profile_update.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return f"/account/{self.request.user.username}/"

    def get_queryset(self):
        return ProfilePatient.objects.filter(username=self.request.user.username, is_active=True)

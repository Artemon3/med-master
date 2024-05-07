from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.conf import settings
from user.models import Mail_Domains


def create_mail_activate_account(request, user):
    email = request.POST.get('email')
    site = get_current_site(request)
    context = {
        'email': email,
        'user': user,
        'protocol': 'http',
        'domain': site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    subject = render_to_string('send_mail/account_activate.txt', context)
    subject = ''.join(subject.splitlines())
    body = render_to_string('send_mail/activate_account_email.html', context)
    return subject, body, email


def send_mail_activate_account(subject, body, email):
    email_message = EmailMultiAlternatives(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_message.attach_alternative(body, 'text/html')
    email_message.send()

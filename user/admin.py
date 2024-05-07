from .models import ProfilePatient, ProfileDoctor, Mail_Domains
from django.contrib import admin

admin.site.register(ProfilePatient)
admin.site.register(ProfileDoctor)
admin.site.register(Mail_Domains)



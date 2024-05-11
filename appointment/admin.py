from django.contrib import admin

from appointment.models import Patient, Card


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Card)

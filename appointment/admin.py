from django.contrib import admin

from appointment.models import Patient, DateRecord, TimeRecord, Card


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TimeRecord)
class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ('time',)
    list_filter = ("daterecord", 'card')


admin.site.register(DateRecord)
admin.site.register(Card)

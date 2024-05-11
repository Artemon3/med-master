from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from user.models import ProfilePatient

NULLABLE = {'blank': True, 'null': True}


class Card(models.Model):
    photo = models.ImageField('Изображение', upload_to='static/', **NULLABLE)
    name = models.CharField('Фамилия Имя Отчество', max_length=50)
    specialty = models.CharField('Специальность', max_length=50)
    work_experience = models.CharField('Опыт работы', max_length=50)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField('Ф.И.О', max_length=150, default='')
    email = models.EmailField()
    phone = models.CharField('Телефон', max_length=20)
    insurance = models.CharField('Страховой полис', max_length=20)
    user = models.ForeignKey(
        ProfilePatient,
        on_delete=models.CASCADE,
        related_name='patient_record',
        verbose_name='User',
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class VisitManager(models.Manager):
    def overlapping_ranges(self, start_time, end_time):
        return self.get_queryset().filter(
            Q(start_time__lte=start_time, end_time__gt=start_time) |
            Q(start_time__lt=end_time, end_time__gte=end_time) |
            Q(start_time__gte=start_time, end_time__lte=end_time)
        )


class VisitTypes(models.TextChoices):
    NEW = 'NEW', 'новый'
    AWAITING_PAYMENT = 'AWAITING_PAYMENT', 'не оплачен'
    PAID = 'PAID', 'оплачен'
    COMPLETED = 'COMPLETED', 'завершен'
    CANCEL = 'CANCEL', 'отменен'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ProfilePatient, on_delete=models.CASCADE, related_name='visits',
                             verbose_name='Пользователь')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(max_length=20, choices=VisitTypes.choices, blank=True)
    card = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='visits', verbose_name='Doctor')
    comment = models.TextField(max_length=500, verbose_name='Комментарий', blank=True)

    objects = models.Manager()
    card_objects = VisitManager()

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

    def clean(self):
        now = timezone.now()

        if self.end_time <= now:
            raise ValidationError('Запись на указанное время завершена')

        if self.start_time.minute % settings.STEP_TIME_MINUTES != 0 and self.start_time.second != 0:
            raise ValidationError('Некорректная дата или время начала')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

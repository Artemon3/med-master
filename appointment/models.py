from django.db import models
from user.models import ProfilePatient

NULLABLE = {'blank': True, 'null': True}

class Card(models.Model):
    photo = models.ImageField('Изображение', upload_to='static/', **NULLABLE)
    name = models.CharField('Фамилия Имя Отчество', max_length=50)
    specialty = models.CharField('Специальность', max_length=50)
    work_experience = models.CharField('Опыт работы', max_length=50)

    def __str__(self):
        return self.name


class DateRecord(models.Model):
    date = models.DateField('Дата приема', blank=True, null=True)
    weekday = models.CharField(verbose_name='День недели', max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Дата приема'
        verbose_name_plural = 'Даты приема'


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

    def delete(self, *args, **kwargs):
        time = TimeRecord.objects.filter(patient=self)
        time.update(recorded=False)
        super(Patient, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class TimeRecord(models.Model):
    time = models.TimeField(verbose_name='Время приема')
    daterecord = models.ForeignKey(
        DateRecord,
        on_delete=models.CASCADE,
        verbose_name='Дата приема',
        related_name='timerecord',
        blank=True,
        null=True
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        verbose_name='Врач',
        blank=True,
        null=True,
        related_name='card_time'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        verbose_name='Пациент',
        blank=True,
        null=True,
        related_name='time_patient'
    )
    date_now = models.DateTimeField(verbose_name='Время создания записи', auto_now_add=True)
    recorded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.time)

    class Meta:
        verbose_name = 'Время записи'
        verbose_name_plural = 'Время записи'

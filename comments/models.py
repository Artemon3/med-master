from django.db import models

from appointment.models import Card
from user.models import ProfilePatient


class Comments(models.Model):
    comment = models.TextField('Отзыв', max_length=50)
    data = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='Врач', related_name='comments')
    user = models.ForeignKey(ProfilePatient, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return self.user.username

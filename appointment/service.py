import datetime
import numpy as np

from .models import DateRecord, TimeRecord, Card

TIME = (
    '14:00', '14:30',
    '15:00', '15:30',
    '16:00', '16:30',
    '17:00', '17:30',
    '18:00', '18:30',
    '19:00',
)
WEEKDAY = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница')


def create_cards_list(cards):
    dates = np.array(DateRecord.objects.all())
    cards_list = {}
    for card in cards:
        times = np.array(card.card_time.all()).reshape(-1, 11)
        time = {dates[x]: times[x] for x in range(5)}
        cards_list[card] = time
    return cards_list


def create_record():
    time = datetime.date.today()
    date_list = []
    if not DateRecord.objects.filter(date=time).exists():
        for i in range(5):
            date = DateRecord.objects.create(date=time + datetime.timedelta(days=i), weekday=WEEKDAY[i])
            date_list.append(date)
            date.save()
        for i in date_list:
            for k in Card.objects.all():
                for j in TIME:
                    time = TimeRecord.objects.create(time=j, daterecord=i, card=k)
                    time.save()

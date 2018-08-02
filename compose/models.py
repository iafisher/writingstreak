import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse


class DailyEntryManager(models.Manager):
    def today(self, *, user):
        """Retrieve today's entry for the given user. If no entry exists,
        create one with the word count goal set to the same goal as the most
        recent entry for that user.
        """
        today = datetime.date.today()
        try:
            return self.get(user=user, date=today)
        except DailyEntry.DoesNotExist:
            try:
                most_recent = self.filter(user=user).latest('date')
            except DailyEntry.DoesNotExist:
                return self.create(date=today, user=user)
            else:
                return self.create(date=today, user=user,
                    word_count_goal=most_recent.word_count_goal)


class DailyEntry(models.Model):
    date = models.DateField()
    text = models.TextField(blank=True)
    word_count = models.IntegerField()
    word_count_goal = models.IntegerField(default=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = DailyEntryManager()

    class Meta:
        verbose_name_plural = 'daily entries'

    def save(self, *args, **kwargs):
        self.word_count = self.calculate_word_count()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day
        }
        return reverse('compose:archive', kwargs=kwargs)

    def text_as_html(self):
        return '<p>' + '</p><p>'.join(self.text.splitlines()) + '</p>'

    def calculate_word_count(self):
        return len(self.text.split())

    def __str__(self):
        return '{}, {}'.format(self.user, self.date.isoformat())

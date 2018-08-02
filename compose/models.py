import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class WordCountGoal(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    count = models.IntegerField(default=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0.count} words for {0.user}'.format(self)


class DailyWriting(models.Model):
    date = models.DateField()
    text = models.TextField(blank=True)
    word_count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.word_count = self.calculate_word_count()
        ret = super().save(*args, **kwargs)

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        if self.word_count >= self.user.word_count:
            try:
                streak = Streak.objects.get(end_date__gte=yesterday,
                    user=self.user)
            except Streak.DoesNotExist:
                streak = Streak.objects.create(start_date=today,
                    end_date=today, user=self.user)
            else:
                streak.end_date = today
                streak.save()
        elif self.word_count < self.user.word_count:
            try:
                streak = Streak.objects.get(end_date=today, user=self.user)
            except Streak.DoesNotExist:
                pass
            else:
                if streak.start_date == today:
                    streak.delete()
                else:
                    streak.end_date = yesterday
                    streak.save()

        return ret

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
        return '{}\'s Daily Writing, {} ({} word{})'.format(
            self.user, self.date.isoformat(), self.word_count,
            '' if self.word_count == 1 else 's')


class Streak(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}\'s streak, {} to {}'.format(self.user,
            self.start_date.isoformat(), self.end_date.isoformat())

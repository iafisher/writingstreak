import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse


class DailyEntryManager(models.Manager):
    def today(self, *, user):
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
        goal = WordCountGoal.objects.filter(user=self.user).latest('start_date')
        if self.word_count >= goal.count:
            try:
                streak = Streak.objects.get(end_date__gte=yesterday,
                    user=self.user)
            except Streak.DoesNotExist:
                streak = Streak.objects.create(start_date=today,
                    end_date=today, user=self.user)
            else:
                streak.end_date = today
                streak.save()
        else:
            try:
                streak = Streak.objects.get(end_date=today, user=self.user)
            except Streak.DoesNotExist:
                pass
            else:
                streak.pop_last_day()
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


@receiver(pre_delete, sender=DailyWriting)
def delete_writing(sender, instance, **kwargs):
    today = datetime.date.today()
    try:
        streak = Streak.objects.get(user=instance.user, end_date=today)
    except Streak.DoesNotExist:
        pass
    else:
        streak.pop_last_day()


class WordCountGoal(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    count = models.IntegerField(default=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0.count} words for {0.user}'.format(self)


class Streak(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def pop_last_day(self):
        if self.start_date == self.end_date:
            self.delete()
        else:
            self.end_date -= datetime.timedelta(1)
            self.save()

    def __str__(self):
        return '{}\'s streak, {} to {}'.format(self.user,
            self.start_date.isoformat(), self.end_date.isoformat())

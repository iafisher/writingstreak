import datetime

from django.contrib.auth.models import User
from django.db import models
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
        ordering = ('-date',)

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

    def calculate_word_count(self):
        return len(self.text.split())

    def text_as_html(self):
        return '<p>' + '</p><p>'.join(self.text.splitlines()) + '</p>'

    def __str__(self):
        prefix = '{}, {}'.format(self.user, self.date.isoformat())
        if self.text:
            return prefix + ' ({}...)'.format(self.text[:40])
        else:
            return prefix


def get_current_streak(user):
    """Get the length of the user's current streak, not including today."""
    last_date = datetime.date.today()
    entries = DailyEntry.objects.filter(user=user, date__lt=last_date) \
        .order_by('-date')

    count = 0
    for entry in entries:
        # Exit early for skipped days and for days below the word count goal.
        if last_date - entry.date != datetime.timedelta(1):
            break
        elif entry.word_count < entry.word_count_goal:
            break
        count += 1
        last_date = entry.date
    return count


def get_longest_streak(user):
    """Get the length of the user's longest streak."""
    entries = DailyEntry.objects.filter(user=user).order_by('-date')

    count = 1
    longest = 0
    last_date = datetime.date.today() + datetime.timedelta(1)
    for entry in entries:
        # Exit early for skipped days and for days below the word count goal.
        if last_date - entry.date != datetime.timedelta(1):
            longest = max(count, longest)
            count = 1
        elif entry.word_count < entry.word_count_goal:
            longest = max(count, longest)
            count = 1
        else:
            count += 1
        last_date = entry.date
    return max(count, longest)

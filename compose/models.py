from django.db import models
from django.urls import reverse

class DailyWriting(models.Model):
    date = models.DateField()
    text = models.TextField(blank=True)
    word_count = models.IntegerField()

    def save(self, *args, **kwargs):
        self.word_count = self.calculate_word_count()
        ret = super().save(*args, **kwargs)
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
        return 'Daily Writing, {} ({} word{})'.format(
            self.date.isoformat(), self.word_count,
            '' if self.word_count == 1 else 's')

from django.db import models
from django.urls import reverse

class DailyWriting(models.Model):
    date = models.DateField()
    text = models.TextField()

    def get_absolute_url(self):
        kwargs = {
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day
        }
        return reverse('compose:archive', kwargs=kwargs)

    def text_as_html(self):
        return '<p>' + '</p><p>'.join(self.text.splitlines()) + '</p>'

    def __str__(self):
        return 'Daily Writing, ' + self.date.isoformat()

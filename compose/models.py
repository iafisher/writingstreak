from django.db import models

class DailyWriting(models.Model):
    date = models.DateField()
    text = models.TextField()

    def __str__(self):
        return 'Daily Writing, ' + self.date.isoformat()

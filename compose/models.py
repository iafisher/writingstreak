from django.db import models

class DailyWriting(models.Model):
    date = models.DateField()
    text = models.TextField()

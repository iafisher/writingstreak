# Generated by Django 2.0.7 on 2018-08-02 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0008_auto_20180801_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streak',
            name='min_word_count',
        ),
    ]

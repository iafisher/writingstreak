# Generated by Django 2.0.7 on 2018-07-19 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0004_remove_dailywriting_backup'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailywriting',
            name='word_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

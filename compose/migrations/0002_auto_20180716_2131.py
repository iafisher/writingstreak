# Generated by Django 2.0.7 on 2018-07-17 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailywriting',
            name='date',
            field=models.DateField(),
        ),
    ]

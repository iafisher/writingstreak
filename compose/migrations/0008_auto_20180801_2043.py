# Generated by Django 2.0.7 on 2018-08-02 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compose', '0007_streak_wsuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wsuser',
            options={'verbose_name': 'Writing Streak user'},
        ),
        migrations.AddField(
            model_name='dailywriting',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='compose.WSUser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streak',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='compose.WSUser'),
            preserve_default=False,
        ),
    ]

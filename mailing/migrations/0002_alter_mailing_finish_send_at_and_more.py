# Generated by Django 5.1.3 on 2024-11-28 15:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='finish_send_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 28, 18, 44, 39, 526754), verbose_name='Дата и время окончания отправки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='first_send_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 28, 18, 44, 39, 526754), verbose_name='Дата и время первой отправки'),
        ),
    ]

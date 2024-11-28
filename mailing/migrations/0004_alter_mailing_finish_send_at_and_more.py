# Generated by Django 5.1.3 on 2024-11-28 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_alter_mailing_finish_send_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='finish_send_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 28, 19, 28, 7, 221237), verbose_name='Дата и время окончания отправки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='first_send_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 28, 19, 28, 7, 221237), verbose_name='Дата и время первой отправки'),
        ),
    ]
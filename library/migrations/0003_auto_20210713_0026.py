# Generated by Django 3.2.5 on 2021-07-13 00:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20210712_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksmaster',
            name='price',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='issues',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 0, 26, 52, 905619)),
        ),
    ]

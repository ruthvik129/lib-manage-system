# Generated by Django 3.2.5 on 2021-07-13 01:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20210713_0026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorymaster',
            old_name='count',
            new_name='copies_available',
        ),
        migrations.AlterField(
            model_name='issues',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 1, 5, 13, 825247)),
        ),
    ]

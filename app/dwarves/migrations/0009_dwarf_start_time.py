# Generated by Django 3.2.9 on 2021-12-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarves', '0008_auto_20211207_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='dwarf',
            name='start_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 2.1.4 on 2018-12-26 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20181226_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventrecord',
            name='eligible_branches',
            field=models.CharField(max_length=75),
        ),
    ]

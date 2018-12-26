# Generated by Django 2.1.4 on 2018-12-19 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('type', models.CharField(max_length=50)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=110)),
                ('description', models.TextField(max_length=2010)),
                ('duration_number', models.CharField(max_length=10)),
                ('duration_string', models.CharField(max_length=10)),
                ('registration_start', models.DateTimeField()),
                ('registration_end', models.DateTimeField()),
                ('event_date', models.DateTimeField()),
                ('fees', models.FloatField()),
                ('eligible_branches', models.CharField(max_length=50)),
                ('outside_student', models.IntegerField(default=0)),
                ('venue', models.TextField(max_length=2010)),
                ('resource_person', models.CharField(max_length=110)),
                ('resource_person_data', models.TextField(max_length=2010)),
                ('registered_student', models.IntegerField(default=0)),
                ('registration_open', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.1.1 on 2018-12-04 19:37

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
            name='CompetitionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=55)),
                ('description', models.TextField(max_length=1010)),
                ('duration', models.CharField(max_length=25)),
                ('resource_person', models.CharField(max_length=55)),
                ('resource_person_data', models.TextField(max_length=510)),
                ('registration_start', models.DateTimeField()),
                ('registration_end', models.DateTimeField()),
                ('event_date', models.IntegerField()),
                ('event_month', models.CharField(max_length=25)),
                ('event_year', models.IntegerField()),
                ('eligible_branches', models.CharField(max_length=10)),
                ('outside_student', models.CharField(max_length=5)),
                ('venue', models.TextField(max_length=1010)),
                ('registered', models.IntegerField(default=0)),
                ('fees', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GuestLectureRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=55)),
                ('description', models.TextField(max_length=1010)),
                ('duration', models.CharField(max_length=25)),
                ('resource_person', models.CharField(max_length=55)),
                ('resource_person_data', models.TextField(max_length=510)),
                ('registration_start', models.DateTimeField()),
                ('registration_end', models.DateTimeField()),
                ('event_date', models.IntegerField()),
                ('event_month', models.CharField(max_length=25)),
                ('event_year', models.IntegerField()),
                ('eligible_branches', models.CharField(max_length=10)),
                ('outside_student', models.CharField(max_length=5)),
                ('venue', models.TextField(max_length=1010)),
                ('registered', models.IntegerField(default=0)),
                ('fees', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonthRecordcompetition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MonthRecordguest_lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MonthRecordseminar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MonthRecordtraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MonthRecordworkshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SeminarRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=55)),
                ('description', models.TextField(max_length=1010)),
                ('duration', models.CharField(max_length=25)),
                ('resource_person', models.CharField(max_length=55)),
                ('resource_person_data', models.TextField(max_length=510)),
                ('registration_start', models.DateTimeField()),
                ('registration_end', models.DateTimeField()),
                ('event_date', models.IntegerField()),
                ('event_month', models.CharField(max_length=25)),
                ('event_year', models.IntegerField()),
                ('eligible_branches', models.CharField(max_length=10)),
                ('outside_student', models.CharField(max_length=5)),
                ('venue', models.TextField(max_length=1010)),
                ('registered', models.IntegerField(default=0)),
                ('fees', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecordCompetition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('paid', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_student', to=settings.AUTH_USER_MODEL)),
                ('registered_event_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition', to='events.CompetitionRecord')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecordGuestLecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('paid', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_student', to=settings.AUTH_USER_MODEL)),
                ('registered_event_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_event', to='events.GuestLectureRecord')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecordSeminar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('paid', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seminar_student', to=settings.AUTH_USER_MODEL)),
                ('registered_event_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seminar_event', to='events.SeminarRecord')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecordTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('paid', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRecordWorkshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('paid', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshop_student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=55)),
                ('description', models.TextField(max_length=1010)),
                ('duration', models.CharField(max_length=25)),
                ('resource_person', models.CharField(max_length=55)),
                ('resource_person_data', models.TextField(max_length=510)),
                ('registration_start', models.DateTimeField()),
                ('registration_end', models.DateTimeField()),
                ('event_date', models.IntegerField()),
                ('event_month', models.CharField(max_length=25)),
                ('event_year', models.IntegerField()),
                ('eligible_branches', models.CharField(max_length=10)),
                ('outside_student', models.CharField(max_length=5)),
                ('venue', models.TextField(max_length=1010)),
                ('registered', models.IntegerField(default=0)),
                ('fees', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('c_o_e', models.CharField(max_length=75)),
                ('event_name', models.CharField(max_length=55)),
                ('description', models.TextField(max_length=1010)),
                ('duration', models.CharField(max_length=25)),
                ('resource_person', models.CharField(max_length=55)),
                ('resource_person_data', models.TextField(max_length=510)),
                ('registration_start', models.DateTimeField()),
                ('registration_end', models.DateTimeField()),
                ('event_date', models.IntegerField()),
                ('event_month', models.CharField(max_length=25)),
                ('event_year', models.IntegerField()),
                ('eligible_branches', models.CharField(max_length=10)),
                ('outside_student', models.CharField(max_length=5)),
                ('venue', models.TextField(max_length=1010)),
                ('registered', models.IntegerField(default=0)),
                ('fees', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='YearRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='studentrecordworkshop',
            name='registered_event_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshop_event', to='events.WorkshopRecord'),
        ),
        migrations.AddField(
            model_name='studentrecordtraining',
            name='registered_event_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_event', to='events.TrainingRecord'),
        ),
    ]

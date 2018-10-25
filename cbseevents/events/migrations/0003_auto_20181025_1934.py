# Generated by Django 2.1.1 on 2018-10-25 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20181012_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrecordcompetition',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_student', to='account.StudentRecord'),
        ),
        migrations.AlterField(
            model_name='studentrecordguestlecture',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_lecture_student', to='account.StudentRecord'),
        ),
        migrations.AlterField(
            model_name='studentrecordseminar',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seminar_student', to='account.StudentRecord'),
        ),
        migrations.AlterField(
            model_name='studentrecordtraining',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_student', to='account.StudentRecord'),
        ),
        migrations.AlterField(
            model_name='studentrecordworkshop',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshop_student', to='account.StudentRecord'),
        ),
        migrations.DeleteModel(
            name='StudentRecord',
        ),
    ]

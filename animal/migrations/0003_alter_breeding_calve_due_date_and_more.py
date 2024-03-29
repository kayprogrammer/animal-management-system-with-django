# Generated by Django 4.0.4 on 2022-06-04 08:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0002_alter_healthreport_animal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breeding',
            name='calve_due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='breeding',
            name='date_calved',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='breeding',
            name='pregnancy_diagnosis_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='clientdata',
            name='date_bought',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='finance',
            name='date_incurred',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='healthreport',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

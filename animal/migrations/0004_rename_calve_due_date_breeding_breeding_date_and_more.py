# Generated by Django 4.0.4 on 2022-06-04 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0003_alter_breeding_calve_due_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breeding',
            old_name='calve_due_date',
            new_name='breeding_date',
        ),
        migrations.RenameField(
            model_name='breeding',
            old_name='date_calved',
            new_name='calved_date',
        ),
    ]

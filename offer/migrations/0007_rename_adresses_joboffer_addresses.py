# Generated by Django 4.2.7 on 2023-11-29 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0006_joboffer_apply_form_joboffer_days_until_expiration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joboffer',
            old_name='adresses',
            new_name='addresses',
        ),
    ]
# Generated by Django 5.0 on 2024-01-08 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0003_remove_candidate_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='future_recruitment',
            field=models.BooleanField(default=False),
        ),
    ]

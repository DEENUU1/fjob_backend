# Generated by Django 5.0 on 2023-12-17 12:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('offer', '0005_alter_joboffer_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]

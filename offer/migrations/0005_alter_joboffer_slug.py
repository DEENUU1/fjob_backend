# Generated by Django 5.0 on 2023-12-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0004_joboffer_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
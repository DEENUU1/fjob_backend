# Generated by Django 5.0 on 2023-12-17 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
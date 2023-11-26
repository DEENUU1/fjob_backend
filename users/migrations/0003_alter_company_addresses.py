# Generated by Django 4.2.7 on 2023-11-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_address'),
        ('users', '0002_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='addresses',
            field=models.ManyToManyField(to='location.address'),
        ),
    ]

# Generated by Django 5.0 on 2024-01-02 22:22

import company.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='logo', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'], message='Only png, jpg, jpeg files are allowed'), company.models.validate_file_size]),
        ),
    ]

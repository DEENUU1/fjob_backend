# Generated by Django 4.2.7 on 2023-12-04 22:38

import candidate.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_candidate_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='resume',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'], message='Only PDF files are allowed'), candidate.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Reviewed', 'Reviewed'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]

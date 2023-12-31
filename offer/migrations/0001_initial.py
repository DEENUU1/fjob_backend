# Generated by Django 5.0 on 2023-12-22 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Employment Type',
                'verbose_name_plural': 'Employment Types',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Experience',
                'verbose_name_plural': 'Experiences',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_from', models.FloatField()),
                ('salary_to', models.FloatField()),
                ('currency', models.CharField(choices=[('PLN', 'PLN'), ('EURO', 'EURO'), ('USD', 'USD')], max_length=10)),
                ('schedule', models.CharField(choices=[('MONTHLY', 'MONTHLY'), ('YEARLY', 'YEARLY'), ('WEEKLY', 'WEEKLY'), ('DAILY', 'DAILY'), ('HOURLY', 'HOURLY')], max_length=10)),
            ],
            options={
                'verbose_name': 'Salary',
                'verbose_name_plural': 'Salaries',
                'ordering': ['-salary_from'],
            },
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Work Type',
                'verbose_name_plural': 'Work Types',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('is_remote', models.BooleanField(default=False)),
                ('is_hybrid', models.BooleanField(default=False)),
                ('days_until_expiration', models.IntegerField(default=30)),
                ('apply_form', models.URLField(blank=True, null=True)),
                ('skills', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('DRAFT', 'DRAFT'), ('PENDING', 'PENDING'), ('ACTIVE', 'ACTIVE'), ('EXPIRED', 'EXPIRED')], default='DRAFT', max_length=10)),
                ('company_logo', models.URLField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('is_scraped', models.BooleanField(default=True)),
                ('company_name', models.CharField(blank=True, max_length=50, null=True)),
                ('addresses', models.ManyToManyField(blank=True, to='location.address')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('employment_type', models.ManyToManyField(blank=True, to='offer.employmenttype')),
                ('experience', models.ManyToManyField(blank=True, to='offer.experience')),
                ('salary', models.ManyToManyField(blank=True, to='offer.salary')),
                ('work_type', models.ManyToManyField(blank=True, to='offer.worktype')),
            ],
            options={
                'verbose_name': 'Job Offer',
                'verbose_name_plural': 'Job Offers',
                'ordering': ['-created_at'],
            },
        ),
    ]

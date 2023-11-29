# Generated by Django 4.2.7 on 2023-11-29 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0007_rename_adresses_joboffer_addresses'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('message', models.TextField(blank=True, max_length=5000, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.joboffer')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Candidate',
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-29 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_package_is_active_packagepurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='price_pln',
        ),
        migrations.RemoveField(
            model_name='package',
            name='stripe_price_id_pln',
        ),
    ]
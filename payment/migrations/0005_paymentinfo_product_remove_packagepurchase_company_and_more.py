# Generated by Django 4.2.7 on 2023-11-29 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer', '0003_remove_joboffer_package'),
        ('payment', '0004_remove_package_price_pln_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_bool', models.BooleanField(default=False)),
                ('stripe_checkout_id', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('NEW_COMPANY', 'NEW_COMPANY'), ('NEW_OFFER', 'NEW_OFFER')], max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('value', models.IntegerField(default=1)),
                ('price_euro', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_euro_id', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='packagepurchase',
            name='company',
        ),
        migrations.RemoveField(
            model_name='packagepurchase',
            name='package',
        ),
        migrations.RemoveField(
            model_name='userpayment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Package',
        ),
        migrations.DeleteModel(
            name='PackagePurchase',
        ),
        migrations.DeleteModel(
            name='UserPayment',
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.product'),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
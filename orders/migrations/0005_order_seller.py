# Generated by Django 4.1.1 on 2022-09-13 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0006_seller_email'),
        ('orders', '0004_orderproduct_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sellers.seller'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.1 on 2022-09-13 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0005_seller_delete_sellerdetails_alter_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
    ]

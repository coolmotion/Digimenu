# Generated by Django 5.1 on 2024-10-03 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_order_shop_order_restaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='restaurant',
            new_name='resturant',
        ),
    ]

# Generated by Django 5.1 on 2024-10-03 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_order_shop'),
        ('main', '0012_alter_portion_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shop',
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
            preserve_default=False,
        ),
    ]

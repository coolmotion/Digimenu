# Generated by Django 5.1 on 2024-08-17 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_address2_profile_resturant_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resturant_slogan',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

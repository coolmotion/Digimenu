# Generated by Django 5.1 on 2024-08-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_profile_description_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(blank=True, default='0', max_length=400, null=True),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]

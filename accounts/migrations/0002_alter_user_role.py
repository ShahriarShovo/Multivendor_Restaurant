# Generated by Django 3.2.17 on 2023-02-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Vendor'), (2, 'Customer')], null=True),
        ),
    ]

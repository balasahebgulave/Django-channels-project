# Generated by Django 3.0.1 on 2020-01-10 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0005_machineconfiguration_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machineconfiguration',
            name='user',
        ),
    ]
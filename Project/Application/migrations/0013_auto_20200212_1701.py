# Generated by Django 3.0.1 on 2020-02-12 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0012_auto_20200131_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userseed',
            name='username',
            field=models.CharField(default='None', max_length=100, unique=True),
        ),
    ]

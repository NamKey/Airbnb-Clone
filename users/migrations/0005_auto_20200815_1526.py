# Generated by Django 3.1 on 2020-08-15 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200815_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_confirmed',
            new_name='email_verified',
        ),
        migrations.AddField(
            model_name='user',
            name='email_secretkey',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]

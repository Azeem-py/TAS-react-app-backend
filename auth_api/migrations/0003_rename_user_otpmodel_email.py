# Generated by Django 4.1.3 on 2023-03-19 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0002_customuser_isverified_otpmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpmodel',
            old_name='user',
            new_name='email',
        ),
    ]

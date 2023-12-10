# Generated by Django 4.1.3 on 2023-05-26 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_admin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchinfo',
            name='branchAdminEmail',
        ),
        migrations.AddField(
            model_name='branchinfo',
            name='city',
            field=models.CharField(default='new york', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branchinfo',
            name='country',
            field=models.CharField(default='usa', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branchinfo',
            name='state',
            field=models.CharField(default='NEW YORK', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branchinfo',
            name='zip_code',
            field=models.CharField(default='122345', max_length=10),
            preserve_default=False,
        ),
    ]
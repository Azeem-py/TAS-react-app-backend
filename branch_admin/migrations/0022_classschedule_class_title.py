# Generated by Django 4.1.3 on 2023-07-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_admin', '0021_classschedule_referenceclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='classschedule',
            name='class_title',
            field=models.CharField(default='Grade 1 MATH', max_length=200),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.3 on 2023-05-10 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master_admin', '0001_initial'),
        ('branch_admin', '0007_alter_parentinfo_homenumber_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TutorInfo',
            new_name='EmployeeInfo',
        ),
    ]
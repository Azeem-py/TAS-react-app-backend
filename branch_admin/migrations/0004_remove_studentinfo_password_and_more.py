# Generated by Django 4.1.3 on 2023-05-03 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_admin', '0003_remove_parentinfo_additional_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfo',
            name='password',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='sibling',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='sibling_name',
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='address',
            field=models.CharField(default='USA', max_length=10000),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='country',
            field=models.CharField(default='USA', max_length=1000),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='date_of_birth',
            field=models.DateField(default='2004-03-23'),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='gender',
            field=models.CharField(default='male', max_length=100),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='grade',
            field=models.CharField(default='grade 2', max_length=100),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='school',
            field=models.CharField(default='good college', max_length=100),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='state',
            field=models.CharField(default='USA', max_length=1000),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='zip_code',
            field=models.CharField(default='12345', max_length=100),
        ),
    ]

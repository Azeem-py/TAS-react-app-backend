# Generated by Django 4.1.3 on 2023-05-28 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_admin', '0002_remove_branchinfo_branchadminemail_branchinfo_city_and_more'),
        ('branch_admin', '0013_rename_bio_employeeinfo_add_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='master_admin.branchinfo'),
            preserve_default=False,
        ),
    ]

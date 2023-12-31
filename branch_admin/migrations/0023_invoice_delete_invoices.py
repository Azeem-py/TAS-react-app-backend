# Generated by Django 4.1.3 on 2023-10-07 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch_admin', '0022_classschedule_class_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoiceType', models.IntegerField(choices=[(1, 'Single'), (2, 'Bulk')])),
                ('issue_Date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
                ('class_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch_admin.classschedule')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch_admin.parentinfo')),
            ],
        ),
        migrations.DeleteModel(
            name='Invoices',
        ),
    ]

# Generated by Django 4.2.10 on 2024-02-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_employee_date_of_join'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_of_join',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

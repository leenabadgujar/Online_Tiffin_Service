# Generated by Django 3.2.5 on 2021-09-13 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_application_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application_form',
            name='delivery_time',
            field=models.TimeField(),
        ),
    ]
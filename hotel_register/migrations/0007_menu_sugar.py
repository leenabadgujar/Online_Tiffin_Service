# Generated by Django 3.2.5 on 2021-12-02 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_register', '0006_auto_20211202_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='sugar',
            field=models.IntegerField(default=0),
        ),
    ]

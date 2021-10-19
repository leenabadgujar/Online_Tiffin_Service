# Generated by Django 3.2.6 on 2021-09-24 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0020_auto_20210922_1759'),
        ('delivery_boy', '0006_delivery_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery_payment',
            name='boy_details',
        ),
        migrations.AddField(
            model_name='delivery_payment',
            name='application_Form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food.application_form'),
        ),
    ]
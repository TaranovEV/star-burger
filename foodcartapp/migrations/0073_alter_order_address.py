# Generated by Django 3.2.12 on 2022-06-26 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0072_alter_order_registered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=200, verbose_name='адрес'),
        ),
    ]

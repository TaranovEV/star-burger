# Generated by Django 3.2.12 on 2022-06-18 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0064_auto_20220618_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderquantity',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='стоимость'),
        ),
    ]

# Generated by Django 3.2.12 on 2022-06-18 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0062_auto_20220618_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='комментарий'),
        ),
    ]

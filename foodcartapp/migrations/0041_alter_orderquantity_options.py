# Generated by Django 3.2 on 2022-04-12 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_auto_20220412_1301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderquantity',
            options={'verbose_name': 'Элемент заказа', 'verbose_name_plural': 'Элементы заказа'},
        ),
    ]

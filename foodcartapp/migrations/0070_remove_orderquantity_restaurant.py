# Generated by Django 3.2.12 on 2022-06-18 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0069_alter_orderquantity_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderquantity',
            name='restaurant',
        ),
    ]

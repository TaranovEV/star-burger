# Generated by Django 3.2.12 on 2022-06-16 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0059_auto_20220616_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coordinateaddress',
            old_name='longtitude',
            new_name='longitude',
        ),
    ]
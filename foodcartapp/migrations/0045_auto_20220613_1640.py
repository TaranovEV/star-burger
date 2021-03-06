# Generated by Django 3.2.12 on 2022-06-13 13:40

from django.db import migrations

def copy_price(apps, schema_editor):
    Product = apps.get_model('foodcartapp', 'Product')
    OrderQuantity = apps.get_model('foodcartapp', 'OrderQuantity')
    replace_objects = OrderQuantity.objects.all()
    if replace_objects.exists():
        for position in replace_objects.iterator():
            for product in position.order.products.all():
                price = Product.objects.get(id=product.id).price
                position.price = price
                position.save()

def move_backward(apps, schema_editor):
    Product = apps.get_model('foodcartapp', 'Product')
    OrderQuantity = apps.get_model('foodcartapp', 'OrderQuantity')
    replace_objects = OrderQuantity.objects.all()
    if replace_objects.exists():
        for position in replace_objects.iterator():
            for product in position.order.products.all():
                price = Product.objects.get(id=product.id).price
                position.price = price
                position.save()

class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_orderquantity_price'),
    ]

    operations = [
         migrations.RunPython(copy_price,
                              move_backward)
    ]

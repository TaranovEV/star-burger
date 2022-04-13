from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import Product, Order, OrderQuantity

import json

def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    key = 'products'
    order = request.data

    if (order.get(key) != order.get(key) or 
        not isinstance(order.get(key), list) or
        not order.get(key)):
        content = {'error': f'{key} is empty or string'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    else:
        create_order = Order.objects.create(first_name=order['firstname'],
                         last_name=order['lastname'],
                         address=order['address'],
                         phonenumber=order['phonenumber'],)
        for position_order in order['products']:
            position = Product.objects.get(pk=position_order['product'])
            OrderQuantity.objects.create(order=create_order,
                                 product=position,
                                 quantity=position_order['quantity'])

        return Response(order)

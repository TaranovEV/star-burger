from itertools import product
from django.http import JsonResponse

from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Product, Order, OrderQuantity
from django.db import transaction


class ProductSerializer(ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['product', 'quantity']
        extra_kwargs = {
            'product': {'write_only': True},
            'quantity': {'write_only': True}
        }


class OrderSerializer(ModelSerializer):
    products = ProductSerializer(many=True, allow_empty=False, write_only=True)
    firstname = serializers.CharField(source='first_name')
    lastname = serializers.CharField(source='last_name')

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'address', 'phonenumber']


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

@transaction.atomic
@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        create_order = Order.objects.create(first_name=serializer.validated_data['first_name'],
                                            last_name=serializer.validated_data['last_name'],
                                            address=serializer.validated_data['address'],
                                            phonenumber=serializer.validated_data['phonenumber'],)

        for order_position in serializer.validated_data['products']:
            position = Product.objects.get(name=order_position['product'])
            if position is not None:
                OrderQuantity.objects.create(order=create_order,
                                             product=position,
                                             quantity=order_position['quantity'])
        order = serializer.data
        order['id'] = create_order.id
        return Response(order)                             
    return Response(serializer.validated_data)

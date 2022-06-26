from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F


class OrderQuantityQuerySet(models.QuerySet):
    def cost_order(self):
        all_fields = self.prefetch_related('order', 'product')
        all_fields = (
            all_fields.annotate(
                cost_position=F('quantity') * F('cost')).all()
        )
        return (
            all_fields.values('order').annotate(
                cost_order=Sum('cost_position')
                ).values('order',
                         'order__address',
                         'order__first_name',
                         'order__last_name',
                         'order__phonenumber',
                         'cost_order',
                         'order__status_order',
                         'order__payment_method'
                    )
        )


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class Order(models.Model):
    STATUSES = (
        ('N', 'Необработанный'),
        ('Y', 'Обработан'),
    )
    PAYMENT_METHODS = (
        ('C', 'Наличными'),
        ('E', 'Электронно'),
    )
    status_order = models.CharField(verbose_name='статус',
                                    max_length=2,
                                    choices=STATUSES,
                                    default='N')
    payment_method = models.CharField(verbose_name='способ оплаты',
                                      max_length=2,
                                      choices=PAYMENT_METHODS,)
    comment = models.TextField(verbose_name='комментарий',
                               blank=True)
    products = models.ManyToManyField(Product,
                                      through='OrderQuantity',
                                      related_name='orders',
                                      verbose_name='позиции',)
    first_name = models.CharField(verbose_name='имя',
                                  max_length=100,)
    last_name = models.CharField(verbose_name='фамилия',
                                 max_length=100,)
    address = models.CharField(verbose_name='адрес',
                               max_length=200,)
    phonenumber = PhoneNumberField(verbose_name='телефон',
                                   region="RU")

    registered_at = models.DateTimeField(auto_now_add=True,)
    called_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.address}'


class OrderQuantity(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name='товар',
                                related_name='in_order_quantity',
                                on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              verbose_name='заказы',
                              related_name='in_order_quantity',
                              on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество',
                                                validators=[MinValueValidator(1)])
    cost = models.DecimalField('стоимость',
                               max_digits=8,
                               decimal_places=2,
                               validators=[MinValueValidator(0)])
    objects = OrderQuantityQuerySet.as_manager()

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return '{}_{}'.format(self.product.__str__(), self.order.__str__())


class CoordinateAddress(models.Model):
    address = models.CharField(verbose_name='адрес',
                               max_length=150,)
    latitude = models.DecimalField('широта',
                                   max_digits=8,
                                   decimal_places=2,
                                   validators=[MinValueValidator(0)])
    longitude = models.DecimalField('долгота',
                                    max_digits=8,
                                    decimal_places=2,
                                    validators=[MinValueValidator(0)])

from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F



class OrderQuantityQuerySet(models.QuerySet):  
    def cost_order(self):
        all_fields = self.select_related('order', 'product')
        all_fields = (
            all_fields.annotate(cost_position=F('quantity') * F('product__price')).all()
        )
        return (
            all_fields.values('order').annotate(
                cost_order=Sum('cost_position')
                ).values('order',
                         'order__address',
                         'order__first_name',
                         'order__last_name',
                         'order__phonenumber',
                         'cost_order'
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
    status_order = models.CharField(verbose_name='статус',
                                    max_length=2,
                                    choices=STATUSES,
                                    default='N')
    comment = models.CharField(verbose_name='Комментарий',
                               max_length=200,
                               default='',
                               blank=True)
    products = models.ManyToManyField(
        Product,
        through='OrderQuantity',
        related_name='orders',
        verbose_name='позиции',
    )
    first_name = models.CharField(verbose_name='имя',
                                  max_length=100,
                                  null=False,
                                  blank=False,
    )
    last_name = models.CharField(verbose_name='фамилия',
                                 max_length=100,
                                 null=False,
                                 blank=False,
    )
    address = models.CharField(verbose_name='адрес',
                               max_length=150,
                               null=False,
                               blank=False,
    )
    phonenumber = PhoneNumberField(verbose_name='телефон',
                                   null=False,
                                   blank=False,
                                   region="RU"
    )
    cost = models.DecimalField('стоимость заказа', null=True, blank=True,
                                max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(0)])
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.address}'


class OrderQuantity(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name='Товар',
                                on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество',
                                                blank=True,
                                                null=True)
    objects = OrderQuantityQuerySet.as_manager()

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return '{}_{}'.format(self.product.__str__(), self.order.__str__())
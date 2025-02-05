from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
import random
import string
from django.utils.text import slugify

User = get_user_model()


class Category(MPTTModel):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Название в URL', max_length=200, unique=True)
    parent = TreeForeignKey('self', verbose_name='Родительская категория', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)
    image = models.ImageField(
        'Картинка 896x485 для показа в списках',
        upload_to='category_img/',
        default='/category_img/default_category_img.png'
    )

    def __str__(self):
        return f'{self.title}'

    @staticmethod
    def _rand_slug():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self._rand_slug() + '-pickBetter' + self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    # Общие поля
    name = models.TextField(verbose_name='Название', )
    category = TreeManyToManyField(
        'Category',
        blank=False,
        null=False,
        related_name='products',
        verbose_name='Категория',
    )
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.FloatField(verbose_name='Цена в рублях', )
    items_left = models.IntegerField(verbose_name='Осталось единиц товара')
    pub_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    image1 = models.ImageField(
        'Картинка 536x639 для страницы продукта',
        upload_to='product_img/',
        default='/product_img/default_product_detail_img.png'
    )
    image2 = models.ImageField(
        'Картинка 536x639 для страницы продукта',
        upload_to='product_img/',
        blank=True
    )
    image3 = models.ImageField(
        'Картинка 536x639 для страницы продукта',
        upload_to='product_img/',
        blank=True
    )
    image4 = models.ImageField(
        'Картинка 536x639 для страницы продукта',
        upload_to='product_img/',
        blank=True
    )
    image5 = models.ImageField(
        'Картинка 1140x760 для описания на странице продукта',
        upload_to='product_img/',
        blank=True
    )
    image6 = models.ImageField(
        'Картинка 433x516 для показа в списках',
        upload_to='product_img/',
        default='/product_img/default_products_list_img.png'
    )
    link_to_a_video = models.TextField(verbose_name='Ссылка на видео', blank=True)
    recommend = models.BooleanField("Рекомендовать", default=False)

    # Поля для дополнительных характеристик
    product_type = models.TextField('Тип товара', blank=True, null=True)
    compatibility = models.TextField('Совместимость', blank=True, null=True)
    thread_type = models.TextField('Тип резьбы', blank=True, null=True)
    mounting_type = models.TextField('Тип крепления', blank=True, null=True)
    imitation_of_a_shot = models.BooleanField('Имитация выстрела', blank=True, null=True)
    laser_sight = models.BooleanField('С ЛЦУ', blank=True, null=True)
    weight = models.FloatField('Вес в гр.', blank=True, null=True)
    principle_of_operation = models.TextField('Принцип действия', blank=True, null=True)
    length = models.IntegerField('Длина в мм', blank=True, null=True)
    diameter = models.FloatField('Диаметр в мм', blank=True, null=True)
    gearbox = models.TextField('Гирбокс', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def categories(self): return ",".join([str(p) for p in self.category.all()])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

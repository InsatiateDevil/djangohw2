from django.db import models

from users.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Категория',
                                     help_text='Введите название товара')
    description = models.TextField(verbose_name='Описание товара',
                                   help_text='Введите описание товара',
                                   blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category_name']

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Товар',
                                    help_text='Введите название товара')
    description = models.TextField(verbose_name='Описание товара',
                                   help_text='Введите описание товара',
                                   blank=True, null=True)
    preview_image = models.ImageField(upload_to='products/image',
                                      verbose_name='Изображения для предварительного просмотра',
                                      help_text='Загрузите изображения',
                                      blank=True, null=True)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория',
                                 help_text='Введите категорию товара',
                                 blank=True, null=True)
    price = models.IntegerField(verbose_name='Цена',
                                help_text='Введите цену на продукт')
    created_at = models.DateTimeField(verbose_name='Дата создания карточки',
                                      auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        verbose_name='Дата последнего изменения карточки', auto_now=True,
        editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='Автор', blank=True, null=True,
                              related_name='products')
    is_published = models.BooleanField(default=False,
                                       verbose_name='Доступно публике')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['product_name', 'price', 'category']
        permissions = [
            ('product_set_published_status', 'Публиковать товар'),
            ('product_change_description', 'Изменять описание товара'),
            ('product_change_category', 'Изменять категорию товара'),
                       ]

    def __str__(self):
        return f"{self.product_name} - {self.price}"


class Contact(models.Model):
    country = models.CharField(max_length=100, verbose_name='Страна',
                               blank=True, null=True)
    inn = models.CharField(max_length=100, verbose_name='ИНН', blank=True,
                           null=True)
    address = models.CharField(max_length=500, verbose_name='Адрес', blank=True,
                               null=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.country} - {self.inn} - {self.address}"


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(verbose_name='содержание')
    preview_image = models.ImageField(null=True, blank=True,
                                      verbose_name='изображение для предпросмотра')
    created_at = models.DateTimeField(verbose_name='Дата создания статьи',
                                      auto_now_add=True, editable=False)
    is_published = models.BooleanField(default=False,
                                       verbose_name='опубликовано',
                                       help_text='Опубликовано')
    view_counter = models.PositiveIntegerField(default=0, editable=False,
                                               verbose_name='Количество просмотров')
    author = models.ForeignKey(
        User, verbose_name='Автор', blank=True, null=True,
        on_delete=models.CASCADE, help_text='Укажите автора статьи',
        related_name='blogs')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        permissions = [
            ('blog_set_published_status', 'Публиковать статью')
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='versions', verbose_name='продукт')
    version_number = models.CharField(max_length=100,
                                      verbose_name='номер версии')
    version_name = models.CharField(max_length=100,
                                    verbose_name='название версии')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.version_name} - {self.version_number}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'

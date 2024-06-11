from django.db import models


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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['product_name', 'price', 'category']

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

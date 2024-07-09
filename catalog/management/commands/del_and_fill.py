import json
import os
import time

from django.core.management import BaseCommand

from catalog.models import Product, Category, Version
from config.settings import BASE_DIR
from users.models import User

file_path = os.path.join(BASE_DIR, 'db.json')


class Command(BaseCommand):

    @staticmethod
    def json_read(path_to_file):
        with open(path_to_file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()
        Version.objects.all().delete()
        User.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []
        version_for_create = []
        user_for_create = []
        dict_list = Command.json_read(file_path)

        # Обходим все значения категорий из фиктсуры для получения информации
        # об одном объекте
        for category in dict_list:
            if category['model'] == 'catalog.category':
                category_for_create.append(
                    Category(pk=category['pk'],
                             category_name=category['fields']['category_name'],
                             description=category['fields']['description'])
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in dict_list:
            if product['model'] == 'catalog.product':
                product_for_create.append(
                    Product(pk=product['pk'],
                            product_name=product['fields']['product_name'],
                            description=product['fields']['description'],
                            preview_image=product['fields']['preview_image'],
                            category=Category.objects.get(
                                pk=product['fields']['category']),
                            price=product['fields']['price'],
                            created_at=product['fields']['created_at'],
                            updated_at=product['fields']['updated_at'])
                )

        Product.objects.bulk_create(product_for_create)

        for version in dict_list:
            if version['model'] == 'catalog.version':
                version_for_create.append(
                    Version(pk=version['pk'], product=Product.objects.get(
                        pk=version['fields']['product']),
                            version_number=version['fields']['version_number'],
                            version_name=version['fields']['version_name'],
                            is_active=version['fields']['is_active'])
                )

        Version.objects.bulk_create(version_for_create)

        for user in dict_list:
            if user['model'] == 'users.user':
                user_for_create.append(
                    User(pk=user['pk'],
                         password=user['fields']['password'],
                         is_superuser=user['fields'][
                             'is_superuser'],
                         email=user['fields']['email'],
                         is_active=user['fields']['is_active'],
                         is_staff=user['fields']['is_staff'],
                         ))

        User.objects.bulk_create(user_for_create)

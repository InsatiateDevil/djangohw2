import json
from django.core.management import BaseCommand

from catalog.models import Product, Category

file_path = 'db.json'


class Command(BaseCommand):

    @staticmethod
    def json_read(path_to_file):
        with open(path_to_file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()


        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read(file_path):
            if category['model'] == 'catalog.category':
                category_for_create.append(
                    Category(pk = category['pk'],
                             category_name=category['fields']['category_name'],
                             description=category['fields']['description'])
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read(file_path):
            if product['model'] == 'catalog.product':
                product_for_create.append(
                    Product(product_name=product['fields']['product_name'],
                            description=product['fields']['description'],
                            preview_image=product['fields']['preview_image'],
                            category=Category.objects.get(
                                pk=product['fields']['category']),
                            price=product['fields']['price'],
                            created_at=product['fields']['created_at'],
                            updated_at=product['fields']['updated_at'])
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

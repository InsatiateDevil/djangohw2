import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Contact
from config.settings import BASE_DIR

FILE_FOR_SAVE_DATA = BASE_DIR.joinpath('data', 'data.json')


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products': products, 'title': 'Домашняя страница магазина'}
    return render(request, 'home.html', context=context)


def contacts(request):
    if request.POST:
        with open(FILE_FOR_SAVE_DATA, 'a+', encoding='utf-8') as data_file:
            json.dump(dict(request.POST), data_file,
                      ensure_ascii=False, indent=4)
    context = {'contacts': Contact.objects.all(), 'title': 'Контакты'}
    return render(request, 'contacts.html', context=context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    content = {'product': product, 'title': product.product_name}
    return render(request, 'product_details.html', context=content)



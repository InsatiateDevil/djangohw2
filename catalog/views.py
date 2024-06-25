import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import requests

from catalog.forms import ProductForm
from catalog.models import Product, Contact
from config.settings import BASE_DIR

FILE_FOR_SAVE_DATA = BASE_DIR.joinpath('data', 'data.json')


# Create your views here.
def home(request):
    products = Product.objects.all()
    objects_per_page = 4
    paginator = Paginator(products, objects_per_page)
    page_number = request.GET.get('p')
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)
    context = {'objects': page.object_list, 'paginator': paginator,
               'page': page, 'title': 'Домашняя страница магазина', }
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


def add_product(request):
    if request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_details')
    else:
        form = ProductForm()
    content = {'title': 'Добавление продукта', 'form': form}
    return render(request, 'add_product.html', context=content)

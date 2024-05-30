import json
from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render

from config.settings import BASE_DIR

FILE_FOR_SAVE_DATA = BASE_DIR.joinpath('data', 'data.json')


# Create your views here.
def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.POST:
        with open(FILE_FOR_SAVE_DATA, 'a+', encoding='utf-8') as data_file:
            json.dump(dict(request.POST), data_file,
                      ensure_ascii=False, indent=4)
    return render(request, 'contacts.html')
